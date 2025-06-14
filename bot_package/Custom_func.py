import os
import asyncio
import json

#Get Yo-kai lists :
with open("./files/yokai_list.json") as yokai_list:
    yokai_data = json.load(yokai_list)
    list_len = {
        "E" : len(yokai_data["E"]["yokai_list"]),
        "D" : len(yokai_data["D"]["yokai_list"]),
        "C" : len(yokai_data["C"]["yokai_list"]),
        "B" : len(yokai_data["B"]["yokai_list"]),
        "A" : len(yokai_data["A"]["yokai_list"]),
        "S" : len(yokai_data["S"]["yokai_list"]),
        "LegendaryS" : len(yokai_data["LegendaryS"]["yokai_list"]),
        "treasureS" : len(yokai_data["treasureS"]["yokai_list"]),
        "DivinityS" : len(yokai_data["DivinityS"]["yokai_list"]),
        "SpecialS" : len(yokai_data["SpecialS"]["yokai_list"]),
        "Boss" : len(yokai_data["Boss"]["yokai_list"])
    }
#Make the class list and the proba    
class_list = ['E', 'D', 'C', 'B', 'A', 'S', 'LegendaryS', "treasureS", "SpecialS", 'DivinityS', "Boss"]
proba_list = [0.4175, 0.2, 0.12, 0.12, 0.08, 0.04, 0.0075, 0.0075, 0.0075, 0.005, 0.0025]


#Get the full list
with open("./files/full_name_fr.json") as yk_list_full:
    yokai_list_full = json.load(yk_list_full)


async def classid_to_class(id, reverse : bool = False):
        if reverse == False :
            return yokai_data[id]["class_name"]
        else :
            for classes in yokai_data :
                if yokai_data[classes]["class_name"] == id :
                    return classes
            
        #return nothing if the id or the name was not fund    
        return ""


    
#Get inv func
async def get_inv(id : int):
    if os.path.exists(f"./files/inventory/{str(id)}.json"):
        with open(f"./files/inventory/{str(id)}.json") as f:
            data = json.load(f)
    else :
        #retrun nothing if there's nothing to :/
        data = {}
       
    return data



#save inv func
async def save_inv(data : dict, id : int):
    with open(f"./files/inventory/{str(id)}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)