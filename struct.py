from gfield import Gfield

class Struct:
    def __init__(self):
        self.gfield_dict : dict[int, Gfield] = {}
    
    def add_gfield(self, id, gfield : Gfield):
        self.gfield_dict[id] = gfield
    
    def get_gfield(self, id):
        return self.gfield_dict[id]
    
    def get_dict(self):
        return self.gfield_dict 
    
    def gfields_count(self):
        return len(self.gfield_dict)
    
    def sort_gfield_keys(self):
        sorted_keys = sorted(self.gfield_dict.keys())
        new_dict = {}
        new_id = 0

        for key in sorted_keys:
            gfield = self.gfield_dict[key]
            gfield.id = new_id
            new_dict[new_id] = gfield
            new_id += 1

        self.gfield_dict = new_dict  
    
    def remove_gfield(self, id):
        if id in self.gfield_dict.keys():
            del self.gfield_dict[id]
        self.sort_gfield_keys()

    def __repr__(self):
        return str(self.gfield_dict)
    