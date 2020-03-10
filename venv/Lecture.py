import networkx as nx
import os
import math
from random import randint

'''
marf2910
lafo0701
'''
class LectureFichier:
    def __init__(self):
        self.ListeMot=list()
        self.DictionnaireUnigramme={}
        self.Graph=nx.Graph()
        self.DictionnaireAComparer={}
        self.ListeMotCommun=[]
        self.DictonnaireAuteur={}


    def addAuteur(self, auteur):
        if auteur in self.DictonnaireAuteur:
            None
        else:
            if "." in auteur:
                None
            else:
                self.DictonnaireAuteur[auteur] = 0

    def EnleverCaractere(self,liste):
        PONC = ["!", '"', "'", ")", "(", ",", ".", ";", ":", "?", "-", "_","—"]
        ListeRetour = []
        liste=liste.replace("\n"," ")
        NewListe = liste.split()
        AutreListe=[]
        for mot in NewListe:
            for signe in PONC:
                mot = mot.replace(signe," ")
            mot=mot.lower()
            AutreListe=mot.split()
            for mot in AutreListe:
                if len(mot)>2:
                    ListeRetour.append(mot)
        return ListeRetour

    def EnleverMot2Lettre(self,liste):
        ListeRetour=[]
        liste = liste.replace("\n", " ")
        liste = liste.lower()
        NewListe = liste.split()
        for mot in NewListe:
            if len(mot) > 2:
                ListeRetour.append(mot)
        return ListeRetour

    def GetListe(self):
        return(self.ListeMot)

    def GetRandomMot(self):
        FirstMot = str(self.ListeMot[randint(0, (len(self.ListeMot) - 1))] + " " + self.ListeMot[
            randint(0, (len(self.ListeMot) - 1))])
        while not self.Graph.has_node(FirstMot):
            FirstMot = str(self.ListeMot[randint(0, (len(self.ListeMot) - 1))] + " "
                           + self.ListeMot[randint(0, (len(self.ListeMot) - 1))])
        return FirstMot

    def LireAComparer(self,path,modelecture):
        self.DictionnaireAComparer.clear()
        ListeTemp=[]
        f=open(path,'r', encoding="utf8")
        for lines in f:
            ListeTemp=self.EnleverCaractere(lines)
            if modelecture ==2:
                for index in range(len(ListeTemp)-1):
                    if str(ListeTemp[index] + " " + ListeTemp[index + 1]) in self.DictionnaireAComparer:
                        self.DictionnaireAComparer[str(ListeTemp[index] + " " + ListeTemp[index + 1])] += 1
                    else:
                        self.DictionnaireAComparer[str(ListeTemp[index] + " " + ListeTemp[index + 1])] = 1
            elif modelecture==1:
                for i in range(len(ListeTemp)):
                    if ListeTemp[i] in self.DictionnaireAComparer:
                        self.DictionnaireAComparer[ListeTemp[i]] += 1
                    else:
                        self.DictionnaireAComparer[ListeTemp[i]] = 1
            else:
                print("mauvais mode de lecture le fichier n'a pas ete lu")

    def Lire_fichierUnigramme(self,repertoire,auteur,ponctuation): #Analyse un auteur et update le dictionnaire
        # que le dict de la freq des mots
        self.DictionnaireUnigramme.clear()
        self.ListeMot.clear()
        ListeAuteur = os.listdir(repertoire)
        ListeAuteur.__delitem__(0)
        repertoireauteur = repertoire + "\\" + auteur
        if auteur in ListeAuteur:
            ListeTexte = os.listdir(repertoireauteur)
            ListeTexte.__delitem__(0)
            for texte in ListeTexte:
                path = repertoireauteur + "\\" + texte
                f = open(path, 'r', encoding="utf8")
                for lines in f:
                    if ponctuation:
                        TempListe = self.EnleverCaractere(lines)
                    else:
                        TempListe = self.EnleverMot2Lettre(lines)
                    for i in range(len(TempListe)):
                        if TempListe[i] in self.DictionnaireUnigramme:
                            self.DictionnaireUnigramme[TempListe[i]] += 1
                            self.ListeMot.append(TempListe[i])
                        else:
                            self.DictionnaireUnigramme[TempListe[i]] = 1
                            self.ListeMot.append(TempListe[i])
                f.close()
        else:
            if "." not in auteur:
                print("pas d'auteur nomme :", auteur)# #


    def Lire_fichierModeBigramme(self,repertoire,auteur,ponctuation):  # li un fichier en mode bigramme et update le graph et la iste des mots et le dict
        self.DictionnaireUnigramme.clear()
        self.ListeMot.clear()
        self.Graph.clear()
        ListeAuteur = os.listdir(repertoire)
        ListeAuteur.__delitem__(0)
        repertoireauteur = repertoire + "\\" + auteur
        if auteur in ListeAuteur:
            ListeTexte = os.listdir(repertoireauteur)
            ListeTexte.__delitem__(0)
            for file in ListeTexte:
                path = repertoireauteur + "\\" + file
                f = open(path, 'r', encoding="utf8")
                for lines in f:
                    if ponctuation:
                        TempListe=self.EnleverCaractere(lines)
                    else:
                        TempListe=self.EnleverMot2Lettre(lines)
                    for index in range(len(TempListe)-1):
                        self.ListeMot.append(TempListe[index])
                        if str(TempListe[index] + " " + TempListe[index + 1]) in self.DictionnaireUnigramme:
                            self.DictionnaireUnigramme[str(TempListe[index] + " " + TempListe[index + 1])] += 1
                        else:
                            self.DictionnaireUnigramme[str(TempListe[index] + " " + TempListe[index + 1])] = 1
                        if index <(len(TempListe)-2):
                            if self.Graph.has_node(TempListe[index]+" "+TempListe[index+1]):
                                if self.Graph.has_edge(TempListe[index]+" "+TempListe[index+1], TempListe[index + 2]):
                                    data = self.Graph.get_edge_data(TempListe[index]+" "+TempListe[index+1], TempListe[index + 2])
                                    self.Graph.add_edge(TempListe[index]+" "+TempListe[index+1], TempListe[index + 2], weight=data["weight"] + 1)
                                else:
                                    self.Graph.add_edge(TempListe[index]+" "+TempListe[index+1], TempListe[index + 2], weight=1)
                            else:
                                self.Graph.add_node(TempListe[index]+" "+TempListe[index+1])
                                self.Graph.add_edge(TempListe[index]+" "+TempListe[index+1], TempListe[index + 2], weight=1)
                f.close()

    def printDictionnaire(self):
            print("Dictionnaire de la frequence des mots dans le texte : \n")
            print(self.DictionnaireUnigramme)

    def PrintFrequenceNMot(self,Frequence,auteur):
        if len(self.DictionnaireUnigramme)==0:
            None
        else:
            sortedliste=sorted(self.DictionnaireUnigramme,key=self.DictionnaireUnigramme.get,reverse=True)
            if Frequence>(len(sortedliste)):
                Frequence=len(sortedliste)
            print("dans les textes de :",auteur, "le", Frequence,"e mot le plus frequent est : ", sortedliste[Frequence])

    def motRandom(self):
        FirstMot = str(self.ListeMot[randint(0, (len(self.ListeMot) - 1))] + " " + self.ListeMot[
            randint(0, (len(self.ListeMot) - 1))])
        while not self.Graph.has_node(FirstMot):
            FirstMot = str(self.ListeMot[randint(0, (len(self.ListeMot) - 1))] + " "
                           + self.ListeMot[randint(0, (len(self.ListeMot) - 1))])
        return FirstMot

    def GenererTexteAleatoire(self, NombreMot, Frequence, nomfichier, auteur):
        TexteFinale = list()
        ListeSuffixPossible = []
        FirstMot = self.motRandom()
        TexteFinale.append(FirstMot)
        Edges = (self.Graph.edges(FirstMot))
        for index in range(NombreMot):
            for edges in Edges:
                data = self.Graph.get_edge_data(edges[0], edges[1])
                ListeSuffixPossible.append([data["weight"], edges[1]])
            SortedList = sorted(ListeSuffixPossible, reverse=True)
            if len(SortedList) == 0:
                TexteFinale.append(".")
                FirstMot = self.motRandom()
                TexteFinale.append(FirstMot)
                Edges = (self.Graph.edges(FirstMot))
                for edges in Edges:
                    data = self.Graph.get_edge_data(edges[0], edges[1])
                    ListeSuffixPossible.append([data["weight"], edges[1]])
                SortedList = sorted(ListeSuffixPossible, reverse=True)
            InfoCurrent = str(edges[0]).split()
            if Frequence != 0:
                TempFreq = Frequence
                if Frequence > int(len(SortedList) - 1):
                    if len(SortedList) != 0:
                        TempFreq = int(len(SortedList) - 1)
                        NextMot = SortedList[TempFreq]
                    else:
                        break
                else:
                    NextMot = SortedList[Frequence - 1]
            else:
                if len(SortedList) != 0:
                    random = randint(0, len(SortedList))
                    if random == 0:
                        NextMot = SortedList[random]
                    else:
                        NextMot = SortedList[random - 1]
            TexteFinale.append(NextMot[1])
            if len(InfoCurrent) > 1:
                Edges = self.Graph.edges(InfoCurrent[1] + " " + NextMot[1])
            else:
                Edges = self.Graph.edges(InfoCurrent[0] + " " + NextMot[1])
            SortedList.clear()
            ListeSuffixPossible.clear()
        f = open(nomfichier, "w", encoding="utf-8")
        f.write(auteur + "\nDebut: ")
        for index in range(len(TexteFinale) - 1):
            f.write(TexteFinale[index])
            f.write(" ")
        f.write("\nFin")
        f.close()

    def ComparerAuteurAvecTexte(self,repertoire,auteur,texteinconu,modecomparaison):

        self.ListeMotCommun.clear()
        if modecomparaison ==2:
            self.Lire_fichierModeBigramme(repertoire,auteur,True)
            self.LireAComparer(texteinconu, modecomparaison)
        elif modecomparaison==1:
            self.Lire_fichierUnigramme(repertoire,auteur,True)
            self.LireAComparer(texteinconu,modecomparaison)
        else: return 0

        for word in self.DictionnaireAComparer:
            if word in self.DictionnaireUnigramme:
                self.ListeMotCommun.append(word)
        self.DictonnaireAuteur[auteur] = len(self.ListeMotCommun)
        if "." not in auteur:
            print("selon le repertoire de "+auteur+ " le texte a : "+str(len(self.ListeMotCommun))+" mots en commun avec le fichier de comparaison")

    def ComparerDictionnaireAuteur(self):
        freqMax = 0
        auteur = None
        for a in self.DictonnaireAuteur:
            if freqMax < self.DictonnaireAuteur[a]:
                freqMax = self.DictonnaireAuteur[a]
                auteur = a
        print("L'auteur le plus ressemblant au style de ce texte est: " + auteur)
