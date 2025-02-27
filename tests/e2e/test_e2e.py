import requests
import pytest
import time
import uuid

# Base URLs for the services
CAMPAIGN_URL = "http://localhost:7070"
TEMPLATE_URL = "http://localhost:7071"
RECIPIENT_URL = "http://localhost:7072"

@pytest.fixture(scope="module")
def campaign_details():
    # Verify services are healthy
    assert requests.get(f"{CAMPAIGN_URL}/health").status_code == 200
    assert requests.get(f"{TEMPLATE_URL}/health").status_code == 200
    assert requests.get(f"{RECIPIENT_URL}/health").status_code == 200

    # Get a template ID
    template_response = requests.get(f"{TEMPLATE_URL}/email/templates")
    assert template_response.status_code == 200
    template_id = template_response.json()["data"][0]["id"]

    # Get a recipient list ID
    recipient_response = requests.get(f"{RECIPIENT_URL}/recipients/lists")
    assert recipient_response.status_code == 200
    recipient_id = recipient_response.json()["data"][0]["id"]

    # Create a campaign with a unique name to avoid 409 Conflict
    scheduled_time = int(time.time()) + 3600  # 1 hour from now in seconds (UTC)
    unique_name = f"Test Campaign {uuid.uuid4()}"
    payload = {
        "campaignName": unique_name,
        "emailTemplateId": template_id,
        "recipientListId": recipient_id,
        "scheduledTime": scheduled_time
    }
    response = requests.post(f"{CAMPAIGN_URL}/campaigns", json=payload)
    assert response.status_code == 201  # Expect 201 Created, not 200 OK
    campaign_data = response.json()["data"]
    yield campaign_data["id"], template_id, recipient_id, scheduled_time

def test_create_campaign(campaign_details):
    campaign_id, _, _, _ = campaign_details
    response = requests.get(f"{CAMPAIGN_URL}/campaigns/{campaign_id}")
    assert response.status_code == 200
    assert "Test Campaign" in response.json()["data"]["campaignName"]  # Partial match due to UUID
    assert response.json()["data"]["emailTemplateId"] is not None
    assert response.json()["data"]["recipientListId"] is not None
    assert response.json()["data"]["scheduledTime"] > int(time.time())
