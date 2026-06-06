def get_all_users(db):
    rows = db.execute("""
        SELECT u.id, u.user_name,
               COALESCE(SUM(a.play_count), 0) AS total_plays
        FROM user u
        LEFT JOIN annotation a ON a.user_id = u.id
            AND a.item_type = 'media_file'
            AND a.play_count > 0
        GROUP BY u.id
        ORDER BY total_plays DESC
    """).fetchall()
    return [dict(r) for r in rows]


def get_user_by_name(db, user_name):
    row = db.execute(
        "SELECT id, user_name FROM user WHERE user_name = ?", (user_name,)
    ).fetchone()
    return dict(row) if row else None


def get_top_songs(db, user_id, limit=10):
    rows = db.execute("""
        SELECT mf.title, mf.artist, COALESCE(a.play_count, 0) AS play_count
        FROM annotation a
        JOIN media_file mf ON mf.id = a.item_id
        WHERE a.item_type = 'media_file'
          AND a.user_id = ?
          AND a.play_count > 0
        ORDER BY a.play_count DESC
        LIMIT ?
    """, (user_id, limit)).fetchall()
    return [dict(r) for r in rows]


def get_top_albums(db, user_id, limit=10):
    rows = db.execute("""
        SELECT mf.album AS name, mf.artist,
               SUM(COALESCE(a.play_count, 0)) AS play_count
        FROM annotation a
        JOIN media_file mf ON mf.id = a.item_id
        WHERE a.item_type = 'media_file'
          AND a.user_id = ?
          AND a.play_count > 0
        GROUP BY mf.album_id
        ORDER BY play_count DESC
        LIMIT ?
    """, (user_id, limit)).fetchall()
    return [dict(r) for r in rows]


def get_top_artists(db, user_id, limit=10):
    rows = db.execute("""
        SELECT ar.name, SUM(COALESCE(a.play_count, 0)) AS play_count
        FROM annotation a
        JOIN media_file mf ON mf.id = a.item_id
        JOIN artist ar ON ar.id = mf.artist_id
        WHERE a.item_type = 'media_file'
          AND a.user_id = ?
          AND a.play_count > 0
        GROUP BY ar.id
        ORDER BY play_count DESC
        LIMIT ?
    """, (user_id, limit)).fetchall()
    return [dict(r) for r in rows]


def get_global_top_songs(db, limit=10):
    rows = db.execute("""
        SELECT mf.title, mf.artist,
               SUM(COALESCE(a.play_count, 0)) AS play_count
        FROM annotation a
        JOIN media_file mf ON mf.id = a.item_id
        WHERE a.item_type = 'media_file'
          AND a.play_count > 0
        GROUP BY mf.id
        ORDER BY play_count DESC
        LIMIT ?
    """, (limit,)).fetchall()
    return [dict(r) for r in rows]


def get_cross_user_matrix(db, limit=20):
    users = db.execute(
        "SELECT id, user_name FROM user ORDER BY user_name"
    ).fetchall()
    users = [dict(u) for u in users]

    top_songs = db.execute("""
        SELECT mf.id, mf.title, mf.artist,
               SUM(COALESCE(a.play_count, 0)) AS total
        FROM annotation a
        JOIN media_file mf ON mf.id = a.item_id
        WHERE a.item_type = 'media_file'
          AND a.play_count > 0
        GROUP BY mf.id
        ORDER BY total DESC
        LIMIT ?
    """, (limit,)).fetchall()
    top_songs = [dict(s) for s in top_songs]

    if not top_songs:
        return {"songs": [], "users": [], "matrix": []}

    song_ids = [s["id"] for s in top_songs]
    placeholders = ",".join("?" * len(song_ids))

    plays = db.execute(f"""
        SELECT item_id, user_id, play_count
        FROM annotation
        WHERE item_type = 'media_file'
          AND item_id IN ({placeholders})
    """, song_ids).fetchall()

    lookup = {}
    for p in plays:
        lookup[(p["item_id"], p["user_id"])] = p["play_count"] or 0

    matrix = []
    for user in users:
        row = [lookup.get((sid, user["id"]), 0) for sid in song_ids]
        matrix.append(row)

    return {
        "songs": [f"{s['title']} — {s['artist']}" for s in top_songs],
        "users": [u["user_name"] for u in users],
        "matrix": matrix,
    }
