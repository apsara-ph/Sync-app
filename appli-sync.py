##----- Importation des Modules -----##
from tkinter import *
from tkinter import filedialog
import os.path, time
import filecmp
import subprocess
import os, shutil

##----- Variables globales -----##
dirPath1= "ProjetSynchro/monDossier1"
dirPath2= "ProjetSynchro/monDossier2"
dirPath3= "ProjetSynchro/monDossier3"

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

def checkDirExistance(dirPath):# Vérification de l'existance d'un chemin de dossier
    res=False
    if os.path.isdir(dirPath):
        res=True
    return res


def compareDirBIS(d1,d2):# Comparaison des fichiers entre deux dossiers
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
                if (synchroDirBIS(d1+"/"+str(c[i]), d2+"/"+str(c[i]))==True):# A REVOIR
                    c1.append(c[i])
                else:
                    c2.append(c[i])
        if (c2==[]):
            res = True
    return res




def compareDir():# Comparaison des fichiers entre deux dossiers
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
            #filecmp.dircmp(d1, d2).report_full_closure()   
            l=filecmp.dircmp(d1, d2).left_only
            r=filecmp.dircmp(d1, d2).right_only
            c=filecmp.dircmp(d1, d2).common

            lblElementInLeftOnly.configure(text=l)
            lblElementInRightOnly.configure(text=r)
            #lblElementCommon.configure(text=c) #lblElementCommon.configure(text='%s' % c)
            c1=[]
            c2=[]
            for i in range(len(c)):
                if os.path.isfile(d1+"/"+str(c[i]))==True:
                    if (filecmp.cmp(d1+"/"+str(c[i]), d2+"/"+str(c[i]), shallow=True)==True):
                        c1.append(c[i])
                    else:
                        c2.append(c[i])
                else:
                    if (compareDirBIS(d1+"/"+str(c[i]), d2+"/"+str(c[i]))==True):# A REVOIR
                        c1.append(c[i])
                    else:
                        c2.append(c[i])
            lblElementCommonTrue.configure(text=c1)
            lblElementCommonFalse.configure(text=c2)
    else :
        print("Désolé, il y a une erreur sur la saisie des dossiers")

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
    print("Analyse des manipulations de synchronisation")
    if(d1==d2):
        print("Vous avez sélectionné le même dossier")
    else:
        for i in range (len(l)):
            print(l[i] + " à copier")
            if os.path.isfile(d1+"/"+str(l[i]))==True:
                shutil.copy(d1+"/"+str(l[i]), d2+"/"+str(l[i])) #copie de fichier
                nb_creatBIS+=1
            else:
                shutil.copytree(d1+"/"+str(l[i]), d2+"/"+str(l[i])) #copie de repertoire
                nb_creatBIS+=1
        l=[]
        for i in range (len(r)):
            print(r[i] + " à supprimer")
            if os.path.isfile(d2+"/"+str(r[i]))==True:
                os.remove(d2+"/"+str(r[i])) #supression d'un fichier
                nb_delBIS+=1
            else:
                shutil.rmtree(os.path.join(d2,str(r[i]))) #supression d'un repertoire
                nb_delBIS+=1
        r=[]
        for i in range(len(c)):
            if os.path.isfile(d1+"/"+str(c[i]))==True:
                if (filecmp.cmp(d1+"/"+str(c[i]), d2+"/"+str(c[i]), shallow=True)==True):
                    print(str(c[i])+": OK !")
                else:
                    print(c[i]+": Contenu de fichier différent")
                    os.remove(d2+"/"+str(c[i])) # supression de l'ancien fichier
                    shutil.copy(d1+"/"+str(c[i]), d2+"/"+str(c[i])) #copie du nouveau fichier
                    nb_modifBIS+=1
            else:
                if (synchroDirBIS(d1+"/"+str(c[i]), d2+"/"+str(c[i]))==True):# A REVOIR
                    print(str(c[i])+": OK !")
                else:
                    shutil.rmtree(os.path.join(d2,str(c[i])))
                    shutil.copytree(d1+"/"+str(c[i]), d2+"/"+str(c[i]))
                    nb_modifBIS+=1
        res=True
    return res


def synchroDir():
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
            print(l[i] + " à copier")
            if os.path.isfile(d1+"/"+str(l[i]))==True:
                shutil.copy(d1+"/"+str(l[i]), d2+"/"+str(l[i])) #copie de fichier
                nb_creat+=1
            else:
                shutil.copytree(d1+"/"+str(l[i]), d2+"/"+str(l[i])) #copie de repertoire
                nb_creat+=1
        l=[]
        for i in range (len(r)):
            print(r[i] + " à supprimer")
            if os.path.isfile(d2+"/"+str(r[i]))==True:
                os.remove(d2+"/"+str(r[i])) #supression d'un fichier
                nb_del+=1
            else:
                shutil.rmtree(os.path.join(d2,str(r[i]))) #supression d'un repertoire
                nb_del+=1
        r=[]
        for i in range(len(c)):
            if os.path.isfile(d1+"/"+str(c[i]))==True:
                if (filecmp.cmp(d1+"/"+str(c[i]), d2+"/"+str(c[i]), shallow=True)==True):
                    print(str(c[i])+": OK !")
                else:
                    print(c[i]+": Contenu de fichier différent")
                    os.remove(d2+"/"+str(c[i])) # supression de l'ancien fichier
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
    lblElementInLeftOnly.configure(text='')
    lblElementInRightOnly.configure(text='')
    #lblElementCommon.configure(text='')
    lblElementCommonTrue.configure(text='')
    lblElementCommonFalse.configure(text='')


