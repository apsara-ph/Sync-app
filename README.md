# Sync-app
Application de synchronisation de fichiers en mode unidirectionnel (gauche -> droite)
## Description de l'application
Application graphique codée en python avec Tkinter 
## Fonctionnalités
- Deux options de synchronisation : intégrale ou par filtre d'extension (Bouton __SYNCHRO__)
- Comparaison des deux dossiers selectionnés (Bouton __ANALYSIS__)
- Possibilité de choisir le fonctionnement (comparaison/synchronisation des fichiers) en mode continu (Bouton __ON__/__OFF__)
- Affichage de la base de données associée à une comparaison/synchronisation des fichiers (Bouton __BDD__)
- Réinitialisation de la base de données et des élèments de comparaison (Bouton __RESET__)

## Fonctionnement
La synchronisation s'effectue en se référant sur le dossier de gauche.  
*Remarque* : la synchronisation par extension s'effectue de manière récursive seulement dans le(s) sous-repertoire(s) de droite communs pré-existant(s).  
    
La base de données est générée automatiquement suite aux évenements suivants :
* Bouton __ANALYSIS__: elle indique pour chaque élèment qui compose les dossiers, leur état actuel (localisation, date/heure de création, date/heure de modification, taille) et les opérations à effectuer pour une eventuelle synchronisation (création, modification, suppression)
* Bouton __SYNCHRO__: elle informe de l'état de l'opération (0/1: Non traitée/Traitée)

## Installation
1. Utilisez Python Version 3.9.2
2. Clonez le repo
   ```sh
   git clone https://github.com/apsara-ph/Sync-app.git
   ```
3. Exécutez le fichier appli-sync depuis le dossier Sync-app
   ```sh
   py appli-sync.py
   ```
4. Sélectionnez les dossiers de votre choix puis testez !
