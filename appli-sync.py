##----- Importation des Modules -----##
from tkinter import *
from tkinter import filedialog
import tkinter as tk
import os.path, time, filecmp, subprocess, os, shutil, sqlite3
from intervallometre import Intervallometre
from extEntry import ExtEntry

##----- Définition des Fonctions -----##

def selectLeftFolder():
    global repLeft
    repLeft = filedialog.askdirectory(initialdir="/",title='Selectionnez un repertoire')
    if len(repLeft) > 0:
        lblLeft.configure(text="%s" % repLeft)
    return repLeft

def selectRightFolder():
    global repRight
    repRight = filedialog.askdirectory(initialdir="/",title='Selectionnez un repertoire')
    if len(repRight) > 0:
        lblRight.configure(text="%s" % repRight)
    return repRight

def checkDirExistance(dirPath): # Vérification de l'existence d'un chemin
    res=False
    if os.path.isdir(dirPath):
        res=True
    return res

def compareDirBIS(d1,d2):
    res=False
    l=filecmp.dircmp(d1, d2).left_only
    r=filecmp.dircmp(d1, d2).right_only
    c=filecmp.dircmp(d1, d2).common
    c1=[]
    c2=[]
    if (l==[] and r==[]):
        for i in range(len(c)):
            if os.path.isfile(d1+"/"+str(c[i]))==True:
                if (filecmp.cmp(d1+"/"+str(c[i]), d2+"/"+str(c[i]), shallow=True)==True):
                    c1.append(c[i])
                else:
                    c2.append(c[i])
            else:
                if (synchroDirBIS(d1+"/"+str(c[i]), d2+"/"+str(c[i]))==True):
                    c1.append(c[i])
                else:
                    c2.append(c[i])
        if (c2==[]):
            res = True
    return res

def compareDir(): # Comparaison entre deux dossiers
    d1=repLeft
    d2=repRight
    if (checkDirExistance(d1)==True and checkDirExistance(d2)==True):
        if (d1==d2):
            lblEtat.configure(text='Same folder selected')
        else:
            lblLeftDirSize.configure(text=str(sizeDir(d1))+' octets')
            lblRightDirSize.configure(text=str(sizeDir(d2))+' octets')
            lblEtat.configure(text='Analysis Results')
            lblDifferences.configure(text='Differences')
            lblOnlyLeftElement.configure(text='Only in left folder :')
            lblOnlyRightElement.configure(text='Only in right folder :')
            lblSimilarities.configure(text='Similarities')
            lblSameElementFalse.configure(text='Same name/different content')
            lblSameElementTrue.configure(text='Same name/same content')  
            l=filecmp.dircmp(d1, d2).left_only
            r=filecmp.dircmp(d1, d2).right_only
            c=filecmp.dircmp(d1, d2).common

            lblElementInLeftOnly.configure(text=l)
            lblElementInRightOnly.configure(text=r)

            c1=[]
            c2=[]
            for i in range(len(c)):
                if os.path.isfile(d1+"/"+str(c[i]))==True:
                    if (filecmp.cmp(d1+"/"+str(c[i]), d2+"/"+str(c[i]), shallow=True)==True):
                        c1.append(c[i])
                    else:
                        c2.append(c[i])
                else:
                    if (compareDirBIS(d1+"/"+str(c[i]), d2+"/"+str(c[i]))==True):
                        c1.append(c[i])
                    else:
                        c2.append(c[i])
            lblElementCommonTrue.configure(text=c1)
            lblElementCommonFalse.configure(text=c2)
    else :
        print("Désolé, il y a une erreur sur la saisie des dossiers")
    genBDD()

