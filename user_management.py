import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table
import logging

# Configure logging
logging.basicConfig(
    filename='user_management.log', 
    level=logging.DEBUG, 
    format='%(asctime)s %(levelname)s: %(message)s'
)

# Database URI (ensure this is correct for your MySQL setup)
DATABASE_URI = 'mysql+pymysql://root:1234@localhost/product_recommendations'

# Create engine and metadata
engine = create_engine(DATABASE_URI)
meta = MetaData()

# Define users table (ensure it's already created in MySQL)
try:
    users_table = Table('users', meta, autoload_with=engine)
except Exception as e:
    logging.error(f"Error loading table schema: {e}")

def add_user(user_id, username, password):
    """Insert a new user into the database with correct values."""
    try:
        # Ensure the correct data is inserted into the database
        insert_stmt = users_table.insert().values(user_id=user_id, username=username, password=password)
        conn = engine.connect()
        trans = conn.begin()  # Start a transaction

        # Execute the insert statement
        conn.execute(insert_stmt)
        trans.commit()  # Commit the transaction to save changes

        logging.info(f"User '{username}' added successfully with user_id '{user_id}'.")
        print(f"User '{username}' added with user_id '{user_id}' and password '{password}'.")  # Debugging print
        return True

    except Exception as e:
        trans.rollback()  # Rollback in case of error
        logging.error(f"Error adding user '{username}': {e}")
        print(f"Error adding user '{username}': {e}")  # Debugging print
        return False

    finally:
        conn.close()

def validate_user_by_id(user_id):
    """Verify the user's existence using their user_id."""
    select_stmt = users_table.select().where(users_table.c.user_id == user_id)
    conn = engine.connect()

    try:
        # Fetch the result based on the user_id
        result = conn.execute(select_stmt).fetchone()

        if result:
            # User ID exists
            logging.info(f"Login successful for user_id: {user_id}")
            print(f"Login successful for user_id: {user_id}")
            return True
        else:
            logging.warning(f"User ID '{user_id}' not found during login attempt.")
            print("User ID not found.")
            return False

    except Exception as e:
        logging.error(f"Error verifying user with user_id '{user_id}': {e}")
        print(f"Error verifying user with user_id {user_id}: {e}")
        return False

    finally:
        conn.close()


def get_username_by_id(user_id):
    """Retrieve the username based on the user_id."""
    select_stmt = users_table.select().where(users_table.c.user_id == user_id)
    conn = engine.connect()

    try:
        # Fetch the result based on the user_id
        result = conn.execute(select_stmt).fetchone()

        if result:
            # Assuming the result tuple is (user_id, username, password), we need index 1 for username
            username = result[1]  # Correctly reference the username from the tuple
            logging.info(f"Username '{username}' retrieved for user_id '{user_id}'.")
            return username
        else:
            logging.warning(f"User ID '{user_id}' not found.")
            return None

    except Exception as e:
        logging.error(f"Error retrieving username for user_id '{user_id}': {e}")
        print(f"Error retrieving username for user_id '{user_id}': {e}")
        return None

    finally:
        conn.close()

def get_user_id_by_username(username):
    """Retrieve the user_id based on the username."""
    select_stmt = users_table.select().where(users_table.c.username == username)
    conn = engine.connect()

    try:
        # Fetch the result based on the username
        result = conn.execute(select_stmt).fetchone()

        if result:
            # Assuming the result tuple is (user_id, username, password), we need index 0 for user_id
            user_id = result[0]  # Correctly reference the user_id from the tuple
            logging.info(f"User ID '{user_id}' retrieved for username '{username}'.")
            return user_id
        else:
            logging.warning(f"Username '{username}' not found.")
            return None

    except Exception as e:
        logging.error(f"Error retrieving user ID for username '{username}': {e}")
        print(f"Error retrieving user ID for username '{username}': {e}")
        return None

    finally:
        conn.close()
 


def verify_user(username, password):
    """Verify the user's credentials."""
    select_stmt = users_table.select().where(users_table.c.username == username)
    conn = engine.connect()

    try:
        # Fetch the result based on the username
        result = conn.execute(select_stmt).fetchone()

        if result:
            # Assuming the result tuple is (user_id, username, password), we need index 2 for password
            stored_password = result[2]  # Correctly reference the password from the tuple

            # Compare the passwords after stripping any spaces
            if stored_password.strip() == password.strip():
                logging.info(f"Login successful for user: {username}")
                print(f"Login successful for user: {username}")
                return True
            else:
                logging.warning(f"Incorrect password for user: {username}")
                print("Incorrect password.")
                return False
        else:
            logging.warning(f"Username '{username}' not found during login attempt.")
            print("Username not found.")
            return False

    except Exception as e:
        logging.error(f"Error verifying user '{username}': {e}")
        print(f"Error verifying user {username}: {e}")
        return False

    finally:
        conn.close()


# Function to check if a username already exists
def user_exists(username):
    """Check if a username already exists in the database."""
    select_stmt = users_table.select().where(users_table.c.username == username)
    conn = engine.connect()
    
    try:
        result = conn.execute(select_stmt).fetchone()
        exists = result is not None
        logging.info(f"User exists: {exists} for username '{username}'")
        return exists
    except Exception as e:
        logging.error(f"Error checking if user '{username}' exists: {e}")
        print(f"Error checking if user '{username}' exists: {e}")
        return False
    finally:
        conn.close()


# Function to generate a new user_id starting from 5000
def generate_user_id():
    """Generate a new user_id, starting from 5000."""
    select_stmt = users_table.select().order_by(users_table.c.user_id.desc()).limit(1)
    conn = engine.connect()

    try:
        result = conn.execute(select_stmt).fetchone()
        if result:
            new_user_id = result[0] + 1  # Increment the highest user_id
        else:
            new_user_id = 5000  # Start from 5000 if no users exist

        logging.info(f"Generated new user_id: {new_user_id}")
        return new_user_id

    except Exception as e:
        logging.error(f"Error generating new user_id: {e}")
        print(f"Error generating new user_id: {e}")
        return None

    finally:
        conn.close()
