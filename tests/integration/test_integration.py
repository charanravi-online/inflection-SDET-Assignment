import requests
import pytest
import time
import uuid

# Base URLs for the services
CAMPAIGN_URL = "http://localhost:7070"
TEMPLATE_URL = "http://localhost:7071"
RECIPIENT_URL = "http://localhost:7072"

# Health check
def test_service_health():
    assert requests.get(f"{CAMPAIGN_URL}/health").status_code == 200
    assert requests.get(f"{TEMPLATE_URL}/health").status_code == 200
    assert requests.get(f"{RECIPIENT_URL}/health").status_code == 200

def test_fetch_templates():
    response = requests.get(f"{TEMPLATE_URL}/email/templates")
    assert response.status_code == 200
    assert "data" in response.json()

def test_fetch_recipients():
    response = requests.get(f"{RECIPIENT_URL}/recipients/lists")
    assert response.status_code == 200
    assert "data" in response.json()