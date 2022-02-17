from database import mydb

class Comment:
    __id: int
    __content: str
    __postID: int
    __userID: int

    def __init__(self, id: int, content: str, postID: int, userID: int) -> None:
        self.__id = id
        self.__content = content
        self.__postID = postID
        self.__userID = userID

    # Geteri
    def get_id(self):
        return self.__id

    def get_content(self):
        return self.__content

    def get_postID(self):
        return self.__postID

    def get_userID(self):
        return self.__userID

    # Seteri
    def set_id(self, novi_id):
        self.__id = id

    def set_content(self, novi_content):
        self.__content = novi_content

    def set_postID(self, novi_postID):
        self.__postID = novi_postID

    def set_userID(self, novi_userID):
        self.__userID = novi_userID

    # ...