def synchroDirBIS(d1,d2):
    global nb_delBIS
    global nb_modifBIS
    global nb_creatBIS
    nb_delBIS=0
    nb_modifBIS=0
    nb_creatBIS=0
    res=False
    l=filecmp.dircmp(d1, d2).left_only
    r=filecmp.dircmp(d1, d2).right_only
    c=filecmp.dircmp(d1, d2).common
    print("Analyse des manipulations de synchronisation bis")
    if(d1==d2):
        print("Vous avez sélectionné le même dossier")
    else:
        for i in range (len(l)):
            if (str(EtyExtension.get()) == str(l[i]).split('.')[-1]) or (str(EtyExtension.get()) == ""):
                print(l[i] + " à copier")
                if os.path.isfile(d1+"/"+str(l[i]))==True:
                    shutil.copy(d1+"/"+str(l[i]), d2+"/"+str(l[i])) #copie de fichier
                    nb_creatBIS+=1
                else:
                    shutil.copytree(d1+"/"+str(l[i]), d2+"/"+str(l[i])) #copie de repertoire
                    nb_creatBIS+=1
        l=[]
        for i in range (len(r)):
            if (str(EtyExtension.get()) == str(r[i]).split('.')[-1]) or (str(EtyExtension.get()) == ""):
                print(r[i] + " à supprimer")
                if os.path.isfile(d2+"/"+str(r[i]))==True:
                    os.remove(d2+"/"+str(r[i])) #supression du fichier
                    nb_delBIS+=1
                else:
                    shutil.rmtree(os.path.join(d2,str(r[i]))) #supression du repertoire
                    nb_delBIS+=1
        r=[]
        for i in range(len(c)):
            if os.path.isfile(d1+"/"+str(c[i]))==True:
                if (str(EtyExtension.get()) == str(c[i]).split('.')[-1]) or (str(EtyExtension.get()) == ""):
                    if (filecmp.cmp(d1+"/"+str(c[i]), d2+"/"+str(c[i]), shallow=True)==True):
                        print(str(c[i])+": OK !")
                    else:
                        print(c[i]+": Contenu de fichier différent")
                        os.remove(d2+"/"+str(c[i])) #supression du fichier
                        shutil.copy(d1+"/"+str(c[i]), d2+"/"+str(c[i])) #copie du nouveau fichier
                        nb_modifBIS+=1
            else:
                if (synchroDirBIS(d1+"/"+str(c[i]), d2+"/"+str(c[i]))==True):
                    print(str(c[i])+": OK !")
                else:
                    shutil.rmtree(os.path.join(d2,str(c[i])))
                    shutil.copytree(d1+"/"+str(c[i]), d2+"/"+str(c[i]))
                    nb_modifBIS+=1
        res=True
    return res

def synchroDir(): # Synchronisation des dossiers
    global nb_del
    global nb_modif 
    global nb_creat
    nb_del=0
    nb_modif=0
    nb_creat=0

    d1=repLeft
    d2=repRight
    res=False
    l=filecmp.dircmp(d1, d2).left_only
    r=filecmp.dircmp(d1, d2).right_only
    c=filecmp.dircmp(d1, d2).common
    if(d1==d2):
        print("Vous avez sélectionné le même dossier")
        lblEtat.configure(text="Sorry,...Same folder selected")
    else:
        print("Analyse des manipulations de synchronisation")
        lblEtat.configure(text='Synchronization...')
        for i in range (len(l)):
            if (str(EtyExtension.get()) == str(l[i]).split('.')[-1]) or (str(EtyExtension.get()) == ""):
                print(l[i] + " à copier")
                if os.path.isfile(d1+"/"+str(l[i]))==True:
                        shutil.copy(d1+"/"+str(l[i]), d2+"/"+str(l[i])) #copie de fichier
                        nb_creat+=1
                else:
                    shutil.copytree(d1+"/"+str(l[i]), d2+"/"+str(l[i])) #copie de repertoire
                    nb_creat+=1
        l=[]
        for i in range (len(r)):
            if (str(EtyExtension.get()) == str(r[i]).split('.')[-1]) or (str(EtyExtension.get()) == ""):
                print(r[i] + " à supprimer")
                if os.path.isfile(d2+"/"+str(r[i]))==True:
                    os.remove(d2+"/"+str(r[i])) #supression du fichier
                    nb_del+=1
                else:
                    shutil.rmtree(os.path.join(d2,str(r[i]))) #supression du repertoire
                    nb_del+=1
        r=[]
        for i in range(len(c)):
            if os.path.isfile(d1+"/"+str(c[i]))==True:
                if (str(EtyExtension.get()) == str(c[i]).split('.')[-1]) or (str(EtyExtension.get()) == ""):
                    if (filecmp.cmp(d1+"/"+str(c[i]), d2+"/"+str(c[i]), shallow=True)==True):
                        print(str(c[i])+": OK !")
                    else:
                        print(c[i]+": Contenu de fichier différent")
                        os.remove(d2+"/"+str(c[i])) #supression du fichier
                        shutil.copy(d1+"/"+str(c[i]), d2+"/"+str(c[i])) #copie du nouveau fichier
                        nb_modif+=1
            else:
                if (synchroDirBIS(d1+"/"+str(c[i]), d2+"/"+str(c[i]))==True):# A REVOIR
                    print(str(c[i])+": OK !")
                    nb_modif+=nb_modifBIS
                    nb_creat+=nb_creatBIS
                    nb_del+=nb_delBIS
                else:
                    shutil.rmtree(os.path.join(d2,str(c[i])))
                    shutil.copytree(d1+"/"+str(c[i]), d2+"/"+str(c[i]))
                    nb_modif+=1
        res=True
        lblOperations.configure(text='Operations')
        lblAllOperations.configure(text='Modified : '+ str(nb_modif)+', Created : '+ str(nb_creat) +', Deleted : '+ str(nb_del))
        compareDir()
    return res

