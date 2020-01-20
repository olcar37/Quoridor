"""Module permettant l'initiation d'une partie Quoridor et d'y jouer"""


import copy
from netx import *


class QuoridorError(Exception):
    """Classe d'erreur relative au jeu."""

class Quoridor:
    """"Classe permettant de jouer au jeu Quoridor"""

    def __init__(self, joueurs, murs=None):
        """Initialise une partie de Quoridor"""
        # On vérifie si l'argument 'joueurs' est un itérable
        if not isinstance(joueurs, list) and not isinstance(joueurs, tuple):
            raise QuoridorError("L'argument 'joueurs' n'est pas un itérable.")

        # On vérifie que l'itérable 'joueurs' ne contient pas plus de 2 joueurs
        if len(joueurs) > 2:
            raise QuoridorError(
                "L'itérable de joueurs en contient plus de deux.")

        # On vérifie qu'il n'y a pas moins de 2 joueurs
        if len(joueurs) < 2:
            raise QuoridorError(
                "L'itérable de joueurs n'en contient pas deux.")

        # On verifie le type de variable de chaque joueur et copie les données en conséquence
        if isinstance(joueurs[0], str):
            self.joueur1 = copy.deepcopy(joueurs[0])
            self.pos1 = (5, 1)
            self.compteur1 = 10
        elif isinstance(joueurs[0], dict):
            self.joueur1 = copy.deepcopy(joueurs[0]['nom'])
            self.pos1 = copy.deepcopy(joueurs[0]['pos'])
            self.compteur1 = copy.deepcopy(joueurs[0]['murs'])

        if isinstance(joueurs[1], str):
            self.joueur2 = copy.deepcopy(joueurs[1])
            self.pos2 = (5, 9)
            self.compteur2 = 10
        elif isinstance(joueurs[1], dict):
            self.joueur2 = copy.deepcopy(joueurs[1]['nom'])
            self.pos2 = copy.deepcopy(joueurs[1]['pos'])
            self.compteur2 = copy.deepcopy(joueurs[1]['murs'])

        # On vérifie que le nombre de mur plaçable de chaque joueur est adéquat
        if self.compteur1 < 0 or self.compteur1 > 10 or self.compteur2 < 0 or self.compteur2 > 10:
            raise QuoridorError(
                "Le nombre de murs qu'un joueur peut placer est >10 ou négatif.")

        # On copie le contenu de de l'argument 'murs'
        self.hori, self.ver = [], []
        if isinstance(murs, dict):
            if 'horizontaux' in murs:
                self.hori = (copy.deepcopy(murs['horizontaux']))
            if 'verticaux' in murs:
                self.ver = (copy.deepcopy(murs['verticaux']))
        elif murs is not None:
            raise QuoridorError("L'argument 'murs' n'est pas un dictionnaire")

        # On vérifie le total de murs de la partie
        if len(self.hori) + len(self.ver) + self.compteur1 + self.compteur2 != 20:
            raise QuoridorError(
                "Le total des murs placés et plaçable n'est pas égal à 20.")

        # On vérifie la position des joueurs
        if self.pos1 == self.pos2:
            raise QuoridorError("La position d'un joueur est invalide.")

        for pos in [self.pos1, self.pos2]:
            if (pos[0] < 1) or (pos[0] > 9) or (pos[1] < 1) or (pos[1] > 9):
                raise QuoridorError("La position d'un joueur est invalide.")

        # On vérifie si des murs se superposent
        for pos in self.hori:
            if (pos[0] + 1, pos[1]) in self.hori or (pos[0] - 1, pos[1]) in self.hori:
                raise QuoridorError("La position d'un mur est invalide.")
        for pos in self.ver:
            if (pos[0], pos[1] + 1) in self.ver or (pos[0], pos[1] - 1) in self.ver:
                raise QuoridorError("La position d'un mur est invalide.")

        # On vérifie la position des murs
        for pos in self.hori:
            if pos[0] < 1 or pos[0] > 8 or pos[1] < 2 or pos[1] > 9:
                raise QuoridorError("La position d'un mur est invalide")
        for pos in self.ver:
            if pos[0] < 2 or pos[0] > 9 or pos[1] < 1 or pos[1] > 8:
                raise QuoridorError("La position d'un mur est invalide")

        self.état_partie()

        self.graphe = construire_graphe(
            [joueur['pos'] for joueur in self.etat['joueurs']],
            self.etat['murs']['horizontaux'],
            self.etat['murs']['verticaux']
        )

        # On vérifie qu'aucun joueur n'est enfermé
        if not nx.has_path(self.graphe, self.pos1, 'B1') or not nx.has_path(self.graphe, self.pos2, 'B2'):
            raise QuoridorError("L'un des joueurs en enfermé.")

    def __str__(self):
        """Produit la représentation en art ASCII de l'état actuel."""
        self.état_partie()
        # On fabrique les cases du damier où les pions peuvent être placés
        dam = [
            f'{k} | .   .   .   .   .   .   .   .   . |\n' for k in range(1, 10)]

        # On obtient la position des pions et on les place
        x1, y1 = self.etat['joueurs'][0]['pos'][0], self.etat['joueurs'][0]['pos'][1]
        x2, y2 = self.etat['joueurs'][1]['pos'][0], self.etat['joueurs'][1]['pos'][1]

        dam[y1 - 1] = dam[y1 - 1][0] + dam[y1 - 1][1:].replace('.', '1', x1)
        dam[y1 - 1] = dam[y1 - 1][0] + dam[y1 - 1][1:].replace('1', '.', x1 - 1)

        dam[y2 - 1] = dam[y2 - 1][0] + dam[y2 - 1][1:].replace('.', '2', x2)
        dam[y2 - 1] = dam[y2 - 1][0] + dam[y2 - 1][1:].replace('2', '.', x2 - 1)

        # On insère les rangées où peuvent être placés les murs
        for k in range(1, 16, 2):
            dam.insert(k, '  |' + ' '*35 + '|\n')

        # On insère les murs horizontaux
        for x, y in self.etat['murs']['horizontaux']:
            dam[2*y - 3] = dam[2*y - 3][:4*x - 1:] + \
                '-------' + dam[2 * y - 3][4*x + 6::]

        # On insère les murs verticaux
        for x, y in self.etat['murs']['verticaux']:
            for k in range(3):
                dam[2*(y - 1) + k] = dam[2*(y - 1) + k][:4*x -
                                                        2:] + '|' + dam[2*(y - 1) + k][4*x - 1::]

        # On afficher le damier au complet et à l'endroit
        dam.reverse()
        NOMA = self.etat['joueurs'][0]['nom']
        NOMB = self.etat['joueurs'][1]['nom']
        return f'Légende: 1={NOMA}, 2={NOMB}\n   -----------------------------------\n' + ''.join(
            dam) + '--|-----------------------------------\n  | 1   2   3   4   5   6   7   8   9'

    def état_partie(self):
        """Produit l'état actuel de la partie."""
        self.etat = {
            'joueurs': [
                {'nom': self.joueur1, 'murs': self.compteur1, 'pos': self.pos1},
                {'nom': self.joueur2, 'murs': self.compteur2, 'pos': self.pos2},
            ],
            'murs': {
                'horizontaux': [],
                'verticaux': [],
            }
        }

        for mur in self.hori:
            self.etat['murs']['horizontaux'].append(mur)
        for mur in self.ver:
            self.etat['murs']['verticaux'].append(mur)

        # Met à jour l'état de la partie après avoir joué
        return self.etat

    def déplacer_jeton(self, joueur, position):
        """Déplace le jeton du joueur spécifié."""
        self.état_partie()

        self.graphe = construire_graphe(
            [joueur['pos'] for joueur in self.etat['joueurs']],
            self.etat['murs']['horizontaux'],
            self.etat['murs']['verticaux']
        )

        if joueur not in (1, 2):
            raise QuoridorError("Le numéro du joueur est autre que 1 ou 2.")
        if position in list(self.graphe.successors((self.etat['joueurs'][joueur - 1]['pos']))):
            if joueur == 1:
                self.pos1 = position
            elif joueur == 2:
                self.pos2 = position
        else:
            raise QuoridorError(
                "La position est invalide pour l'état de jeu actuel.")

        self.état_partie()

    def placer_mur(self, joueur, position, orientation):
        """Place un mur pour le joueur spécifié."""
        if joueur not in (1, 2):
            raise QuoridorError("Le numéro du joueur est autre que 1 ou 2.")

        if (joueur == 1 and self.compteur1 == 0) or (joueur == 2 and self.compteur2 == 0):
            raise QuoridorError("Le joueur a déjà placé tous ses murs.")

        self.graphe = construire_graphe(
            [joueur['pos'] for joueur in self.etat['joueurs']],
            self.etat['murs']['horizontaux'],
            self.etat['murs']['verticaux']
        )

        if orientation == 'horizontal':
            if (position or (position[0] + 1, position[1]) or (position[0] - 1, position[1])) in self.hori:
                raise QuoridorError("Un mur occupe déjà cette position.")
            if position[0] < 1 or position[0] > 8 or position[1] < 2 or position[1] > 9:
                raise QuoridorError("La position d'un mur est invalide")
            self.hori.append(position)
        elif orientation == 'vertical':
            if (position or (position[0], position[1] - 1) or (position[0], position[1] + 1)) in self.ver:
                raise QuoridorError("Un mur occupe déjà cette position.")
            if position[0] < 2 or position[0] > 9 or position[1] < 1 or position[1] > 8:
                raise QuoridorError("La position d'un mur est invalide")
            self.ver.append(position)

        if joueur == 1:
            self.compteur1 -= 1
        elif joueur == 2:
            self.compteur2 -= 1

        self.état_partie()

    def partie_terminée(self):
        """Vérifie si la partie est terminée."""
        if self.pos1[1] == 9:
            return self.joueur1
        if self.pos2[1] == 1:
            return self.joueur2
        else:
            return False

    def jouer_coup(self, joueur):
        """Pour le joueur spécifié, joue automatiquement un coup."""
        if self.partie_terminée() is not False:
            raise QuoridorError("La partie est déjà terminée.")

        self.état_partie()

        self.graphe = construire_graphe(
            [self.pos1, self.pos2],
            self.etat['murs']['horizontaux'],
            self.etat['murs']['verticaux']
        )

        if joueur == 1:
            self.déplacer_jeton(joueur, nx.shortest_path(
                self.graphe, self.pos1, 'B1')[1])

        elif joueur == 2:
            self.déplacer_jeton(joueur, nx.shortest_path(
                self.graphe, self.pos2, 'B2')[1])
        else:
            raise QuoridorError("Le numéro du joueur est autre que 1 ou 2.")

        self.état_partie()
