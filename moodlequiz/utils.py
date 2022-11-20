


class CDATA:
    def __init__(self,text):
        self.text = text

    def __repr__(self):
        return f"<![CDATA[{self.text}]]>"