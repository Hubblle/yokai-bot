import json
import bot_package.data as data

# this function is call for saw if the user have data
# and if he don't have info calculate he number of orbe
async def create_user_info(user_id: int) -> None:
    if not str(user_id) in data.MONEY_DATA.keys():
        data.MONEY_DATA[str(user_id)] = 0
        '''
        calcul le nombre que devrai avoir l'utilisateur 
        en fonction de son nombre de yokai en double
        si le yokai est en double, l'utilisateur gagne autant de point 
        que de point de complétion de la collection pour chaque doublon
        '''
        user_inventory = data.open_json(f"./files/inventory/{user_id}.json")
        for yokai in user_inventory.items():
            nom, info = yokai
            if isinstance(info, list):
                if len(info) > 1:

                    point = data.class_to_point[info[0]]
                    bonus_copies = int(info[1]) - 1
                    data.MONEY_DATA[str(user_id)] += point * bonus_copies
        with open("./files/monnaie.json", "w") as money_file:
            json.dump(data.MONEY_DATA, money_file, indent=4)


# used to add orbe to a specific user
async def add(user_id: int, amount: int) -> None:
    await create_user_info(user_id)
    data.MONEY_DATA[str(user_id)] += amount
    with open("./files/monnaie.json", "w") as money_file:
        json.dump(data.MONEY_DATA, money_file, indent=4)

# use to set at 0 the wallet of a spécific user
async def reset(user_id: int) -> None:
    data.MONEY_DATA[str(user_id)] = 0
    with open("./files/monnaie.json", "w") as money_file:
        json.dump(data.MONEY_DATA, money_file, indent=4)

# del the wallet of a specific user
async def del_info(user_id: int) -> None:
    if str(user_id) in data.MONEY_DATA.keys():
        del data.MONEY_DATA[str(user_id)]
        with open("./files/monnaie.json", "w") as money_file:
            json.dump(data.MONEY_DATA, money_file, indent=4)




async def add_rank_orbe(user_id: int, rank) -> None:
    await create_user_info(user_id)
    p = data.class_to_point[rank]
    data.MONEY_DATA[str(user_id)] += p
    with open("./files/monnaie.json", "w") as money_file:

        json.dump(data.MONEY_DATA, money_file, indent=4) 

