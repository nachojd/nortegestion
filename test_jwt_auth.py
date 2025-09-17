#!/usr/bin/env python
"""
Test JWT authentication endpoints
"""
import requests
import json

# Configuration
BASE_URL = 'http://localhost:8000'  # Local development server
# For production testing: BASE_URL = 'http://5.161.102.34'

def test_api_info():
    """Test API info endpoint"""
    try:
        print("🔍 Testing API info endpoint...")
        response = requests.get(f"{BASE_URL}/api/")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Message: {data.get('message')}")
            print(f"   Version: {data.get('version')}")
            print("✅ API info endpoint working")
            return True
        else:
            print(f"❌ API info failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ API info error: {e}")
        return False

def test_jwt_login():
    """Test JWT login endpoint"""
    try:
        print("🔐 Testing JWT login...")

        # Test credentials
        credentials = {
            'username': 'motocenter@nortegestion.com',
            'password': 'motocenter123'
        }

        response = requests.post(
            f"{BASE_URL}/api/auth/login/",
            json=credentials,
            headers={'Content-Type': 'application/json'}
        )

        print(f"   Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            access_token = data.get('access')
            refresh_token = data.get('refresh')

            if access_token and refresh_token:
                print("✅ JWT login successful")
                print(f"   Access token length: {len(access_token)}")
                print(f"   Refresh token length: {len(refresh_token)}")
                return True, access_token, refresh_token
            else:
                print("❌ JWT login failed: Missing tokens")
                return False, None, None
        else:
            print(f"❌ JWT login failed: {response.text}")
            return False, None, None

    except Exception as e:
        print(f"❌ JWT login error: {e}")
        return False, None, None

def test_authenticated_api(access_token):
    """Test authenticated API endpoint"""
    try:
        print("🔒 Testing authenticated API access...")

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        # Test products endpoint
        response = requests.get(f"{BASE_URL}/api/products/", headers=headers)
        print(f"   Products endpoint status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"   Products count: {len(data) if isinstance(data, list) else 'N/A'}")
            print("✅ Authenticated API access working")
            return True
        else:
            print(f"❌ Authenticated API failed: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Authenticated API error: {e}")
        return False

def test_token_refresh(refresh_token):
    """Test token refresh endpoint"""
    try:
        print("🔄 Testing token refresh...")

        response = requests.post(
            f"{BASE_URL}/api/auth/refresh/",
            json={'refresh': refresh_token},
            headers={'Content-Type': 'application/json'}
        )

        print(f"   Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            new_access_token = data.get('access')

            if new_access_token:
                print("✅ Token refresh successful")
                print(f"   New access token length: {len(new_access_token)}")
                return True, new_access_token
            else:
                print("❌ Token refresh failed: Missing new token")
                return False, None
        else:
            print(f"❌ Token refresh failed: {response.text}")
            return False, None

    except Exception as e:
        print(f"❌ Token refresh error: {e}")
        return False, None

def main():
    """Run all tests"""
    print("🧪 JWT Authentication Test Suite")
    print("=" * 50)

    # Test API info
    if not test_api_info():
        print("\n❌ FAIL: API not accessible")
        return

    print()

    # Test JWT login
    success, access_token, refresh_token = test_jwt_login()
    if not success:
        print("\n❌ FAIL: JWT login not working")
        print("\n💡 Make sure to create motocenter user first:")
        print("   python create_motocenter_user.py")
        return

    print()

    # Test authenticated API
    if not test_authenticated_api(access_token):
        print("\n❌ FAIL: Authenticated API not working")
        return

    print()

    # Test token refresh
    success, new_token = test_token_refresh(refresh_token)
    if not success:
        print("\n❌ FAIL: Token refresh not working")
        return

    print()
    print("🎉 ALL TESTS PASSED!")
    print("✅ JWT authentication system is working correctly")
    print("\n🚀 Ready for production deployment!")

if __name__ == '__main__':
    main()