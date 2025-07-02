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
  