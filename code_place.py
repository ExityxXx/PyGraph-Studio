from pg_item import PG_Item

class CodePlace(PG_Item):
    def __init__(self, id, name, code):
        super().__init__(id, name)
        self.code = code

    def get_code(self):
        return self.code

    def __repr__(self):
        return f"CodePlace(id={self.id}, name={self.name}, code={self.code})"
    