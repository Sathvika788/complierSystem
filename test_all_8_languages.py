# test_all_8_languages.py
import requests
import time

base_url = "https://compiler-api-6k95.onrender.com/"

def test_all_languages():
    print("🚀 Testing All 8 Languages (Including SQL!)")
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
            "code": 'print("Hello Python!")\nfor i in range(3):\n    print(f"Count: {i}")'
        },
        {
            "id": 4,
            "name": "Java",
            "code": '''public class Main {
    public static void main(String[] args) {
        System.out.println("Hello Java!");
        for (int i = 1; i <= 3; i++) {
            System.out.println("Number: " + i);
        }
    }
}'''
        },
        {
            "id": 5,
            "name": "JavaScript",
            "code": 'console.log("Hello JavaScript!");\nfor (let i = 1; i <= 3; i++) {\n    console.log(`Iteration: ${i}`);\n}'
        },
        {
            "id": 6,
            "name": "Go", 
            "code": '''package main
import "fmt"
func main() {
    fmt.Println("Hello Go!")
    for i := 1; i <= 3; i++ {
        fmt.Printf("Loop: %d\\n", i)
    }
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
            "code": '''SELECT name, email FROM users;
SELECT p.name, p.price, o.quantity 
FROM products p 
JOIN orders o ON p.id = o.product_id;'''
        }
    ]
    
    for test in test_cases:
        print(f"\n🧪 Testing {test['name']} (ID: {test['id']})...")
        
        try:
            response = requests.post(
                f"{base_url}/api/v1/submissions",
                json={
                    "source_code": test["code"],
                    "language_id": test["id"],
                    "stdin": ""
                },
                timeout=10
            )
            
            if response.status_code == 200:
                submission_id = response.json()["submission_id"]
                print(f"   ✅ Submitted! ID: {submission_id}")
                
                time.sleep(3)
                result = requests.get(f"{base_url}/api/v1/submissions/{submission_id}").json()
                
                print(f"   Status: {result.get('status')}")
                if result.get('stdout'):
                    output = result.get('stdout')
                    # Show first few lines of output
                    lines = output.split('\n')
                    if len(lines) > 5:
                        print(f"   📤 Output: {lines[0]}")
                        print(f"           ... ({len(lines)-1} more lines)")
                    else:
                        print(f"   📤 Output: {output.strip()}")
                if result.get('stderr'):
                    error = result.get('stderr')
                    if "coming soon" not in error and "not found" not in error:
                        print(f"   ❌ Error: {error[:100]}...")
            else:
                print(f"   ❌ Submission failed: {response.status_code}")
                
        except Exception as e:
            print(f"   💥 Error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 All 8 Languages Tested! (SQL replaces Ruby)")

if __name__ == "__main__":
    test_all_languages()