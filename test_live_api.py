import requests
import time

base_url = "https://compiler-api-6k95.onrender.com"  # Remove the trailing slash

def test_all_languages():
    print("🚀 Testing All 8 Languages with Live API!")
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
            # Use the correct endpoint format
            response = requests.post(
                f"{base_url}/api/v1/submissions",
                json={
                    "source_code": test["code"],
                    "language_id": test["id"],
                    "stdin": ""
                },
                timeout=30
            )
            
            print(f"   Status Code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Success!")
                print(f"   Response: {result}")
                
            elif response.status_code == 422:
                print(f"   ❌ Validation Error - Check request format")
                print(f"   Error details: {response.json()}")
                
            else:
                print(f"   ❌ Failed with status: {response.status_code}")
                print(f"   Response: {response.text}")
                
        except Exception as e:
            print(f"   💥 Error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Testing Complete!")

def test_simple_compile():
    print("\n🧪 Testing Simple Compile Endpoint...")
    try:
        response = requests.post(
            f"{base_url}/api/compile",
            json={
                "language": "python",
                "code": "print('Hello from simple endpoint!')"
            },
            timeout=10
        )
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")

if __name__ == "__main__":
    test_simple_compile()
    test_all_languages()