# get_submission_results.py
import requests
import json
import time

base_url = "http://localhost:8001"

def get_submission_results():
    print("📋 Retrieving Submission Results...")
    
    # Submission IDs from your previous test
    submission_ids = [
        "314ffceb-86b8-49da-a7cc-5d01fef18c1e",  # Python
        "bbac5b69-6280-4944-8c60-e10b905b246d",  # JavaScript
        "16d7f572-1484-4d11-8600-c1e0ce9f8b94",  # Java
        "7078778b-d9ce-408f-b84b-103459dbae35"   # C++
    ]
    
    languages = ["Python", "JavaScript", "Java", "C++"]
    
    # Wait a bit for processing
    print("⏳ Waiting for submissions to process...")
    time.sleep(5)
    
    for i, submission_id in enumerate(submission_ids):
        print(f"\n🔍 Checking {languages[i]} submission: {submission_id}")
        try:
            response = requests.get(f"{base_url}/api/v1/submissions/{submission_id}")
            print(f"   Status: {response.status_code}")
            result = response.json()
            print(f"   Result: {json.dumps(result, indent=2)}")
            
            # Check if we need to wait longer
            if result.get('status') in ['In Queue', 'Processing']:
                print("   ⏳ Still processing...")
                
        except Exception as e:
            print(f"   Error: {e}")

if __name__ == "__main__":
    get_submission_results()