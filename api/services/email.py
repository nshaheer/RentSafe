import base64

import jinja2

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail,
    Attachment,
    FileContent,
    FileName,
    FileType,
    Disposition,
    ContentId,
)

from services.formatter import LeaseFormatterService


class EmailService:

    SG_API_KEY = "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"

    @staticmethod
    def _get_email_html(lease):

        return (
            jinja2.Environment(
                loader=jinja2.FileSystemLoader("./templates/"),
                trim_blocks=True,
                lstrip_blocks=True,
            )
            .get_template("lease_email.html")
            .render(issue_count=len(lease["Issues"]), **lease)
            .replace("\n", "")
        )

    @staticmethod
    def email_lease_analysis(to_email, lease):

        formatted = LeaseFormatterService.format_lease_for_android(lease)
        subject = "RentSafe - "
        if len(formatted["Issues"]):
            subject += "{} issues(s) found".format(len(formatted["Issues"]))
        else:
            subject += "No issues found"

        content = EmailService._get_email_html(formatted)
        message = Mail(
            from_email="stariqmi@uwaterloo.ca",
            to_emails=to_email,
            subject=subject,
            html_content=content,
        )

        with open(lease["LeaseDocumentPath"], "rb") as f:
            data = f.read()
            f.close()
        encoded = base64.b64encode(data).decode()
        attachment = Attachment()
        attachment.file_content = FileContent(encoded)
        attachment.file_type = FileType("application/pdf")
        attachment.file_name = FileName(lease["LeaseDocumentName"])
        attachment.disposition = Disposition("attachment")
        attachment.content_id = ContentId("")
        message.attachment = attachment

        try:
            sg = SendGridAPIClient(EmailService.SG_API_KEY)
            sg.send(message)
            return True
        except Exception as e:
            print(e)
            return False
