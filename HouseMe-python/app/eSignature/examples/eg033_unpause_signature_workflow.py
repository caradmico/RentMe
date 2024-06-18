from docusign_esign import EnvelopesApi, EnvelopeDefinition
from docusign_esign.models import Workflow
from flask import session

from ...docusign import create_api_client


class Eg033UnpauseSignatureWorkflowController:
    @staticmethod
    def get_args():
        """ Get session arguments """
        return {
            "account_id": session["ds_account_id"],
            "envelope_id": session["paused_envelope_id"],
            "base_path": session["ds_base_path"],
            "access_token": session["ds_access_token"],
        }

    @classmethod
    def worker(cls, args):
        """
        1. Call the envelope update method
        """

        # Create the envelope definition
        #ds-snippet-start:eSign33Step3
        env = EnvelopeDefinition(workflow=Workflow(workflow_status="in_progress"))
        #ds-snippet-end:eSign33Step3

        # Exceptions will be caught by the calling function
        #ds-snippet-start:eSign33Step2
        api_client = create_api_client(
            base_path=args["base_path"], access_token=args["access_token"]
        )
        #ds-snippet-end:eSign33Step2

        # Call Envelopes::update API method
        # Exceptions will be caught by the calling function
        #ds-snippet-start:eSign33Step4
        envelopes_api = EnvelopesApi(api_client)
        results = envelopes_api.update(
            account_id=args["account_id"],
            envelope_id=args["envelope_id"],
            envelope=env,
            resend_envelope=True
        )
        #ds-snippet-end:eSign33Step4
        return {"envelope_id": results.envelope_id}
