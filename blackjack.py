import random

# Définition des classes Carte et CarteBlackjack
class Carte:
    def __init__(self, enseigne, valeur):
        self.enseigne = enseigne
        self.valeur = valeur

    def __repr__(self):
        return f"{self.valeur} de {self.enseigne}"

class CarteBlackjack(Carte):
    def valeur_blackjack(self):
        if self.valeur in ["valet", "dame", "roi"]:
            return 10
        elif self.valeur == "as":
            return [1, 11]
        else:
            return int(self.valeur)

# Classe Croupier
class Croupier:
    def __init__(self):
        self.jeu_de_cartes = [CarteBlackjack(enseigne, valeur) for enseigne in ["pique", "coeur", "trèfle", "carreau"] for valeur in ["as", "2", "3", "4", "5", "6", "7", "8", "9", "10", "valet", "dame", "roi"]]
        random.shuffle(self.jeu_de_cartes)
        self.main = []

    def distribuer_carte(self):
        return self.jeu_de_cartes.pop()

    def ajouter_carte(self, carte):
        self.main.append(carte)

    def calculer_score(self):
        score = 0
        as_present = False
        for carte in self.main:
            valeur = carte.valeur_blackjack()
            if isinstance(valeur, list):
                as_present = True
                score += 11
            else:
                score += valeur

        if score > 21 and as_present:
            score -= 10

        return score
        
    def distribuer_carte(self):
        if not self.jeu_de_cartes:  # Vérifier si le jeu de cartes est vide
            self.jeu_de_cartes = [CarteBlackjack(enseigne, valeur) for enseigne in ["pique", "coeur", "trèfle", "carreau"] for valeur in ["as", "2", "3", "4", "5", "6", "7", "8", "9", "10", "valet", "dame", "roi"]]
            random.shuffle(self.jeu_de_cartes)  # Remélanger le jeu de cartes
        return self.jeu_de_cartes.pop()

# Classe Joueur
class Joueur:
    def __init__(self, bankroll):
        self.main = []
        self.bankroll = bankroll
        self.mise = 0

    def ajouter_carte(self, carte):
        self.main.append(carte)

    def calculer_score(self):
        score = 0
        as_present = False
        for carte in self.main:
            valeur = carte.valeur_blackjack()
            if isinstance(valeur, list):
                as_present = True
                score += 11
            else:
                score += valeur

        if score > 21 and as_present:
            score -= 10

        return score


# Fonctions de jeu
def tirer(croupier, joueur_ou_croupier):
    carte = croupier.distribuer_carte()
    joueur_ou_croupier.ajouter_carte(carte)

    if isinstance(joueur_ou_croupier, Joueur):
        print(f"Carte tirée pour le joueur : {carte}")
        print(f"Score actuel du joueur : {joueur_ou_croupier.calculer_score()}")
    else:
        print(f"Carte tirée pour le croupier : {carte}")
        # Vous pouvez choisir d'afficher ou de masquer cette information
        print(f"Score actuel du croupier : {joueur_ou_croupier.calculer_score()}")

def jouer_croupier(croupier):
    while croupier.calculer_score() < 17:
        croupier.ajouter_carte(croupier.distribuer_carte())
        print(f"Carte tirée pour le croupier : {croupier.main[-1]}")
        print(f"Score actuel du croupier : {croupier.calculer_score()}")

# Boucle principale du jeu
def jouer_blackjack():
    croupier = Croupier()
    joueur = Joueur(1000)  # Exemple de bankroll
    continuer = True

    while continuer:
        joueur.main = []
        croupier.main = []
        mise = obtenir_mise(joueur)
        initialiser_main(croupier, joueur)

        # Afficher la main initiale et le score
        print("Votre main initiale :", afficher_main(joueur))
        print("Votre score initial :", joueur.calculer_score())
        print("Main initiale du croupier :", afficher_main(croupier), "[Une carte cachée]")

        while choix_du_joueur():
            tirer(croupier, joueur)
            if joueur.calculer_score() > 21:
                print("Vous avez dépassé 21.")
                break

        # Jouer la main du croupier si le joueur ne dépasse pas 21
        if joueur.calculer_score() <= 21:
            while croupier.calculer_score() < 17:
                tirer(croupier, croupier)
                print(f"Le croupier tire une carte. Score du croupier : {croupier.calculer_score()}")

        # Afficher les mains finales et les scores
        print(f"Votre main finale : {afficher_main(joueur)}")
        print(f"Votre score final : {joueur.calculer_score()}")
        print(f"Main finale du croupier : {afficher_main(croupier)}")
        print(f"Score final du croupier : {croupier.calculer_score()}")

        # Déterminer et afficher le résultat
        resultat = determiner_gagnant(croupier, joueur)
        print("Résultat de la main :", resultat)

        # Demander au joueur s'il souhaite continuer
        continuer_rep = input("Voulez-vous jouer une autre main ? (oui/non) ")
        continuer = continuer_rep.lower() == "oui"

def obtenir_mise(joueur):
    while True:
        try:
            mise = int(input("Entrez votre mise : "))
            if 0 < mise <= joueur.bankroll:
                joueur.mise = mise
                joueur.bankroll -= mise
                return mise
            else:
                print(f"Veuillez entrer une mise valide. Votre bankroll est de {joueur.bankroll}.")
        except ValueError:
            print("Veuillez entrer un nombre valide pour la mise.")

def initialiser_main(croupier, joueur):
    joueur.ajouter_carte(croupier.distribuer_carte())
    croupier.ajouter_carte(croupier.distribuer_carte())
    joueur.ajouter_carte(croupier.distribuer_carte())
    croupier.ajouter_carte(croupier.distribuer_carte())

    # Afficher la première carte du croupier et laisser la seconde cachée
    print("Main du croupier :", croupier.main[0], "[Cachée]")
    print("Votre main :", afficher_main(joueur))
def afficher_main(joueur_ou_croupier):
    return ', '.join(str(carte) for carte in joueur_ou_croupier.main)


def choix_du_joueur():
    while True:
        reponse = input("Voulez-vous tirer une carte ? (oui/non) ")
        if reponse.lower() in ["oui", "non"]:
            return reponse.lower() == "oui"
        else:
            print("Réponse non valide. Veuillez répondre par 'oui' ou 'non'.")

def determiner_gagnant(croupier, joueur):
    score_joueur = joueur.calculer_score()
    score_croupier = croupier.calculer_score()

    if score_joueur > 21:
        return "Vous avez perdu, dépassement de 21."
    elif score_croupier > 21:
        return "Vous avez gagné, le croupier a dépassé 21."
    elif score_joueur > score_croupier:
        return "Vous avez gagné, votre score est plus élevé."
    elif score_joueur < score_croupier:
        return "Vous avez perdu, le score du croupier est plus élevé."
    else:
        return "Égalité."

jouer_blackjack()












   
   
