USE SOCIAL_MEDIA;

DROP TABLE IF EXISTS People;
CREATE TABLE People(
  person_id VARCHAR(255),
  age INT,
  dob DATE,
  gender VARCHAR(255),
  fname VARCHAR(255),
  lname VARCHAR(255),
  PRIMARY KEY(person_id)
);
LOAD DATA INFILE '/var/lib/mysql-files/project/People.csv' IGNORE INTO TABLE People FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS
(person_id, age, dob, gender, fname, lname);

DROP TABLE IF EXISTS Group_T;
CREATE TABLE Group_T(
  group_id INT,
  group_name varchar(255),
  num_followers INT DEFAULT NULL, -- TODO calc this dynamically or as a temp var calc when needed
  PRIMARY KEY(group_id)
);
LOAD DATA INFILE '/var/lib/mysql-files/project/Groups.csv' IGNORE INTO TABLE Group_T FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS
(group_id, group_name, num_followers);

DROP TABLE IF EXISTS Topics;
CREATE TABLE Topics(
  topic_id INT,
  topic_name VARCHAR(255),
  num_posts INT DEFAULT NULL, -- TODO calc this dynamically or as a temp var calc when needed
  PRIMARY KEY(topic_id)
);
LOAD DATA INFILE '/var/lib/mysql-files/project/Topics.csv' IGNORE INTO TABLE Topics FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS
(topic_id, topic_name, num_posts);

DROP TABLE IF EXISTS Auth;
CREATE TABLE Auth(
  person_id VARCHAR(255),
  pass VARCHAR(255),
  login_date DATE,
  PRIMARY KEY(person_id)
);
LOAD DATA INFILE '/var/lib/mysql-files/project/Auth.csv' IGNORE INTO TABLE Auth FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS
(person_id, pass, login_date);

DROP TABLE IF EXISTS post_topics;
CREATE TABLE post_topics(
  post_id INT,
  topic_id INT,
  PRIMARY KEY(post_id, topic_id)
);
LOAD DATA INFILE '/var/lib/mysql-files/project/post_topics.csv' IGNORE INTO TABLE post_topics FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS
(post_id, topic_id);

DROP TABLE IF EXISTS followers_topics;
CREATE TABLE followers_topics(
  topic_id INT,
  person_id VARCHAR(255),
  PRIMARY KEY(topic_id, person_id)
);
LOAD DATA INFILE '/var/lib/mysql-files/project/followers_topics.csv' IGNORE INTO TABLE followers_topics FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS
(topic_id, person_id);

DROP TABLE IF EXISTS followers_people;
CREATE TABLE followers_people(
  person_id VARCHAR(255),
  follows_id VARCHAR(255),
  PRIMARY KEY(person_id, follows_id)
);
LOAD DATA INFILE '/var/lib/mysql-files/project/followers_people.csv' IGNORE INTO TABLE followers_people FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS
(person_id, follows_id);

DROP TABLE IF EXISTS followers_groups;
CREATE TABLE followers_groups(
  group_id INT,
  person_id VARCHAR(255),
  PRIMARY KEY(group_id, person_id)
);
LOAD DATA INFILE '/var/lib/mysql-files/project/followers_groups.csv' IGNORE INTO TABLE followers_groups FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS
(group_id, person_id);

DROP TABLE IF EXISTS Posts;
CREATE TABLE Posts(
  post_id INT NOT NULL AUTO_INCREMENT,
  post_date DATE,
  group_id INT,
  author VARCHAR(255),
  content LONGTEXT,
  PRIMARY KEY(post_id)
);
LOAD DATA INFILE '/var/lib/mysql-files/project/Posts.csv' IGNORE INTO TABLE Posts FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS
(post_id, post_date, group_id, author, content);

-- ================================
-- Adding Foreign Key relationships
-- ================================

ALTER TABLE Posts
ADD FOREIGN KEY (author) REFERENCES People(person_id),
ADD FOREIGN KEY (group_id) REFERENCES Group_T(group_id);

ALTER TABLE Auth
ADD FOREIGN KEY (person_id) REFERENCES People(person_id);

ALTER TABLE post_topics
ADD FOREIGN KEY (post_id) REFERENCES Posts(post_id),
ADD FOREIGN KEY (topic_id) REFERENCES Topics(topic_id);

ALTER TABLE followers_topics
ADD FOREIGN KEY (topic_id) REFERENCES Topics(topic_id),
ADD FOREIGN KEY (person_id) REFERENCES People(person_id);

ALTER TABLE followers_people
ADD FOREIGN KEY (person_id) REFERENCES People(person_id),
ADD FOREIGN KEY (follows_id) REFERENCES People(person_id);

ALTER TABLE followers_groups
ADD FOREIGN KEY (group_id) REFERENCES Group_T(group_id),
ADD FOREIGN KEY (person_id) REFERENCES People(person_id);