
from src.env.helpers import is_prd_environment
from src.shared.credentials import SshCredential, MySqlCredential

from functools import wraps
import pymysql
import sshtunnel

sshtunnel.SSH_TIMEOUT = 5.0
sshtunnel.TUNNEL_TIMEOUT = 5.0

def establish_mysql_connection(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        mysql_credentials = MySqlCredential().get_all_credentials()

        if is_prd_environment():
            connection = pymysql.connect(
                user=mysql_credentials.get("username"),
                passwd=mysql_credentials.get("password"),
                host=mysql_credentials.get("host"),
                port=tunnel.local_bind_port,
                db=mysql_credentials.get("database"),
            )
            print("Remote connection establish with success")

            try:
                cursor = connection.cursor()
                result = func(cursor, *args, **kwargs)
                connection.commit()
                return result
            except Exception as e:
                print(f"Error: {e}")
                connection.rollback()
            finally:
                if cursor:
                    cursor.close()
                if connection:
                    connection.close()
                print("Connection closed")
        
        else:
            ssh_credentials = SshCredential().get_all_credentials()
            
            with sshtunnel.SSHTunnelForwarder(
                ssh_address_or_host=ssh_credentials.get("host"),
                ssh_username=ssh_credentials.get("username"),
                ssh_password=ssh_credentials.get("password"),
                remote_bind_address=(
                    ssh_credentials.get("hostname"),
                    ssh_credentials.get("port")
                )
            ) as tunnel:
                connection = pymysql.connect(
                    user=mysql_credentials.get("username"),
                    passwd=mysql_credentials.get("password"),
                    host=mysql_credentials.get("host"),
                    port=tunnel.local_bind_port,
                    db=mysql_credentials.get("database"),
                )
                print("Local connection establish with success")

                try:
                    cursor = connection.cursor()
                    result = func(cursor, *args, **kwargs)
                    connection.commit()
                    return result
                except Exception as e:
                    print(f"Error: {e}")
                    connection.rollback()
                finally:
                    if cursor:
                        cursor.close()
                    if connection:
                        connection.close()
                    print("Connection closed")

    return wrapper