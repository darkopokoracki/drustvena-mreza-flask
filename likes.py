import mysql.connector


mydb = mysql.connector.connect (
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'drustvena'
)

class Likes:
    __id: int
    __whomID: int
    __postID: int
    __whoID: int

    def __init__(self, id: int, whomID: int, postID: int, whoID: int) -> None:
        self.__id = id
        self.__whomID = whomID
        self.__postID = postID
        self.__whoID = whoID

    # Geteri
    def get_id(self):
        return self.__id

    def get_whomID(self):
        return self.__whomID

    def get_postID(self):
        return self.__postID

    def get_whoID(self):
        return self.__whoID

    # Seteri
    def set_id(self, novi_id):
        self.__id = novi_id

    def set_whomID(self, novi_whomID):
        self.__userID = novi_whomID

    def set_postID(self, novi_postID):
        self.__postID = novi_postID

    def set_whoID(self, novi_whoID):
        self.__whoID = novi_whoID

    def add_like(self):
        cursor = mydb.cursor(prepared = True)
        sql = "INSERT INTO likes VALUES(null, ?, ?, ?);"
        values = (self.__whomID, self.__postID, self.__whoID)
        cursor.execute(sql, values)

        mydb.commit()