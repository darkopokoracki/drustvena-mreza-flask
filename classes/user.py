import mysql.connector 
from passlib.hash import sha256_crypt
from flask import session

mydb = mysql.connector.connect (
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'drustvena'
)

class User:
    __id: int
    __firstname: str
    __lastname: str
    __email: str
    __username: str
    __password: str
    __profile_image: str

    def __init__(self, id: int, firstname: str, lastname: str, email: str, username: str, password: str, profile_image: str) -> None:
        self.__id = id
        self.__firstname = firstname
        self.__lastname = lastname
        self.__email = email
        self.__username = username
        self.__password = password
        self.__profile_image = profile_image

    # Geteri
    def get_id(self):
        return self.__id

    def get_firstname(self):
        return self.__firstname

    def get_lastname(self):
        return self.__lastname

    def get_email(self):
        return self.__email

    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password

    def get_profile_image(self):
        return self.__profile_image

    # Seteri
    def set_id(self, novi_id):
        self.__id = novi_id

    def set_firstname(self, novi_firstname):
        self.__firstname = novi_firstname

    def set_lastname(self, novi_lastname):
        self.__lastname = novi_lastname

    def set_email(self, novi_email):
        self.__email = novi_email

    def set_username(self, novi_username):
        self.__username = novi_username

    def set_password(self, novi_password):
        self.__password = novi_password
    
    def set_profile_image(self, nova_profile_image):
        self.__profile_image = nova_profile_image

    
    def __str__(self) -> str:
        res = f"FirstName: {self.__firstname}\n"
        res += f"LastName: {self.__lastname}\n"
        res += f"Username: {self.__username}\n"

        return res

    def register(self):
        #Moramo da hasujemo password:
        self.__password = sha256_crypt.encrypt(self.__password)

        cursor = mydb.cursor(prepared = True)
        sql = 'INSERT INTO user VALUES(null, ?, ?, ?, ?, ?, ?)'
        values = (self.__firstname, self.__lastname, self.__email, self.__username, self.__password, self.__profile_image)
        cursor.execute(sql, values)

        mydb.commit()

    def login(self):
        session['username'] = self.__username
        session['firstname'] = self.__firstname
        session['lastname'] = self.__lastname
        session['id'] = self.__id
        session['picture'] = self.__profile_image

    def update(self):
        cursor = mydb.cursor(prepared = True)
        sql = 'UPDATE user SET firstName = ?, last_name = ?, username = ?, profile_image = ? WHERE uderID = ?'
        values = (self.__firstname, self.__lastname, self.__username, self.__profile_image, self.__id)
        cursor.execute(sql, values)

        mydb.commit()
        session['username'] = self.__username
        session['picture'] = self.__profile_image