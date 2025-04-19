# ScientifyBot Y
__Requirements :__

- Python 3.12+
- Libraries : discord.py / colorlog
- Créer les dossiers/fichiers : `/files/error/` & `/files/logs/discord.log`

Créer un fichier `/files/configuration.json` tel que : 

``
{
    "token" : "Votre token",
    "prefix" : ".",
    "team_members_id" : [ID Discord des personnes pouvant exécuter des commandes d'administration.]
}
``

Créer un fichier `/files/bot-data.json` tel que :


``
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
``



__Informations :__
Dans le code, le "rang" d'un Yo-kai est appelé "class".

--> Le code ne semble pas fonctionner sous windows pour la fonction `classid_to_class(str(), true)`, il n'a aucun problème sous linux/debian.

Merci de lire `CONTRIBUTING.md` pour savoir comment contribuer.
