import mysql.connector # activate venv
from mysql.connector import errorcode

PERSON_ID = ""
LOGIN_DATE = ""

query_login_auth = (
  "SELECT fname, lname, login_date FROM "
  "People NATURAL JOIN	Auth "
  "WHERE person_id=%s AND	pass=%s"
)

query_list_all_posts = (

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
      "1. List all posts with a limit on posts shown\n"
      "2. List all posts without a limit on posts shown\n"
      "3. List all of your posts\n"
    )
    

  def main_1():
    print(
      "---\n"
      "Post Activities\n"
      "1. Go Back\n"
      "2. List posts\n"
      "3. List unread posts\n"
      "4. Create a Post\n"
      "5. View a specific post\n"
    )
    
    selection = input()
    if selection == "1":
      main()
    if selection == "2":
      main_1_2()
    
    elif selection == "2":
      pass


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