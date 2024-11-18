import json
import vars
from functions import available_functions


def check_design(design):
    # Check if design size is bigger than the board size
    if int(design['size']) > len(design['properties']) + len(design['functions']):
        raise ValueError("Design cannot be longer than the board size")
    # Check if any field is empty
    for item in ['properties', 'functions']:
        for row in design[item]:
            for k, v in row.items():
                if k == '' or v == '':
                    raise ValueError("There exist empty field in gameboard design.")
    # Check if locations are unique:
    locations = [row['location'] for row in design['properties']]
    if len(locations) - len(set(locations)) > 0:
        raise Exception("Duplicate locations detected.")
    # Check if Properties location are unique:
    properties_names = [row['name'] for row in design['properties']]
    if len(properties_names) - len(set(properties_names)) > 0:
        raise Exception("Duplicate property name detected.")


class Gameboard:

    def __init__(self):
        # self.__design = {}
        self.actual_layout = {}
        self.game_id = None
        self.go_location = None
        self.jail_location = None
        self.design_file_name = None

    def load_default_gameboard(self):

        default_design_path = vars.DEFAULT_GAMEBOARD_DESIGN_PATH
        default_design = {}
        if default_design_path.is_file():
            try:
                default_design = json.load(open(default_design_path, "r"))
                self.design_file_name = default_design_path.name
            except:
                default_design = {}

        check_design(default_design)
        # self.__design = default_design

        layout = {}
        for row in default_design['properties']:
            layout.update({
                int(row['location']): {
                    "name": row['name'],
                    "price": row['price'],
                    "rent": row['rent'],
                    "is_ownable": row['is_ownable'],
                    "ownership": None,
                    "owner_name": ''
                }
            })
        for row in default_design['functions']:

            if row['name'].lower() == 'go':
                self.go_location = int(row['location'])
            elif row['name'].lower() == 'just visiting / in jail':
                self.jail_location = int(row['location'])

            try:
                layout.update({
                    int(row['location']): {
                        "name": row['name'],
                        "function": available_functions[row['name']],
                        "is_ownable": row['is_ownable']
                    }
                })
            except KeyError:
                print('Function is not defined :', row['name'])
        self.actual_layout = {
            'size': default_design['size'],
            "layout": layout
        }

    def load_design(self, design_path):
        design = {}
        if design_path.is_file():
            try:
                design = json.load(open(design_path, "r"))
                self.design_file_name = design_path.name
            except:
                design = {}
        check_design(design)
        layout = {}
        for row in design['properties']:
            layout.update({
                int(row['location']): {
                    "name": row['name'],
                    "price": row['price'],
                    "rent": row['rent'],
                    "is_ownable": row['is_ownable'],
                    "ownership": None,
                    "owner_name": ''
                }
            })
        for row in design['functions']:

            if row['name'].lower() == 'go':
                self.go_location = int(row['location'])
            elif row['name'].lower() == 'just visiting / in jail':
                self.jail_location = int(row['location'])

            try:
                layout.update({
                    int(row['location']): {
                        "name": row['name'],
                        "function": available_functions[row['name']],
                        "is_ownable": row['is_ownable']
                    }
                })
            except KeyError:
                print('Function is not defined :', row['name'])
        self.actual_layout = {
            'size': design['size'],
            "layout": layout
        }

    # def make_new_gameboard(self):
    #     new_gameboard_design = {
    #         "size": 0,
    #         "properties": [],
    #         "functions": []
    #     }


