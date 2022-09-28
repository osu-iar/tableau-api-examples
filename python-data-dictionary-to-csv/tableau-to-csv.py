import tableauserverclient as TSC
import os
import sys

from dotenv import load_dotenv
from typing import List


load_dotenv()


def connect_to_tableau() -> TSC.Server:
    # Create an authentication object and sign in to the server
    # Tableau Doc: https://tableau.github.io/server-client-python/docs/api-ref#authentication
    auth: TSC.PersonalAccessTokenAuth = TSC.PersonalAccessTokenAuth(
        os.getenv('tableau_token_name'),
        os.getenv('tableau_token_value')
    )
    server: TSC.Server = TSC.Server('https://analytics.oregonstate.edu', use_server_version=True)

    server.auth.sign_in(auth)
    return server


def build_view_search_requirements(project_name: str, view_name: str) -> TSC.RequestOptions:
    # Build the req_options parameter
    # Tableau Doc: https://tableau.github.io/server-client-python/docs/filter-sort
    req_options = TSC.RequestOptions()

    # filter to the project
    req_options.filter.add(
        TSC.Filter(
            TSC.RequestOptions.Field.ProjectName,
            TSC.RequestOptions.Operator.Equals,
            project_name
        )
    )

    # filter to the view
    req_options.filter.add(
        TSC.Filter(
            TSC.RequestOptions.Field.Name,
            TSC.RequestOptions.Operator.Equals,
            view_name
        )
    )

    return req_options


def find_view(server: TSC.Server, project_name: str, view_name: str) -> TSC.ViewItem:
    # find the desired workbook
    req_options = build_view_search_requirements(project_name, view_name)

    matching_views: List[TSC.ViewItem]
    pagination_item: TSC.PaginationItem
    matching_views, pagination_item = server.views.get(req_options)

    # Check how many items were found
    if pagination_item.total_available == 0:
        print('Error: No matching views found.')
        sys.exit(1)
    elif pagination_item.total_available > 1:
        print('Warning: Multiple views found. Going with the first found view.')

    view = matching_views[0]
    return view


def main():
    server_client: TSC.Server = connect_to_tableau()
    view: TSC.ViewItem = find_view(server_client, 'HelioCampus Dashboards', 'Data Dictionary')

    server_client.views.populate_csv(view)
    with open('./out.csv', 'wb') as f:
        f.write(b''.join(view.csv))


if __name__ == '__main__':
    main()
