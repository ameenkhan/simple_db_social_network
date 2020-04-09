-- Person can create a post
INSERT INTO Posts (post_date, group_id, author, content) VALUES
(CURDATE(), 0, 'citrus2014', 'test');

-- Login get fname, lname
SELECT fname, lname FROM
	People
		NATURAL JOIN
	Auth
WHERE
	pass="tin" AND
	person_id="odalv";

-- Posts

-- odalv tin
-- 1) Posts you've authored
SELECT post_id FROM Posts WHERE author = "odalv";

-- 2) People you follow
SELECT follows_id FROM followers_people WHERE person_id = "odalv";
-- posts authored by those people
SELECT post_id FROM Posts WHERE author IN (SELECT follows_id FROM followers_people WHERE person_id = "odalv");

-- 3) Groups you follow
SELECT group_id FROM followers_groups WHERE person_id = "odalv";
-- post_ids from those groups
SELECT DISTINCT(post_id) from Posts WHERE group_id IN (SELECT group_id FROM followers_groups WHERE person_id = "odalv");

-- 4) Topics you follow
SELECT topic_id FROM followers_topics WHERE person_id = "odalv";
-- post_ids associated with that topic
SELECT DISTINCT(post_id) from post_topics WHERE topic_id IN (SELECT topic_id FROM followers_topics WHERE person_id = "odalv");

SELECT DISTINCT(post_id) from Posts WHERE
	author = "odalv"
	OR
	author IN (SELECT follows_id FROM followers_people WHERE person_id = "odalv")
	OR
	group_id IN (SELECT group_id FROM followers_groups WHERE person_id = "odalv")
	OR
	post_id IN (SELECT DISTINCT(post_id) from post_topics WHERE topic_id IN (SELECT topic_id FROM followers_topics WHERE person_id = "odalv"))
