# Manager.py Documentation

Un script de gestion pour le bot.

## Vue d’ensemble

**But :** Fournit des outils pour gérer les inventaires, les données Yo-kai et effectuer des vérifications système.

## Fonctions principales

1. **Afficher les infos d’inventaire** (`inv_info()`)  
   - Mode simple : affiche les statistiques de base  
   - Mode avancé : répartition détaillée des Yo-kai par classe  

2. **Gestionnaire de clés** (`key_manager()`)  
   - Supprime des Yo-kai des inventaires  
   - Remplace des Yo-kai par d’autres  

3. **Ajustement d’inventaire** (`adjust()`)  
   - Vérifie le nombre total de Yo-kai → parfois le nombre de Yo-kai d’une classe n’est pas correct  

4. **Organisation des listes** (`organise_list()`)  
   - Trie les listes de Yo-kai par ordre alphabétique  
   - Détection des doublons → indique si des Yo-kai apparaissent dans plusieurs classes (le bot n’est pas conçu pour gérer cela)  

5. **Vérifications système** (`check()`)  
   - Validation des fichiers de pièces  
   - Vérification des identifiants d’images de Yo-kai  

6. **Ajustement des identifiants** (`adjust_id()`)  
   - Ajoute les Yo-kai manquants à la liste des identifiants (`./files/full_name_fr.json`)  

## Utilisation

Lancez le script et choisissez une option depuis le menu principal :  
```bash
python manager.py
```
### Exemple de menu :
Choisissez une action :
[1] Afficher les infos du dossier inv.
[2] Gestionnaire de clés.
[3] Ajuster l’inventaire.
[4] Organiser la liste.
[5] Vérifications
[6] Ajuster les identifiants Yo-kai

## Dépendances de la structure des fichiers

Le script attend les fichiers/dossiers suivants :

- `./files/inventory/` - Fichiers d’inventaire utilisateur
- `./files/yokai_list.json` - Liste principale des Yo-kai
- `./files/full_name_fr.json` - Traductions des Yo-kai
- `./files/coin/` - Fichiers de données de pièces
- `./files/items.json` - Base de données des objets

## Notes

- Utilise des opérations asynchrones pour la validation des images
- Maintient la cohérence des données entre les fichiers
