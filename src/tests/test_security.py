import pytest
from src.core.security import SecurityManager

class TestSecurity:
    def test_resource_limits(self):
        security_manager = SecurityManager()
        
        # This should not raise an exception
        security_manager.set_resource_limits(5.0, 256000)
    
    def test_environment_setup(self, tmp_path):
        security_manager = SecurityManager()
        security_manager.setup_environment(str(tmp_path))
        
        import os
        assert os.getenv('HOME') == str(tmp_path)