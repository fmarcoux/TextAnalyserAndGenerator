import networkx as nx
import os
import math
from random import randint


class LectureFichier:
    def __init__(self):
        self.ListeMot=list()
        self.DictionnaireUnigramme={}
        self.Graph=nx.Graph()
        self.DictionnaireAComparer={}
        self.ListeMotCommun=[]

    def EnleverCaractere(self,liste):
        PONC = ["!", '"', "'", ")", "(", ",", ".", ";", ":", "?", "-", "_","—"]
        ListeRetour = []
        NewListe = liste.split()
        for mot in NewListe:
            for signe in PONC:
                mot = mot.replace(signe," ")
            mot = mot.replace("\n", " ")
            mot = mot.lstrip()
            mot = mot.rstrip()
            if len(mot)>2:
                ListeRetour.append(mot)
        return ListeRetour

    def GetListe(self):
        return(self.ListeMot)

    def LireAComparer(self,path,modelecture):

        ListeTemp=[]
        f=open(path,'r', encoding="utf8")
        for lines in f:
            ListeTemp=self.EnleverCaractere(lines)
            if modelecture ==2:
                self.DictionnaireAComparer.clear()
                for index in range(len(ListeTemp) - 2):
                    if str(ListeTemp[index] + " " + ListeTemp[index + 1]) in self.DictionnaireAComparer:
                        self.DictionnaireAComparer[str(ListeTemp[index] + " " + ListeTemp[index + 1])] += 1
                    else:
                        self.DictionnaireAComparer[str(ListeTemp[index] + " " + ListeTemp[index + 1])] = 1
            elif modelecture==1:
                self.DictionnaireAComparer.clear()
                for i in range(len(ListeTemp) - 1):
                    if ListeTemp[i] in self.DictionnaireAComparer:
                        self.DictionnaireAComparer[ListeTemp[i]] += 1
                    else:
                        self.DictionnaireAComparer[ListeTemp[i]] = 1
                else:
                    print("mauvais mode de lecture le fichier n'a pas ete lu")


    def Lire_fichierUnigramme(self,repertoire,auteur): #Analyse un auteur et update le dictionnaire
        # que le dict de la freq des mots
        self.DictionnaireUnigramme.clear()
        self.ListeMot.clear()
        self.Graph.clear()
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
                    ListeNouveauMot = self.EnleverCaractere(lines)
                    for i in range(len(ListeNouveauMot) - 1):
                        if ListeNouveauMot[i] in self.DictionnaireUnigramme:
                            self.DictionnaireUnigramme[ListeNouveauMot[i]] += 1
                            self.ListeMot.append(ListeNouveauMot[i])
                        else:
                            self.DictionnaireUnigramme[ListeNouveauMot[i]] = 1
                            self.ListeMot.append(ListeNouveauMot[i])
                f.close()
        else:
            print("pas d'auteur nomme :", auteur)# #


    def Lire_fichierModeBigramme(self,repertoire,auteur):  # li un fichier en mode bigramme et update le graph et la iste des mots et le dict
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
                    TempListe=self.EnleverCaractere(lines)
                    for index in range(len(TempListe) - 1):
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

    def partition(self,arr, low, high):
        i = (low - 1)  # index of smaller element
        pivot = arr[high]  # pivot

        for j in range(low, high):

            # If current element is smaller than or
            # equal to pivot
            if arr[j] <= pivot:
                # increment index of smaller element
                i = i + 1
                arr[i], arr[j] = arr[j], arr[i]

        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return (i + 1)

    # The main function that implements QuickSort
    # arr[] --> Array to be sorted,
    # low  --> Starting index,
    # high  --> Ending index

    # Function to do Quick sort
    def quickSort(self,arr, low, high):
        if low < high:
            # pi is partitioning index, arr[p] is now
            # at right place
            pi = self.partition(arr, low, high)

            # Separately sort elements before
            # partition and after partition
            self.quickSort(arr, low, pi - 1)
            self.quickSort(arr, pi + 1, high)


    def printUnigramme(self):
            print("Dictionnaire de la frequence des mots dans le texte : \n")
            print(self.DictionnaireUnigramme)


    def PrintFrequenceNMot(self,Frequence):
        sortedliste=sorted(self.DictionnaireUnigramme,key=self.DictionnaireUnigramme.get,reverse=True)
        count = 0
        for w in sorted(self.DictionnaireUnigramme,key=self.DictionnaireUnigramme.get,reverse=True):

            if count !=Frequence:
                print(w,self.DictionnaireUnigramme[w])
                count+=1

    def GenererTexteAleatoire(self,NombreMot,Frequence):
        TexteFinale = list()
        ListeSuffixPossible=[]
        FirstMot=str(self.ListeMot[randint(0,(len(self.ListeMot)-1))]+" "+self.ListeMot[randint(0,(len(self.ListeMot)-1))])
        while not self.Graph.has_node(FirstMot):
            FirstMot = str(self.ListeMot[randint(0,(len(self.ListeMot)-1))] + " "
                           + self.ListeMot[randint(0,(len(self.ListeMot)-1))])
        TexteFinale.append(FirstMot)
        print("mot trouve:"+FirstMot)
        Edges=(self.Graph.edges(FirstMot))
        for index in range(NombreMot):
            for edges in Edges:
                data = self.Graph.get_edge_data(edges[0], edges[1])
                ListeSuffixPossible.append([data["weight"], edges[1]])
            SortedList = sorted(ListeSuffixPossible, reverse=True)
            InfoCurrent=str(edges[0]).split()
            if Frequence != 0:
                TempFreq = Frequence
                if Frequence > int(len(SortedList) - 1):
                    if len(SortedList)!=0:
                        TempFreq = int(len(SortedList)-1)
                        NextMot = SortedList[TempFreq]
                    else:
                        break
                else:
                    NextMot = SortedList[Frequence - 1]
            else:
                if len(SortedList) != 0:
                    random=randint(0, len(SortedList))
                    if random==0:
                        print(SortedList[0])
                        NextMot = SortedList[random]
                    else:
                        NextMot=SortedList[random-1]
            TexteFinale.append(NextMot[1])
            print("Next mot: " + str(NextMot) + "\n" + "InfoCurrent :" + str(InfoCurrent))
            Edges = self.Graph.edges(InfoCurrent[1] + " " + NextMot[1])
            SortedList.clear()
            ListeSuffixPossible.clear()
        print(TexteFinale)


    def ComparerAuteurAvecTexte(self,repertoire,auteur,texteinconu,modecomparaison):
        ValCal=0
        if modecomparaison ==2:
            self.Lire_fichierModeBigramme()
            self.LireAComparer(texteinconu, modecomparaison)
        elif modecomparaison==1:
            self.Lire_fichierUnigramme()
            self.LireAComparer(texteinconu,modecomparaison)
        else: return 0
        for word in self.DictionnaireAComparer:
            if word in self.DictionnaireUnigramme:
                DifFreq=abs(self.DictionnaireAComparer[word]-self.DictionnaireUnigramme[word])
                self.ListeMotCommun.append(word)
                ValCal+=pow(DifFreq,2)
        Terminos=math.sqrt(ValCal)
        print(terminos)











