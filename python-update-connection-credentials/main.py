import tableauserverclient as TSC
import os
import sys

from dotenv import load_dotenv
from typing import Iterator, Tuple, Any


load_dotenv()


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


def get_all_connections(server_client: TSC.Server) -> Iterator[Tuple[str, Any, TSC.ConnectionItem]]:
    workbook: TSC.WorkbookItem
    datasource: TSC.DatasourceItem
    flow: TSC.FlowItem
    connection: TSC.ConnectionItem

    # Yield the connections in workbooks
    for workbook in TSC.Pager(server_client.workbooks):
        server_client.workbooks.populate_connections(workbook)
        for connection in workbook.connections:
            yield 'workbook', workbook, connection

    # Yield the connections in datasets
    for datasource in TSC.Pager(server_client.datasources):
        server_client.datasources.populate_connections(datasource)
        for connection in datasource.connections:
            yield 'datasource', datasource, connection

    for flow in TSC.Pager(server_client.flows):
        server_client.flows.populate_connections(flow)
        for connection in flow.connections:
            yield 'flow', flow, connection


def main():
    server: TSC.Server = connect_to_tableau()
    for obj_type, obj, connection in get_all_connections(server):
        if connection.username == os.getenv('tableau_username_to_update'):
            connection.username = os.getenv('tableau_username_to_update')
            connection.password = os.getenv('tableau_new_user_password')
            connection.embed_password = True

            if obj_type == 'workbook':
                server.workbooks.update_connection(obj, connection)
            elif obj_type == 'datasource':
                server.datasources.update_connection(obj, connection)
            elif obj_type == 'flow':
                server.flows.update_connection(obj, connection)


if __name__ == '__main__':
    main()