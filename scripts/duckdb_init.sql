ATTACH 'C:\\Users\\si929x\\Desktop\\projects\\kiwi\\data\\sqlite\\sakila.db' AS sakila (TYPE sqlite, READ_ONLY);
ATTACH 'C:\\Users\\si929x\\Desktop\\projects\\kiwi\\data\\sqlite\\Chinook.db' AS chinook (TYPE sqlite, READ_ONLY);
SET search_path TO chinook
--CREATE table tbl1 (i INTEGER);
--INSERT INTO tbl1
--    VALUES (1), (2), (3);