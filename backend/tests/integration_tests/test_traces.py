import pytest
import requests
from urllib.parse import urljoin


@pytest.fixture
def base_url():
    return "http://127.0.0.1:8000"


def test_create_trace(base_url):
    """Test creating a trace record."""
    # Prepare the request data
    data = {
        "prompt": "How do I reset my password?",
        "generation": "To reset your password, click on 'Forgot Password' and follow the instructions sent to your email.",
        "trace_metadata": {
            "use_case": "customer support",
            "resource_id": "resA101",
            "workflow_step": "initial query",
            "model_version": "1.0",
            "prompt_version": "1.0",
        },
        "user": {"username": "user001"},
        "ai_model_config": {"name": "LLM-v1", "temperature": 0.7},
    }

    # Send the POST request to create a trace
    response = requests.post(
        urljoin(base_url, "/traces"),
        json=data,
        headers={"Content-Type": "application/json", "accept": "application/json"},
    )

    # Assert the response status code is 201 (Created)
    assert response.status_code == 201, (
        f"Expected status code 201, got {response.status_code}"
    )

    # Parse the response JSON
    response_data = response.json()

    # Assert the values match what we sent
    assert response_data["prompt"] == data["prompt"]
    assert response_data["generation"] == data["generation"]
    assert response_data["trace_metadata"] == data["trace_metadata"]
    assert response_data["user"]["username"] == data["user"]["username"]
    assert response_data["ai_model_config"]["name"] == data["ai_model_config"]["name"]
    assert response_data["created_at"] is not None
