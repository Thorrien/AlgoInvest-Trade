import csv
from itertools import combinations
import time


class Portefeuille:
    id = 1

    def __init__(self):
        self.id = Portefeuille.id + 1
        Portefeuille.id += 1
        self.solde_initial = 500
        self.listeActions = []
        self.achatTotal = 0
        self.valeurFinale = 0
        self.bénéfice = 0

    def achatAction(self, action):
        self.listeActions.append(action)
        self.solde_initial -= action.valeur
        self.achatTotal += action.valeur

    def calculbénéfice(self):
        for action in self.listeActions:
            self.valeurFinale += (action.valeur*(1+(action.bénéfice/100)))
            self.bénéfice += (action.valeur*(action.bénéfice/100))
        
    def afficherPortefeuille(self):
        print(f" ------ portefeuille {self.id}-----------")
        print(f"Nb Actions : {len(self.listeActions)} Achat initial : {self.achatTotal} Valeur Finale : {self.valeurFinale} Bénéfice : {self.bénéfice}")
        print("Nom, Valeur Initiale, Bénéfice sous 2 ans, Valeur finale ")
        for action in self.listeActions:
            print(f"{action.name}, {action.valeur} €, {action.bénéfice} %, {action.valeur*(1+(action.bénéfice/100))} €")


class Action:

    def __init__(self, name, valeur, bénéfice):
        self.name = name
        self.valeur = valeur
        self.bénéfice = bénéfice

    def printAction(self):
            print(f"Nom : {self.name}")
            print(f"Valeur : {self.valeur}")
            print(f"Bénéfice sous 2 ans : {self.bénéfice}")
            print("------------------------------------")


class LecteurBDDCSV:

    def __init__(self):
        self.listeAction = []

    def creationBDD(self):
        with open('data.csv', 'r', newline='') as fichier_csv:
            lecteur_csv = csv.reader(fichier_csv)
            next(lecteur_csv)
            for ligne in lecteur_csv:
                nom = ligne[0]
                valeur = int(ligne[1])
                bénéfice = int(ligne[2].split('%')[0])
                self.listeAction.append(Action(nom, valeur, bénéfice))

    def printListe(self):
        for element in self.listeAction:
            element.printAction()


class Algorithme:

    def __init__(self):
        self.listePossibilités = []

    def générerPossibilité(self, list):
        for num in range(len(list)):
            for i in combinations(list, num):
                if self.soldeFinal(i) >= 0:
                    portefeuilleTemporaire = Portefeuille()
                    for element in i: 
                        portefeuilleTemporaire.achatAction(element)
                    portefeuilleTemporaire.calculbénéfice()
                    self.listePossibilités.append(portefeuilleTemporaire)

    def préciserTop(self):
        self.listePossibilités.sort(
            key=lambda portefeuille: portefeuille.bénéfice,
            reverse=True)
        self.printPossibilité(0)

    def printPossibilité(self, index):
        print("--------------------------")
        print("Le meilleur investissement est la simulation N° ",
              f"{self.listePossibilités[index].id} constitué des ",
              "actions suivantes : ")
        self.listePossibilités[index].afficherPortefeuille()

    def soldeFinal(self, listAction):
        solde = 500
        for element in listAction:
            solde -= element.valeur
        return solde

    def printPossibilités(self):
        self.listePossibilités.sort(
            key=lambda portefeuille: portefeuille.bénéfice)
        for element in self.listePossibilités:
            print("--------------------------")
            print(f"{element.id} : Nb Actions : {len(element.listeActions)} ",
                  f"Achat initial : {element.achatTotal} Valeur Finale :",
                  f" {element.valeurFinale} Bénéfice : {element.bénéfice}")
            print("--------------------------")

def main():
    tps3 = time.time()
    lecteur = LecteurBDDCSV()
    lecteur.creationBDD()
    algo = Algorithme()
    algo.générerPossibilité(lecteur.listeAction)
    tps4 = time.time()
    print(f'-------------------------------')
    print(f'Toutes les simulations ont été éffectuées en {(tps4 - tps3)} secondes')
    print(f'-------------------------------')
    algo.préciserTop()
    
main()