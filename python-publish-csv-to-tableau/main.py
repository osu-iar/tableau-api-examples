import csv
import tableauserverclient as TSC
import os
import sys

from dotenv import load_dotenv
from tableauhyperapi import HyperProcess, Telemetry, Connection, CreateMode, NOT_NULLABLE, NULLABLE, SqlType, \
TableDefinition, Inserter, escape_name, escape_string_literal, HyperException, TableName
from typing import List


load_dotenv()


def create_table_in_hyper_file(connection: Connection) -> TableDefinition:
    connection.catalog.create_schema('Extract')

    # A schema of 'Extract' and tablename of 'Extract' is required
    my_table = TableDefinition(TableName('Extract', 'Extract'), [
        TableDefinition.Column('make', SqlType.text()),
        TableDefinition.Column('model', SqlType.text()),
        TableDefinition.Column('year', SqlType.int())
    ])

    connection.catalog.create_table(my_table)
    return my_table


def insert_csv_into_hyper_file(connection: Connection, table: TableDefinition):
    with open('example.csv', 'r') as f:
        reader = csv.DictReader(f)

        with Inserter(connection, table) as inserter:
            for row in reader:
                inserter.add_row([row['make'], row['model'], int(row['year'])])

            inserter.execute()

    return


def connect_to_tableau() -> TSC.Server:
    # Create an authentication object and sign in to the server
    # Tableau Doc: https://tableau.github.io/server-client-python/docs/api-ref#authentication
    auth: TSC.PersonalAccessTokenAuth = TSC.PersonalAccessTokenAuth(
        os.getenv('tableau_token_name'),
        os.getenv('tableau_token_value')
    )
    server: TSC.Server = TSC.Server(os.getenv('tableau_server_url'), use_server_version=True)

    server.auth.sign_in(auth)
    return server


def find_project_to_publish_to(server: TSC.Server, project_name: str) -> TSC.ProjectItem:
    req_options: TSC.RequestOptions = TSC.RequestOptions()
    req_options.filter.add(
        TSC.Filter(
            TSC.RequestOptions.Field.Name,
            TSC.RequestOptions.Operator.Equals,
            project_name
        )
    )

    matching_projects: List[TSC.ViewItem]
    pagination_item: TSC.PaginationItem
    matching_projects, pagination_item = server.projects.get(req_options)

    # Check how many items were found
    if pagination_item.total_available == 0:
        print('Error: No matching project found.')
        sys.exit(1)
    elif pagination_item.total_available > 1:
        print('Warning: Multiple projects found. Going with the first found view.')

    project = matching_projects[0]
    return project


def main():
    # Start by converting the CSV file into a hyper extract
    with HyperProcess(telemetry=Telemetry.DO_NOT_SEND_USAGE_DATA_TO_TABLEAU) as hyper:
        with Connection(hyper.endpoint, 'csv-to-hyper-example.hyper', CreateMode.CREATE_AND_REPLACE) as conn:
            my_table: TableDefinition = create_table_in_hyper_file(conn)
            insert_csv_into_hyper_file(conn, my_table)

    # Generate server_client
    server_client: TSC.Server = connect_to_tableau()

    # get the project to deploy our extract to
    project: TSC.ProjectItem = find_project_to_publish_to(server_client, sys.argv[1])

    # choose publishing mode - Overwrite, Append, or CreateNew
    publish_mode = TSC.Server.PublishMode.Overwrite

    new_datasource: TSC.DatasourceItem = TSC.DatasourceItem(project_id=project.id)
    new_datasource = server_client.datasources.publish(
        new_datasource,
        'csv-to-hyper-example.hyper',
        publish_mode,
    )

    print(f'Datasource published to folder: {new_datasource.project_name}')
    print(f'New datasource ID: {new_datasource.id}')


if __name__ == '__main__':
    main()
