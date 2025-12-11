from db import get_connection

def register():
    conn = get_connection()
    cursor = conn.cursor()

    username = input("Enter new username: ")
    password = input("Enter new password: ")

    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)",
                   (username, password))
    conn.commit()

    print("Registration successful!\n")


def login():
    conn = get_connection()
    cursor = conn.cursor()

    username = input("Enter username: ")
    password = input("Enter password: ")

    cursor.execute("SELECT id FROM users WHERE username=%s AND password=%s",
                   (username, password))
    result = cursor.fetchone()

    if result:
        print("\nLogin successful!")
        return result[0]
    else:
        print("Invalid credentials.\n")
        return None
