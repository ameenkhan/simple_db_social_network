import mysql.connector # activate venv
from mysql.connector import errorcode

PERSON_ID = ""
LOGIN_DATE = ""

query_login_auth = (
  "SELECT fname, lname, login_date FROM "
  "People NATURAL JOIN	Auth "
  "WHERE person_id=%s AND	pass=%s"
)

query_list_all_posts_lim_100 = (
  "SELECT DISTINCT(post_id), post_date, author, content, group_id from Posts WHERE "
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
  "SELECT DISTINCT(post_id), post_date, author, content, group_id from Posts WHERE "
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
  "SELECT DISTINCT(post_id), post_date, author, content, group_id from Posts WHERE author = %s ORDER BY(post_date) DESC;"
)

query_list_all_posts_unread = (
  "SELECT DISTINCT(post_id), post_date, author, content, group_id from Posts WHERE "
	"( "
	"	author IN (SELECT follows_id FROM followers_people WHERE person_id = %s) "
	"	OR "
	"	group_id IN (SELECT group_id FROM followers_groups WHERE person_id = %s) "
	"	OR "
	"	post_id IN (SELECT DISTINCT(post_id) from post_topics WHERE topic_id IN (SELECT topic_id FROM followers_topics WHERE person_id = %s)) "
	") "
	"AND "
	"post_date > (SELECT login_date FROM Auth WHERE person_id = %s) "
	"ORDER BY(post_date) DESC;"
)

query_list_groups_user_follows = (
  "SELECT group_name FROM Group_T WHERE group_id IN (SELECT group_id FROM followers_groups WHERE person_id = %s) OR group_id = 0;"
)

query_user_follows_group = (
  "SELECT gro
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

  cursor = cnx.cursor(buffered=True)
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
      for post_id, post_date, author, content, group_id in cursor:
        print(f"Post ID: {post_id}")
        print(f"Post Date: {post_date}")
        if group_id:
          print(f"Group ID: {group_id}")
        else:
          print("No group associated with this post")
        print(f"Author: {author}")
        print(str(content), "\n\n")

    elif selection == "3":
      cursor.execute(query_list_all_posts_no_lim, (PERSON_ID, PERSON_ID, PERSON_ID, PERSON_ID))
      print("Listing all posts you follow")
      for post_id, post_date, author, content, group_id in cursor:
        print(f"Post ID: {post_id}")
        print(f"Post Date: {post_date}")
        if group_id:
          print(f"Group ID: {group_id}")
        else:
          print("No group associated with this post")
        print(f"Author: {author}")
        print(str(content), "\n\n")
    
    elif selection == "4":
      cursor.execute(query_list_all_posts_your_posts, (PERSON_ID,))
      print("Listing all posts with a limit of 100 posts shown")
      for post_id, post_date, author, content, group_id  in cursor:
        print(f"Post ID: {post_id}")
        print(f"Post Date: {post_date}")
        if group_id != 0:
          print(f"Group ID: {group_id}")
        else:
          print("No group associated with this post")
        print(f"Author: {author}")
        print(str(content), "\n\n")
    
    main_1_2()

  def main_1():
    print(
      "---\n"
      "Post Activities\n"
      "1. Go Back\n"
      "2. List posts\n"
      "3. List unread posts\n"
      "4. Create a Post (to reply to a post you must first view it - option 5)\n"
      "5. View a specific post\n" #give the option to give a +/- 1 or reply here
    )
    
    selection = input()
    if selection == "1":
      main()

    elif selection == "2":
      main_1_2()
    
    elif selection == "3":
      cursor.execute(query_list_all_posts_unread, (PERSON_ID, PERSON_ID, PERSON_ID, PERSON_ID))
      print("Listing all unread posts (determined by login time)")
      for post_id, post_date, author, content, group_id in cursor:
        print(f"Post ID: {post_id}")
        print(f"Post Date: {post_date}")
        if group_id:
          print(f"Group ID: {group_id}")
        else:
          print("No group associated with this post")
        print(f"Author: {author}")
        print(str(content), "\n\n")
      main_1()

    elif selection == "4":
      print(
        "\nCreating a post\n"
        "What is the post content?\n"
      )
      cr_content = input()

      print(
        "\nThese are the groups you follow\n"
      )
      cursor.execute(query_list_groups_user_follows, (PERSON_ID,))

      for group_name in cursor:
        print(group_name[0])

      print("\n\nWhich group would you like to post in?\n")
      
      cr_group = input()
      cursor.execute(query_user_follows_group)

      main_1()


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
      "1.   Post Activities\n"
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