# Social Media Project

This project was made using Python3 and MySQL. The MySQL-Python connector was used to establish a connection between the DB server and the application logic - written in pure python3.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the MySQL connector.

```bash
pip install mysql-connector-python
```

## Setting up your environment

1. Ensure that the `mysql-connector-python` is installed correctly
2. Run the `src/load_db.sql` file on a MySQL server
    1. Copy the `.csv` files from the `/data` directory into the DB server's `/var/lib/mysql-files/project` directory or change the load script appropriately
3. `main.py` attempts to establish a connection with the DB server using the following credentials. Change them as required.
```python
cnx = mysql.connector.connect(user='user_ece356_test', password='user_ece356_test',
                              host='192.168.56.101',
                              database='SOCIAL_MEDIA')
```
4. The application is run in the cli by starting the `main.py` script.

```bash
python3 src/main.py
```

## Demo
A demo recording of the application is also available `demo.mp4`