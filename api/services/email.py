import jinja2

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from services.formatter import LeaseFormatterService


class EmailService:

    SG_API_KEY = "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"

    @staticmethod
    def _get_email_html(lease):
        formatted = LeaseFormatterService.format_lease_for_android(lease)

        return (
            jinja2.Environment(
                loader=jinja2.FileSystemLoader("./templates/"),
                trim_blocks=True,
                lstrip_blocks=True,
            )
            .get_template("lease_email.html")
            .render(issue_count=len(formatted["Issues"]), **formatted)
            .replace("\n", "")
        )

    @staticmethod
    def email_lease_analysis(to_email, lease):

        content = EmailService._get_email_html(lease)
        message = Mail(
            from_email="stariqmi@uwaterloo.ca",
            to_emails=to_email,
            subject="RentSafe - Lease Analysis ({})".format(lease["LeaseDocumentName"]),
            html_content=content,
        )

        try:
            sg = SendGridAPIClient(EmailService.SG_API_KEY)
            sg.send(message)
        except Exception as e:
            print(e)
