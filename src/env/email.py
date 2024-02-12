class MailConfig:
	def __init__(self, username, password, recipient):
		# Gmail SMTP Server Settings
		self.server = "smtp.gmail.com"  # SMTP server address for Gmail
		self.port = 587  # Port number for Gmail's SMTP server
		self.username = username  # Your Gmail email address
		self.password = password  # Your Gmail email password

		# Mailing Recipient
		self.recipient = recipient  # Email address of the recipient