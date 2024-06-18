from os import path
from docusign_admin.apis import BulkImportsApi
from flask import session, Response
import time

from app.admin.utils import create_admin_api_client, get_organization_id
from app.ds_config import DS_CONFIG


class Eg004AddUsersViaBulkImportController:
    @staticmethod
    def get_example_csv():
        """
        Creates an example of a CSV file, such as that needs to be sent to the Docusign server
        """

        # Returns an example of a CSV file
        return (
            "AccountID,UserName,UserEmail,PermissionSet\n"
            f"{session['ds_account_id']},Example User1,exampleuser1@example.com,DS Admin\n"
            f"{session['ds_account_id']},Example User2,exampleuser2@example.com,DS Admin\n"
        )

    @staticmethod
    def worker(self, request):
        """
        Create a user list import request and
        returns a list of pending and completed import requests:
        1. Create the import API object
        2. Getting a CSV file from a form and converting it to a string
        3. Creating an import API object
        4. Setting headers for creating bulk import request
        5. Returns the response from the create_bulk_import_add_users_request method
        """

        # Get organization ID
        organization_id = get_organization_id()

        # Create the export API object
        #ds-snippet-start:Admin4Step2
        api_client = create_admin_api_client(
            access_token=session["ds_access_token"]
        )
        #ds-snippet-end:Admin4Step2

        # Getting a CSV file from a form and saving it
        uploaded_file = request.files['csv_file']
        csv_folder_path = path.abspath(path.join(path.dirname(path.realpath(__file__)), "csv"))
        csv_file_path = path.join(csv_folder_path, "uploaded_file.csv")

        if uploaded_file and not uploaded_file.filename == '':
            uploaded_file.save(csv_file_path)
        else:
            content = Eg004AddUsersViaBulkImportController.get_example_csv()

            modified_content = content.replace("xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", session["ds_account_id"])

            with open(csv_file_path, "w") as file:
                file.write(modified_content)

        # Creating an import API object
        #ds-snippet-start:Admin4Step3
        import_api = BulkImportsApi(api_client=api_client)

        # Setting headers for creating bulk import request
        header_name, header_value = "Content-Disposition", "filename=myfile.csv"
        api_client.set_default_header(header_name, header_value)

        # Returns the response from the create_bulk_import_add_users_request method
        response = import_api.create_bulk_import_add_users_request(
            organization_id,
            csv_file_path
        )
        #ds-snippet-end:Admin4Step3

        # Save user list import id in a client session
        session['import_data_id'] = response.id
        
        return response

    @staticmethod
    def check_status():
        """Check request status"""

        organization_id = get_organization_id()

        api_client = create_admin_api_client(
            access_token=session["ds_access_token"]
        )

        # Creating an import API object
        import_api = BulkImportsApi(api_client=api_client)

        #ds-snippet-start:Admin4Step4
        import_results = import_api.get_bulk_user_import_request(organization_id, session['import_data_id'])
        #ds-snippet-end:Admin4Step4

        if import_results.status == "completed":
            return import_results
        else:
            return None
