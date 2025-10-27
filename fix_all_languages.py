# fix_all_languages.py
import os
import inspect

def check_language_implementation(file_path, class_name):
    """Check if a language class implements all required methods"""
    try:
        # Dynamically import the module
        import importlib.util
        spec = importlib.util.spec_from_file_location("language_module", file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Get the class
        language_class = getattr(module, class_name)
        
        # Check required methods
        required_methods = ['name', 'extension', 'compile_code', 'execute']
        missing_methods = []
        
        for method in required_methods:
            if not hasattr(language_class, method):
                missing_methods.append(method)
            elif method in ['name', 'extension']:
                # Check if they are properties
                attr = getattr(language_class, method)
                if not isinstance(attr, property):
                    missing_methods.append(f"{method} (should be property)")
        
        if missing_methods:
            print(f"❌ {class_name}: Missing {missing_methods}")
            return False
        else:
            print(f"✅ {class_name}: All methods implemented")
            return True
            
    except Exception as e:
        print(f"❌ {class_name}: Error checking - {e}")
        return False

def fix_language_files():
    languages_dir = "src/languages"
    language_files = {
        "python.py": "PythonLanguage",
        "java.py": "JavaLanguage", 
        "javascript.py": "JavaScriptLanguage",
        "go.py": "GoLanguage",
        "rust.py": "RustLanguage",
        "csharp.py": "CSharpLanguage",
        "ruby.py": "RubyLanguage",
        "c_cpp.py": ["CLanguage", "CppLanguage"]
    }
    
    print("🔍 Checking Language Implementations...")
    
    for file, classes in language_files.items():
        file_path = os.path.join(languages_dir, file)
        if os.path.exists(file_path):
            print(f"\n📄 {file}:")
            if isinstance(classes, list):
                for cls in classes:
                    check_language_implementation(file_path, cls)
            else:
                check_language_implementation(file_path, classes)
        else:
            print(f"\n📄 {file}: ❌ File not found")

if __name__ == "__main__":
    fix_language_files()