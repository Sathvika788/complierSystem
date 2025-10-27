# language_mapping.py
LANGUAGE_MAPPING = {
    1: "Go",        # ID 1 is actually Go
    2: "C++",       # ID 2 is C++ (placeholder)
    3: "Python",    # ID 3 is Python
    4: "Java",      # ID 4 is Java  
    5: "JavaScript", # ID 5 is JavaScript
    6: "Rust",      # ID 6 is Rust (not installed)
    7: "C#",        # ID 7 is C# (not installed)
    8: "Ruby"       # ID 8 is Ruby (placeholder)
}

def get_working_languages():
    return {
        "python": 3,
        "javascript": 5, 
        "java": 4,
        "go": 1
    }