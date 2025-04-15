import os
import psycopg2
from psycopg2 import sql
from psycopg2.extras import DictCursor
from dotenv import load_dotenv
from typing import Optional, List, Dict, Any, Tuple
import pandas as pd

class DatabaseManager:
    def __init__(self):
        load_dotenv()
        self.connection = None
        self.cursor = None
        
    def connect(self) -> None:
        """Establishes a connection to the PostgreSQL database using credentials from .env file"""
        try:
            self.connection = psycopg2.connect(
                dbname=os.getenv('DB_NAME'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT')
            )
            self.cursor = self.connection.cursor(cursor_factory=DictCursor)
        except Exception as e:
            raise Exception(f"Error connecting to database: {str(e)}")

    def close(self) -> None:
        """Closes the database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def commit(self) -> None:
        """Commits the current transaction"""
        if self.connection:
            self.connection.commit()

    def rollback(self) -> None:
        """Rolls back the current transaction"""
        if self.connection:
            self.connection.rollback()

    def insert(self, schema: str, table: str, data: Dict[str, Any]) -> None:
        """
        Inserts data into a specified table in a given schema
        
        Args:
            schema (str): The schema name
            table (str): The table name
            data (Dict[str, Any]): Dictionary containing column names and values to insert
        """
        if not self.connection:
            self.connect()
            
        try:
            columns = sql.SQL(', ').join(map(sql.Identifier, data.keys()))
            values = sql.SQL(', ').join(map(sql.Literal, data.values()))
            
            query = sql.SQL("INSERT INTO {}.{} ({}) VALUES ({})").format(
                sql.Identifier(schema),
                sql.Identifier(table),
                columns,
                values
            )
            
            self.cursor.execute(query)
            self.commit()
            
        except Exception as e:
            self.rollback()
            raise Exception(f"Error inserting data: {str(e)}")

    def delete(self, schema: str, table: str, where_clause: Optional[str] = None, params: Optional[Tuple] = None) -> None:
        """
        Deletes data from a specified table in a given schema
        
        Args:
            schema (str): The schema name
            table (str): The table name
            where_clause (str, optional): WHERE clause for the delete operation
            params (Tuple, optional): Parameters for the WHERE clause
        """
        if not self.connection:
            self.connect()
            
        try:
            query = sql.SQL("DELETE FROM {}.{}").format(
                sql.Identifier(schema),
                sql.Identifier(table)
            )
            
            if where_clause:
                query = sql.SQL("{} WHERE {}").format(query, sql.SQL(where_clause))
            
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
                
            self.commit()
            
        except Exception as e:
            self.rollback()
            raise Exception(f"Error deleting data: {str(e)}")

    def insert_dataframe(self, df, table_name: str) -> bool:
        """
        Insert a pandas DataFrame into a database table
        
        Args:
            df: pandas DataFrame to insert
            table_name: Name of the table to insert into
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.connection:
            self.connect()
            
        try:
            # Convert DataFrame to list of tuples
            records = [tuple(x) for x in df.to_numpy()]
            
            # Get column names
            columns = df.columns.tolist()
            
            # Create the INSERT query
            query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
                sql.Identifier(table_name),
                sql.SQL(', ').join(map(sql.Identifier, columns)),
                sql.SQL(', ').join([sql.Placeholder()] * len(columns))
            )
            
            # Execute the query for each record
            for record in records:
                self.cursor.execute(query, record)
                
            self.commit()
            return True
            
        except Exception as e:
            self.rollback()
            raise Exception(f"Error inserting DataFrame: {str(e)}")

    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close() 