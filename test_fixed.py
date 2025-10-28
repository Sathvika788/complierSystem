import requests
import time

base_url = "https://compiler-api-6k95.onrender.com"  # No trailing slash!

def test_all_languages():
    print("🚀 Testing All 8 Languages with Fixed API!")
    print("=" * 60)
    
    test_cases = [
        {
            "id": 1,
            "name": "C",
            "code": '#include <stdio.h>\nint main() { printf("Hello C!\\n"); return 0; }'
        },
        {
            "id": 2, 
            "name": "C++",
            "code": '#include <iostream>\nint main() { std::cout << "Hello C++!" << std::endl; return 0; }'
        },
        {
            "id": 3,
            "name": "Python", 
            "code": 'print("Hello Python!")'
        },
        {
            "id": 4,
            "name": "Java",
            "code": '''public class Main {
    public static void main(String[] args) {
        System.out.println("Hello Java!");
    }
}'''
        },
        {
            "id": 5,
            "name": "JavaScript",
            "code": 'console.log("Hello JavaScript!");'
        },
        {
            "id": 6,
            "name": "Go", 
            "code": '''package main
import "fmt"
func main() {
    fmt.Println("Hello Go!")
}'''
        },
        {
            "id": 7,
            "name": "Rust",
            "code": 'fn main() { println!("Hello Rust!"); }'
        },
        {
            "id": 8,
            "name": "SQL",
            "code": 'SELECT "Hello SQL" as message;'
        }
    ]
    
    for test in test_cases:
        print(f"\n🧪 Testing {test['name']} (ID: {test['id']})...")
        
        try:
            # Test the Judge0-compatible endpoint
            response = requests.post(
                f"{base_url}/api/v1/submissions",
                json={
                    "source_code": test["code"],
                    "language_id": test["id"],
                    "stdin": ""
                },
                timeout=30
            )
            
            print(f"   📊 Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ SUCCESS!")
                if "message" in result:
                    print(f"   📝 {result['message']}")
                if "data" in result:
                    print(f"   🔧 Data received")
                    
            elif response.status_code == 422:
                error_data = response.json()
                print(f"   ❌ VALIDATION ERROR")
                print(f"   📋 Details: {error_data}")
                
            else:
                print(f"   ❌ FAILED: {response.status_code}")
                print(f"   📄 Response: {response.text[:100]}...")
                
        except requests.exceptions.Timeout:
            print(f"   ⏰ TIMEOUT: Request took too long")
        except requests.exceptions.ConnectionError:
            print(f"   🔌 CONNECTION ERROR: Cannot reach the API")
        except Exception as e:
            print(f"   💥 UNEXPECTED ERROR: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 All Tests Completed!")

def test_simple_endpoints():
    print("\n" + "=" * 60)
    print("🧪 Testing Simple Endpoints...")
    
    # Test root endpoint
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        print(f"✅ Root endpoint: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Root endpoint failed: {e}")
    
    # Test compile endpoint
    try:
        response = requests.post(
            f"{base_url}/api/compile",
            json={"language": "python", "code": "print('Simple test')"},
            timeout=10
        )
        print(f"✅ Compile endpoint: {response.status_code} - {response.json().get('message', 'No message')}")
    except Exception as e:
        print(f"❌ Compile endpoint failed: {e}")

if __name__ == "__main__":
    test_simple_endpoints()
    test_all_languages()