def remiseZero(event):
    lblLeft.configure(text='')
    lblRight.configure(text='')
    lblEtat.configure(text="")
    lblDifferences.configure(text="")
    lblOnlyLeftElement.configure(text="")
    lblElementInLeftOnly.configure(text="")
    lblOnlyRightElement.configure(text="")
    lblElementInRightOnly.configure(text="")
    lblSimilarities.configure(text="")
    lblSameElementFalse.configure(text="")
    lblElementCommonFalse.configure(text="")
    lblSameElementTrue.configure(text="")
    lblElementCommonTrue.configure(text='')
    lblOperations.configure(text='')
    lblAllOperations.configure(text='')

    try:
        baseDeDonnees = sqlite3.connect('files.db')
        curseur = baseDeDonnees.cursor()
        curseur.execute("DROP TABLE IF EXISTS Files") # Suppression des données
        baseDeDonnees.commit()
        print("Données supprimées")
        baseDeDonnees.close()
    except sqlite3.Error as error:
        print("Problème de suppression")

def deleteAnalysis():
    lblEtat.configure(text="")
    lblDifferences.configure(text="")
    lblOnlyLeftElement.configure(text="")
    lblElementInLeftOnly.configure(text="")
    lblOnlyRightElement.configure(text="")
    lblElementInRightOnly.configure(text="")
    lblSimilarities.configure(text="")
    lblSameElementFalse.configure(text="")
    lblElementCommonFalse.configure(text="")
    lblSameElementTrue.configure(text="")
    lblElementCommonTrue.configure(text='')
    lblOperations.configure(text='')
    lblAllOperations.configure(text='')

    try:
        baseDeDonnees = sqlite3.connect('files.db')
        curseur = baseDeDonnees.cursor()
        curseur.execute("DROP TABLE IF EXISTS Files") # Suppression des données
        baseDeDonnees.commit()
        print("Données supprimées")
        baseDeDonnees.close()
    except sqlite3.Error as error:
        print("Problème de suppression")

def sizeDir(path): # Taille d'un dossier en octets
    size=0
    if checkDirExistance(path)==True:
        for root, dirs, files in os.walk(path):
            for fic in files:
                size+=os.path.getsize(os.path.join(root,fic))
        return size
    else:
        print("Le chemin saisie n'existe pas")

##----- Fonctions annexes pour intégration BDD -----##

