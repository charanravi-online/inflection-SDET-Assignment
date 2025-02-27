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


def test_create_campaign_with_deps():
    # Fetch a template ID
    template_response = requests.get(f"{TEMPLATE_URL}/email/templates")
    assert template_response.status_code == 200
    template_id = template_response.json()["data"][0]["id"]

    # Fetch a recipient list ID
    recipient_response = requests.get(f"{RECIPIENT_URL}/recipients/lists")
    assert recipient_response.status_code == 200
    recipient_id = recipient_response.json()["data"][0]["id"]

    # Create a campaign with a unique name
    scheduled_time = int(time.time()) + 3600  # 1 hour from now
    unique_name = f"Integration Test {uuid.uuid4()}"
    payload = {
        "campaignName": unique_name,
        "emailTemplateId": template_id,
        "recipientListId": recipient_id,
        "scheduledTime": scheduled_time
    }
    response = requests.post(f"{CAMPAIGN_URL}/campaigns", json=payload)
    assert response.status_code == 201  # Expect 201 Created
    campaign = response.json()["data"]
    assert campaign["emailTemplateId"] == template_id
    assert campaign["recipientListId"] == recipient_id

