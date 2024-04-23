import unittest
from unittest.mock import patch
from src.shared.connections.credentials import SmtpCredential, SshCredential, MySqlCredential


OS_ENVIRON_DICT = {
    "SMTP_SENDER_EMAIL" : "smtp_sender_email",
    "SMTP_SENDER_PASSWORD" : "smtp_sender_password",
    "SMTP_RECEIVER_EMAIL" : "smtp_reciever_email",
    "IMAP_SENDER_EMAIL" : "imap_sender_email",
    "IMAP_SENDER_PASSWORD" : "imap_sender_password",
    "IMAP_RECEIVER_EMAIL" : "imap_reciever_email",
    "SSH_USERNAME": "ssh_username",
    "SSH_PASSWORD": "ssh_password",
    "MYSQL_USERNAME": "mysql_username",
    "MYSQL_PASSWORD": "mysql_password",
    "MYSQL_DATABASE": "mysql_database",
}


class TestCredentials(unittest.TestCase):

    @patch("src.shared.connections.credentials.os.getenv", side_effect=lambda x: OS_ENVIRON_DICT.get(x))
    def test_smtp_credentials(self, mock_getenv):
        smtp_credentials = SmtpCredential(getenv=mock_getenv)
        self.assertEqual(smtp_credentials.get_port(), 587)
        self.assertEqual(smtp_credentials.get_server(), "smtp.gmail.com")
        self.assertEqual(smtp_credentials.get_sender(), 'smtp_sender_email')
        self.assertEqual(smtp_credentials.get_password(), 'smtp_sender_password')
        self.assertEqual(smtp_credentials.get_receiver(), 'smtp_reciever_email')

    @patch("src.shared.connections.credentials.os.getenv", side_effect=lambda x: OS_ENVIRON_DICT.get(x))
    def test_ssh_credentials(self, mock_getenv):
        ssh_credentials = SshCredential(getenv=mock_getenv)
        self.assertEqual(ssh_credentials.get_host(), "ssh.pythonanywhere.com")
        self.assertEqual(ssh_credentials.get_port(), 3306)
        self.assertEqual(ssh_credentials.get_username(), 'ssh_username')
        self.assertEqual(ssh_credentials.get_password(), 'ssh_password')
        self.assertEqual(ssh_credentials.get_hostname(), 'ssh_username.mysql.pythonanywhere-services.com')

    @patch("src.shared.connections.credentials.os.getenv", side_effect=lambda x: OS_ENVIRON_DICT.get(x))
    def test_mysql_credentials(self, mock_getenv):
        mysql_credentials = MySqlCredential(getenv=mock_getenv)
        self.assertEqual(mysql_credentials.get_host(), "127.0.0.1")
        self.assertEqual(mysql_credentials.get_username(), 'mysql_username')
        self.assertEqual(mysql_credentials.get_password(), 'mysql_password')
        self.assertEqual(mysql_credentials.get_database(), 'mysql_username$mysql_database')

if __name__ == '__main__':
    unittest.main()