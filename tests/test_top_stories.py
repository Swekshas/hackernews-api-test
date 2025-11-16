import pytest
from core.api_client import APIClient

client = APIClient()

@pytest.mark.regression
def test_fetch_top_stories_ids():
    response = client.get("/topstories.json")
    assert response.status_code == 200
    stories = response.json()
    # Ensure list is not empty
    assert isinstance(stories, list)
    assert len(stories) > 0, "Top stories returned an empty list, unexpected behavior"

    # Validate all IDs are positive integers
    assert all(isinstance(i, int) and i > 0 for i in stories), "Top stories contain invalid IDs"

    # Ensure IDs are unique
    assert len(stories) == len(set(stories)), "Top stories contain duplicate IDs"

    # API should not return null values
    assert all(i is not None for i in stories)

    # Detect rate limiting or unexpected errors
    assert response.headers.get("Content-Type", "").startswith("application/json")

@pytest.mark.regression
@pytest.mark.parametrize("endpoint", [
    "/newstories.json",
    "/beststories.json",
])
def test_fetch_story_collections(endpoint):
    response = client.get(endpoint)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert all(isinstance(item, int) for item in data)