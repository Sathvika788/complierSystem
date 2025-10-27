# test_available_compilers.py
import subprocess
import requests
import time

base_url = "http://localhost:8001"

def test_available_compilers():
    print("🚀 Testing Currently Available Compilers...")
    
    # Test system compilers
    print("🔧 System Compiler Check:")
    compilers = [
        ("Java", "javac -version"),
        ("Go", "go version"),
        (".NET", "dotnet --version"), 
        ("Ruby", "ruby --version"),
        ("Node.js", "node --version"),
        ("Python", "python --version")
    ]
    
    available = []
    for name, cmd in compilers:
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print(f"   ✅ {name}: Available")
                available.append(name.lower())
            else:
                print(f"   ❌ {name}: Not working")
        except:
            print(f"   ❌ {name}: Not found")
    
    print(f"\n📊 Available: {', '.join(available)}")
    
    # Test API with available languages
    print(f"\n🌐 Testing API with Available Languages:")
    
    test_cases = []
    if "java" in available:
        test_cases.append({
            "id": 4, "name": "Java", 
            "code": '''public class Main {
    public static void main(String[] args) {
        System.out.println("Java is working!");
        for (int i = 1; i <= 3; i++) {
            System.out.println("Count: " + i);
        }
    }
}'''
        })
    
    # We know Python and JavaScript work from earlier tests
    test_cases.extend([
        {
            "id": 3, "name": "Python",
            "code": 'print("Python is working!")\nfor i in range(1, 4):\n    print(f"Count: {i}")'
        },
        {
            "id": 5, "name": "JavaScript", 
            "code": 'console.log("JavaScript is working!");\nfor (let i = 1; i <= 3; i++) {\n    console.log(`Count: ${i}`);\n}'
        }
    ])
    
    for test in test_cases:
        print(f"\n🧪 Testing {test['name']} (ID: {test['id']})...")
        try:
            response = requests.post(f"{base_url}/api/v1/submissions", json={
                "source_code": test["code"],
                "language_id": test["id"],
                "stdin": ""
            }, timeout=10)
            
            if response.status_code == 200:
                submission_id = response.json()["submission_id"]
                print(f"   ✅ Submitted! ID: {submission_id}")
                
                # Wait and get result
                time.sleep(3)
                result = requests.get(f"{base_url}/api/v1/submissions/{submission_id}").json()
                
                print(f"   Status: {result.get('status')}")
                if result.get('stdout'):
                    print(f"   📤 Output: {result.get('stdout').strip()}")
                if result.get('stderr'):
                    print(f"   ❌ Error: {result.get('stderr')}")
            else:
                print(f"   ❌ Submission failed: {response.status_code}")
                
        except Exception as e:
            print(f"   💥 Error: {e}")

if __name__ == "__main__":
    test_available_compilers()