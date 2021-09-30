import sqlalchemy

engine = sqlalchemy.create_engine('postgresql://lubov:password@localhost:5432/music')
connection = engine.connect()

sel1 = connection.execute("""SELECT name_genre, COUNT(musician_id) m FROM musician_genre
LEFT JOIN genre ON musician_genre.genre_id = genre.id
GROUP BY name_genre
ORDER BY m DESC;
""").fetchall()
print(sel1)

sel2 = connection.execute("""SELECT COUNT(name_track) FROM track
LEFT JOIN album ON track.album_id = album.id
WHERE year_of_issue BETWEEN 2019 AND 2020;
""").fetchall()
print(sel2)

sel3 = connection.execute("""SELECT name_album, ROUND(AVG(duration), 2) d FROM track
LEFT JOIN album ON track.album_id = album.id
GROUP BY name_album
ORDER BY d DESC;
""").fetchall()
print(sel3)

sel4 = connection.execute("""SELECT DISTINCT name FROM musician_album ma
LEFT JOIN musician m ON ma.musician_id = m.id
JOIN album ON ma.album_id = album.id
WHERE NOT year_of_issue = 2020;
""").fetchall()
print(sel4)

sel5 = connection.execute("""SELECT DISTINCT name_collection FROM collection c
JOIN collection_track ct ON c.id = ct.collection_id
JOIN track t ON ct.track_id = t.id
JOIN album a ON t.album_id = a.id
JOIN musician_album ma ON a.id = ma.album_id
JOIN musician m ON ma.musician_id = m.id
WHERE m.name = 'Сплин';
""").fetchall()
print(sel5)

sel6 = connection.execute("""SELECT name_album FROM musician m
JOIN musician_album ma ON m.id = ma.musician_id
JOIN album a ON ma.album_id = a.id
WHERE m.id IN (SELECT id FROM musician m
JOIN musician_genre mg ON m.id = mg.musician_id
GROUP BY id
HAVING COUNT(genre_id) > 1);
""").fetchall()
print(sel6)

sel7 = connection.execute("""SELECT name_track FROM track 
WHERE NOT id IN (SELECT DISTINCT track_id FROM collection_track);
""").fetchall()
print(sel7)

sel8 = connection.execute("""SELECT name FROM musician m
JOIN musician_album ma ON m.id = ma.musician_id
JOIN album a ON ma.album_id = a.id
JOIN track t ON a.id = t.album_id
WHERE t.duration = (SELECT DISTINCT MIN(duration) FROM track);
""").fetchall()
print(sel8)

sel9 = connection.execute("""SELECT name_tn.name_album FROM (SELECT name_album, COUNT(name_track) tn FROM album a
JOIN track t ON a.id = t.album_id
GROUP BY name_album) name_tn
WHERE name_tn.tn = (SELECT MIN(name_tn.tn) FROM (SELECT name_album, COUNT(name_track) tn FROM album a
JOIN track t ON a.id = t.album_id
GROUP BY name_album) name_tn);
""").fetchall()
print(sel9)