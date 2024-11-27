"""
Client class for MySQL connection
"""

from typing import Any, Dict, List, Optional, Tuple

import mysql.connector
from mysql.connector import Error

from logger.logger import setup_logger
from db.mysql import config

logger = setup_logger(config.MYSQL_CLIENT_LOG_PATH)


class MySQLClient:
    """
    Client class for MySQL connection
    """

    _instance = None
    _connection = None

    def __new__(cls, *args, **kwargs):
        """
        Singleton class implementation.
        """

        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self):
        """
        Initializes the MySQL Client with connection parameters.
        """

        if not self._connection or not self.connection.is_connected():
            try:
                self.connection = mysql.connector.connect(
                    host=config.MYSQL_HOST,
                    user=config.MYSQL_USER,
                    password=config.MYSQL_PASSWORD,
                    database=config.MYSQL_DB,
                    port=config.MYSQL_PORT,
                    autocommit=False
                )
                if self.connection.is_connected():
                    logger.info("Successfully connected to the database.")
            except Error as e:
                logger.error("Error connecting to MySQL: %s", str(e))
                raise

    def close(self):
        """Closes the connection to the MySQL database."""

        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("MySQL connection closed.")

    def execute_query(
        self, query: str, params: Optional[Tuple[Any, ...]] = None
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Executes a SELECT query and returns the results.

        :param query: The SELECT query to execute.
        :param params: Optional tuple of parameters to pass with the query.
        :return: A list of dictionaries representing rows, or None for non-SELECT queries.
        """

        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query, params)
            if cursor.with_rows:
                result = cursor.fetchall()
                return result
            else:
                self.connection.commit()
                return None
        except Error as e:
            self.connection.rollback()
            logger.error("Error executing query: %s", str(e))
            raise
        finally:
            cursor.close()

    def insert(
        self, table: str, data: Dict[str, Any]
    ) -> int:
        """
        Inserts a record into a table.

        :param table: The table name.
        :param data: A dictionary of column names and their corresponding values.
        :return: The ID of the inserted row.
        """
        columns = ', '.join(f"`{col}`" for col in data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        values = tuple(data.values())

        query = f"INSERT INTO `{table}` ({columns}) VALUES ({placeholders})"
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, values)
            self.connection.commit()
            inserted_id = cursor.lastrowid
            logger.info("Inserted record with ID: %s", str(inserted_id))
            return inserted_id
        except Error as e:
            self.connection.rollback()
            logger.error("Error inserting record: %s", str(e))
            raise
        finally:
            cursor.close()

    def update(
        self, table: str, data: Dict[str, Any], where: str, params: Tuple[Any, ...]
    ) -> int:
        """
        Updates records in a table based on a condition.

        :param table: The table name.
        :param data: A dictionary of column names and their new values.
        :param where: The WHERE clause (e.g., "id = %s").
        :param params: Parameters to pass to the WHERE clause.
        :return: The number of rows affected.
        """
        set_clause = ', '.join(f"`{col}` = %s" for col in data.keys())
        values = tuple(data.values()) + params

        query = f"UPDATE `{table}` SET {set_clause} WHERE {where}"
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, values)
            self.connection.commit()
            affected = cursor.rowcount
            logger.info("Updated %s records.", str(affected))
            return affected
        except Error as e:
            self.connection.rollback()
            logger.error("Error updating records: %s", str(e))
            raise
        finally:
            cursor.close()

    def delete(
        self, table: str, where: str, params: Tuple[Any, ...]
    ) -> int:
        """
        Deletes records from a table based on a condition.

        :param table: The table name.
        :param where: The WHERE clause (e.g., "id = %s").
        :param params: Parameters to pass to the WHERE clause.
        :return: The number of rows affected.
        """
        query = f"DELETE FROM `{table}` WHERE {where}"
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params)
            self.connection.commit()
            affected = cursor.rowcount
            logger.info("Deleted %s records.", str(affected))
            return affected
        except Error as e:
            self.connection.rollback()
            logger.error("Error deleting records: %s", str(e))
            raise
        finally:
            cursor.close()
