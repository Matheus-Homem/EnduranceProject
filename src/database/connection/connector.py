import logging
from typing import Dict, Literal

import sshtunnel
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from src.shared.credentials import PRD, MySqlCredential, SshCredential

sshtunnel.SSH_TIMEOUT = 20.0
sshtunnel.TUNNEL_TIMEOUT = 20.0


class DatabaseConnector:

    def __init__(
        self,
        use_production_db: bool,
    ):
        self.logger = logging.getLogger(__class__.__name__)
        self.use_production_db = use_production_db
        self.Session = None
        self.engine = None
        self.ssh_tunnel = None
        self.connection_type: Literal["local", "production"] = None

    def _is_prd_environment(self) -> bool:
        return PRD == "EnduranceProject"

    def _create_engine(self, mysql_credentials: MySqlCredential, ssh_credentials: SshCredential) -> None:
        try:
            mysql_keys = mysql_credentials.get_all_credentials(use_production_db=self.use_production_db)
            ssh_keys = ssh_credentials.get_all_credentials()

            if self._is_prd_environment():
                self.connection_type = "production"
                engine_url = self._construct_engine_url(mysql_keys)
            else:
                self.connection_type = "local"
                engine_url = self._get_local_engine_url(mysql_keys, ssh_keys)

            self.engine = create_engine(engine_url, pool_recycle=3600)
            self.Session = scoped_session(sessionmaker(bind=self.engine))
        except Exception as e:
            self.logger.error(f"Failed to create engine: {e}")
            raise

    def _get_local_engine_url(self, mysql_keys: Dict, ssh_keys: Dict) -> str:
        try:
            self.ssh_tunnel = sshtunnel.SSHTunnelForwarder(
                ssh_address_or_host=ssh_keys.get("host"),
                ssh_username=ssh_keys.get("username"),
                ssh_password=ssh_keys.get("password"),
                remote_bind_address=(
                    ssh_keys.get("hostname"),
                    ssh_keys.get("port"),
                ),
            )
            self.ssh_tunnel.start()
            return self._construct_engine_url(mysql_keys, local_environment=True)
        except Exception as e:
            self.logger.error(f"Failed to start SSH tunnel: {e}")
            raise

    def _construct_engine_url(self, mysql_keys: Dict, local_environment: bool = False) -> str:
        if local_environment:
            return f"mysql+pymysql://{mysql_keys.get('username')}:{mysql_keys.get('password')}@localhost:{self.ssh_tunnel.local_bind_port}/{mysql_keys.get('database')}"
        return f"mysql+pymysql://{mysql_keys.get('username')}:{mysql_keys.get('password')}@{mysql_keys.get('hostname')}/{mysql_keys.get('database')}"

    def get_session(self, mysql_credentials: MySqlCredential, ssh_credentials: SshCredential) -> Session:
        if self.Session is None:
            self._create_engine(mysql_credentials, ssh_credentials)
            self.logger.info(f"Session created successfully for {self.connection_type} environment")
            return self.Session
        return self.Session

    def close(self) -> None:
        if self.Session:
            self.Session.remove()
            self.logger.info("Session closed successfully")
        if self.engine:
            self.engine.dispose()
        if self.ssh_tunnel:
            self.ssh_tunnel.stop()
            self.logger.info("SSH tunnel stopped successfully")
