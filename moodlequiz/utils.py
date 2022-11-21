


class CDATA(str):
    def __init__(self,text):
        self.__text__ = text

    def __repr__(self):
        return f"CDATA({self.__text__})"

    def __str__(self):
        return f"<![CDATA[{self.__text__}]]>"

    def __len__(self):
        return len(self.__text__)