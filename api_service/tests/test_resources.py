from api_service.models import Url as UrlModel


def test_shorten_url(client, db):
    # Test shortening a new URL
    response = client.post("/api/v1/url", json={"url": "https://www.example.com"})
    assert response.status_code == 200
    assert "short_url" in response.json

    # Test shortening an existing URL
    response = client.post("/api/v1/url", json={"url": "https://www.example.com"})
    assert response.status_code == 200
    assert "short_url" in response.json


def test_delete_url(client, db):
    # Create a URL to be deleted
    url = UrlModel(
        short_url="http://localhost:5000/abc123",
        long_url="https://www.example.com",
        short_code="abc123",
        count=0,
    )
    db.session.add(url)
    db.session.commit()

    # Test deleting the URL
    response = client.delete(f"/api/v1/url?id={url.id}")
    assert response.status_code == 200
    assert response.json == {"message": "Deleted"}

    # Test attempting to delete a non-existent URL
    response = client.delete("/api/v1/url?id=99999")
    assert response.status_code == 404
    assert "not_found" in response.json


def test_redirect_url(client, db):
    # Create a URL to be redirected
    url = UrlModel(
        short_url="http://localhost:5000/abc123",
        long_url="https://www.example.com",
        short_code="abc123",
        count=0,
    )
    db.session.add(url)
    db.session.commit()

    # Test redirecting to the URL
    response = client.get(f"/api/v1/redirect/{url.short_code}", follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["Location"] == url.long_url

    # Test attempting to redirect to a non-existent URL
    response = client.get("/api/v1/redirect/nonexistent", follow_redirects=False)
    assert response.status_code == 404
    assert "error" in response.json


def test_url_stats(client, db):
    # Create some URLs with different counts
    url1 = UrlModel(
        short_url="http://localhost:5000/abc123",
        long_url="https://www.example.com",
        short_code="abc123",
        count=10,
    )
    url2 = UrlModel(
        short_url="http://localhost:5000/def456",
        long_url="https://www.example.org",
        short_code="def456",
        count=5,
    )
    db.session.add(url1)
    db.session.add(url2)
    db.session.commit()

    # Test getting the top URLs
    response = client.get("/api/v1/stats")
    assert response.status_code == 200
    assert len(response.json["data"]) == 2
    assert response.json["data"][0]["long_url"] == url1.long_url
    assert response.json["data"][0]["count"] == url1.count
    assert response.json["data"][1]["long_url"] == url2.long_url
    assert response.json["data"][1]["count"] == url2.count

    # Test getting the top URLs when there are none
    db.session.delete(url1)
    db.session.delete(url2)
    db.session.commit()
    response = client.get("/api/v1/stats")
    assert response.status_code == 200
    assert response.json == []
