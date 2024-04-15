import unittest
from unittest.mock import patch

class TestSshCredential(unittest.TestCase):

    @patch('os.getenv')
    def test_ssh_credential(self, mock_getenv):
        mock_getenv.side_effect = [
            "SMTP_SENDER_EMAIL",
            "SMTP_SENDER_PASSWORD",
            "SMTP_RECIEVER_EMAIL",
            "IMAP_SENDER_EMAIL",
            "IMAP_SENDER_PASSWORD",
            "IMAP_RECIEVER_EMAIL",
            "SSH_USERNAME",
            "SSH_PASSWORD",
            "MYSQL_USERNAME",
            "MYSQL_PASSWORD",
            "MYSQL_DATABASE"
        ]
        
        from src.shared.connections.credentials import SshCredential
        credential = SshCredential()

        self.assertEqual(credential.get_host(), "ssh.pythonanywhere.com")
        self.assertEqual(credential.get_port(), 3306)
        self.assertEqual(credential.get_username(), 'SSH_USERNAME')
        self.assertEqual(credential.get_password(), 'SSH_PASSWORD')
        self.assertEqual(credential.get_hostname(), 'SSH_USERNAME.mysql.pythonanywhere-services.com')

if __name__ == '__main__':
    unittest.main()