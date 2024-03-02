from src.env.credentials import credentials
import imaplib

class IMAPConnection:

	def __init__(self):
		
		self.server = "imap.gmail.com"
		self.email = credentials.IMAP_RECIPIENT
		self.password = credentials.IMAP_PASSWORD
		self.sender = credentials.IMAP_SENDER
		self._configure()
		self._search_inbox(sender_address=self.sender)

	def _configure(self):
		self.mail = imaplib.IMAP4_SSL(self.server)
		self.mail.login(self.email, self.password)

	def _search_inbox(self, sender_address):
		self.mail.select("inbox")
		self.result, self.data = self.mail.search(None, f"FROM '{sender_address}'")

	def get_mail(self):
		return self.mail
	
	def get_data(self):
		return self.data