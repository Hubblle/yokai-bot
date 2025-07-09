import os
import asyncio
import json



# Function to open JSON data
def open_json(file_path: str):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# Function to save JSON data
def save_json(file_path: str, data: dict, ):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)




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
    
#get image and emoji list :
with open("./files/bot-data.json") as bot_data:
    bot_data = json.load(bot_data)
    image_link = {}
    for link in bot_data["image_link"]:
        image_link[link] = bot_data["image_link"][link]
        
    emoji = {}
    for emojis in bot_data["emoji"] :
        emoji[emojis] = bot_data["emoji"][emojis]
        
        
# Get configuration.json
with open("./configuration.json", "r") as config:
    config_data = json.load(config)
    team_member_id = config_data["team_members_id"]
    team_bypass_cooldown = config_data["team_bypass_cooldown"]
    
    
#Get all coin related stuff (a lot)
with open("./files/coin.json") as coin_brute :
    coin_data = json.load(coin_brute)
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