def convertMonth(m):
    res='00'
    l=['Jan','Fev','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    for i in range(len(l)):
        if (m==l[i]):
            if (i<9):
                res='0'+str(i+1)
            else:
                res=str(i+1)
    return res

def formatCreationDay(filePath): # Retourne la date au format jjmmaaaa
    jj= time.ctime(os.path.getctime(filePath))[8:10]
    mm=time.ctime(os.path.getctime(filePath))[4:7]
    aaaa=time.ctime(os.path.getctime(filePath))[20:24]
    if (int(jj)<10):
        jj= time.ctime(os.path.getctime(filePath))[9:10]
        dd = '0'+jj+convertMonth(mm)+aaaa
    else:
        dd = jj+convertMonth(mm)+aaaa
    return dd

def formatModificationDay(filePath):
    jj= time.ctime(os.path.getmtime(filePath))[8:10]
    mm=time.ctime(os.path.getmtime(filePath))[4:7]
    aaaa=time.ctime(os.path.getmtime(filePath))[20:24]
    if (int(jj)<10):
        jj= time.ctime(os.path.getmtime(filePath))[9:10]
        dd = '0'+jj+convertMonth(mm)+aaaa
    else:
        dd = jj+convertMonth(mm)+aaaa
    return dd

##----- Fonctions DB -----##

def genBDD():
    d1=repLeft
    d2=repRight
    l=filecmp.dircmp(d1, d2).left_only
    r=filecmp.dircmp(d1, d2).right_only
    c=filecmp.dircmp(d1, d2).common
    c1=[]
    c2=[]

    filePath="monDossier1/file0"

    baseDeDonnees = sqlite3.connect('files.db')
    curseur = baseDeDonnees.cursor()
    curseur.execute("CREATE TABLE IF NOT EXISTS Files (id INTEGER PRIMARY KEY AUTOINCREMENT, nameFile TEXT NOT NULL, localisation TEXT NOT NULL, manipulation TEXT NOT NULL, creationDate VARCHAR(50),creationTime TEXT, lastModificationDate VARCHAR(50),lastModificationTime VARCHAR(50), size INTEGER,state INTEGER)") # Création de la base de données
    baseDeDonnees.commit() 


    for i in range(len(c)):
        if os.path.isfile(d1+"/"+str(c[i]))==True:
            if (filecmp.cmp(d1+"/"+str(c[i]), d2+"/"+str(c[i]), shallow=True)==True):
                c1.append(c[i])
            else:
                c2.append(c[i])
        else:
            if (compareDirBIS(d1+"/"+str(c[i]), d2+"/"+str(c[i]))==True):
                c1.append(c[i])
            else:
                c2.append(c[i])

    for i in range(len(l)): #copié
        filePath=d1+"/"+str(l[i])

        timeCreation=time.ctime(os.path.getctime(filePath))[11:19] 
        timeCreation0=timeCreation[0:2]+timeCreation[3:5]+timeCreation[6:8]

        dateCreation=formatCreationDay(filePath)

        timeModification=time.ctime(os.path.getmtime(filePath))[11:19] 
        timeModification0=timeModification[0:2]+timeModification[3:5]+timeModification[6:8]

        dateModification=formatModificationDay(filePath)

        sizeFile=str(os.path.getsize(filePath))

        data=(l[i], 'left', 'à copier',dateCreation,timeCreation0,dateModification,timeModification0,sizeFile,0)
        curseur.execute("INSERT INTO Files (nameFile, localisation, manipulation,creationDate,creationTime,lastModificationDate,lastModificationTime,size,state) VALUES (?,?,?,?,?,?,?,?,?)",data)
        #curseur.execute("INSERT INTO Files (nameFile, localisation, manipulation,creationDate,creationTime,lastModificationDate,lastModificationTime,size,state) VALUES ('coucou.txt', 'left', 'à copier',"+ dateCreation +","+timeCreation0+","+dateModification + ","+timeModification0+","+sizeFile+",0)")


    for i in range(len(r)): #supprimé
        filePath=d2+"/"+str(r[i])

        timeCreation=time.ctime(os.path.getctime(filePath))[11:19]
        timeCreation0=timeCreation[0:2]+timeCreation[3:5]+timeCreation[6:8]

        dateCreation=formatCreationDay(filePath)

        timeModification=time.ctime(os.path.getmtime(filePath))[11:19]
        timeModification0=timeModification[0:2]+timeModification[3:5]+timeModification[6:8]

        dateModification=formatModificationDay(filePath)

        sizeFile=str(os.path.getsize(filePath))

        data=(r[i],'right','à supprimer', dateCreation,timeCreation0,dateModification,timeModification0,sizeFile,0)
        curseur.execute("INSERT INTO Files (nameFile, localisation, manipulation,creationDate,creationTime,lastModificationDate,lastModificationTime,size,state) VALUES (?,?,?,?,?,?,?,?,?)",data)

    
    for i in range(len(c1)): #none
        filePath=d2+"/"+str(c1[i])

        timeCreation=time.ctime(os.path.getctime(filePath))[11:19]
        timeCreation0=timeCreation[0:2]+timeCreation[3:5]+timeCreation[6:8]

        dateCreation=formatCreationDay(filePath)

        timeModification=time.ctime(os.path.getmtime(filePath))[11:19]
        timeModification0=timeModification[0:2]+timeModification[3:5]+timeModification[6:8]

        dateModification=formatModificationDay(filePath)

        sizeFile=str(os.path.getsize(filePath))

        data=(c1[i],'both','None', dateCreation,timeCreation0,dateModification,timeModification0,sizeFile,1)
        curseur.execute("INSERT INTO Files (nameFile, localisation,manipulation,creationDate,creationTime,lastModificationDate,lastModificationTime,size,state) VALUES (?,?,?,?,?,?,?,?,?)",data)

    
    for i in range(len(c2)): #modifié  
        filePath=d2+"/"+str(c2[i]) 
            
        timeCreation=time.ctime(os.path.getctime(filePath))[11:19]
        timeCreation0=timeCreation[0:2]+timeCreation[3:5]+timeCreation[6:8]

        dateCreation=formatCreationDay(filePath)

        timeModification=time.ctime(os.path.getmtime(filePath))[11:19]
        timeModification0=timeModification[0:2]+timeModification[3:5]+timeModification[6:8]

        dateModification=formatModificationDay(filePath)

        sizeFile=str(os.path.getsize(filePath))

        data=(c2[i],'both','à modifier', dateCreation,timeCreation0,dateModification,timeModification0,sizeFile,0)
        curseur.execute("INSERT INTO Files (nameFile, localisation, manipulation,creationDate,creationTime,lastModificationDate,lastModificationTime,size,state) VALUES (?,?,?,?,?,?,?,?,?)",data)

    baseDeDonnees.commit()
    baseDeDonnees.close()

def afficherBDD():
    baseDeDonnees = sqlite3.connect('files.db')
    curseur = baseDeDonnees.cursor()
    curseur.execute("CREATE TABLE IF NOT EXISTS Files (id INTEGER PRIMARY KEY AUTOINCREMENT, nameFile TEXT NOT NULL, localisation TEXT NOT NULL, manipulation TEXT NOT NULL, creationDate VARCHAR(50),creationTime TEXT, lastModificationDate VARCHAR(50),lastModificationTime VARCHAR(50), size INTEGER,state INTEGER)") # Création de la base de données
    baseDeDonnees.commit()
    
    curseur.execute("SELECT * FROM Files")
    for resultat in curseur:
        print(resultat)

    baseDeDonnees.commit()
    baseDeDonnees.close()

##----- Mode de fonctionnement -----##
   
def modeContinuOn():
    print("mode continu")
    lblMode.configure(text="Mode Continu activé")
    global tCompare,tSynchro
    tCompare=Intervallometre(10,compareDir)
    tCompare.setDaemon(True)
    tCompare.start()
    tSynchro=Intervallometre(10,synchroDir)
    tSynchro.setDaemon(True)
    tSynchro.start()

def modeContinuOff():
    print("arret du mode continu")
    lblMode.configure(text="Mode Continu desactivé")
    tCompare.stop()
    tSynchro.stop()

    
#----- Création de la fenêtre -----##
fen = Tk()
fen.geometry("1200x650")
fen.title('Synchronization')

#Titre 
lblLeftDir=Label(fen , text ="Folder sync...", font=("Helvetica", 16))
lblLeftDir.grid(row=0, column=1, columnspan=10, padx=3, pady=8, sticky=S+W+E)


#Dossier gauche
lblLeftDir=Label(fen , text ="Left Folder :")
lblLeftDir.grid(row=1, column=1, padx=3, pady=8, sticky=S+W+E)

lblLeft = Label(fen,bg = 'grey', width="30", font=("Helvetica", 10), highlightcolor= "green", relief=FLAT)
lblLeft.grid(row=1, column=2, padx=3, pady=8, sticky=S+W+E)

lblLeftDirSize = Label(fen,bg = 'white', width="30", font=("Helvetica", 10), highlightcolor= "green", relief=FLAT)
lblLeftDirSize.grid(row=2, column=2, padx=3, pady=8, sticky=S+W+E)

btnLeftDir = Button(fen, text='Browse...', width='10',bg='white', command = selectLeftFolder)
btnLeftDir.grid(row=1, column=3, padx=3, pady=8, sticky=S+W+E)


#Dossier de droite
lblRightDir=Label(fen , text ="Right Folder :")
lblRightDir.grid(row=1, column=6, padx=3, pady=8, sticky=S+W+E)

lblRight = Label(fen,bg = 'grey', width="30", font=("Helvetica", 10), highlightcolor= "green", relief=FLAT)
lblRight.grid(row=1, column=7, padx=3, pady=8, sticky=S+W+E)

lblRightDirSize = Label(fen,bg = 'white', width="30", font=("Helvetica", 10), highlightcolor= "green", relief=FLAT)
lblRightDirSize.grid(row=2, column=7, padx=3, pady=8, sticky=S+W+E)

btnRightDir = Button(fen, text='Browse...', width='10',bg='white', command = selectRightFolder)
btnRightDir.grid(row=1, column=8, padx=3, pady=8, sticky=S+W+E)

#Resultats
lblEtat=Label(fen, font=("Helvetica", 10))
lblEtat.grid(row=9, column=1, columnspan=10, padx=3, pady=8, sticky=S+W+E)

lblDifferences=Label(fen , font=("Helvetica", 12))
lblDifferences.grid(row=10, column=1, columnspan=10, padx=3, pady=8, sticky=S+W+E)

lblOnlyLeftElement=Label(fen)
lblOnlyLeftElement.grid(row=11, column=1, columnspan=5, padx=3, pady=8, sticky=S+W+E)

lblElementInLeftOnly = Label(fen, font=("Helvetica", 10))
lblElementInLeftOnly.grid(row=12, column=1, columnspan=5, padx=3, pady=8)

lblOnlyRightElement=Label(fen)
lblOnlyRightElement.grid(row=11, column=5, columnspan=5, padx=3, pady=8, sticky=S+W+E)

lblElementInRightOnly = Label(fen, font=("Helvetica", 10))
lblElementInRightOnly.grid(row=12, column=5, columnspan=5, padx=3, pady=8)



lblSimilarities=Label(fen , font=("Helvetica", 12))
lblSimilarities.grid(row=15, column=1, columnspan=10, padx=3, pady=8, sticky=S+W+E)

lblSameElementFalse=Label(fen)
lblSameElementFalse.grid(row=16, column=1, columnspan=5, padx=3, pady=8, sticky=S+W+E)

lblElementCommonFalse = Label(fen, font=("Helvetica", 10))
lblElementCommonFalse.grid(row=17, column=1, columnspan=5, padx=3, pady=8)

lblSameElementTrue=Label(fen)
lblSameElementTrue.grid(row=16, column=5, columnspan=5, padx=3, pady=8, sticky=S+W+E)

lblElementCommonTrue = Label(fen, font=("Helvetica", 10))
lblElementCommonTrue.grid(row=17, column=5, columnspan=5, padx=3, pady=8)

lblOperations=Label(fen, font=("Helvetica", 12))
lblOperations.grid(row=19, column=1, columnspan=10, padx=3, pady=8)

lblAllOperations=Label(fen)
lblAllOperations.grid(row=20, column=1, columnspan=10, padx=3, pady=8)

##----- Les boutons -----##

##----- Bouton Compare -----##
btnStartAnalysis = Button(fen, text='ANALYSIS', width='8',bg='pale green', command=compareDir)
btnStartAnalysis.grid(row=1, column=9, padx=3, pady=8)
#btnStartAnalysis.focus_set()

##----- Bouton Reset -----##
btnDeleteAnalysis = Button(fen, text='RESET', width='8',bg='light pink', command=deleteAnalysis)
btnDeleteAnalysis.grid(row=1, column=10, padx=3, pady=8)

##----- Bouton Synchronisation -----##
btnSynchro = Button(fen, text='SYNCHRO', width='10',bg='light sky blue', command=synchroDir)
btnSynchro.grid(row=3, column=10, padx=3, pady=8)

##----- Bouton Mode Continu ON/OFF -----##
btnContinuOn = Button(fen, text='ON', width='10',bg='green', command=modeContinuOn)
btnContinuOn.grid(row=5, column=10, padx=3, pady=8)

btnContinuOff = Button(fen, text='OFF', width='10',bg='red', command=modeContinuOff)
btnContinuOff.grid(row=6, column=10, padx=3, pady=8)

lblMode=Label(fen, font=("Helvetica", 6))
lblMode.grid(row=7, column=10, padx=3, pady=8)

##----- Bouton afficher BDD -----##
bouton_bdd = Button(fen, text='BDD', width='10',bg='orange', command=afficherBDD)
bouton_bdd.grid(row=19,column=10, padx=3, pady=10)

##----- Bouton Quitter -----##
bouton_quitter = Button(fen, text='Quitter', width='10',bg='red', command=fen.destroy)
bouton_quitter.grid(row=20,column=10, padx=3, pady=10)


##----- Entry Extension -----##
lblExtension = Label(fen, text = "Extension:")
lblExtension.grid(row=3,column=4, padx=3, pady=10)

EtyExtension = ExtEntry(fen)
EtyExtension.grid(row=3,column=5, padx=3, pady=10)

##----- Les évènements -----##
fen.bind("<Escape>", remiseZero)

##----- Programme principal -----##
fen.mainloop()# Boucle d'attente des événements