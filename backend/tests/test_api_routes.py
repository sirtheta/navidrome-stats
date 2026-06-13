from app.db import crud


def test_get_users(client, db_session):
    response = client.get("/api/users")
    expected = [u.model_dump() for u in crud.get_all_users(db_session)]

    assert response.status_code == 200
    assert response.json() == expected
    assert len(expected) == 3
    assert expected[0]["total_plays"] >= expected[1]["total_plays"]


def test_get_top_songs_default_limit(client, db_session):
    response = client.get("/api/top-songs")
    expected = [s.model_dump() for s in crud.get_global_top_songs(db_session, limit=10)]

    assert response.status_code == 200
    assert response.json() == expected
    assert len(response.json()) == 10


def test_get_top_songs_custom_limit(client, db_session):
    response = client.get("/api/top-songs?limit=3")
    expected = [s.model_dump() for s in crud.get_global_top_songs(db_session, limit=3)]

    assert response.status_code == 200
    assert response.json() == expected
    assert response.json()[0] == {
        "title": "Da Funk",
        "artist": "Daft Punk",
        "play_count": 73,
    }


def test_get_top_artists(client, db_session):
    response = client.get("/api/top-artists?limit=5")
    expected = [a.model_dump() for a in crud.get_global_top_artists(db_session, limit=5)]

    assert response.status_code == 200
    assert response.json() == expected
    assert response.json()[0]["name"] == "Radiohead"
    assert response.json()[0]["play_count"] == 230


def test_get_compare_songs(client, db_session):
    response = client.get("/api/compare/songs")
    expected = crud.get_cross_user_matrix(db_session)

    assert response.status_code == 200
    assert response.json() == expected
    assert response.json()["users"] == ["alice", "bob", "charlie"]
    assert len(response.json()["songs"]) == 20
    assert len(response.json()["matrix"]) == 3
    assert len(response.json()["matrix"][0]) == 20


def test_get_user_top_songs(client, db_session):
    response = client.get("/api/user/alice/top-songs")
    expected = [s.model_dump() for s in crud.get_top_songs(db_session, user_id="u1")]

    assert response.status_code == 200
    assert response.json() == expected
    assert response.json()[0]["title"] == "Unfinished Sympathy"
    assert response.json()[0]["play_count"] == 28


def test_get_user_top_albums(client, db_session):
    response = client.get("/api/user/alice/top-albums")
    expected = [a.model_dump() for a in crud.get_top_albums(db_session, user_id="u1")]

    assert response.status_code == 200
    assert response.json() == expected
    assert response.json()[0]["name"] == "Mezzanine"
    assert response.json()[0]["play_count"] == 47


def test_get_user_top_artists(client, db_session):
    response = client.get("/api/user/alice/top-artists")
    expected = [a.model_dump() for a in crud.get_top_artists(db_session, user_id="u1")]

    assert response.status_code == 200
    assert response.json() == expected
    assert response.json()[0]["name"] == "Radiohead"
    assert response.json()[0]["play_count"] == 56


def test_get_user_endpoints_work_for_all_sample_users(client):
    for user_name in ("alice", "bob", "charlie"):
        assert client.get(f"/api/user/{user_name}/top-songs").status_code == 200
        assert client.get(f"/api/user/{user_name}/top-albums").status_code == 200
        assert client.get(f"/api/user/{user_name}/top-artists").status_code == 200


def test_get_user_top_songs_not_found(client):
    response = client.get("/api/user/unknown-user/top-songs")

    assert response.status_code == 404
    assert response.json() == {"message": "user not found"}


def test_get_user_top_albums_not_found(client):
    response = client.get("/api/user/unknown-user/top-albums")

    assert response.status_code == 404
    assert response.json() == {"message": "user not found"}


def test_get_user_top_artists_not_found(client):
    response = client.get("/api/user/unknown-user/top-artists")

    assert response.status_code == 404
    assert response.json() == {"message": "user not found"}
