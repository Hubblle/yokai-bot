import os
import asyncio
import json


"""
This module provide the data imported for various json in a python usable format.

Also some assets like default inv or bag.
"""



#func to fix a bug, on windows only ofc ;)
if os.name == "nt":  # Only execute on Windows
    def fix_encoding(obj):
        #the func that encode well everything; bcs we are french, we use é, à, è
            if isinstance(obj, dict):
                return {fix_encoding(k): fix_encoding(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [fix_encoding(item) for item in obj]
            elif isinstance(obj, str):
                try:
                    return obj.encode('latin-1').decode('utf-8')
                except UnicodeEncodeError:
                    return obj
                except UnicodeDecodeError:
                    return obj
            else:
                return obj

else:
    def fix_encoding(obj):            
        return obj

# Function to open JSON data
def open_json(file_path: str):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return fix_encoding(json.load(f))
    return {}

# Function to save JSON data
def save_json(file_path: str, data: dict, ):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)




#Get Yo-kai lists :
with open("./files/yokai_list.json") as yokai_list:
    yokai_data = fix_encoding(json.load(yokai_list))
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
        "Boss" : len(yokai_data["Boss"]["yokai_list"]),
        "Shiny" : len(yokai_data["Shiny"]["yokai_list"])
    }
#Make the class list and the proba    
class_list = ['E', 'D', 'C', 'B', 'A', 'S', 'LegendaryS', "treasureS", "SpecialS", 'DivinityS', "Boss", "Shiny"]
proba_list = [0.4165, 0.2, 0.12, 0.12, 0.08, 0.04, 0.0075, 0.0075, 0.0075, 0.005, 0.0025, 0.0010]
#                E     D     C     B     A     S      L       t       Sp      D       B      Sh


#Get the full list
"""with open("./files/full_name_fr.json") as yk_list_full:
    yokai_list_full = fix_encoding(json.load(yk_list_full))"""
    
#don't ask why
yokai_list_full = open_json("./files/full_name_fr.json")
    
#get image and emoji list :
with open("./files/bot-data.json") as bot_data:
    bot_data = fix_encoding(json.load(bot_data))
    image_link = {}
    for link in bot_data["image_link"]:
        image_link[link] = bot_data["image_link"][link]
        
    emoji = {}
    for emojis in bot_data["emoji"] :
        emoji[emojis] = bot_data["emoji"][emojis]
        
        
# Get configuration.json
with open("./configuration.json", "r") as config:
    config_data = fix_encoding(json.load(config))
    team_member_id = config_data["team_members_id"]
    team_bypass_cooldown = config_data["team_bypass_cooldown"]
    
    
#Get all coin related stuff (a lot)
with open("./files/coin.json") as coin_brute :
    coin_data = fix_encoding(json.load(coin_brute))
    coin_list = []
    coin_proba = []
    
    for coin in coin_data :
        #get the name of the coin, and his proba, and put it into tow seperate list in the same order
        coin_list.append(coin)
        coin_proba.append(coin_data[coin]["proba"])

coin_loot = {}
for dirpath, dirnames, filenames in os.walk("./files/coin"):
    for file in filenames:
        coin_loot_brute = open_json(f"./files/coin/{file}")
        coin_loot[file.removesuffix(".json")] = {
                "list" : coin_loot_brute["list"]
            }
        
        proba_in_order = []
        element_in_order = []
        
        for element in coin_loot[file.removesuffix(".json")]["list"] :
            #add the element to the list at the same place than his proba
            element_in_order.append(element)
            
            proba_in_order.append(coin_loot[file.removesuffix(".json")]["list"][element][1])
        
        coin_loot[file.removesuffix(".json")]["proba_in_order"] = proba_in_order
        coin_loot[file.removesuffix(".json")]["element_in_order"] = element_in_order
        
#items info :
item = open_json("./files/items.json")

#tag info
TAGS_DATA = open_json("./files/tags.json")

#money info
MONEY_DATA = open_json("./files/monnaie.json")

#blacklist info for normal bkai
with open_json("./files/blacklisted-yokai.json") as f:
    blacklist = list(f.blacklist)

default_medaillum  = {
                        "last_claim" : 10000,
                        "E" : 0,
                        "D" : 0,
                        "C" : 0,
                        "B" : 0,
                        "A" : 0,
                        "S" : 0,
                        "LegendaryS" : 0,
                        "treasureS" : 0,
                        "SpecialS" : 0,
                        "DivinityS" : 0,
                        "Boss" : 0,
                        "Shiny" : 0
                    }

default_bag = {
                    "coin" : 0,
                    "obj" : 0,
                    "treasure" : 0,
                }


#The class to point dict

class_to_point = {
    "E" : 1,
    "D" : 2,
    "C" : 4,
    "B" : 4,
    "A" : 8,
    "S" : 16,
    "LegendaryS" : 24,
    "treasureS" : 24,
    "SpecialS" : 24,
    "DivinityS" : 32,
    "Boss" : 64,
    "Shiny" : 82,
}
