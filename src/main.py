import mysql.connector # activate venv
import time
from mysql.connector import errorcode

PERSON_ID = ""
LOGIN_DATE = ""

query_login_auth = (
  "SELECT fname, lname, login_date FROM "
  "People NATURAL JOIN	Auth "
  "WHERE person_id=%s AND	pass=%s"
)

query_list_all_posts_lim_100 = (
  "SELECT DISTINCT(post_id), post_date, author, content, group_name, react_pos, react_neg from Posts LEFT JOIN Group_T USING (group_id) WHERE "
	"author = %s "
	"OR "
	"author IN (SELECT follows_id FROM followers_people WHERE person_id = %s) "
	"OR "
	"group_id IN (SELECT group_id FROM followers_groups WHERE person_id = %s) "
	"OR "
	"post_id IN (SELECT DISTINCT(post_id) from post_topics WHERE topic_id IN (SELECT topic_id FROM followers_topics WHERE person_id = %s)) "
	"ORDER BY(post_date) DESC "
	"LIMIT 100;"
)

query_list_all_posts_no_lim = (
  "SELECT DISTINCT(post_id), post_date, author, content, group_name, react_pos, react_neg from Posts LEFT JOIN Group_T USING (group_id) WHERE "
	"author = %s "
	"OR "
	"author IN (SELECT follows_id FROM followers_people WHERE person_id = %s) "
	"OR "
	"group_id IN (SELECT group_id FROM followers_groups WHERE person_id = %s) "
	"OR "
	"post_id IN (SELECT DISTINCT(post_id) from post_topics WHERE topic_id IN (SELECT topic_id FROM followers_topics WHERE person_id = %s)) "
	"ORDER BY(post_date) DESC;" 
)

query_list_all_posts_your_posts = (
  "SELECT DISTINCT(post_id), post_date, author, content, group_name, react_pos, react_neg from Posts LEFT JOIN Group_T USING (group_id) WHERE author = %s ORDER BY(post_date) DESC;"
)

query_list_all_posts_unread = (
  "SELECT DISTINCT(post_id), post_date, author, content, group_name, react_pos, react_neg FROM Posts LEFT JOIN Group_T USING (group_id) WHERE "
    "( "
      "author IN (SELECT follows_id FROM followers_people WHERE person_id = %s) "
      "OR "
      "group_id IN (SELECT group_id FROM followers_groups WHERE person_id = %s) "
      "OR "
      "post_id IN (SELECT DISTINCT(post_id) from post_topics WHERE topic_id IN (SELECT topic_id FROM followers_topics WHERE person_id = %s)) "
    ") "
    "AND "
    "post_date > (SELECT login_date FROM Auth WHERE person_id = %s) "
  "ORDER BY(post_date) DESC; "
)

query_list_topics_for_post = (
  "SELECT topic_name FROM post_topics LEFT JOIN Topics USING (topic_id) WHERE post_id = %s;"
)

query_list_groups_user_follows = (
  "SELECT group_name, group_id FROM Group_T WHERE group_id IN (SELECT group_id FROM followers_groups WHERE person_id = %s) OR group_id = 0;"
)

query_list_topics_user_follows = (
  "SELECT topic_id, topic_name FROM Topics WHERE topic_id IN (SELECT topic_id FROM followers_topics WHERE person_id = %s);"
)

# The connector needs to start and commit the transaction using its cnx commands
# group_id, PERSON_ID, content
query_create_new_post = (
  "INSERT INTO Posts (post_date, group_id, author, content) VALUES(CURDATE(),'{0}','{1}','{2}');"
)

query_list_post_details = (
  "SELECT post_id, post_date, group_name, parent_post_id, author, content, react_pos, react_neg FROM "
  "(SELECT * FROM Posts WHERE post_id = %s) as T JOIN Group_T USING(group_id);"
)

