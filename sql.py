import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

class DB:
    def __init__(self):  # Corrected __int__ to __init__
        try:
            self.conn = mysql.connector.connect(
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                database=os.getenv('DB_NAME')
            )
            self.mycursor = self.conn.cursor()
            print('Connection established')
        except mysql.connector.Error as err:  # More specific exception handling
            print(f'Connection error: {err}')

    def fetch_city_names(self):

        city = []
        self.mycursor.execute("""
        SELECT distinct(origin) FROM airways.flight_schedule
        union
        select distinct(destination) from airways.flight_schedule
        """)
        data = self.mycursor.fetchall()

        for item in data:
            city.append(item[0])

        return city

    def fetch_date(self):
        dates = []
        self.mycursor.execute("""WITH RECURSIVE DateRange AS (
        SELECT MIN(validFrom) AS date_value
        FROM airways.flight_schedule
        UNION ALL
        SELECT date_value + INTERVAL 1 DAY
        FROM DateRange
        WHERE date_value < (SELECT MAX(validTo) FROM airways.flight_schedule)
        )
        SELECT date_value
        FROM DateRange
        ORDER BY date_value;
        """)
        date = self.mycursor.fetchall()

        for item in date:
            dates.append(item[0])

        return dates

    def fetch_all_flights(self,Origin,Destination):

        self.mycursor.execute("""
        SELECT * FROM airways.flight_schedule
        where Origin = '{}' and Destination = '{}'
        """.format(Origin,Destination))


        data = self.mycursor.fetchall()
        return data

    def fetch_airline_frequency(self):

        airline = []
        count = []

        self.mycursor.execute("""SELECT airline,count(*) FROM airways.flight_schedule
        group by airline""")
        data = self.mycursor.fetchall()

        for item in data:
            airline.append(item[0])
            count.append(item[1])

        return airline,count

    def busy_airport(self):

        city = []
        frequency = []

        self.mycursor.execute("""
        select origin,count(*) from (SELECT origin FROM airways.flight_schedule
        union all
        SELECT origin FROM airways.flight_schedule) t
        group by t.origin  
        order by count(*) desc limit 5  
        """)

        data = self.mycursor.fetchall()

        for item in data:
            city.append(item[0])
            frequency.append(item[1])

        return city, frequency

    def daily_frequency(self):

        airline = []
        num_flights = []

        self.mycursor.execute("""
        SELECT airline, count(*) FROM airways.flight_schedule
        group by airline
        """)

        data = self.mycursor.fetchall()

        for item in data:
            airline.append(item[0])
            num_flights.append(item[1])

        return airline, num_flights