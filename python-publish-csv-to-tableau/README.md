# python-publish-csv-to-tableau

This example converts a local CSV file to a `.hyper` file which is then uploaded as a published data source.

## Running the Example

1. Copy the file `.env-dist` to `.env` and fill in the values for your authentication token and the Tableau Server URL.
2. Install the script dependencies found in `requirements.txt`
3. Run the script, `main.py`.
   - You will need to define the name of the project folder as the first arguement when running the script.
   - Ex: `python main.py my_project_name`