import unittest
from unittest.mock import patch

class TestCredentials(unittest.TestCase):
    @patch('os.getenv')
    def test_credentials(self, mock_getenv):
        mock_getenv.side_effect = ['username', 'password', 'reciever', 'sender', 'imap_password', 'imap_reciever', 'validated_email', 'mongo_uri']

        from src.env.credentials import Credentials

        credentials = Credentials()

        self.assertEqual(credentials.SMTP_PORT, 587)
        self.assertEqual(credentials.SMTP_SERVER, "smtp.gmail.com")
        self.assertEqual(credentials.SMTP_USERNAME, 'username')
        self.assertEqual(credentials.SMTP_PASSWORD, 'password')
        self.assertEqual(credentials.SMTP_RECIEVER, 'reciever')
        self.assertEqual(credentials.IMAP_SENDER, 'sender')
        self.assertEqual(credentials.IMAP_PASSWORD, 'imap_password')
        self.assertEqual(credentials.IMAP_RECIEVER, 'imap_reciever')
        self.assertEqual(credentials.VALIDATED_EMAIL, 'validated_email')
        self.assertEqual(credentials.MONGO_URI, 'mongo_uri')

if __name__ == '__main__':
    unittest.main()