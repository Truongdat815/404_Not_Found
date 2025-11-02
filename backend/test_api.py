"""
Script test API endpoint /api/analyze
Chạy script này sau khi server đã được khởi động
"""

import requests
import json

# URL của API
url = "http://127.0.0.1:8000/api/analyze"

# Test data - SRS mẫu với conflicts và ambiguities
test_text = """
REQUIREMENT 1: Users must login before accessing the system.
REQUIREMENT 2: Users should not be required to login to view public content.
REQUIREMENT 3: The system should process user requests quickly.
REQUIREMENT 4: Payment method can be credit card or PayPal.
REQUIREMENT 5: Users need to complete the registration form.
"""

# Request body
payload = {
    "text": test_text,
    "model": "gemini-1.5-pro"
}

print("=" * 60)
print("Testing Gemini API Integration")
print("=" * 60)
print(f"\nSending request to: {url}")
print(f"\nTest text:\n{test_text}\n")
print("-" * 60)

try:
    # Gửi request
    response = requests.post(url, json=payload, timeout=30)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("\n✅ SUCCESS! Response received:")
        print("-" * 60)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # Tóm tắt kết quả
        print("\n" + "=" * 60)
        print("SUMMARY:")
        print(f"  - Conflicts found: {len(result.get('conflicts', []))}")
        print(f"  - Ambiguities found: {len(result.get('ambiguities', []))}")
        print(f"  - Suggestions: {len(result.get('suggestions', []))}")
        print("=" * 60)
    else:
        print(f"\n❌ ERROR: {response.status_code}")
        print(response.text)
        
except requests.exceptions.ConnectionError:
    print("\n❌ ERROR: Cannot connect to server!")
    print("Make sure the server is running:")
    print("  uvicorn main:app --reload")
    
except requests.exceptions.Timeout:
    print("\n❌ ERROR: Request timeout!")
    print("Gemini API might be slow or API key invalid.")
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")

