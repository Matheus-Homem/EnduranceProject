from src.shared.connections.builder import Connector, build_connection
from src.report.email.message import MessageBuilder


class EmailManager:
    def __init__(self, calendar):
        # TODO: Implement logger over print
        self.calendar = calendar
    
    def _configure_subject(self, message):
        return MessageBuilder.attach_subject(
            message=message,
            subject=f"Daily Report: {self.calendar.date}"
        )
    
    def _configure_body(self, message):
        return MessageBuilder.attach_text(
            message=message,
            text=f"""
            Daily Report
            Date: {self.calendar.dt_fmtd}
            Day of the Week: {self.calendar.week_day}
            Week Number: {self.calendar.week_number}
            """
        )

    def _attach_files(self, message):
        if self.calendar.get_partitioned_file_path(fmt="pdf"):
            return MessageBuilder.attach_file(
                message=message,
                attachment_path=self.paths.get_partitioned_file_path(fmt="pdf")
            )

    def dispatch(self):
        
        # Build connection and login
        smtp_connection = build_connection(connection_type=Connector.SMTP)
        smtp_connection.account_login()

        # Create and configure message
        message = MessageBuilder.create_multipart_message()
        message = smtp_connection.address_message(message)
        message = self._configure_body(message=message)
        message = self._configure_subject(message=message)
        message = self._attach_files(message=message)

        # Send email
        smtp_connection.send_email(message=message)
