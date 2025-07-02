# ScientifyBot Y
## Requirements :

- Python 3.12+

- Libraries : discord.py / colorlog

- Créer les dossiers/fichiers : `/files/error/` & `/files/logs/discord.log` & `/files/inventory/` 

- Créer un fichier `/configuration.json` tel que le fichier `/configuration.json.example` fourni dans le git.

- Créer un fichier `/files/bot-data.json` tel que :


```
{
    "image_link" : {
        "B" : "Lien image du rang B",
        "E" : "Lien image du rang E",
        "C" : "Lien image du rang E",
        "A" : "Lien image du rang A",
        "D" : "Lien image du rang D",
        "S" : "Lien image du rang S",
        "LegendaryS" : "Lien image pour les légendaires",
        "treasureS" : "Lien image pour les trésor",
        "SpecialS" : "Lien image pour les Spécial",
        "DivinityS" : "Lien image pour les divinité",
        "Boss" : "Lien image pour les Boss"
    },

    "emoji" : {
        "treasureS" : "Markdown émoji trésor",
        "B" : "Markdown émoji B",
        "E" : "Markdown émoji E",
        "C" : "Markdown émoji C",
        "A" : "Markdown émoji A",
        "D" : "Markdown émoji D",
        "S" : "Markdown émoji S",
        "DivinityS": "Markdown émoji divinité",
        "LegendaryS": "Markdown émoji legendaire",
        "SpecialS":"Markdown émoji spécial",
        "Boss":"Markdown émoji Boss"
    }
}
```

- Créer un fichier `/.env` tel que le fichier `.env.example` qui est fourni dans le git.




## Informations :
Dans le code, le "rang" d'un Yo-kai est appelé "class".

Vous pouvez executer `./bot.py` pour lancer le bot

**--> Le code ne semble pas fonctionner sous windows pour la fonction `classid_to_class(str(), true)`, il n'a aucun problème sous linux/debian.**


