# Sync-app
Application de synchronisation de fichiers en mode unidirectionnel (gauche -> droite)
## Description de l'application
Application graphique codée en python avec Tkinter 
## Fonctionnalités
- Deux options de synchronisation : intégrale ou par filtre d'extension (Bouton SYNCHRO)
- Comparaison des deux dossiers selectionnés (Bouton ANALYSIS)
- Possibilité de choisir le fonctionnement (comparaison/synchronisation des fichiers) en mode continu (Bouton ON/OFF)
- Affichage de la base de données associée à une comparaison/synchronisation des fichiers (Bouton BDD)
- Réinitialisation de la base de données (Bouton RESET)

## Fonctionnement
La synchronisation s'effectue en se référant sur le dossier de gauche.  
_remarque_: la synchronisation par extension s'effectue de manière récursive seulement dans le(s) sous-repertoire(s) de droite en commun pré-existant(s).  
    
La base de données est générée automatiquement:
* suite à une comparaison des fichiers (Bouton ANALYSIS): elle indique pour chaque élèment des dossiers, leur état actuel (localisation, date/heure de création, date/heure de modification, taille) et les opérations à effectuer pour une eventuelle synchronisation (création, modification, suppression)
* suite à une opération de synchronisation (Bouton SYNCHRO): elle informe de l'état de l'opération (0/1: Non traitée/Traitée)

## Installation
1. Utilisez Python Version 3.9.2
2. Clonez le repo
   ```sh
   git clone https://github.com/apsara-ph/Sync-app.git
   ```
3. Exécutez le fichier appli-sync
   ```sh
   py appli-sync.py
   ```
4. Sélectionnez les dossiers puis testez !
