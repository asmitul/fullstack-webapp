#!/usr/bin/env python3
"""
Health check script for the backend service.
This script checks if the backend API is running properly.
"""
import sys
import requests

def check_health():
    """Check if the backend API is running properly."""
    try:
        response = requests.get("http://localhost:8000/")
        if response.status_code == 200:
            print("Backend is healthy")
            return True
        else:
            print(f"Backend returned status code {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to backend: {e}")
        return False

if __name__ == "__main__":
    if check_health():
        sys.exit(0)
    else:
        sys.exit(1) 