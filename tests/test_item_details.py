import pytest
from core.api_client import APIClient
from utilities.helpers import json_structure_verification

REQUIRED_FIELDS = ["id", "type", "time", "by"]


@pytest.fixture(scope="module")
def api_client():
    """Fixture for APIClient with setup and teardown."""
    # Setup: Create client
    client = APIClient()
    yield client
    # Teardown: Clean up


@pytest.mark.regression
def test_top_story_details(api_client):
    # Step 1: Get Top Stories
    top_res = api_client.get("/topstories.json")
    assert top_res.status_code == 200
    top_ids = top_res.json()

    assert len(top_ids) > 0
    story_id = top_ids[0]

    # Step 2: Get Story Item
    story_res = api_client.get(f"/item/{story_id}.json")
    assert story_res.status_code == 200
    story = story_res.json()
    assert story is not None, f"API returned no JSON for story id {story_id}: status {story_res.status_code}, text={story_res.text}"

    # Story should not be deleted/dead
    assert not story.get("deleted", False), "Top story is marked deleted"
    assert not story.get("dead", False), "Top story is marked dead"

    # Story should have required fields
    assert story.get("id") == story_id
    assert story.get("type") in ["story", "job", "poll"], "Unexpected item type in top stories"
    assert "title" in story, "Story missing title field"

    # title/url/text may vary, ensure structure is valid
    assert any(k in story for k in ["url", "text"]), "Story missing both url and text"
    # Verify JSON structure using utility
    missing = json_structure_verification(story, REQUIRED_FIELDS)
    assert not missing, f"Story is missing required fields: {missing}"

@pytest.mark.regression
def test_first_comment_of_top_story(api_client):
    # Step 1: Get Top Stories
    top_res = api_client.get("/topstories.json")
    assert top_res.status_code == 200
    story_id = top_res.json()[0]

    # Step 2: Get Story
    story_res = api_client.get(f"/item/{story_id}.json")
    assert story_res.status_code == 200
    story = story_res.json()
    assert story is not None, f"API returned no JSON for story id {story_id}: status {story_res.status_code}, text={story_res.text}"

    # Story has no comments
    if "kids" not in story or len(story["kids"]) == 0:
        pytest.skip("Top story has no comments — skipping comment validation")

    comment_id = story["kids"][0]

    # Step 3: Retrieve Comment
    comment_res = api_client.get(f"/item/{comment_id}.json")
    assert comment_res.status_code == 200
    comment = comment_res.json()
    assert comment is not None, f"API returned no JSON for comment id {comment_id}: status {comment_res.status_code}, text={comment_res.text}"

    # Comment exists but marked deleted/dead
    assert not comment.get("deleted", False), "First comment is deleted"
    assert not comment.get("dead", False), "First comment is marked dead"

    # Comment must be type 'comment'
    assert comment.get("type") == "comment", f"Unexpected item type in kids: {comment.get('type')}"

    # Comment may have no text — but should still include metadata
    assert "id" in comment
    assert "by" in comment, "Comment missing author field"
    assert isinstance(comment.get("time"), int), "Comment missing valid timestamp"
    # Verify JSON structure for comment
    missing_comment = json_structure_verification(comment, REQUIRED_FIELDS)
    assert not missing_comment, f"Comment is missing required fields: {missing_comment}"
