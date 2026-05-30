from gfield import Gfield
from code_place import CodePlace
from pg_item import PG_Item
from variable import PGSVariable

class Struct:
    def __init__(self) -> None:
        self.items_dict : dict[int, 
                               dict[str, PG_Item]
                               ] = {}
        # {
        #   1: {"type": "gfield", "data": Gfield},
        #   2: {"type": "code_place": "data", CodePlace}
        # }
        self.variables : dict[int, PGSVariable] = {}
        # {
        #   1: Variable(name="var1", type=IntVar, value=50)
        #   2: Variable(name="var2", type=FloatVar, value=4.0)
        # }
        self.project_name : str = ""
        self.project_desc : str = ""

    def set_struct_name(self, string : str) -> None:
        if string: self.project_name = string
        else: raise NameError("Error of naming project", "Project (struct) name of empty or None value.")

    def set_struct_desc(self, string : str) -> None:
        self.project_desc = string

    def add_gfield(self, id, gfield : Gfield) -> None:
        self.items_dict[id] = {"type": "gfield", "data": gfield}
    
    def add_code_place(self, id, code_place : CodePlace) -> None:
        self.items_dict[id] = {"type": "code_place", "data": code_place}
    
    def add_variable(self, id, variable : PGSVariable) -> None:
        self.variables[id] = variable

    def get_item(self, id) -> PG_Item:
        return self.items_dict[id]
    
    def get_items(self) -> dict[int, 
                               dict[str, PG_Item]
                               ]:
        return self.items_dict
    
    def get_variables(self) -> dict[int, PGSVariable]:
        return self.variables
    
    def get_variables_names_list(self) -> list[PGSVariable]:
        if not self.items_length(): 
            return
        
        result = []
        for variable in self.get_variables().values():
            result.append(variable.get_name())
        return result
    
    def get_variable(self, id) -> dict[int, PGSVariable]:
        return self.variables[id]
    
    def items_length(self) -> int:
        return len(self.items_dict)
    
    def sort_item_keys(self) -> None:
        sorted_keys = sorted(self.items_dict.keys())
        new_dict = {}
        new_id = 0

        for key in sorted_keys:
            item = self.items_dict[key]
            item["data"].id = new_id
            new_dict[new_id] = item
            new_id += 1

        self.items_dict = new_dict  

    def sort_variables_keys(self) -> None:
        sorted_keys = sorted(self.variables.keys())
        new_dict = {}
        new_id = 0

        for key in sorted_keys:
            item = self.variables[key]
            new_dict[new_id] = item
            new_id += 1

        self.variables = new_dict  

    def remove_item(self, id) -> None:
        if id in self.items_dict.keys():
            del self.items_dict[id]
        self.sort_item_keys()

    def remove_variable(self, id) -> None:
        if id in self.variables.keys():
            del self.variables[id]
        self.sort_variables_keys()

    def remove_all_variables(self) -> None:
        self.variables = {}
        
    def __repr__(self) -> str:
        return str(self.items_dict)
    