try:
  cnx = mysql.connector.connect(user='user_ece356_test', password='user_ece356_test',
                              host='192.168.56.101',
                              database='SOCIAL_MEDIA')
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
  print('\n\nConnection to social media successfully established!\n\n')

  cursor    = cnx.cursor(buffered=True)
  cursor2   = cnx.cursor(buffered=True)
  login_try = 0
  
  while True:
    if login_try == 3:
      print("\nToo many failed login attempts.. exiting now\n\n")
      exit(1)
    
    print("\nEnter username")
    PERSON_ID = input()
    print("\nEnter password")
    password = input()

    cursor.execute(query_login_auth, (PERSON_ID, password))
    if cursor.rowcount == 1:
      for fname, lname, login_date in cursor:
        print(f"\n\nWelcome {fname} {lname}\nLogin date: {login_date}\n\n")
      break

    login_try +=1

  def main_1_2():
    print(
      "---\n"
      "List posts\n"
      "1. Go Back\n"
      "2. List all posts with a limit of 100 posts shown\n"
      "3. List all posts without a limit on posts shown\n"
      "4. List all of your posts\n"
    )
    selection = input()
    if selection == "1":
      main_1()

    elif selection == "2":
      cursor.execute(query_list_all_posts_lim_100, (PERSON_ID, PERSON_ID, PERSON_ID, PERSON_ID))
      print("Listing all posts with a limit of 100 posts shown")
      for post_id, post_date, author, content, group_name, react_pos, react_neg in cursor:
        print(f"Post ID   : {post_id}")
        print(f"Post Date : {post_date}")
        print(f"Group     : {group_name}")
        print(f"Topics    :", end = " ")
        cursor2.execute(query_list_topics_for_post, (post_id,))
        for topic_name in cursor2:
          print(topic_name[0], end = " | ")
        print()
        print(f"Author    : {author}")
        print(f":)        : {react_pos}")
        print(f":(        : {react_neg}")
        print(content, "\n\n")

    elif selection == "3":
      cursor.execute(query_list_all_posts_no_lim, (PERSON_ID, PERSON_ID, PERSON_ID, PERSON_ID))
      print("Listing all posts you follow")
      for post_id, post_date, author, content, group_name, react_pos, react_neg in cursor:
        print(f"Post ID   : {post_id}")
        print(f"Post Date : {post_date}")
        print(f"Group     : {group_name}")
        print(f"Topics    :", end = " ")
        cursor2.execute(query_list_topics_for_post, (post_id,))
        for topic_name in cursor2:
          print(topic_name[0], end = " | ")
        print()
        print(f"Author    : {author}")
        print(f":)        : {react_pos}")
        print(f":(        : {react_neg}")
        print(content, "\n\n")
    
    elif selection == "4":
      cursor.execute(query_list_all_posts_your_posts, (PERSON_ID,))
      print("Listing all of your posts")
      for post_id, post_date, author, content, group_name, react_pos, react_neg in cursor:
        print(f"Post ID   : {post_id}")
        print(f"Post Date : {post_date}")
        print(f"Group     : {group_name}")
        print(f"Topics    :", end = " ")
        cursor2.execute(query_list_topics_for_post, (post_id,))
        for topic_name in cursor2:
          print(topic_name[0], end = " | ")
        print()
        print(f"Author    : {author}")
        print(f":)        : {react_pos}")
        print(f":(        : {react_neg}")
        print(content, "\n\n")
    
    main_1_2()

  def main_1():
    # give the option to give a +/- 1 or reply in option 5
    print(
      "---\n"
      "Post Activities\n"
      "1. Go Back\n"
      "2. List posts\n"                                                           # DONE
      "3. List unread posts\n"                                                    # DONE
      "4. Create a Post (to reply to a post you must first view it - option 5)\n" # DONE
      "5. View a specific post\n"                                                 
    )
    
    selection = input()
    if selection == "1":
      main()

    elif selection == "2":
      main_1_2()
    
    elif selection == "3":
      cursor.execute(query_list_all_posts_unread, (PERSON_ID, PERSON_ID, PERSON_ID, PERSON_ID))
      print("Listing all unread posts (determined by login time)")
      for post_id, post_date, author, content, group_name, react_pos, react_neg in cursor:
        print(f"Post ID   : {post_id}")
        print(f"Post Date : {post_date}")
        print(f"Group     : {group_name}")
        print(f"Topics    :", end = " ")
        cursor2.execute(query_list_topics_for_post, (post_id,))
        for topic_name in cursor2:
          print(topic_name[0], end = " | ")
        print()
        print(f"Author    : {author}")
        print(f":)        : {react_pos}")
        print(f":(        : {react_neg}")
        print(content, "\n\n")
      main_1()

    elif selection == "4":
      print(
        "\nCreating a post\n"
        "What is the post content?\n"
      )
      cr_content = input()

      print(
        "\nThese are the groups you follow\n"
        "Group Name -> Group ID\n\n"
      )
      cursor.execute(query_list_groups_user_follows, (PERSON_ID,))

      list_group_id = list()
      for group_name, group_id in cursor:
        print(f"{group_name} -> {group_id}")
        list_group_id.append(group_id)

      print("\n\nWhich group would you like to post in?\nEnter a group id\n")
      
      cr_group = input()
      cr_group = int(cr_group)

      if cr_group not in list_group_id:
        print("ERROR creating post. You did not enter a group_id of a group you follow.\n")
        pass
      else:
        print(
          "---"
          "\nThese are the topics you follow\n"
          "Topic Name -> Topic ID\n\n"
        )
        list_topic_id = list()
        cursor.execute(query_list_topics_user_follows, (PERSON_ID,))
        for topic_id, topic_name in cursor:
          print(f"{topic_name} -> {topic_id}")
          list_topic_id.append(topic_id)
        
        print('\n\n---\nWhich topics would you like to post in?\nEnter the group ids seperated by commas ","\n')
      
        topic_in = input()
        cr_topics_split = topic_in.split(",")

        topic_err = False
        cr_topics = list()

        for topic in cr_topics_split:
          topic = int(topic)
          cr_topics.append(topic)
          if topic not in list_topic_id:
            print("\nERROR creating post. You entered id(s) of topic(s) you do not follow.\n\n")
            topic_err = True
            break
        
        if topic_err:
          pass
        else:
          # Creating transaction query
          new_post = query_create_new_post
          new_post = new_post.format(cr_group, PERSON_ID, cr_content)
          
          cnx.commit()
          cnx.start_transaction()
          cursor.execute(new_post)
          cursor.execute("SET @p_id = (SELECT LAST_INSERT_ID());")
          for i in cr_topics:
            cursor.execute(f"INSERT INTO post_topics (post_id, topic_id) VALUES(@p_id, {i});")
          cnx.commit()
          
          cursor.execute("SELECT @p_id;")
          for p_id in cursor:
            post_id = p_id[0]
          
          print("\nYour post's ID is:", post_id)
          print("\nPost created successfully!\n\n")

      main_1()

    elif selection == "5":
      print(
        "\nEnter a post id to view it's content:\n"
      )
      u_post_id = input()



  def main_2():
    print(
        "1.   Go Back\n"
        "2.   List Topics you follow\n"
        "3.   List Groups you follow\n"
        "4.   List People you follow\n"
      )
  
  def main():
    print(
      "---\n"
      "What would you like to do?\nEnter the number for the following actions:\n\n"
      "1.   Post Activities\n"                                                    # DONE
      "2.   List the names of Topics, Groups, People you follow\n"
      "3.   Add Topics, Groups, People to follow/ join\n"
      "-99. Exit\n"
      "\n"
    )
    selection = input()
    if selection == "-99":
      print("\nLogging off now.. Cya!\n\n")
      exit(1)

    elif selection == "1":
      main_1()

    elif selection == "2":
      main_2()

    elif selection == "3":
      print("\noptions for 3\n")

  main()