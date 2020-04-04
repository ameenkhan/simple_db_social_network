-- Person can create a post
INSERT INTO Posts (post_date, group_id, author, content) VALUES
(CURDATE(), 0, 'citrus2014', 'test');

-- Person can follow a group 