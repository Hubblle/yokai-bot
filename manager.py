import json
import time
import os
import aiohttp
import asyncio
VERSION = 3

def line(num : int = 1):
    for i in range(num):
        print(" ")
        
# async func to check images
async def check_image(session, yokai_name, yokai_data):
    """Check if image exists for given Yo-kai."""
    if not yokai_data.get('id'):
        return yokai_name, None
        
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
Class_list = ['E', 'D', 'C', 'B', 'A', 'S', 'LegendaryS', "treasureS", "SpecialS", 'DivinityS', "Boss"]
Proba_list = [0.4175, 0.2, 0.12, 0.12, 0.08, 0.04, 0.0075, 0.0075, 0.0075, 0.005, 0.0025]   
        
        
def adjust():
    line(35)
    print("Welcome to the ajustement program !")
    while True :
        print("Please, select a mode :")
        print("   [1] Total number of yokai. \n   [2] Nothing. \n")
        line()
        choise = input("Please, select a number [1-2] ")
    
        if choise == "1" or choise == "2":
            choise = int(choise)
            break
    
        print("The number isn't right, please enter a number in range [1-2]")
        input("Press any key to go back to the menu.")
    
    
    if choise == 1:
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
                    "Boss" : 0
                }
                current_inv = get_inv(file.strip(".json"))
                if current_inv != {} :
                    for yokai in current_inv :
                        #check if the yokai is part of the inv system
                        if yokai in ["E", "D", "C", "B", "A", "S", "LegendaryS", "treasureS", "SpecialS", "DivinityS", "Boss", "last_claim", "", "claim"] :
                            pass
                        
                        else :
                            yokai_class = current_inv[yokai][0]
                            yokai_per_class[yokai_class] += 1
                    
                    for classes in yokai_per_class :
                        if yokai_per_class[classes] != current_inv[classes]:
                            current_inv[classes] = yokai_per_class[classes]
                            corrected_classes += 1
                        
                    save_inv(current_inv, file.strip(".json"))
                    print("The inventorys have been adjusted sucessfully !")
                    print(f"{corrected_classes} total were adjusted")
                    
    if choise == 2:
        print("that func wasn't coded yet :/")
            
            
                    
            
                                        
        
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
        print(f"    Number of inventory file : {total_user} \n    Size of ./files/inventory : {total_size/1000}MB")
        
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
        print(f"    Number of inventory file : {total_user} \n    Size of ./files/inventory : {total_size/1000}MB")
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
            "Boss" : 0
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
            "Boss" : 0
        }
        
        for dirpath, dirnames, filenames in os.walk("./files/inventory"):
            for file in filenames :
                current_inv = get_inv(file.strip(".json"))
                for yokai in current_inv :
                    #check if the yokai is part of the inv system
                    if yokai in ["E", "D", "C", "B", "A", "S", "LegendaryS", "treasureS", "SpecialS", "DivinityS", "Boss","Shiny", "last_claim", "", "claim"] :
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
        print("   [1] Check coin files. \n   [2] Check yokai ids (images).")
        line()
        choise = input("Please, select a number [1-2] ")
    
        if choise == "1" or choise == "2" :
            choise = int(choise)
            break
        
        print("The number isn't right, please enter a number in range [1-2]")
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
                        coin_output += f"total proba = {proba_total} ❌ // "
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
        

func_list = {
    1 : inv_info,
    2 : key_manager,
    3 : adjust,
    4 : organise_list,
    5 : check,
    6 : adjust_id
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
    
    
    choise_range = "1-6"
    choise = input(f"Please select a number [{choise_range}] : ")

    if int(choise) in func_list.keys() :
        func_list[int(choise)]()
    else :
        print(f"The number isn't right, please enter a number in range [{choise_range}]")
        input("Press any key to go back to the main menu.")
    line(35)
    