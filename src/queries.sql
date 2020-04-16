-- Login Authorization
SELECT fname, lname, login_date FROM People NATURAL JOIN Auth WHERE person_id=%s AND	pass=%s;

-- List all posts a user follows with a limit of 100
SELECT DISTINCT(post_id), post_date, author, content, group_name, react_pos, react_neg from Posts 
LEFT JOIN 
Group_T 
USING (group_id) WHERE
	author = %s
	OR
	author IN (SELECT follows_id FROM followers_people WHERE person_id = %s)
	OR
	group_id IN (SELECT group_id FROM followers_groups WHERE person_id = %s)
	OR
	post_id IN (SELECT DISTINCT(post_id) from post_topics WHERE 
		topic_id IN (SELECT topic_id FROM followers_topics WHERE person_id = %s))
ORDER BY(post_date) DESC 
LIMIT 100;

-- List all posts a user follows with no limit
SELECT DISTINCT(post_id), post_date, author, content, group_name, react_pos, react_neg from Posts 
LEFT JOIN Group_T 
USING (group_id) WHERE 
	author = %s 
	OR 
	author IN (SELECT follows_id FROM followers_people WHERE person_id = %s) 
	OR 
	group_id IN (SELECT group_id FROM followers_groups WHERE person_id = %s) 
	OR 
	post_id IN (SELECT DISTINCT(post_id) from post_topics WHERE 
		topic_id IN (SELECT topic_id FROM followers_topics WHERE person_id = %s))
ORDER BY(post_date) DESC; 

-- Search through all posts a user follows for a keyword
SELECT DISTINCT(post_id), post_date, author, content, group_name, react_pos, react_neg from Posts 
LEFT JOIN Group_T 
USING (group_id) WHERE 
	(author = '{0}' 
	OR 
	author IN (SELECT follows_id FROM followers_people WHERE person_id = '{0}') 
	OR 
	group_id IN (SELECT group_id FROM followers_groups WHERE person_id = '{0}') 
	OR 
	post_id IN (SELECT DISTINCT(post_id) from post_topics WHERE 
		topic_id IN (SELECT topic_id FROM followers_topics WHERE person_id = '{0}'))) 
	AND 
	content LIKE '%{1}%' 
ORDER BY(post_date) DESC;

-- list all of your posts
SELECT DISTINCT(post_id), post_date, author, content, group_name, react_pos, react_neg from Posts 
LEFT JOIN Group_T 
USING (group_id) WHERE 
	author = %s 
ORDER BY(post_date) DESC;

-- list all of the unread posts you follow
SELECT DISTINCT(post_id), post_date, author, content, group_name, react_pos, react_neg FROM Posts LEFT JOIN Group_T USING (group_id) WHERE 
	( 
		author IN (SELECT follows_id FROM followers_people WHERE person_id = %s) 
		OR 
		group_id IN (SELECT group_id FROM followers_groups WHERE person_id = %s) 
		OR 
		post_id IN (SELECT DISTINCT(post_id) from post_topics WHERE topic_id IN (SELECT topic_id FROM followers_topics WHERE person_id = %s)) 
	) 
	AND 
	post_date > (SELECT login_date FROM Auth WHERE person_id = %s) 
ORDER BY(post_date) DESC; 

-- List all the topics associated with a post
SELECT topic_name FROM post_topics LEFT JOIN Topics USING (topic_id) WHERE post_id = %s;

-- List all the groups a user follows
SELECT group_name, group_id FROM Group_T WHERE group_id IN (SELECT group_id FROM followers_groups WHERE person_id = %s) OR group_id = 0;

-- List all the groups a user does not follow
SELECT group_name, group_id FROM Group_T WHERE group_id NOT IN (SELECT group_id FROM followers_groups WHERE person_id = %s) OR group_id = 0;

-- List all the topics a user follows
SELECT topic_id, topic_name FROM Topics WHERE topic_id IN (SELECT topic_id FROM followers_topics WHERE person_id = %s);

-- List all the topics a user does not follow
SELECT topic_id, topic_name FROM Topics WHERE topic_id NOT IN (SELECT topic_id FROM followers_topics WHERE person_id = %s);

-- List all the people a user follows
SELECT fname, lname, person_id FROM 
	(SELECT follows_id FROM followers_people WHERE person_id = %s) as x 
	LEFT JOIN 
	People 
	ON x.follows_id = People.person_id;

-- Create a new post
START TRANSACTION;
	INSERT INTO Posts (post_date, group_id, author, content) VALUES(CURDATE(),'{0}','{1}','{2}');
	SET @p_id = (SELECT LAST_INSERT_ID());
	INSERT INTO post_topics (post_id, topic_id) VALUES(@p_id, {i});
	INSERT INTO post_topics (post_id, topic_id) VALUES(@p_id, {i});
COMMIT;

-- Create a reply post
START TRANSACTION;
	INSERT INTO Posts (post_date, group_id, parent_post_id, author, content) VALUES(CURDATE(),'{0}', {1}, '{2}','{3}');
	SET @p_id = (SELECT LAST_INSERT_ID());
	INSERT INTO post_topics (post_id, topic_id) VALUES(@p_id, {i});
	INSERT INTO post_topics (post_id, topic_id) VALUES(@p_id, {i});
COMMIT;

-- Update positive reaction on a post
UPDATE Posts SET react_pos = react_pos + 1 WHERE post_id = %s;

-- Update negative reaction on a post
UPDATE Posts SET react_neg = react_neg - 1 WHERE post_id = %s;

-- List the details of a post
SELECT post_id, post_date, group_name, parent_post_id, author, content, react_pos, react_neg FROM 
  (SELECT * FROM Posts WHERE post_id = %s) as T 
	JOIN Group_T 
	USING(group_id);

-- Find a user
SELECT * FROM People WHERE person_id = %s;

-- Get the details of a topic
SELECT 
	(SELECT COUNT(*) FROM post_topics WHERE topic_id = %s) As posts, 
	(SELECT COUNT(*) FROM followers_topics WHERE topic_id = %s) As followers;

-- Get the details of a group
SELECT 
	(SELECT COUNT(*) FROM Posts WHERE group_id = %s) As posts, 
	(SELECT COUNT(*) FROM followers_groups WHERE group_id = %s) As followers;