def helloWorld():
    lblResultComparison.configure(text="hello world")

def deleteAnalysis():
    lblEtat.configure(text="")
    lblDifferences.configure(text="")
    lblOnlyLeftElement.configure(text="")
    lblElementInLeftOnly.configure(text="")
    lblOnlyRightElement.configure(text="")
    lblElementInRightOnly.configure(text="")
    #lblElementCommon.configure(text="")
    lblSimilarities.configure(text="")
    lblSameElementFalse.configure(text="")
    lblElementCommonFalse.configure(text="")
    lblSameElementTrue.configure(text="")
    lblElementCommonTrue.configure(text='')



def sizeDir(path): # Calcul de la taille d'un dossier en octets
    size=0
    if checkDirExistance(path)==True:
        for root, dirs, files in os.walk(path):
            for fic in files:
                size+=os.path.getsize(os.path.join(root,fic))
        return size
    else:
        print("Le chemin saisie n'existe pas")

#----- Création de la fenêtre -----##
fen = Tk()
fen.geometry("1000x700")
fen.title('Synchronization')

#Titre 
lblLeftDir=Label(fen , text ="Folder sync...", font=("Helvetica", 16))
lblLeftDir.grid(row=0, column=1, columnspan=10, padx=3, pady=8, sticky=S+W+E)


#Dossier gauche
lblLeftDir=Label(fen , text ="Left Folder :")
lblLeftDir.grid(row=1, column=1, padx=3, pady=8, sticky=S+W+E)

lblLeft = Label(fen,bg = 'white', width="30", highlightbackground = "blue", font=("Helvetica", 10),
                    highlightcolor= "green", relief=FLAT)
lblLeft.grid(row=1, column=2, padx=3, pady=8, sticky=S+W+E)

lblLeftDirSize = Label(fen,bg = 'white', width="30", highlightbackground = "black", font=("Helvetica", 10),
                    highlightcolor= "green", relief=FLAT)
lblLeftDirSize.grid(row=2, column=2, padx=3, pady=8, sticky=S+W+E)

btnLeftDir = Button(fen, text='Browse...', width='10',bg='blue', command = selectLeftFolder)
btnLeftDir.grid(row=1, column=3, padx=3, pady=8, sticky=S+W+E)



#Dossier de droite
lblRightDir=Label(fen , text ="Right Folder :")
lblRightDir.grid(row=1, column=6, padx=3, pady=8, sticky=S+W+E)

lblRight = Label(fen,bg = 'white', width="30", highlightbackground = "blue", font=("Helvetica", 10),
                    highlightcolor= "green", relief=FLAT)
lblRight.grid(row=1, column=7, padx=3, pady=8, sticky=S+W+E)

lblRightDirSize = Label(fen,bg = 'white', width="30", highlightbackground = "black", font=("Helvetica", 10),
                    highlightcolor= "green", relief=FLAT)
lblRightDirSize.grid(row=2, column=7, padx=3, pady=8, sticky=S+W+E)

btnRightDir = Button(fen, text='Browse...', width='10',bg='blue', command = selectRightFolder)
btnRightDir.grid(row=1, column=8, padx=3, pady=8, sticky=S+W+E)


#entLeftDir.focus_set()
#entRightDir.focus_set()







#Resultat

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
lblOperations.grid(row=20, column=1, columnspan=10, padx=3, pady=8)

lblAllOperations=Label(fen)
lblAllOperations.grid(row=21, column=1, columnspan=10, padx=3, pady=8)

##----- Bouton Start -----##

btnStartAnalysis = Button(fen, text='ANALYSIS', width='8',bg='green', command=compareDir)
btnStartAnalysis.grid(row=1, column=9, padx=3, pady=8)
#btnStartAnalysis.focus_set()

##----- Bouton Delete -----##
btnDeleteAnalysis = Button(fen, text='CANCEL', width='8',bg='green', command=deleteAnalysis)
btnDeleteAnalysis.grid(row=1, column=10, padx=3, pady=8)

##----- Bouton Synchronisation -----##
btnSynchro = Button(fen, text='Synchronization', width='10',bg='blue', command=synchroDir)
btnSynchro.grid(row=5, column=10, padx=3, pady=8)

##----- Bouton Quitter -----##
bouton_quitter = Button(fen, text='Quitter', width='10',bg='red', command=fen.destroy)
bouton_quitter.grid(row=6,column=10, padx=3, pady=10)


##----- Les évènements -----##
fen.bind("<Escape>", remiseZero)


##----- Programme principal -----##
fen.mainloop()# Boucle d'attente des événements