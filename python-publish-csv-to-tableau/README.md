# python-publish-csv-to-tableau

To upload a dataset as an extract on Tableau Server, it must be converted to a `.hyper` file first. This example converts the CSV file, `example.csv`, to a hyper file then uploads that file to the project specified within the command line arguments.

## Running the Example

1. Copy the file `.env-dist` to `.env` and fill in the values for your authentication token and the Tableau Server URL.
2. Install the script dependencies found in `requirements.txt`
3. Run the script, `main.py`.
   - You will need to define the name of the project folder as the first arguement when running the script.
   - Ex: `python main.py my_project_name`