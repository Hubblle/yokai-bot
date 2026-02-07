import json
import time
import os
import aiohttp
import asyncio
VERSION = 3



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





def line(num : int = 1):
    for i in range(num):
        print(" ")
        
# async func to check images
async def check_image(session, yokai_name, yokai_data):
    """Check if image exists for given Yo-kai."""
    if not yokai_data.get('id'):
        return yokai_name, None
        
    
    asyncio.sleep(0.2)
    url = f"https://api.quark-dev.com/yk/img/{yokai_data['id']}.png"
    try:
        async with session.get(url) as response:
            if response.status == 404:
                print(f"❌ Image not found for {yokai_name} (ID: {yokai_data['id']})")
                return yokai_name, None
            else:
                print(f"✓ Valid image for {yokai_name}")
                return yokai_name, yokai_data['id']
    except Exception as e:
        print(f"Error checking {yokai_name}: {e}")
        return yokai_name, None


        
#Get inv func
def get_inv(id : str):
    if os.path.exists(f"./files/inventory/{id}.json"):
        with open(f"./files/inventory/{id}.json") as f:
            data = json.load(f)
    else :
        #retrun nothing if there's nothing to :/
        data = {}
       
    return data

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

#save inv func
def save_inv(data : dict, id : str):
    with open(f"./files/inventory/{id}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def classid_to_class(id, reverse : bool = False):
    if reverse == False :
        return yokai_data[id]["class_name"]
    else :
        for classes in yokai_data :
            if yokai_data[classes]["class_name"] == id :
                return classes
        
    #return nothing if the id or the name was not fund    
    return ""


#Get bag func
 
def get_bag(id : int):
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
def save_bag(data : dict, id : int):
    """
    A func to save the bag of a user (with his id)
    """
    with open(f"./files/bag/{str(id)}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


#Get Yo-kai lists :
with open("./files/yokai_list.json") as yokai_list:
    yokai_data : dict = json.load(yokai_list)
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

        
        
def adjust():
    line(35)
    print("Welcome to the adjust software !")
    while True :
        print("Please, select a mode :")
        print("   [1] Total number of yokai. \n   [2] Total in the bag. \n")
        line()
        choice = input("Please, select a number [1-2] ")
    
        if choice == "1" or choice == "2":
            choice = int(choice)
            break
    
        print("The number isn't right, please enter a number in range [1-2]")
        input("Press any key to go back to the menu.")
    
    
    if choice == 1:
        corrected_classes = 0
        
        for dirpath, dirnames, filenames in os.walk("./files/inventory"):
            for file in filenames :
                yokai_per_class = {
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
                    "Shiny": 0
                }
                current_inv = get_inv(file.strip(".json"))
                if current_inv != {} :
                    for yokai in current_inv :
                        #check if the yokai is part of the inv system
                        if yokai in ["E", "D", "C", "B", "A", "S", "LegendaryS", "treasureS", "SpecialS", "DivinityS", "Boss", "last_claim", "", "claim", "Shiny"] :
                            pass
                        
                        else :
                            yokai_class = current_inv[yokai][0]
                            yokai_per_class[yokai_class] += 1
                    
                    for classes in yokai_per_class :
                        if yokai_per_class[classes] != current_inv[classes]:
                            current_inv[classes] = yokai_per_class[classes]
                            corrected_classes += 1
                        
                    save_inv(current_inv, file.strip(".json"))
        print("The inventories were adjusted successfully !")
        print(f"{corrected_classes} total were adjusted")
                    
    if choice == 2:
        corrected_classes = 0
        
        for dirpath, dirnames, filenames in os.walk("./files/bag"):
            for file in filenames :
                things_per_class = {
                    "coin":0,
                    "obj": 0,
                    "treasure": 0
                }
                
                current_bag = get_bag(file.strip(".json"))
                if current_bag != {} :
                    for things in current_bag :
                        #check if the object is part of the inv system
                        if type(current_bag[things]) != list :
                            pass
                        
                        else :
                            things_class = current_bag[things][0]
                            things_per_class[things_class] += 1
                    
                    for classes in things_per_class :
                        if things_per_class[classes] != current_bag[classes]:
                            current_bag[classes] = things_per_class[classes]
                            corrected_classes += 1
                        
                    save_bag(current_bag, file.strip(".json"))
        print("The bags were adjusted successfully !")
        print(f"{corrected_classes} total were adjusted")
            
            
                    
            
                                        
        
    line()
    input("Press any key to go back to the main menu.")
    return
         
         
         
def match_adjust():
    line(35)
    exclude = []
    
    from difflib import SequenceMatcher
    def match(s1, s2):
        if s2 in exclude:
            return False

        # Remove spaces and make lowercase
        s1_clean = s1.lower().replace(' ', '')
        s2_clean = s2.lower().replace(' ', '')
        
        # Check for roman numerals vs numbers
        roman_map = {'i': '1', 'ii': '2', 'iii': '3', 'iv': '4', 'v': '5'}
        for roman, num in roman_map.items():
            s1_clean = s1_clean.replace(roman, num)
            s2_clean = s2_clean.replace(roman, num)
        
        
        # Sequence matcher for fuzzy matching
        ratio = SequenceMatcher(None, s1_clean, s2_clean).ratio()
        return ratio > 0.85  # Adjust threshold as needed
    
    
    full_name_fr : dict = open_json("./files/full_name_fr.json")
    
    #get all the yokais
    full_list = list(full_name_fr.keys())
    
    
    for yokai in full_list:
        for yokai_compare in full_list:
            if yokai != yokai_compare:
                if match(yokai, yokai_compare):
                    exclude.append(yokai_compare)
                    print(f" Match found ! {yokai} >> {yokai_compare}")
        
    print("Total yokai excluded: "+str(len(exclude)))
    save_json("./files/exclude_match.json", {"list":exclude})
    line()
    input("Press any key to go back to the main menu.")
    return


def inv_info():
    line(35)
    print("Welcome in the inv info program !")
    while True :
        print("Please, select a mode :")
        print("   [1] Simple mode. \n   [2] Advenced mode.")
        line()
        choise = input("Please, select a number [1-2] ")
    
        if choise == "1" or choise == "2" :
            choise = int(choise)
            break
        
        print("The number isn't right, please enter a number in range [1-2]")
        input("Press any key to go back to the menu.")
    
    #if they chose the simple mode
    if choise == 1 :
        line(35)
        total_user = 0
        total_size = 0
        for dirpath, dirnames, filenames in os.walk("./files/inventory"):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                # skip if it is symbolic link
                if not os.path.islink(fp):
                    total_user += 1
                    total_size += os.path.getsize(fp)
        print("General info :")
        print(f"    Number of inventory file : {total_user} \n    Size of ./files/inventory : {total_size/1000000}MB")
        
    #if they chose the advenced mode
    if choise == 2 :
         #first, get the basic info
        line(35)
        total_user = 0
        total_size = 0
        for dirpath, dirnames, filenames in os.walk("./files/inventory"):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                # skip if it is symbolic link
                if not os.path.islink(fp):
                    total_user += 1
                    total_size += os.path.getsize(fp)
        print("General info :")
        print(f"    Number of inventory file : {total_user} \n    Size of ./files/inventory : {total_size/1000000}MB")
        line()
        
        #get the number of yokai per class
        yokai_per_class = {
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
            "Shiny": 0
        }
        
        yokai_per_class_total = {
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
            "Shiny": 0
        }
        
        for dirpath, dirnames, filenames in os.walk("./files/inventory"):
            for file in filenames :
                current_inv = get_inv(file.strip(".json"))
                for yokai in current_inv :
                    #check if the yokai is part of the inv system
                    if yokai in ["E", "D", "C", "B", "A", "S", "LegendaryS", "treasureS", "SpecialS", "DivinityS", "Boss","Shiny", "last_claim", "", "claim"] :
                        pass
                    
                    elif not type(current_inv[yokai]) == list:
                        pass
                    
                    else :
                        yokai_class = current_inv[yokai][0]
                        
                        #else, add his rank to the total
                        try :
                            for i in range(current_inv[yokai][1]) :
                                yokai_per_class_total[yokai_class] += 1
                        except :
                            yokai_per_class_total[yokai_class] += 1
                        yokai_per_class[yokai_class] += 1
                
        print("Specific infos :")
        print("    Yokai per class :")
        
        for classes in yokai_per_class:
            print(f"    - {classid_to_class(classes)} : {yokai_per_class[classes]}")
            
        line()
        print("    Yokai per class in total :")
        for classes in yokai_per_class_total:
            print(f"    - {classid_to_class(classes)} : {yokai_per_class_total[classes]}")
    
        
    line()
    input("End of the program, press any key to go back to the main menu.")





def key_manager():
    line(35)
    print("key manager")
    while True :
        print("Please, select a mode :")
        print("   [1] Delete a yokai. \n   [2] Replace a yokai.")
        line()
        choise = input("Please, select a number [1-2] ")
    
        if choise == "1" or choise == "2" :
            choise = int(choise)
            break
        
        print("The number isn't right, please enter a number in range [1-2]")
        input("Press any key to go back to the menu.")
        line(35)
    
    if choise == 1:
        line()
        number = 0
        chosen_yokai = input("Please, select the Yokai : ")
        chosen_class = input("Please choose the rank of the yokai : ")
        for dirpath, dirnames, filenames in os.walk("./files/inventory"):
            for file in filenames :
                id = file.strip(".json")
                current_inv = get_inv(id)
                new_inv = get_inv(id)
                for yokai in current_inv :
                    try :
                        if yokai == chosen_yokai and current_inv[yokai][0] == chosen_class :
                            new_inv.pop(yokai)
                            print(f"The yokai {yokai} was removed for the inv of {id} !")
                            number += 1
                    except :
                        pass
                save_inv(new_inv, file.strip(".json"))
                print(f"{number} {chosen_yokai} were removed from the inv.")
        
    
    if choise == 2:
        line()
        chosen_yokai = input("Please, select the Yokai : ")
        chosen_class = input("Please choose the rank for the Yokai : ")
        print(f"Yokai choosen -> {chosen_yokai} // class -> {chosen_class}")
        line()
        replacement_yokai = input("Please, choose the replacement Yokai : ")
        replacement_class = input("Please, choose the replacement class : ")
        
        number = 0
        for dirpath, dirnames, filenames in os.walk("./files/inventory"):
            for file in filenames :
                id = file.strip(".json")
                current_inv = get_inv(id)
                new_inv = get_inv(id)
                for yokai in current_inv :
                    try :
                        if yokai == chosen_yokai and current_inv[yokai][0] == chosen_class :
                            #remove the old yokai
                            new_inv.pop(yokai)
                            number += 1
                            
                            
                            #add the replacement yokai
                            try:
                                new_inv[replacement_yokai] = [replacement_class, current_inv[yokai][1]]
                            except IndexError:  
                                new_inv[replacement_yokai] = [replacement_class]
                            
                            
                            print(f"The yokai {yokai} was removed for the inv of {id} !")
                    except :
                        pass
                
                print(f"{number} {chosen_yokai} were replaced by {replacement_yokai}")
                save_inv(new_inv, file.strip(".json"))
    
    
    line()
    input("End of the program, press any key to go back to the main menu.")
    


def organise_list():
    line(35)
    print("Welcome to the list management program !")
    while True :
        print("Please, select a mode :")
        print("   [1] Sort the list (alphabetically). \n   [2] Check for double yokais.")
        line()
        choise = input("Please, select a number [1-2] ")
    
        if choise == "1" or choise == "2" or choise == "2":
            choise = int(choise)
            break
    
        print("The number isn't right, please enter a number in range [1-2]")
        input("Press any key to go back to the menu.")
        
        
    if choise == 1:
        yokai_list = open_json("./files/yokai_list.json")
        
        for classes in yokai_list:
            yokais = yokai_list[classes]["yokai_list"]
            yokais.sort()
            yokai_list[classes]["yokai_list"] = yokais
            
        save_json("./files/yokai_list.json", yokai_list)
        print("The json was sorted sucessfully !")
        
        
        
    elif choise == 2:
        yokai_list = open_json("./files/yokai_list.json")
        all_yokai = {}
        for classes in yokai_list:
            for yokai in yokai_list[classes]["yokai_list"]:
                try :
                    all_yokai[yokai].append(classes)
                except:
                    all_yokai[yokai] = [classes]
        
        double_yokai = ""
        for yokai in all_yokai:
            
            if len(all_yokai[yokai]) > 1:
                double_yokai_current = f"\n {yokai} : "
                for classes in all_yokai[yokai]:
                    double_yokai_current += f"{classid_to_class(classes)}/ "
                double_yokai += double_yokai_current
        
        print("Here are the double yokai :")
        print(double_yokai)
    
    line()
    input("Press enter to go back to the main menu.")

    
    
    
    
    
def check():
    line(35)
    print("Checks")
    while True :
        print("Please, select a mode :")
        print("   [1] Check coin files. \n   [2] Check yokai ids (images). \n   [3] Check tags.")
        line()
        choise = input("Please, select a number [1-3] ")
    
        if choise == "1" or choise == "2" or choise == "3" :
            choise = int(choise)
            break
        
        print("The number isn't right, please enter a number in range [1-3]")
        input("Press any key to go back to the menu.")
        line(35)
    
    if choise == 1:
        coin_list = open_json("./files/coin.json").keys()
        coin_output_total = ""
        for coin in coin_list:
            coin_output = f"\n  {coin}: "
            coin_file = open_json(f"./files/coin/{coin}.json")
            if coin_file == {}:
                coin_output += "❌ No/empty file"
                
            else:
                try:
                    item_number = len(coin_file["list"].keys())
                    proba_total = 0
                    for loots in coin_file["list"]:
                        proba_total += coin_file["list"][loots][1]
                    proba_total = round(proba_total, 4)
                    if proba_total == 1:
                        coin_output += "total proba ✅ // "
                    else:
                        coin_output += f"total proba adjusted ↗️ ({proba_total})// "
                        for loots in coin_file["list"]:
                            coin_file["list"][loots][1] = round(coin_file["list"][loots][1]/proba_total, 6)
                        save_json(f"./files/coin/{coin}.json", coin_file)
                        
                    coin_output += f"total items: {item_number}"

                    all_items = open_json("./files/items.json").keys()
                    all_yokai = open_json("./files/full_name_fr.json").keys()
                    
                    for item in coin_file["list"]:
                        if coin_file["list"][item][0] in ["obj", "treasure"]:
                            if item not in all_items:
                                coin_output += f"\n    - {item} ❌ Not found in items"
                        elif coin_file["list"][item][0] == "yokai":
                            if item not in all_yokai:
                                coin_output += f"\n    - {item} ❌ Not found in yokais"
                        else:
                            coin_output += f"\n    - {item} ❌ Has a wrong type ! ()"
                
                except Exception as e:
                    coin_output += f"📛 Error during file reading ! >>> {e}"
            coin_output_total+=coin_output
        print(coin_output_total)
        
    if choise == 2:
        async def check_id():
            # Load the JSON file
            with open("./files/full_name_fr.json", "r", encoding="utf-8") as f:
                yokai_data = json.load(f)
            
            async with aiohttp.ClientSession() as session:
                tasks = []
                for yokai_name, data in yokai_data.items():
                    tasks.append(check_image(session, yokai_name, data))
                
                results = await asyncio.gather(*tasks)
                
                # Count valid IDs
                valid_count = 0
                total_count = len(results)
                
                # Update IDs based on results
                for yokai_name, new_id in results:
                    if new_id is not None:
                        valid_count += 1
                    elif new_id is None:
                        yokai_data[yokai_name]['id'] = None
        
    
            # Save updated data
            with open("./files/full_name_fr.json", "w", encoding="utf-8") as f:
                json.dump(yokai_data, f, indent=2, ensure_ascii=False)
            
            # Print statistics
            print(f"\n=== Results ===")
            print(f"Total Yo-kai: {total_count}")
            print(f"Valid IDs: {valid_count}")
            print(f"Invalid/Missing IDs: {total_count - valid_count}")
            print(f"Success rate: {(valid_count/total_count)*100:.1f}%")
                
            
        asyncio.run(check_id())
    
    if choise == 3:
        tag_list = open_json("./files/tags.json")
        tag_output_total = ""
        for tag in tag_list:
            tag_output = f"\n  {tag}: "

            try:
                item_number = len(tag_list[tag]["list"])

                all_items = open_json("./files/items.json").keys()
                all_yokai = open_json("./files/full_name_fr.json").keys()
                
                all_all = list(all_yokai)+list(all_items)
                
                for item in tag_list[tag]["list"]:
                    if item not in all_all:
                        tag_output += f"\n    - {item} ❌ Not found"
                
            except Exception as e:
                tag_output += f"📛 Error during file reading ! >>> {e}"
            tag_output_total+=tag_output
        print(tag_output_total)
        
    line()
    input("End of the program, press any key to go back to the main menu.")

def adjust_id():
    line(35)
    full_name_fr = open_json("./files/full_name_fr.json")
    full_list_raw = open_json("./files/yokai_list.json")
    full_list = []
    
    for cat in full_list_raw:
        full_list += full_list_raw[cat]["yokai_list"]
            

    actual_list = []

    count1 = 0


    for key in full_name_fr :
        actual_list.append(key)
        count1 += 1

    print(f"{count1} Yo-kai translated in English")

    count2 = 0
    for yokai in full_list :
        if not yokai in actual_list :
            full_name_fr[yokai] = {
                "name_en" : None,
                "id" : None
            }
            count2 += 1
            
    print(f"{count2} Yo-kai added to the list")
    print(f"total = {count1 + count2}")

    save_json("./files/full_name_fr.json", full_name_fr)
    
    line()
    input("End of the program, press any key to go back to the main menu.")
        

def avent_manager():
    line(35)
    print("Welcome to the avent calendar manager !")
    while True :
        print("Please, select a mode :")
        print("   [1] View advent statistics. \n   [2] Check advent data. \n   [3] Edit a day. \n   [4] Go back.")
        line()
        choise = input("Please, select a number [1-4] ")
    
        if choise in ["1", "2", "3", "4"]:
            choise = int(choise)
            break
        
        print("The number isn't right, please enter a number in range [1-4]")
        input("Press any key to go back to the menu.")
        line(35)
    
    avent_data = open_json("./files/avent.json")
    
    if choise == 1:
        # View statistics
        line()
        print("=== Avent Calendar Statistics ===")
        total_days = len([k for k in avent_data.keys() if k.isdigit()])
        print(f"Total days configured: {total_days}")
        line()
        
        print("Rewards claimed per day:")
        user_day = avent_data.get("user_day", {})
        for day in range(1, total_days + 1):
            claims = user_day.get(str(day), 0)
            gift = avent_data.get(str(day))
            if gift:
                gift_name = gift[0]
                print(f"  Day {day:2d}: {claims:3d} claims - {gift_name}")
            else:
                print(f"  Day {day:2d}: ❌ No data")
        
        line()
        print(f"Total claims across all days: {sum(user_day.values())}")
    
    elif choise == 2:
        # Check advent data with yokai/item/coin validation
        line()
        print("=== Checking Avent Data ===")
        errors = 0
        
        # Load reference data
        yokai_list_raw = open_json("./files/yokai_list.json")
        items = open_json("./files/items.json")
        coins = open_json("./files/coin.json")
        
        # Build complete yokai list
        all_yokai = []
        for cat in yokai_list_raw:
            all_yokai.extend(yokai_list_raw[cat]["yokai_list"])
        
        # Check days 1-24
        for day in range(1, 25):
            gift = avent_data.get(str(day))
            if not gift:
                print(f"❌ Day {day}: Missing data")
                errors += 1
                continue
            
            # Validate structure: [name, rang, where, amount]
            if len(gift) < 3:
                print(f"❌ Day {day}: Incomplete data (need at least 3 fields)")
                errors += 1
                continue
            
            name, rang, where = gift[0], gift[1], gift[2]
            amount = gift[3] if len(gift) > 3 else 1
            
            # Validate where
            if where not in ["medallium", "bag"]:
                print(f"❌ Day {day}: Invalid 'where' value: {where}")
                errors += 1
                continue
            
            # Validate rang
            valid_ranks = ["Shiny", "Boss", "Divinité / Enma", "Légendaire", "Spécial", "S", "A", "B", "C", "D", "E", "objet", "pièce", "claim", "trésor", "Trésor"]
            if rang not in valid_ranks:
                print(f"❌ Day {day}: Invalid rank: {rang}")
                errors += 1
            
            # Validate amount
            if not isinstance(amount, int) or amount <= 0:
                print(f"❌ Day {day}: Invalid amount: {amount}")
                errors += 1
            
            # Validate existence based on where and rang
            if where == "medallium":
                if rang == "claim":
                    # Claims don't need validation
                    pass
                elif name not in all_yokai:
                    print(f"❌ Day {day}: Yokai '{name}' not found in yokai_list.json")
                    errors += 1
                else:
                    print(f"✓ Day {day}: Yokai '{name}' found")
            
            elif where == "bag":
                if rang == "pièce":
                    if name not in coins:
                        print(f"❌ Day {day}: Coin '{name}' not found in coin.json")
                        errors += 1
                    else:
                        print(f"✓ Day {day}: Coin '{name}' found")
                elif rang == "objet":
                    if name not in items:
                        print(f"❌ Day {day}: Item '{name}' not found in items.json")
                        errors += 1
                    else:
                        print(f"✓ Day {day}: Item '{name}' found")
                else:
                    print(f"❌ Day {day}: Invalid rang for bag: {rang}")
                    errors += 1
        
        # Validate user_day structure
        if "user_day" not in avent_data:
            print("❌ Missing 'user_day' tracking object")
            errors += 1
        else:
            user_day = avent_data["user_day"]
            for day in range(1, 25):
                if str(day) not in user_day:
                    print(f"⚠️  Day {day}: Missing entry in user_day (auto-fixing...)")
                    avent_data["user_day"][str(day)] = 0
                    errors += 1
        
        line()
        if errors == 0:
            print("✅ All checks passed! Advent data is valid.")
        else:
            print(f"⚠️  Found {errors} issue(s)")
            save_json("./files/avent.json", avent_data)
            print("Data auto-corrections saved.")
    
    elif choise == 3:
        # Edit a day
        line()
        try:
            day = int(input("Enter the day number [1-24]: "))
            if day < 1 or day > 24:
                print("Invalid day number!")
                input("Press any key to continue...")
                return
            
            current_gift = avent_data.get(str(day), [])
            print(f"\nCurrent data for day {day}: {current_gift}")
            
            print("\nEnter new gift data (press Enter to keep current value):")
            name = input(f"  Name [{current_gift[0] if len(current_gift) > 0 else 'N/A'}]: ") or (current_gift[0] if len(current_gift) > 0 else "")
            rang = input(f"  Rank [{current_gift[1] if len(current_gift) > 1 else 'N/A'}]: ") or (current_gift[1] if len(current_gift) > 1 else "")
            where = input(f"  Where [{current_gift[2] if len(current_gift) > 2 else 'N/A'}]: ") or (current_gift[2] if len(current_gift) > 2 else "")
            
            try:
                amount = int(input(f"  Amount [{current_gift[3] if len(current_gift) > 3 else 1}]: ") or (current_gift[3] if len(current_gift) > 3 else 1))
            except ValueError:
                amount = current_gift[3] if len(current_gift) > 3 else 1
            
            avent_data[str(day)] = [name, rang, where, amount]
            save_json("./files/avent.json", avent_data)
            print(f"✅ Day {day} updated successfully!")
        
        except ValueError:
            print("Invalid input!")
        
        input("Press any key to continue...")
    
    line()
    input("End of the program, press any key to go back to the main menu.")


func_list = {
    1 : inv_info,
    2 : key_manager,
    3 : adjust,
    4 : organise_list,
    5 : check,
    6 : adjust_id,
    7 : avent_manager,
    8 : match_adjust
}

line(35)
print("Starting the script...")
print(f"Welcome on script manager V{VERSION}")
print("#### Check manager.md for documentation")
line()
time.sleep(0.5)
while True :
    print("Choose something you want to do :")
    print("[1] Show the inv folder info")
    print("[2] Key manager")
    print("[3] Inv adjust")
    print("[4] Organise the list")
    print("[5] Checks")
    print("[6] Adjust yokai ids")
    print("[7] Avent calendar manager")
    print("[8] match manager")
    
    
    choise_range = "1-8"
    choise = input(f"Please select a number [{choise_range}] : ")

    if int(choise) in func_list.keys() :
        func_list[int(choise)]()
    else :
        print(f"The number isn't right, please enter a number in range [{choise_range}]")
        input("Press any key to go back to the main menu.")
    line(35)
