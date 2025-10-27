import pytest
from src.languages.sql import SQLLanguage

class TestSQLCompiler:
    def setup_method(self):
        self.sql_compiler = SQLLanguage()
    
    def test_sql_statement_splitting(self):
        sql = """
        CREATE TABLE users (id INT, name TEXT);
        INSERT INTO users VALUES (1, 'John');
        SELECT * FROM users;
        """
        
        statements = self.sql_compiler._split_sql_statements(sql)
        assert len(statements) == 3
        assert "CREATE TABLE" in statements[0]
        assert "INSERT INTO" in statements[1]
        assert "SELECT *" in statements[2]
    
    def test_input_parsing(self):
        stdin = '{"tables": {"users": {"schema": "CREATE TABLE users (id INT)"}}}'
        result = self.sql_compiler._parse_input(stdin)
        assert "tables" in result
        assert "users" in result["tables"]