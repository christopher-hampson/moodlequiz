


class CDATA(str):
    def __repr__(self):
        return f"CDATA({str(self)})"

    def tagged(self):
        return f"<![CDATA[{str(self)}]]>"