import base64
from os import path

from docusign_esign import EnvelopesApi, EnvelopesApi, EnvelopeDefinition, \
    Document, Signer, CarbonCopy, SignHere, Tabs, Recipients, EnvelopeViewRequest, EnvelopeViewSettings, \
    EnvelopeViewRecipientSettings, EnvelopeViewDocumentSettings, EnvelopeViewTaggerSettings, EnvelopeViewTemplateSettings
from flask import url_for, session, request

from ...consts import pattern, demo_docs_path
from ...docusign import create_api_client


class Eg011EmbeddedSendingController:

    @staticmethod
    def get_args():
        """Get required session and request arguments"""
        # More data validation would be a good idea here
        # Strip anything other than characters listed
        signer_email = pattern.sub("", request.form.get("signer_email"))
        signer_name = pattern.sub("", request.form.get("signer_name"))
        cc_email = pattern.sub("", request.form.get("cc_email"))
        cc_name = pattern.sub("", request.form.get("cc_name"))
        starting_view = pattern.sub("", request.form.get("starting_view"))

        envelope_args = {
            "signer_email": signer_email,
            "signer_name": signer_name,
            "cc_email": cc_email,
            "cc_name": cc_name,
            "status": "created",
        }
        args = {
            "starting_view": starting_view,
            "account_id": session["ds_account_id"],
            "base_path": session["ds_base_path"],
            "access_token": session["ds_access_token"],
            "envelope_args": envelope_args,
            "ds_return_url": url_for("ds.ds_return", _external=True),
            "starting_view": starting_view,
        }
        return args

    @classmethod
    def worker(cls, args, doc_docx_path, doc_pdf_path):
        """
        This function does the work of creating the envelope in
        draft mode and returning a URL for the sender"s view
        """

        # Step 2. Create the envelope with "created" (draft) status
        envelope = cls.create_envelope(args, doc_docx_path, doc_pdf_path)
        envelope_id = envelope.envelope_id

        # Step 3. Create the sender view
        sender_view_url = cls.create_sender_view(args, envelope_id)

        return {"envelope_id": envelope_id, "redirect_url": sender_view_url}
    
    @classmethod
    #ds-snippet-start:eSign11Step3
    def create_sender_view(cls, args, envelope_id):
        view_request = cls.make_envelope_view_request(args)
        # Exceptions will be caught by the calling function
        api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])

        envelope_api = EnvelopesApi(api_client)
        sender_view = envelope_api.create_sender_view(
            account_id=args["account_id"],
            envelope_id=envelope_id,
            envelope_view_request=view_request
        )

        # Switch to Recipient and Documents view if requested by the user
        url = sender_view.url

        return url
    
    @classmethod
    def make_envelope_view_request(cls, args):
        view_request = EnvelopeViewRequest(
            return_url=args["ds_return_url"],
            view_access="envelope",
            settings=EnvelopeViewSettings(
                starting_screen=args["starting_view"],
                send_button_action="send",
                show_back_button="false",
                back_button_action="previousPage",
                show_header_actions="false",
                show_discard_action="false",
                lock_token="",
                recipient_settings=EnvelopeViewRecipientSettings(
                    show_edit_recipients="false",
                    show_contacts_list="false"
                ),
                document_settings=EnvelopeViewDocumentSettings(
                    show_edit_documents="false",
                    show_edit_document_visibility="false",
                    show_edit_pages="false"
                ),
                tagger_settings=EnvelopeViewTaggerSettings(
                    palette_sections="default",
                    palette_default="custom"
                ),
                template_settings=EnvelopeViewTemplateSettings(
                    show_matching_templates_prompt="true"
                )
            )
        )

        return view_request
    #ds-snippet-end:eSign11Step3
    
    @classmethod
    #ds-snippet-start:eSign11Step2
    def create_envelope(cls, args, doc_docx_path, doc_pdf_path):
        envelope_args = args["envelope_args"]
        # Create the envelope request object
        envelope_definition = cls.make_envelope(envelope_args, doc_docx_path, doc_pdf_path)
        api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])
        # Call Envelopes::create API method
        # Exceptions will be caught by the calling function
        envelopes_api = EnvelopesApi(api_client)
        return envelopes_api.create_envelope(account_id=args["account_id"], envelope_definition=envelope_definition)

    @classmethod
    def make_envelope(cls, args, doc_docx_path, doc_pdf_path):
        """
        Creates envelope
        Document 1: An HTML document.
        Document 2: A Word .docx document.
        Document 3: A PDF document.
        DocuSign will convert all of the documents to the PDF format.
        The recipients" field tags are placed using <b>anchor</b> strings.
        """

        # document 1 (html) has sign here anchor tag **signature_1**
        # document 2 (docx) has sign here anchor tag /sn1/
        # document 3 (pdf)  has sign here anchor tag /sn1/
        #
        # The envelope has two recipients.
        # recipient 1 - signer
        # recipient 2 - cc
        # The envelope will be sent first to the signer.
        # After it is signed, a copy is sent to the cc person.

        # create the envelope definition
        env = EnvelopeDefinition(
            email_subject="Please sign this document set"
        )
        doc1_b64 = base64.b64encode(bytes(cls.create_document1(args), "utf-8")).decode("ascii")
        # read files 2 and 3 from a local directory
        # The reads could raise an exception if the file is not available!
        with open(path.join(demo_docs_path, doc_docx_path), "rb") as file:
            doc2_docx_bytes = file.read()
        doc2_b64 = base64.b64encode(doc2_docx_bytes).decode("ascii")
        with open(path.join(demo_docs_path, doc_pdf_path), "rb") as file:
            doc3_pdf_bytes = file.read()
        doc3_b64 = base64.b64encode(doc3_pdf_bytes).decode("ascii")

        # Create the document models
        document1 = Document(  # create the DocuSign document object
            document_base64=doc1_b64,
            name="Order acknowledgement",  # can be different from actual file name
            file_extension="html",  # many different document types are accepted
            document_id="1"  # a label used to reference the doc
        )
        document2 = Document(  # create the DocuSign document object
            document_base64=doc2_b64,
            name="Battle Plan",  # can be different from actual file name
            file_extension="docx",  # many different document types are accepted
            document_id="2"  # a label used to reference the doc
        )
        document3 = Document(  # create the DocuSign document object
            document_base64=doc3_b64,
            name="Lorem Ipsum",  # can be different from actual file name
            file_extension="pdf",  # many different document types are accepted
            document_id="3"  # a label used to reference the doc
        )
        # The order in the docs array determines the order in the envelope
        env.documents = [document1, document2, document3]

        # Create the signer recipient model
        signer1 = Signer(
            email=args["signer_email"],
            name=args["signer_name"],
            recipient_id="1",
            routing_order="1"
        )
        # routingOrder (lower means earlier) determines the order of deliveries
        # to the recipients. Parallel routing order is supported by using the
        # same integer as the order for two or more recipients.

        # create a cc recipient to receive a copy of the documents
        cc1 = CarbonCopy(
            email=args["cc_email"],
            name=args["cc_name"],
            recipient_id="2",
            routing_order="2"
        )

        # Create signHere fields (also known as tabs) on the documents,
        # We"re using anchor (autoPlace) positioning
        #
        # The DocuSign platform searches throughout your envelope"s
        # documents for matching anchor strings. So the
        # signHere2 tab will be used in both document 2 and 3 since they
        # use the same anchor string for their "signer 1" tabs.
        sign_here1 = SignHere(
            anchor_string="**signature_1**",
            anchor_units="pixels",
            anchor_y_offset="10",
            anchor_x_offset="20"
        )

        sign_here2 = SignHere(
            anchor_string="/sn1/",
            anchor_units="pixels",
            anchor_y_offset="10",
            anchor_x_offset="20"
        )

        # Add the tabs model (including the sign_here tabs) to the signer
        # The Tabs object wants arrays of the different field/tab types
        signer1.tabs = Tabs(sign_here_tabs=[sign_here1, sign_here2])

        # Add the recipients to the envelope object
        recipients = Recipients(signers=[signer1], carbon_copies=[cc1])
        env.recipients = recipients

        # Request that the envelope be sent by setting |status| to "sent".
        # To request that the envelope be created as a draft, set to "created"
        env.status = args["status"]

        return env

    @classmethod
    def create_document1(cls, args):
        """ Creates document 1 -- an html document"""

        return f"""
        <!DOCTYPE html>
        <html>
            <head>
              <meta charset="UTF-8">
            </head>
            <body style="font-family:sans-serif;margin-left:2em;">
            <h1 style="font-family: "Trebuchet MS", Helvetica, sans-serif;
                color: darkblue;margin-bottom: 0;">World Wide Corp</h1>
            <h2 style="font-family: "Trebuchet MS", Helvetica, sans-serif;
              margin-top: 0px;margin-bottom: 3.5em;font-size: 1em;
              color: darkblue;">Order Processing Division</h2>
            <h4>Ordered by {args["signer_name"]}</h4>
            <p style="margin-top:0em; margin-bottom:0em;">Email: {args["signer_email"]}</p>
            <p style="margin-top:0em; margin-bottom:0em;">Copy to: {args["cc_name"]}, {args["cc_email"]}</p>
            <p style="margin-top:3em;">
                Candy bonbon pastry jujubes lollipop wafer biscuit biscuit. Topping brownie sesame snaps sweet roll pie. 
                Croissant danish biscuit soufflé caramels jujubes jelly. Dragée danish caramels lemon drops dragée. 
                Gummi bears cupcake biscuit tiramisu sugar plum pastry. Dragée gummies applicake pudding liquorice. 
                Donut jujubes oat cake jelly-o. 
                Dessert bear claw chocolate cake gummies lollipop sugar plum ice cream gummies cheesecake.
            </p>
            <!-- Note the anchor tag for the signature field is in white. -->
            <h3 style="margin-top:3em;">Agreed: <span style="color:white;">**signature_1**/</span></h3>
            </body>
        </html>
        """
    #ds-snippet-end:eSign11Step2
