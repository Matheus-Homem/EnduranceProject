import sshtunnel
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from src.shared.credentials import PRD, MySqlCredential, SshCredential
from src.shared.logger import LoggingManager

sshtunnel.SSH_TIMEOUT = 5.0
sshtunnel.TUNNEL_TIMEOUT = 5.0


class DatabaseConnector:
    def __init__(self, logger=LoggingManager(class_name=__name__.__class__)):
        self.mysql_credentials = MySqlCredential().get_all_credentials()
        self.logger = logger.get_logger()
        self.Session = None
        self.engine = None
        self._create_engine()

    def _is_prd_environment(self) -> bool:
        return PRD == "EnduranceProject"

    def _create_engine(self) -> None:
        if self._is_prd_environment():
            self.logger.info("Creating remote engine")
            engine_url = self._get_remote_engine_url()
        else:
            self.logger.info("Creating local engine")
            engine_url = self._get_local_engine_url()

        self.engine = create_engine(engine_url, pool_recycle=3600)
        self.Session = scoped_session(sessionmaker(bind=self.engine))
        self.logger.info("Engine created successfully")

    def _get_remote_engine_url(self) -> str:
        return f"mysql+pymysql://{self.mysql_credentials['username']}:{self.mysql_credentials['password']}@{self.mysql_credentials['hostname']}/{self.mysql_credentials['database']}"

    def _get_local_engine_url(self) -> str:
        ssh_credentials = SshCredential().get_all_credentials()
        ssh_tunnel = sshtunnel.SSHTunnelForwarder(
            ssh_address_or_host=ssh_credentials.get("host"),
            ssh_username=ssh_credentials.get("username"),
            ssh_password=ssh_credentials.get("password"),
            remote_bind_address=(
                ssh_credentials.get("hostname"),
                ssh_credentials.get("port"),
            ),
        )
        ssh_tunnel.start()
        return f"mysql+pymysql://{self.mysql_credentials['username']}:{self.mysql_credentials['password']}@localhost:{ssh_tunnel.local_bind_port}/{self.mysql_credentials['database']}"
