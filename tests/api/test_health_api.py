import pytest
import requests
from tests.support.api_constants import API_HEALTH_CHECK, API_MESSAGES

@pytest.mark.api
@pytest.mark.api_health
@pytest.mark.basic
@pytest.mark.full
def test_health_check():
    response = requests.get(API_HEALTH_CHECK)
    body = response.json()
    assert response.status_code == 200
    assert body["message"] == API_MESSAGES["NOTES_API_RUNNING"]
    assert body["success"] is True
