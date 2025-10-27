import pytest
import asyncio
from src.core.compiler import compiler_manager

class TestCompiler:
    @pytest.mark.asyncio
    async def test_python_execution(self):
        result = await compiler_manager.execute_code(
            source_code="print('Hello, World!')",
            language_id=3,
            stdin=""
        )
        assert result["exit_code"] == 0
        assert "Hello, World!" in result["stdout"]
    
    @pytest.mark.asyncio
    async def test_sql_execution(self):
        sql_code = """
        CREATE TABLE test (id INT, name TEXT);
        INSERT INTO test VALUES (1, 'Alice'), (2, 'Bob');
        SELECT * FROM test;
        """
        
        result = await compiler_manager.execute_code(
            source_code=sql_code,
            language_id=8,
            stdin=""
        )
        
        assert result["exit_code"] == 0
        assert "Alice" in result["stdout"]
        assert "Bob" in result["stdout"]
    
    @pytest.mark.asyncio
    async def test_unsupported_language(self):
        with pytest.raises(ValueError):
            await compiler_manager.execute_code(
                source_code="test",
                language_id=999,
                stdin=""
            )