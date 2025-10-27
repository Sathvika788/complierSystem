# src/languages/sql.py
import os
import tempfile
import subprocess
from typing import Dict, Any
from src.languages.base import BaseLanguage

class SQLLanguage(BaseLanguage):
    @property
    def name(self) -> str:
        return "SQL"
    
    @property
    def extension(self) -> str:
        return ".sql"
    
    def _setup_sample_database(self, cursor):
        """Set up sample tables with data for demonstration"""
        # Create sample tables
        sample_schema = [
            """CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT,
                age INTEGER
            )""",
            """CREATE TABLE products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                price REAL,
                category TEXT
            )""",
            """CREATE TABLE orders (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                product_id INTEGER,
                quantity INTEGER,
                order_date TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (product_id) REFERENCES products (id)
            )"""
        ]
        
        sample_data = [
            # Users
            "INSERT INTO users VALUES (1, 'John Doe', 'john@email.com', 30)",
            "INSERT INTO users VALUES (2, 'Jane Smith', 'jane@email.com', 25)",
            "INSERT INTO users VALUES (3, 'Bob Johnson', 'bob@email.com', 35)",
            
            # Products
            "INSERT INTO products VALUES (1, 'Laptop', 999.99, 'Electronics')",
            "INSERT INTO products VALUES (2, 'Book', 19.99, 'Education')",
            "INSERT INTO products VALUES (3, 'Headphones', 149.99, 'Electronics')",
            
            # Orders
            "INSERT INTO orders VALUES (1, 1, 1, 1, '2024-01-15')",
            "INSERT INTO orders VALUES (2, 2, 2, 3, '2024-01-16')",
            "INSERT INTO orders VALUES (3, 1, 3, 2, '2024-01-17')",
            "INSERT INTO orders VALUES (4, 3, 1, 1, '2024-01-18')"
        ]
        
        # Execute schema and data
        for sql in sample_schema + sample_data:
            try:
                cursor.execute(sql)
            except:
                pass  # Tables might already exist
    
    def compile_code(self, code: str, input_data: str, timeout: int, memory_limit: int) -> Dict[str, Any]:
        try:
            import sqlite3
            
            # Create in-memory database
            conn = sqlite3.connect(':memory:')
            cursor = conn.cursor()
            
            # Set up sample database
            self._setup_sample_database(cursor)
            
            # Split SQL commands
            sql_commands = [cmd.strip() for cmd in code.split(';') if cmd.strip()]
            
            results = []
            errors = []
            
            for i, sql_command in enumerate(sql_commands):
                if not sql_command.strip():
                    continue
                    
                try:
                    # Execute SQL command
                    cursor.execute(sql_command)
                    
                    # Handle different types of SQL commands
                    sql_upper = sql_command.upper().strip()
                    
                    if sql_upper.startswith('SELECT'):
                        # For SELECT queries, format the results nicely
                        rows = cursor.fetchall()
                        if cursor.description:
                            # Get column names
                            columns = [desc[0] for desc in cursor.description]
                            results.append(f"Query {i+1} Results:")
                            results.append(" | ".join(columns))
                            results.append("-" * (len(" | ".join(columns)) + 10))
                            
                            for row in rows:
                                results.append(" | ".join(str(cell) for cell in row))
                            results.append(f"({len(rows)} row(s) returned)")
                            results.append("")
                        else:
                            results.append(f"Query {i+1}: No results")
                    
                    elif sql_upper.startswith(('INSERT', 'UPDATE', 'DELETE')):
                        # For DML commands, show affected rows
                        affected = cursor.rowcount
                        results.append(f"Query {i+1}: {sql_upper.split()[0]} completed - {affected} row(s) affected")
                        conn.commit()
                    
                    elif sql_upper.startswith(('CREATE', 'ALTER', 'DROP')):
                        # For DDL commands
                        results.append(f"Query {i+1}: {sql_upper.split()[0]} completed successfully")
                    
                    else:
                        results.append(f"Query {i+1}: Executed successfully")
                        
                except sqlite3.Error as e:
                    errors.append(f"Query {i+1} Error: {e}")
            
            conn.close()
            
            output = '\n'.join(results)
            error_output = '\n'.join(errors) if errors else ''
            
            success = len(errors) == 0
            if not sql_commands:
                output = "No SQL commands found. Use semicolons to separate multiple commands."
                success = False
            
            return {
                'success': success,
                'output': output,
                'error': error_output,
                'exit_code': 0 if success else 1
            }
            
        except ImportError:
            return {
                'success': False,
                'output': '',
                'error': 'SQLite3 module not available. SQL support requires Python sqlite3.',
                'exit_code': -1
            }
        except Exception as e:
            return {
                'success': False,
                'output': '',
                'error': f'SQL execution error: {e}',
                'exit_code': -1
            }
    
    def execute(self, code: str, input_data: str, timeout: int, memory_limit: int) -> Dict[str, Any]:
        return self.compile_code(code, input_data, timeout, memory_limit)