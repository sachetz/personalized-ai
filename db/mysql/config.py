"""
Config for the MySQL DB Connector Client
"""

import os
from dotenv import load_dotenv

load_dotenv()

MYSQL_CLIENT_LOG_PATH = os.getenv("MYSQL_CLIENT_LOG_PATH", "logs/mysql_client.log")
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DB = os.getenv("MYSQL_DB", "personalisedai")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3307")
