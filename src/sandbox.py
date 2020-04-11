# import mysql.connector # activate venv
# from mysql.connector import errorcode

# try:
#   cnx = mysql.connector.connect(user='user_ece356_test', password='user_ece356_test',
#                               host='192.168.56.101',
#                               database='SOCIAL_MEDIA')
# except mysql.connector.Error as err:
#   if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
#     print("Something is wrong with your user name or password")
#   elif err.errno == errorcode.ER_BAD_DB_ERROR:
#     print("Database does not exist")
#   else:
#     print(err)
# else:
#   print('We in!')
#   cursor = cnx.cursor(buffered=True)

#   query = (
#     "SELECT person_id, age, dob, gender FROM People"
#   )
#   cursor.execute(query)
#   for person_id, age, dob, gender in cursor:
#     print(person_id, age, dob, gender)

#   query = (
#     "SELECT gender FROM People"
#   )
#   cursor.execute(query)
#   for gender in cursor:
#     print(gender)

#   cnx.close()

#   # while True:
#   for i in range(3):
#     print(
#       "say"
#       "something"
#     )
#     selection = input()
#     print(
#       "you said",
#       selection
#     )
#   print(cursor.rowcount)

query_create_new_post = (
  "START TRANSACTION;\n"
  "INSERT INTO Posts (post_date, group_id, author, content) VALUES(CURDATE(),{0},{1},{2});\n"
  "SET @p_id = (SELECT LAST_INSERT_ID());\n"
)
print("\n\n\n")


query_create_new_post = query_create_new_post.format("1","2","3")

for i in range(3):
  query_create_new_post += "INSERT INTO post_topics (@p_id, i);\n"

query_create_new_post += "ROLLBACK;"

print(query_create_new_post)

print("\n\n\n")