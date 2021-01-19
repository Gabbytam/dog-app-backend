#import * means import everything from peewee
from peewee import *

#property from python, import it to use it in class
import datetime

#connecting to the database
#we have access to PostgresqlDatabase from peewee
DATABASE = PostgresqlDatabase('dogs_app', host = 'localhost', port = 5432)

class Dog(Model):
    name = CharField()
    owner = CharField()
    breed = CharField()
    created_at = DateTimeField(default = datetime.datetime.now)

    # class Meta provides special construction instructions to a Python class object 
    class Meta:
        database = DATABASE

#connecting to database, creating tables (if it exists it will skip), then close 
def initialize():
    DATABASE.connect()
    #creates a table passing in the class Dog from above
    DATABASE.create_tables([Dog], safe=True)
    print("TABLES Created")
    DATABASE.close()