import os
import json
import bot_package.data as data
from difflib import SequenceMatcher

"""
A module containing utility functions for the bot
This module provides functions for handling inventories, managing data encoding,
and performing smart string matching for Yo-kai names. It includes functionality for:
- Encoding fixes for French characters
- Loading and saving player inventories and bags
- Converting between class IDs and class names
- Smart string matching for Yo-kai names with special cases
Functions:

    fix_encoding(obj): Handles proper encoding of French characters in data structures
    classid_to_class(id, reverse): Converts between class IDs and class names
    get_inv(id): Retrieves a user's inventory
    save_inv(data, id): Saves a user's inventory
    get_bag(id): Retrieves a user's bag
    save_bag(data, id): Saves a user's bag
    smart_match(s1, s2): Performs intelligent string matching for Yo-kai names

Note:
    The encoding fix function is only active on Windows systems due to specific
    encoding requirements for French characters.
    
Every general func needed by the bot should be writen here.

"""


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


#Get the full list
with open("./files/full_name_fr.json") as yk_list_full:
    yokai_list_full = fix_encoding(json.load(yk_list_full))


asset_for_class_id_to_class = {
    "coin" : "pièce",
    "obj" : "objet",
    "treasure": "trésor"
}


async def classid_to_class(id, reverse : bool = False):
    """Transform class_id to the coresponding class_name (can be reversed)

    Args:
        id (_type_): _description_
        reverse (bool, optional): True: name to ID\nFlase: ID to name. Defaults to False.

    Returns:
        str: A classID or a classNAME coresponding to the name/id input
    """
    if reverse == False :
        try:
            return data.yokai_data[id]["class_name"]
        except KeyError:
            return asset_for_class_id_to_class[id]
        
    else :
        for classes in data.yokai_data :
            if data.yokai_data[classes]["class_name"] == id :
                return classes
            
        for item in asset_for_class_id_to_class :
            if asset_for_class_id_to_class[item] == id :
                return item
    #return nothing if the id or the name was not fund    
    return ""


    
#Get inv func
async def get_inv(id : int):
    """
    A func to get the inv of a user (with his id)
    """
    if os.path.exists(f"./files/inventory/{str(id)}.json"):
        with open(f"./files/inventory/{str(id)}.json") as f:
            data = fix_encoding(json.load(f))
    else :
        #retrun nothing if there's nothing to :/
        data = {}
       
    return data



#save inv func
async def save_inv(data : dict, id : int):
    """
    A func to save the inv of a user (with his id)
    """
    with open(f"./files/inventory/{str(id)}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
        
        
        
#Get bag func
async def get_bag(id : int):
    """
    A func to get the bag of a user (with his id)
    """
    if os.path.exists(f"./files/bag/{str(id)}.json"):
        with open(f"./files/bag/{str(id)}.json") as f:
            data = fix_encoding(json.load(f))
    else :
        #retrun nothing if there's nothing to :/
        data = {}
       
    return data



#save bag func
async def save_bag(data : dict, id : int):
    """
    A func to save the bag of a user (with his id)
    """
    with open(f"./files/bag/{str(id)}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
exlude_match=['Castelius I', 'Castelius III', 'Castelius II', 'Jibanyan', 'Jibanyan S', 'Robonyan', 'Oronyan', 'Komasan', 'Komajiro', 'Komasan S', 'Komajiro S', 'Corniot', 'Bicorniot', 'Sale de bain', 'Potache', 'Felipaix', 'Métaureaulog', 'M. Felipaix', 'Ornella', 'Sornella', 'Robonyan F', 'Ultramax N', 'Ultramax K', 'Oranyan', 'Gale de bain', 'Métaréaulog', 'Jibanyan B', 'Komasan B', 'Usapyon B', 'Jiganyan', 'Scientifiborg Y', 'Dépotache', 'Survolt', 'Supervolt', 'Usapyon', 'Oridjinn', 'Horridjinn', 'Superobonyan', 'Jibanyan T', 'Komasan T', 'Roi Jibanyan', 'Supernyan', 'Domniscian', 'Domniscian 2.0', 'Don Morleone', 'Don Dorleone', 'Robonyan 28', 'Usapyon T', 'Kuroi Jibanyan', 'ScientifiBot Y', 'UZApyon', 'Omai Tourbillonnant', 'Or Tourbillonnant']
async def smart_match(s1: str, s2: str) -> bool:
    """
    A func that return if s1 match s2
    Not only perfect match, usefull when we need the user to input a yokai.
    Some yokai can only match perfectly, cause they are to similar.
    """
    # Direct match
    if s1 == s2:
        return True
    
    # Remove spaces and make lowercase
    s1_clean = s1.lower().replace(' ', '')
    s2_clean = s2.lower().replace(' ', '')
    
    # Check for roman numerals vs numbers
    roman_map = {'i': '1', 'ii': '2', 'iii': '3', 'iv': '4', 'v': '5'}
    for roman, num in roman_map.items():
        s1_clean = s1_clean.replace(roman, num)
        s2_clean = s2_clean.replace(roman, num)
    
    # Exact match after cleaning
    if s1_clean == s2_clean:
        return True
    
    if s2 in exlude_match:
        return False
    
    # Sequence matcher for fuzzy matching
    ratio = SequenceMatcher(None, s1_clean, s2_clean).ratio()
    return ratio > 0.85  # Adjust threshold as needed

async def manage_cooldown(user_id: int, check_only: bool = False) -> bool:
    """Manage the cooldown list for goodbye message
    
    Args:
        user_id (int): The user to check/add
        check_only (bool, optional): Only check if user exists. Defaults to False.
    
    Returns:
        bool: True if user has seen message, False if not
    """
    try:
        with open("./files/cooldownlist.json", "r") as f:
            cooldown_list = json.load(f)
    except:
        cooldown_list = {}

    # Check if user exists
    if str(user_id) in cooldown_list:
        return True

    # If check_only, don't modify file
    if check_only:
        return False

    # Add user and save
    cooldown_list[str(user_id)] = True
    with open("./files/cooldownlist.json", "w") as f:
        json.dump(cooldown_list, f, indent=2)
    return False