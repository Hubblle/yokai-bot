# ScientifyBot Y
## Requirements :

- Python 3.12+
- Libraries : discord.py / colorlog
- Créer les dossiers/fichiers : `/files/error/` & `/files/logs/discord.log` & `/files/inventory` 

- Créer un fichier `/files/configuration.json` tel que : 

```
{
    "team_members_id" : [ID Discord des personnes pouvant exécuter des commandes d'administration.]
}
```

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

- Créer un fichier `./.env` tel que le fichier `.env.example` qui est fourni dans le git.




## Informations :
Dans le code, le "rang" d'un Yo-kai est appelé "class".

Vous pouvez executer `./bot.py` pour lancer le bot

**--> Le code ne semble pas fonctionner sous windows pour la fonction `classid_to_class(str(), true)`, il n'a aucun problème sous linux/debian.**

## Participer :
Merci de votre intérêt ! Voici comment contribuer :

1. **Forkez** le dépôt.
2. **Modifiez** votre fork à votre guise.
3. Rendez-vous dans l'onglet **"Pull Requests"** du repo : https://github.com/Hubblle/yokai-bot/pulls.
4. Cliquez sur **"New pull request"** puis sur **"Compare across forks"**.
![image](https://github.com/user-attachments/assets/ee7709eb-7410-4a74-9d9a-b6201031c359)

6. Vérifiez que votre fork est bien sélectionné et ouvrez votre Pull Request.
7. Attendez qu'elle soit examinée. Si des commentaires vous sont adressés, répondez aux questions et apportez les modifications nécessaires.
8. Une fois validée, votre contribution sera fusionnée dans le projet ! 🎉
