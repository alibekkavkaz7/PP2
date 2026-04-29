import psycopg2
from config import DB
#
def connect():
    return psycopg2.connect(
        host=DB["host"],
        database=DB["database"],
        user=DB["user"],
        password=DB["password"]
    )