from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_unregister_participant_from_activity():
    activity_name = "Chess Club"
    new_email = "newstudent@mergington.edu"

    # Ensure the student is not already signed up.
    current = client.get("/activities").json()
    if new_email in current[activity_name]["participants"]:
        client.delete(f"/activities/{activity_name}/participants/{new_email}")

    signup_response = client.post(f"/activities/{activity_name}/signup?email={new_email}")
    assert signup_response.status_code == 200

    unregister_response = client.delete(f"/activities/{activity_name}/participants/{new_email}")
    assert unregister_response.status_code == 200
    assert unregister_response.json()["message"] == f"Removed {new_email} from {activity_name}"

    remaining = client.get("/activities").json()
    assert new_email not in remaining[activity_name]["participants"]
