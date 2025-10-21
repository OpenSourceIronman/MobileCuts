#!/usr/bin/env python3

# Standard Libraries
from datetime import datetime

# External Libraries
import sqlite3
from passlib.hash import argon2
import pytz 					                # World Timezone Definitions  https://pypi.org/project/pytz/

class Database:

    def __init__(self):
        """ Initialize the database connection, cursor, and create tables
        """
        self.conn = sqlite3.connect('MobileCuts.db')
        self.cursor = self.conn.cursor()

        self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS UserTable
                                (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL,
                                 role TEXT CHECK(role IN ('Barber', 'Customer')) NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

        self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS BarberTable
                                (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL,
                                 firstName TEXT, is_active INTEGER DEFAULT 1, range INTEGER, base_lat_location FLOAT, base_long_location FLOAT,
                                 FOREIGN KEY (user_id) REFERENCES UserTable(id) ON DELETE CASCADE)''')

        self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS CustomerTable
                                (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL,
                                 firstName TEXT, appointment_lat_location FLOAT, appointment_long_location FLOAT,
                                 FOREIGN KEY (user_id) REFERENCES UserTable(id) ON DELETE CASCADE)''')


    def register(self, firstName: str, email: str, password: str, roleType: str = 'Customer'):
        """ Register a new user with the given email, password, and role type.

        Args:
            firstName (str): The first name of the user.
            email (str): The email address of the user.
            password (str): The password of the user.
            roleType (str): The app role type of the user (default: 'Customer').
        """
        hash = argon2.hash(password)   # automatically generates salt and stores params in the hash string

        zulu = pytz.timezone('UTC') #pt = pytz.timezone('America/Los_Angeles')
        now = datetime.now(zulu).strftime('%Y-%m-%d-%H%M') + 'Z'
        self.cursor.execute("INSERT INTO UserTable (email, password_hash, role, created_at) VALUES (?, ?, ?, ?)", (email, hash, roleType, now))

        if roleType == 'Customer':
            self.cursor.execute("INSERT INTO CustomerTable (user_id, firstName) VALUES (?, ?)", (self.cursor.lastrowid, firstName))
        elif roleType == 'Barber':
            self.cursor.execute("INSERT INTO BarberTable (user_id, firstName) VALUES (?, ?)", (self.cursor.lastrowid, firstName))
        else:
            raise ValueError(f"Invalid role type: {roleType}")

        self.conn.commit()


    def login(self, email: str, password: str) -> tuple:
        """ Log in a user with the given email and password.

        Args:
            email (str): The email address of the user.
            password (str): The password of the user.

        Returns:
            tuple: A tuple containing a boolean indicating whether the login was successful and the user ID.
        """
        id = None
        row = self.cursor.execute("SELECT password_hash FROM UserTable WHERE email = ?", (email,)).fetchone()
        if not row:
            return (False, "Invalid email or password")

        storedHash = row[0]
        isValidLogin = argon2.verify(password, storedHash)
        if isValidLogin:
            row = self.cursor.execute("SELECT id FROM UserTable WHERE email = ?", (email,)).fetchone()
            id = row[0]

        return (isValidLogin, id)


    def update_customer_profile(self, userId: int, firstName: str, latLocation: float, longLocation: float):
        """ Update customer profile information in the database.

        Args:
            userId (int): The ID of the user.
            firstName (str): The first name of the user.
            latLocation (float): The latitude location for the appointment of the user.
            longLocation (float): The longitude location for the appointment of the user.
        """
        self.cursor.execute("UPDATE CustomerTable SET firstName = ?, appointment_lat_location = ?, appointment_long_location = ? WHERE user_id = ?",
                             (firstName, latLocation, longLocation, userId))
        self.conn.commit()


    def update_barber_profile(self, userId: int, firstName: str, isActive: bool, range: int, baseLatLocation: float, baseLongLocation: float):
        """ Update barber profile information in the database.

        Args:
            userId (int): The ID of the user.
            firstName (str): The first name of the user.
            isActive (bool): Whether the barber is active or not.
            range (int): The range the barber is willing to travel for appointments.
            baseLatLocation (float): The latitude location for the barber's base location.
            baseLongLocation (float): The longitude location for the barber's base location.
        """
        self.cursor.execute("UPDATE BarberTable SET firstName = ?, is_active = ?, range = ?, base_lat_location = ?, base_long_location = ? WHERE user_id = ?",
                             (firstName, int(isActive), range, baseLatLocation, baseLongLocation, userId))
        self.conn.commit()


    def set_barber_active_flag(self, id: int, flagValue: bool) -> None:
        """ Set the active flag for a barber.

        Args:
            id (int): The ID of the barber.
            flagValue (bool): The value to set the active flag to.
        """
        self.cursor.execute(f"UPDATE BarberTable SET is_active = ? WHERE id = ?", (flagValue, id))

        self.conn.commit()


if __name__ == "__main__":
    db = Database()
    #db.register("Blaze", "Blaze@example.com", "password", "Barber")
    #db.register("Blaze", "Blaze@gmail.com", "password", "Customer")
    loggedIn, id = db.login("Blaze@gmail.com", "password")
    print(id)
    #print(db.login("test@example.com", "wrongpassword"))
    db.update_barber_profile(id, "Blaze", False, 10, 37.7749, -122.4194)
    db.update_barber_profile(id, "Sharalyn", True, 69, 38.7749, -102.4194)
    db.set_barber_active_flag(id, False)
    db.update_customer_profile(id, "Sharalyn", 0.7749, -0.4194)
