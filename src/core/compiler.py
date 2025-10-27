# src/core/compiler.py (Fixed execute_code method)
import logging
from typing import Dict, Optional, List
from src.languages.c_cpp import CppLanguage, CLanguage
from src.languages.python import PythonLanguage
from src.languages.java import JavaLanguage
from src.languages.javascript import JavaScriptLanguage
from src.languages.go import GoLanguage
from src.languages.rust import RustLanguage
from src.languages.csharp import CSharpLanguage
from src.languages.sql import SQLLanguage

logger = logging.getLogger(__name__)

class CompilerManager:
    def __init__(self):
        self.languages: Dict[int, any] = {}
        self._register_languages()
        logger.info(f"CompilerManager initialized with {len(self.languages)} languages")

    def _register_languages(self):
        """Register all available programming languages"""
        # Clear existing languages
        self.languages.clear()
        
        # Register all 8 languages
        self.languages[1] = CLanguage()           # C
        self.languages[2] = CppLanguage()         # C++
        self.languages[3] = PythonLanguage()      # Python
        self.languages[4] = JavaLanguage()        # Java
        self.languages[5] = JavaScriptLanguage()  # JavaScript
        self.languages[6] = GoLanguage()          # Go
        self.languages[7] = RustLanguage()        # Rust
        self.languages[8] = SQLLanguage()         # SQL (replaces Ruby)

    def get_language(self, language_id: int) -> Optional[any]:
        """Get language by ID"""
        return self.languages.get(language_id)

    def execute_code(self, language_id: int, source_code: str = None, code: str = None, 
                    input_data: str = "", stdin: str = "", timeout: int = 30, 
                    memory_limit: int = 256000, **kwargs) -> Dict:
        """Execute code in the specified language - handles both 'code' and 'source_code' parameters"""
        language = self.get_language(language_id)
        
        if not language:
            return {
                'success': False,
                'output': '',
                'error': f'Unsupported language: {language_id}',
                'exit_code': -1
            }
        
        try:
            # Handle both parameter names: 'code' and 'source_code'
            actual_code = code if code is not None else source_code
            if actual_code is None:
                return {
                    'success': False,
                    'output': '',
                    'error': 'No code provided. Use either "code" or "source_code" parameter.',
                    'exit_code': -1
                }
            
            # Handle both input parameter names
            actual_input = input_data if input_data else stdin
            
            # Execute the code using the language's execute method
            result = language.execute(
                code=actual_code,
                input_data=actual_input,
                timeout=timeout,
                memory_limit=memory_limit
            )
            return result
            
        except Exception as e:
            logger.error(f"Execution failed for language {language_id}: {e}")
            return {
                'success': False,
                'output': '',
                'error': f'Execution failed: {str(e)}',
                'exit_code': -1
            }

    def get_available_languages(self) -> List[Dict]:
        """Get list of all available languages"""
        languages_list = []
        for lang_id, lang_instance in self.languages.items():
            if hasattr(lang_instance, 'name'):
                languages_list.append({
                    'id': lang_id,
                    'name': lang_instance.name
                })
            else:
                languages_list.append({
                    'id': lang_id,
                    'name': f'Language {lang_id}'
                })
        return languages_list

    def validate_language(self, language_id: int) -> bool:
        """Check if language ID is valid"""
        return language_id in self.languages

# Global compiler manager instance
compiler_manager = CompilerManager()