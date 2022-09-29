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


def main():
    # Start by converting the CSV file into a hyper extract
    with HyperProcess(telemetry=Telemetry.DO_NOT_SEND_USAGE_DATA_TO_TABLEAU) as hyper:
        with Connection(hyper.endpoint, 'csv-to-hyper-example.hyper', CreateMode.CREATE_AND_REPLACE) as conn:
            my_table: TableDefinition = create_table_in_hyper_file(conn)
            insert_csv_into_hyper_file(conn, my_table)

    # upload
    server_client: TSC.Server = connect_to_tableau()
    server_client.datasources.publish()


if __name__ == '__main__':
    main()
