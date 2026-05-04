import os
import json
import bot_package.data as data
import bot_package.economy as eco
from difflib import SequenceMatcher
import aiofiles

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


async def classid_to_class(id:str, reverse : bool = False)->str:
    """Transform class_id to the coresponding class_name (can be reversed)

    Args:
        id (str): the id (or the name) of the class
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
        async with aiofiles.open(f"./files/inventory/{str(id)}.json") as f:
            content = await f.read()
            data = fix_encoding(json.loads(content))
    else :
        # Return nothing if there's nothing to :/
        data = {}
       
    return data



#save inv func
async def save_inv(data : dict, id : int):
    """
    A func to save the inv of a user (with his id)
    """
    async with aiofiles.open(f"./files/inventory/{str(id)}.json", "w", encoding="utf-8") as f:
        await f.write(json.dumps(data, indent=2, ensure_ascii=False))
        
        
        
        
#Get bag func
async def get_bag(id : int):
    """
    A func to get the bag of a user (with his id)
    """
    if os.path.exists(f"./files/bag/{str(id)}.json"):
        async with aiofiles.open(f"./files/bag/{str(id)}.json") as f:
            content = await f.read()
            data = fix_encoding(json.loads(content))
    else :
        #retrun nothing if there's nothing to :/
        data = {}
       
    return data



#save bag func
async def save_bag(data : dict, id : int):
    """
    A func to save the bag of a user (with his id)
    """
    async with aiofiles.open(f"./files/bag/{str(id)}.json", "w", encoding="utf-8") as f:
        await f.write(json.dumps(data, indent=2, ensure_ascii=False))
        
        
exlude_match= data.open_json("./files/exclude_match.json")["list"]
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


##########################
## Data management part ##
##########################

async def add(input_id : int, thing : str, rang : str, where:str, rank_orbe: bool = False, number : str = '1'):
    """A function that add things to a Medallium or a bag, works like the give command

    Args:
        input_id (int): The user's id
        thing (str): the thing
        rang (str): the thing class (the id format)
        where (str): where to add, bag/medallium
        rank_orbe (bool, optional): Whenever orbs will be gaved to. Defaults to False.
        number (str, optional): how many. Defaults to '1'.
    """
    
        
    #get the inv or the bag:
    if where == "bag":
        inv = await get_bag(input_id)
        default_inv = data.default_bag
        async def save_inv_t(data, id):
            await save_bag(data=data, id=id)
        
    elif where == "medallium":
        inv = await get_inv(input_id)
        default_inv = data.default_medallium
        async def save_inv_t(data, id):
            await save_inv(data=data, id=id)
        
    
    #format the number :
    try :
        number = int(number)
    except :
        pass
    
    
    
    
    if rang == "claim":
        #In case they are trying to give claims
        
        inv = await get_inv(input_id)
        
        if inv == {}:
            inv = data.default_medallium

        inv["claim"] = number
        await save_inv_t(inv, input_id)
        return 0
    
    
    
    #so, now that we know that the function is used to give a yokai/item, we have to: 
    # format the input:

    number = int(number)
    
    #Verify if the input id has an inventory file :
    if inv == {}:
        #set the inv to the default
        inv = default_inv
        
        inv[thing] = [rang]
        
        inv[rang] = 1
        if not number == 1 :
            inv[thing].append(int(number))
        await save_inv_t(data=inv, id=input_id)

    else :
        #we have to verify :
        # 1. If the yokai is already in the inv
        # 2. If yes, if there is already many oh this yokai
        # and we do it in range(number) to give several yokai
        for _ in range(number) :
            try:
                inv[thing]
                try:
                    #stack the yokai
                    inv[thing][1] += 1
                    # give orb if the argument is true
                    if rank_orbe:
                        eco.add_rank_orbe(input_id,rang)
                except Exception:
                    #catch an exception if the yokai was not stacked
                    #so we know there is only one and we can add the mention of two yokai ( .append(2) )
                    inv[thing].append(2)
            except KeyError:
                #return an exception if the yokai was not in the inv
                #add it
                inv[thing] = [rang]
                #add one more to the yokai count of the corresponding class
                try:
                    inv[rang] += 1
                except:
                    inv[rang] = 1
                    
            #save the inv
            await save_inv_t(data=inv, id=input_id)
        
            
async def remove(input_id:int, yokai : str, rang : str, where:str, number : int = 1): 
    """
    A function that removes things to a Medallium or a bag, works like the remove command

    Args:
        input_id (int): The user's id
        thing (str): the thing
        rang (str): the thing class (the id format)
        where (str): where to remove, bag/medallium
        number (str, optional): how many. Defaults to '1'.
    """

        #get the inv or the bag:
    if where == "bag":
        inv = await get_bag(input_id)
        async def save_inv_t(data, id):
            await save_bag(data=data, id=id)
        
    elif where == "medallium":
        inv = await get_inv(input_id)
        async def save_inv_t(data, id):
            await save_inv(data=data, id=id)

        

    #we have to verify :
    # 1. If the yokai is already in the inv
    # 2. If yes, if there is already many oh this yokai
    # and we do it in range(number) to delete several yokai
    
    for i in range(number) :
        try :
            one_more_author = inv[yokai][1] > 1
        
        
        except KeyError:
            return
        
        except IndexError :
            number = 1
            one_more_author = False
            
        if one_more_author == True :
            if number - i > inv[yokai][1] :
                return 0
                
                
            #just remove the mention of several yokai if there are juste two
            if inv[yokai][1] == 2:
                inv[yokai].remove(inv[yokai][1])
            else:
                inv[yokai][1] -= 1
                    
        else :
            inv.pop(yokai)
            inv[rang] -= 1
        await save_inv_t(data=inv, id=input_id)
        
