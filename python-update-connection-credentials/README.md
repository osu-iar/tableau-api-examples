# python-update-connection-credentials

This example polls Tableau Server for all connection items visible to the authenticated user and updates the credentials for each connection item. This example is very simple in the fact that it does **not** utilize filtering and simply checks every object it can see. IAR's use case does not greatly benefit from doing so, but yours may.

{% warning %}

**Warning:** Due to limitations of Tableau Server, you cannot update the credentials of a given connection **unless the authenticated user owns the item**. Even if the authenticated user has admin rights to the resources, attempting to update the resource will result in a failure.

{% endwarning %}

## Running the Example

1. Copy the file `.env-dist` to `.env` and fill in the values for your authentication token and the Tableau Server URL.
2. Install the script dependencies found in `requirements.txt`
3. Run the script, `main.py`.