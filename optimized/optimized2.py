import csv
import time


class Action:

    def __init__(self, name, valeur, bénéfice):
        self.name = name
        self.valeur = valeur
        self.bénéfice = bénéfice
        self.bénéfice2Ans = (self.valeur*(self.bénéfice/100))

    def printAction(self):
        print("------------------------------------")
        print(f"Nom : {self.name}  Valeur "
              f": {self.valeur}   Bénéfice sous 2 ans : {self.bénéfice} %")


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
        self.meilleurInvestissement = []
        self.bénéficeInvestissement = 0

    def knapScack(self, maximum, listAction):
        n = len(listAction)
        table = [[0 for x in range(maximum + 1)] for X in range(n + 1)]

        for i in range(n+1):
            for j in range(maximum+1):
                if i == 0 or j == 0:
                    table[i][j] = 0
                elif listAction[i-1].valeur <= j:
                    table[i][j] = max(listAction[i-1].bénéfice2Ans
                                      + table[i-1][j-listAction[i-1].valeur],
                                      table[i-1][j])
                else:
                    table[i][j] = table[i-1][j]

        total_benefit = table[n][maximum]
        remaining_capacity = maximum

        for i in range(n, 0, -1):
            if remaining_capacity < 0:
                break
            elif remaining_capacity - listAction[i-1].valeur < 0:
                break
            elif total_benefit == table[i-1][remaining_capacity]:
                continue
            else:
                self.meilleurInvestissement.append(listAction[i-1])
                total_benefit -= listAction[i-1].bénéfice2Ans
                remaining_capacity -= listAction[i-1].valeur

        self.meilleurInvestissement.reverse()
        self.bénéficeInvestissement = table[n][maximum]

    def printTop(self):
        print("--------------------------")
        print("Le meilleur investissement qui génère"
              f"{self.bénéficeInvestissement} est constitué des"
              "actions suivantes : ")
        for element in self.meilleurInvestissement:
            element.printAction()


def main2():

    tps3 = time.time()
    lecteur = LecteurBDDCSV()
    lecteur.creationBDD()
    algo = Algorithme()
    algo.knapScack(500, lecteur.listeAction)
    tps4 = time.time()
    print('-------------------------------')
    print("Toutes les simulations ont été éffectuées "
          f"en {(tps4 - tps3)} secondes")
    print('-------------------------------')
    algo.printTop()


main2()
