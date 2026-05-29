class PGSVariable:
    def __init__(self, name : str, type, value) -> None:
        self.name = name
        self.type = type
        self.value = value
    
    def get_name(self) -> str:
        return self.name
    
    def get_type(self):
        return self.type

    def get_value(self):
        return self.value
    
    def __repr__(self):
        return f"Variable(name={self.name}, type={self.type}, value={self.value})"