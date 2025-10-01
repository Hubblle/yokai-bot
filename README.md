# ScientifyBot Y
## Requirements :

- Python 3.12+

- Paquet: discord.py / python-dotenv

- Créer un fichier `/configuration.json` tel que le fichier `/configuration.json.example` fourni dans le git.

- Créer un fichier `/files/bot-data.json` tel que le fichier `/files/bot-data.json.example` fourni dans le git.:

- Créer un fichier `/.env` tel que le fichier `.env.example` qui est fourni dans le git.




## Informations :
Dans le code, le "rang" d'un Yo-kai est appelé "class".

Vous pouvez executer `./bot.py` pour lancer le bot

Pour toutes questions, créer un ticket : https://discord.gg/K4H4xhHqUb
(For any information, please visit : https://discord.gg/K4H4xhHqUb)

## Manager.py
Le script manager.py est fourni pour toutes taches de maintenance sur le bot (voir manager.md)

Il est important de noter que après l'ajout de Yo-kai dans la liste, il faut utiliser la fonction "6. **Ajustement des identifiants** (`adjust_id()`)", ou les ajouter manuellement au fichier `./files/full_name_fr.json` sinon le bot risque de provoquer des erreurs quand on les obtients.
