class Node:
    def __init__(self, uid, header, code):
        self.uid = uid
        self.header = header
        self.code = code
        
    def __repr__(self):
        return f"Node(uid={self.uid}, header={self.header}, code={self.code})"
