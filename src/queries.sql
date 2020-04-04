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