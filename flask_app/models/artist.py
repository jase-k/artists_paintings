from flask_app.config.mysqlconnection import MySQLConnection
from flask import flash
import bcrypt
import re

db = 'artists_schema'

class Artist():
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password'] #will come from the database hashed
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def registerArtist(cls, data):
        query = "INSERT INTO artists (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW())"

        #hash Password before adding to database: 
        data["password"] = cls.hashPW(data['password'])

        id = MySQLConnection(db).query_db(query, data)
        print("New artist created with the id : ", id)

        return id
    
    @staticmethod
    def hashPW(password):
        hashed = bcrypt.hashpw(bytes(password, "utf8"), bcrypt.gensalt(14))
        print(f'Password: {password}, hashed into: {hashed}')
        return hashed

    @staticmethod
    def validateRegistration(data):
        is_valid = True
        if len(data['first_name']) < 3:
            flash('First Name needs more than two characters', 'first_name')
            is_valid = False
        if len(data['last_name']) < 3:
            flash('Last name needs more than two characters', 'last_name')
            is_valid = False

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
        if( not EMAIL_REGEX.match(data['email'])):
            flash("Must enter valid email", 'email')
            is_valid = False
        
        #Validates Password:
        if(len(data['password']) < 8):
            flash("Password must be at least 8 characters", 'password')
            is_valid = False
        if(len(data['password']) > 25):
            flash("Password must be shorter than 26 characters", 'password')
            is_valid = False
            
        numberandchar = re.compile(r'^.*[0-9].*')
        if(not numberandchar.match(data['confirm_password'])):
            flash("Password must contain at least 1 number", 'password')
            is_valid = False
        

        return is_valid