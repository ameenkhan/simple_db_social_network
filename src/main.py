import mysql.connector # activate venv
import time
from mysql.connector import errorcode

PERSON_ID = ""
LOGIN_DATE = ""

# username, password
query_login_auth = (
  "SELECT fname, lname, login_date FROM "
  "People NATURAL JOIN	Auth "
  "WHERE person_id=%s AND	pass=%s"
)

# PERSON_ID, PERSON_ID, PERSON_ID, PERSON_ID
query_list_all_posts_lim_100 = (
  "SELECT DISTINCT(post_id), post_date, parent_post_id, author, content, group_name, react_pos, react_neg from Posts LEFT JOIN Group_T USING (group_id) WHERE "
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

# PERSON_ID, PERSON_ID, PERSON_ID, PERSON_ID
query_list_all_posts_no_lim = (
  "SELECT DISTINCT(post_id), post_date, parent_post_id, author, content, group_name, react_pos, react_neg from Posts LEFT JOIN Group_T USING (group_id) WHERE "
	"author = %s "
	"OR "
	"author IN (SELECT follows_id FROM followers_people WHERE person_id = %s) "
	"OR "
	"group_id IN (SELECT group_id FROM followers_groups WHERE person_id = %s) "
	"OR "
	"post_id IN (SELECT DISTINCT(post_id) from post_topics WHERE topic_id IN (SELECT topic_id FROM followers_topics WHERE person_id = %s)) "
	"ORDER BY(post_date) DESC;" 
)

# {PERSON_ID}, {keyword}
query_search_following_posts = (
  "SELECT DISTINCT(post_id), post_date, parent_post_id, author, content, group_name, react_pos, react_neg from Posts LEFT JOIN Group_T USING (group_id) WHERE "
	"(author = '{0}' "
	"OR "
	"author IN (SELECT follows_id FROM followers_people WHERE person_id = '{0}') "
	"OR "
	"group_id IN (SELECT group_id FROM followers_groups WHERE person_id = '{0}') "
	"OR "
	"post_id IN (SELECT DISTINCT(post_id) from post_topics WHERE topic_id IN (SELECT topic_id FROM followers_topics WHERE person_id = '{0}'))) "
	"AND "
	"content LIKE '%{1}%' "
	"ORDER BY(post_date) DESC;"
)

# PERSON_ID
query_list_all_posts_your_posts = (
  "SELECT DISTINCT(post_id), post_date, parent_post_id, author, content, group_name, react_pos, react_neg from Posts LEFT JOIN Group_T USING (group_id) WHERE author = %s ORDER BY(post_date) DESC;"
)

# PERSON_ID, PERSON_ID, PERSON_ID, PERSON_ID
query_list_all_posts_unread = (
  "SELECT DISTINCT(post_id), post_date, parent_post_id, author, content, group_name, react_pos, react_neg FROM Posts LEFT JOIN Group_T USING (group_id) WHERE "
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

# PERSON_ID
query_list_topics_for_post = (
  "SELECT topic_name FROM post_topics LEFT JOIN Topics USING (topic_id) WHERE post_id = %s;"
)

# PERSON_ID
query_list_groups_user_follows = (
  "SELECT group_name, group_id FROM Group_T WHERE group_id IN (SELECT group_id FROM followers_groups WHERE person_id = %s) OR group_id = 0;"
)

# PERSON_ID
query_list_groups_user_does_not_follow = (
  "SELECT group_name, group_id FROM Group_T WHERE group_id NOT IN (SELECT group_id FROM followers_groups WHERE person_id = %s) OR group_id = 0;"
)

# PERSON_ID
query_list_topics_user_follows = (
  "SELECT topic_id, topic_name FROM Topics WHERE topic_id IN (SELECT topic_id FROM followers_topics WHERE person_id = %s);"
)

# PERSON_ID
query_list_topics_user_does_not_follow = (
  "SELECT topic_id, topic_name FROM Topics WHERE topic_id NOT IN (SELECT topic_id FROM followers_topics WHERE person_id = %s);"
)

# PERSON_ID
query_list_people_user_follows = (
  "SELECT fname, lname, person_id FROM "
	"(SELECT follows_id FROM followers_people WHERE person_id = %s) as x "
	"LEFT JOIN "
	"People "
	"ON x.follows_id = People.person_id;"
)

# The connector needs to start and commit the transaction using its cnx commands
# group_id, PERSON_ID, content
query_create_new_post = (
  "INSERT INTO Posts (post_date, group_id, author, content) VALUES(CURDATE(),'{0}','{1}','{2}');"
)

# group_id, parent_post_id, PERSON_ID, content
query_create_reply = (
  "INSERT INTO Posts (post_date, group_id, parent_post_id, author, content) VALUES(CURDATE(),'{0}', {1}, '{2}','{3}');"
)

#POST_ID
query_update_react_pos = (
  "UPDATE Posts SET react_pos = react_pos + 1 WHERE post_id = %s;"
)

#POST_ID
query_update_react_neg = (
  "UPDATE Posts SET react_neg = react_neg + 1 WHERE post_id = %s;"
)

#POST_ID
query_list_post_details = (
  "SELECT post_id, post_date, group_name, parent_post_id, author, content, react_pos, react_neg FROM "
  "(SELECT * FROM Posts WHERE post_id = %s) as T JOIN Group_T USING(group_id);"
)

# user_id
query_find_a_user = (
  "SELECT * FROM People WHERE person_id = %s;"
)

# topic_id, topic_id
query_topic_details = (
  "SELECT "
  "  (SELECT COUNT(*) FROM post_topics WHERE topic_id = %s) As posts, "
  "  (SELECT COUNT(*) FROM followers_topics WHERE topic_id = %s) As followers;"
)

# group_id, group_id
query_group_details = (
  "SELECT "
  "  (SELECT COUNT(*) FROM Posts WHERE group_id = %s) As posts, "
  "  (SELECT COUNT(*) FROM followers_groups WHERE group_id = %s) As followers;"
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

  # Create a post
  def create_post(reply_post_id=None):
    print(
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

        # Determine if this new post is a reply or a new post
        if reply_post_id:
          new_post = query_create_reply
          new_post = new_post.format(cr_group, reply_post_id, PERSON_ID, cr_content)
        else:
          new_post = query_create_new_post
          new_post = new_post.format(cr_group, PERSON_ID, cr_content)
        
        cnx.commit()
        cnx.start_transaction()
        print(f"\n{new_post}\n\n")
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

  # List a post details
  def post_detail(p_id):
    cursor.execute(query_list_post_details, (p_id,))
    for res in cursor:
      print(f"Post ID   : {res[0]}")
      print(f"Post Date : {res[1]}")
      print(f"Group     : {res[2]}")
      print(f"Topics    :", end = " ")
      cursor2.execute(query_list_topics_for_post, (res[0],))
      for topic_name in cursor2:
        print(topic_name[0], end = " | ")
      print()
      print(f"Reply To  : {res[3]}")
      print(f"Author    : {res[4]}")
      print(f":)        : {res[6]}")
      print(f":(        : {res[7]}")
      print(res[5], "\n\n")
    print()
          
  # List Posts options
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
      for post_id, post_date, parent_post_id, author, content, group_name, react_pos, react_neg in cursor:
        print(f"Post ID   : {post_id}")
        print(f"Post Date : {post_date}")
        print(f"Group     : {group_name}")
        print(f"Topics    :", end = " ")
        cursor2.execute(query_list_topics_for_post, (post_id,))
        for topic_name in cursor2:
          print(topic_name[0], end = " | ")
        print()
        print(f"Reply To  : {parent_post_id}")
        print(f"Author    : {author}")
        print(f":)        : {react_pos}")
        print(f":(        : {react_neg}")
        print(content, "\n\n")

    elif selection == "3":
      cursor.execute(query_list_all_posts_no_lim, (PERSON_ID, PERSON_ID, PERSON_ID, PERSON_ID))
      print("Listing all posts you follow")
      for post_id, post_date, parent_post_id, author, content, group_name, react_pos, react_neg in cursor:
        print(f"Post ID   : {post_id}")
        print(f"Post Date : {post_date}")
        print(f"Group     : {group_name}")
        print(f"Topics    :", end = " ")
        cursor2.execute(query_list_topics_for_post, (post_id,))
        for topic_name in cursor2:
          print(topic_name[0], end = " | ")
        print()
        print(f"Reply To  : {parent_post_id}")
        print(f"Author    : {author}")
        print(f":)        : {react_pos}")
        print(f":(        : {react_neg}")
        print(content, "\n\n")
    
    elif selection == "4":
      cursor.execute(query_list_all_posts_your_posts, (PERSON_ID,))
      print("Listing all of your posts")
      for post_id, post_date, parent_post_id, author, content, group_name, react_pos, react_neg in cursor:
        print(f"Post ID   : {post_id}")
        print(f"Post Date : {post_date}")
        print(f"Group     : {group_name}")
        print(f"Topics    :", end = " ")
        cursor2.execute(query_list_topics_for_post, (post_id,))
        for topic_name in cursor2:
          print(topic_name[0], end = " | ")
        print()
        print(f"Reply To  : {parent_post_id}")
        print(f"Author    : {author}")
        print(f":)        : {react_pos}")
        print(f":(        : {react_neg}")
        print(content, "\n\n")
    
    main_1_2()

  # Specific post activities
  def main_1_5(p_id):
    post_detail(p_id)
    print(
      "1. Go Back\n"
      "2. React with a :)\n"
      "3. React with a :(\n"
      "4. Respond with a reply post\n"
    )
    selection = input()

    if selection == "1":
      main_1()
    elif selection == "2":
      cursor.execute(query_update_react_pos, (p_id,))
      main_1_5(p_id)
    elif selection == "3":
      cursor.execute(query_update_react_neg, (p_id,))
      main_1_5(p_id)
    elif selection == '4':
      print(f"\nCreating a reply for post: {p_id}\n")
      print("\nCreating a new post\n")
      create_post(p_id)
      main_1()

  # Post Activites
  def main_1():
    # give the option to give a +/- 1 or reply in option 5
    print(
      "\n---\n"
      "Post Activities\n"
      "1. Go Back\n"
      "2. List posts\n"                                                           # DONE
      "3. List unread posts\n"                                                    # DONE
      "4. Create a Post (to reply to a post you must first view it - option 5)\n" # DONE
      "5. View a specific post\n"                                                 # DONE
      "6. Search for a post\n"                                                    # DONE
    )
    
    selection = input()
    if selection == "1":
      main()
    elif selection == "2":
      main_1_2()
    elif selection == "3":
      cursor.execute(query_list_all_posts_unread, (PERSON_ID, PERSON_ID, PERSON_ID, PERSON_ID))
      print("Listing all unread posts (determined by login time)")
      for post_id, post_date, parent_post_id, author, content, group_name, react_pos, react_neg in cursor:
        print(f"Post ID   : {post_id}")
        print(f"Post Date : {post_date}")
        print(f"Group     : {group_name}")
        print(f"Topics    :", end = " ")
        cursor2.execute(query_list_topics_for_post, (post_id,))
        for topic_name in cursor2:
          print(topic_name[0], end = " | ")
        print()
        print(f"Reply To  : {parent_post_id}")
        print(f"Author    : {author}")
        print(f":)        : {react_pos}")
        print(f":(        : {react_neg}")
        print(content, "\n\n")
      main_1()
    elif selection == "4":
      print("\nCreating a new post\n")
      create_post()
      main_1()
    elif selection == "5":
      print(
        "\nEnter a post id to view it's content:\n"
      )
      u_post_id = input()
      cursor.execute(query_list_post_details, (u_post_id,))

      if cursor.rowcount == 0:
        print("\nNo post exists with that id...\n")
        main_1()
      else:
        main_1_5(u_post_id)
    elif selection == "6":
      print("\nEnter a keyword to search through all posts you follow\n")
      u_search = input()
      search_query = query_search_following_posts.format(PERSON_ID, u_search)
      cursor.execute(search_query)
      print(f"\nAll posts containing {u_search}:\n")
      for post_id, post_date, parent_post_id, author, content, group_name, react_pos, react_neg in cursor:
        print(f"Post ID   : {post_id}")
        print(f"Post Date : {post_date}")
        print(f"Group     : {group_name}")
        print(f"Topics    :", end = " ")
        cursor2.execute(query_list_topics_for_post, (post_id,))
        for topic_name in cursor2:
          print(topic_name[0], end = " | ")
        print()
        print(f"Reply To  : {parent_post_id}")
        print(f"Author    : {author}")
        print(f":)        : {react_pos}")
        print(f":(        : {react_neg}")
        print(content, "\n\n")
      main_1()

  # Entities you follow
  def main_2():
    print(
        "\n---\nEntities You Follow\n"
        "1.   Go Back\n"
        "2.   List Topics you follow\n"
        "3.   List Groups you follow\n"
        "4.   List People you follow\n"
      )
    selection = input()
    if selection == "1":
      main()
    elif selection == "2":
      print(
        "---"
        "\nThese are the topics you follow\n"
        "Topic Name -> Topic ID\n\n"
      )
      cursor.execute(query_list_topics_user_follows, (PERSON_ID,))
      for topic_id, topic_name in cursor:
        print(f"{topic_name} -> {topic_id}")
      print()
      main_2()
    elif selection == "3":
      print(
        "\nThese are the groups you follow\n"
        "Group Name -> Group ID\n\n"
      )
      cursor.execute(query_list_groups_user_follows, (PERSON_ID,))
      for group_name, group_id in cursor:
        print(f"{group_name} -> {group_id}")
      print()
      main_2()
    elif selection == "4":
      print(
        "\nThese are the people you follow\n"
        "First Name | Last Name | Their User ID\n\n"
      )
      cursor.execute(query_list_people_user_follows, (PERSON_ID,))
      
      for fname, lname, person_id in cursor:
        print(f"{fname} | {lname} | {person_id}")
      print()
      main_2()

  # Add Entities to follow
  def main_3():
    print(
      "\n---\nEntities To Add\n"
      "1.   Go Back\n"
      "2.   Follow a new Topic\n"       # DONE
      "3.   Follow a new Group\n"       #
      "4.   Follow a new Person\n"
    )
    selection = input()
    if selection == "1":
      main()
    elif selection == "2":
      print(
        "\nThese are the topics you do not follow\n"
        "Topics Name -> Topic_ID\n"
      )

      cursor.execute(query_list_topics_user_does_not_follow, (PERSON_ID,))
      for topic_id, topic_name in cursor:
        print(f"{topic_name} -> {topic_id}")
      print(
        "\nEnter multiple Topic_IDs seperated by commas, to follow\n"
      )
      
      u_topics_split = input()
      u_topics_split = u_topics_split.split(",")

      cnx.commit()
      cnx.start_transaction()
      for topic in u_topics_split:
        topic = int(topic)
        cursor.execute(f"INSERT INTO followers_topics (topic_id, person_id) VALUES({topic},'{PERSON_ID}')")        
      cnx.commit()
      print("\nSuccessfully following new topics\n")
      main_3()
    elif selection == "3":
      print(
        "\nThese are the groups you do not follow\n"
        "Group Name -> Group_ID\n"
      )

      cursor.execute(query_list_groups_user_does_not_follow, (PERSON_ID,))
      for group_name, group_id in cursor:
        print(f"{group_name} -> {group_id}")
      print(
        "\nEnter multiple Group_IDs seperated by commas, to follow\n"
      )
      
      u_groups_split = input()
      u_groups_split = u_groups_split.split(",")

      cnx.commit()
      cnx.start_transaction()
      for group in u_groups_split:
        group = int(group)
        cursor.execute(f"INSERT INTO followers_groups (group_id, person_id) VALUES({group},'{PERSON_ID}')")        
      cnx.commit()
      print("\nSuccessfully following new groups\n")
      main_3()
    elif selection == "4":
      print("\nEnter a user id to follow the person if they exist\n")
      u_person_id = input()
      cursor.execute(query_find_a_user, (u_person_id,))
      
      if cursor.rowcount == 0:
        print("\nPerson not found\n")
        main_3()
      else:
        print(f"\nYou are now following {u_person_id}\n")
        main_3()
      
  # Details of a Topic or Group
  def main_4():
    print(
      "\nDetails of a Topic or a Group\n"
      "1. Go Back\n"
      "2. Details of a Topic\n"
      "3. Details of a Group\n"
    )

    selection = input()
    if selection == "1":
      main()
    elif selection == "2":
      print("\nEnter a Topic ID to find out how many posts and followers it has\n")
      u_topic_id = input()
      cursor.execute(query_topic_details, (u_topic_id,u_topic_id))
      cursor2.execute(f"SELECT topic_name FROM Topics WHERE topic_id = {u_topic_id}")
      print("\n\n")
      for res in cursor2:
        print(f"The Topic - {res[0]}")
      for posts, followers in cursor:
        print(f"Posts: {posts}")
        print(f"Followers: {followers}")
      print()
      main_4()
    elif selection == "3":
      print("\nEnter a Group ID to find out how many posts and followers it has\n")
      u_group_id = input()
      cursor.execute(query_group_details, (u_group_id,u_group_id))
      cursor2.execute(f"SELECT group_name FROM Group_T WHERE group_id = {u_group_id}")
      print("\n\n")
      for res in cursor2:
        print(f"The group - {res[0]}")
      for posts, followers in cursor:
        print(f"Posts: {posts}")
        print(f"Followers: {followers}")
      print()
      main_4()

  def main():
    print(
      "---\n"
      "What would you like to do?\nEnter the number for the following actions:\n\n"
      "1.   Post Activities\n"                                                    # DONE
      "2.   List the names of Topics, Groups, People you follow\n"
      "3.   Add Topics, Groups, People to follow\n"
      "4.   Details of a Topic or Group\n"
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
      main_3()
    elif selection == "4":
      main_4()

  main()