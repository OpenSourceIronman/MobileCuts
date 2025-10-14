# External libraries
import sqlite3


def __init__(self):
    """ Initialize the database connection and cursor """
    self.conn = sqlite3.connect('MobileCuts.db')
    self.cursor = self.conn.cursor()
    self.c.execute(f'''CREATE TABLE IF NOT EXISTS BarberTable
                       (id INTEGER PRIMARY KEY AUTOINCREMENT, firstName TEXT, isActive INTEGER, range INTEGER, baseLatLocation FLOAT, baseLongLocation FLOAT)''')

def set_barber_active_flag(self, id: int, flagValue: bool) -> None:
    """ Save sim.batteryPackPercentageLog list to auto incrementing tables based on date and time in a SQlite database

    Args:
        sim (Simulation): The simulation object containing the battery pack percentage log.
    """
    self.cursor.execute(f"UPDATE BarberTable SET isActive = ? WHERE id = ?", (flagValue, id))

    self.conn.commit()
