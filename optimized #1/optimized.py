import csv
import time


class Action:

    def __init__(self, name, valeur, bénéfice):
        self.name = name
        self.valeur = valeur
        self.bénéfice = bénéfice
        self.bénéfice2Ans = ((self.valeur/100)*(self.bénéfice/100))

    def printAction(self):
        print("------------------------------------")
        print(f"Nom : {self.name}  Valeur : {self.valeur}   ",
              f"Bénéfice sous 2 ans : {self.bénéfice2Ans} ")


class LecteurBDDCSV:

    def __init__(self):
        self.listeAction = []

    def creationBDD(self):
        with open('data.csv', 'r', newline='') as fichier_csv:
            lecteur_csv = csv.reader(fichier_csv)
            next(lecteur_csv)
            for ligne in lecteur_csv:
                if float(ligne[1].replace(",", ".")) > 0 and float(
                        ligne[2].replace(",", ".")) > 0:
                    nom = ligne[0]
                    valeur = int(float(ligne[1].replace(",", "."))*100)
                    bénéfice = float(ligne[2].replace(",", "."))
                    self.listeAction.append(Action(nom, valeur, bénéfice))
            self.listeAction.sort(key=lambda action: action.bénéfice,
                                  reverse=True)

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
                    if (j - listAction[i-1].valeur) >= 0 and (
                            j - listAction[i-1].valeur) < len(table[i-1]):
                        table[i][j] = max(
                            listAction[i-1].bénéfice2Ans +
                            table[i-1][j-listAction[i-1].valeur],
                            table[i-1][j])
                    else:
                        table[i][j] = table[i-1][j]
                else:
                    table[i][j] = table[i-1][j]

        total_benefit = table[n][maximum]
        remaining_capacity = maximum

        for i in range(n, 0, -1):
            if remaining_capacity < 0:
                break
            if total_benefit == table[i-1][remaining_capacity]:
                continue
            if remaining_capacity - listAction[i-1].valeur < 0:
                break
            else:
                self.meilleurInvestissement.append(listAction[i-1])
                total_benefit -= listAction[i-1].bénéfice2Ans
                remaining_capacity -= listAction[i-1].valeur
        print(table[n][maximum])
        self.bénéficeInvestissement = table[n][maximum]

    def printTop(self):
        solde = 0
        bénéfice = 0
        for element in self.meilleurInvestissement:
            element.valeur = round((element.valeur/100), 2)
            bénéfice += element.bénéfice2Ans
            print(f"{element.name} , {element.valeur} ,",
                  f" {element.bénéfice2Ans}")
            solde += element.valeur
        print("--------------------------")
        print("Le meilleur investissement qui a couté ",
              f"{round(solde, 2)} et qui génère {bénéfice} ",
              "est constitué des actions suivantes : ")


def main2():
    tps3 = time.time()
    lecteur = LecteurBDDCSV()
    lecteur.creationBDD()
    algo = Algorithme()
    algo.knapScack(50000, lecteur.listeAction)
    tps4 = time.time()
    print('-------------------------------')
    print("Toutes les simulations ont été ",
          f"éffectuées en {(tps4 - tps3)} secondes")
    print('-------------------------------')
    algo.printTop()


main2()
