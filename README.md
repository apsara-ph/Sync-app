# Sync-app
Application de synchronisation de fichiers en mode unidirectionnel (gauche -> droite)
## Description de l'application
Application graphique codée en python avec Tkinter 
## Fonctionnalités
- Deux options de synchronisation : intégrale ou par filtre d'extension. La synchronisation par extension s'effectue de manière récursive dans le(s) sous-repertoire(s) de droite pré-existant(s)
- Possibilité de choisir le fonctionnement (comparaison/synchronisation des fichiers) en mode continu (ON/OFF)
- Traçage des opérations de synchronisation via une base de donnée avec sqlite3 
## Installation
1. Utiliser Python Version 3.9.2
2. Cloner le repo
   ```sh
   git clone https://github.com/apsara-ph/Sync-app.git
   ```
3. Exécuter le fichier appli-sync
   ```sh
   py appli-sync.py
   ```