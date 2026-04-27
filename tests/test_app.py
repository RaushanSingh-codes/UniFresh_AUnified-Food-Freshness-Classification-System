def test_home(client):
    res = client.get("/")
    assert res.status_code in [200,302]