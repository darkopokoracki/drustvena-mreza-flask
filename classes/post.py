from database import mydb

class Post:
    __id: int
    __title :str
    __content: str
    __image: str
    __userID: int

    def __init__(self, id: int, title: str, content: str, image: str, userID: int) -> None:
        self.__id = id
        self.__title = title
        self.__content = content
        self.__image = image
        self.__userID = userID

    # Geteri
    def get_id(self):
        return self.__id
    
    def get_title(self):
        return self.__title

    def get_content(self):
        return self.__content

    def get_image(self):
        return self.__image

    def get_userID(self):
        return self.__userID

    # Seteri
    def set_id(self, novi_id):
        self.__id = novi_id

    def set_title(self, novi_title):
        self.__title = novi_title

    def set_content(self, novi_content):
        self.__content = novi_content

    def set_image(self, nova_slika):
        self.__image = nova_slika

    def set_userID(self, novi_userID):
        self.__userID = novi_userID

    def __str__(self) -> str:
        res = f"Title: {self.__title}\n"

        return res

    def add_post(self):
        cursor = mydb.cursor(prepared = True)
        sql = 'INSERT INTO post VALUES(null, ?, ?, ?, ?)'
        values = (self.__title, self.__content, self.__image, self.__userID)
        cursor.execute(sql, values)
        
        mydb.commit()
    
        