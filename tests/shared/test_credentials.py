import unittest
from os import getenv

from src.shared.credentials import MySqlCredential, SshCredential


class TestCredentials(unittest.TestCase):

    def test_ssh_credentials(self):
        ssh_credentials = SshCredential().get_all_credentials()
        ssh_username = getenv("SSH_USERNAME")

        self.assertEqual(ssh_credentials["host"], "ssh.pythonanywhere.com")
        self.assertEqual(ssh_credentials["port"], 3306)
        self.assertEqual(ssh_credentials["username"], getenv("SSH_USERNAME"))
        self.assertEqual(ssh_credentials["password"], getenv("SSH_PASSWORD"))
        self.assertEqual(
            ssh_credentials["hostname"],
            f"{ssh_username}.mysql.pythonanywhere-services.com",
        )

    def test_mysql_credentials_prd(self):
        mysql_credentials = MySqlCredential().get_all_credentials(use_production_db=True)
        mysql_username = getenv("MYSQL_USERNAME")
        mysql_database_prd = getenv("MYSQL_DATABASE_PRD")

        self.assertEqual(mysql_credentials["host"], "127.0.0.1")
        self.assertEqual(mysql_credentials["username"], getenv("MYSQL_USERNAME"))
        self.assertEqual(mysql_credentials["password"], getenv("MYSQL_PASSWORD"))
        self.assertEqual(mysql_credentials["database"], f"{mysql_username}${mysql_database_prd}")
        self.assertEqual(
            mysql_credentials["hostname"],
            f"{mysql_username}.mysql.pythonanywhere-services.com",
        )

    def test_mysql_credentials_dev(self):
        mysql_credentials = MySqlCredential().get_all_credentials()
        mysql_username = getenv("MYSQL_USERNAME")
        mysql_database_dev = getenv("MYSQL_DATABASE_DEV")

        self.assertEqual(mysql_credentials["host"], "127.0.0.1")
        self.assertEqual(mysql_credentials["username"], getenv("MYSQL_USERNAME"))
        self.assertEqual(mysql_credentials["password"], getenv("MYSQL_PASSWORD"))
        self.assertEqual(mysql_credentials["database"], f"{mysql_username}${mysql_database_dev}")
        self.assertEqual(
            mysql_credentials["hostname"],
            f"{mysql_username}.mysql.pythonanywhere-services.com",
        )


if __name__ == "__main__":
    unittest.main()
