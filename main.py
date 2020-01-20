"""Module pour afficher le jeu et tratier les commandes"""


import argparse
import time
from api import jouer_coup, debuter_partie
from quoridorx import QuoridorX
from quoridor import Quoridor

def analyser_commande():
    """Analyse la ligne de commande"""
    parser = argparse.ArgumentParser(description='Jeu Quoridor - phase 1')
    parser.add_argument('idul', type=str, metavar='idul',
                        help='IDUL du joueur.')
    parser.add_argument('-a', action='store_true',
                        help='Joueur en mode automatique contre le serveur')
    parser.add_argument('-x', action='store_true',
                        help='Jouer en mode manuel avec un affichage graphique')
    parser.add_argument('-ax', action='store_true',
                        help='Jouer en mode automatique avec un affichage graphique')
    return parser.parse_args()

def afficher_damier_ascii(et):
    """Affiche le damier en art ASCII"""
    # On fabrique les cases du damier où les pions peuvent être placés
    dam = [
        f'{k} | .   .   .   .   .   .   .   .   . |\n' for k in range(1, 10)]

    # On obtient la position des pions et on les place
    x1, y1 = et['joueurs'][0]['pos'][0], et['joueurs'][0]['pos'][1]
    x2, y2 = et['joueurs'][1]['pos'][0], et['joueurs'][1]['pos'][1]

    dam[y1 - 1] = dam[y1 - 1][0] + dam[y1 - 1][1:].replace('.', '1', x1)
    dam[y1 - 1] = dam[y1 - 1][0] + dam[y1 - 1][1:].replace('1', '.', x1 - 1)

    dam[y2 - 1] = dam[y2 - 1][0] + dam[y2 - 1][1:].replace('.', '2', x2)
    dam[y2 - 1] = dam[y2 - 1][0] + dam[y2 - 1][1:].replace('2', '.', x2 - 1)

    # On insère les rangées où peuvent être placés les murs
    for k in range(1, 16, 2):
        dam.insert(k, '  |' + ' '*35 + '|\n')

    # On insère les murs horizontaux
    for x, y in et['murs']['horizontaux']:
        dam[2*y - 3] = dam[2*y - 3][:4*x - 1:] + \
            '-------' + dam[2 * y - 3][4*x + 6::]

    # On insère les murs verticaux
    for x, y in et['murs']['verticaux']:
        for k in range(3):
            dam[2*(y - 1) + k] = dam[2*(y - 1) + k][:4*x -
                                                    2:] + '|' + dam[2*(y - 1) + k][4*x - 1::]

    # On afficher le damier au complet et à l'endroit
    dam.reverse()
    NOMA = et['joueurs'][0]['nom']
    NOMB = et['joueurs'][1]['nom']
    return f'Légende: 1={NOMA}, 2={NOMB}\n   -----------------------------------\n' + ''.join(
        dam) + '--|-----------------------------------\n  | 1   2   3   4   5   6   7   8   9'

c = analyser_commande()

#Mode manuel
if not (c.a or c.x or c.ax):
    jeu = Quoridor((c.idul, 'robot'))
    ID, etat = debuter_partie(c.idul)

    while True:
        TYPE_COUP = input('Quel type de coup voulez-vous jouer? (D/MH/MV) ')
        POSI = input('À quelle position (x,y) voulez-vous jouer ce coup ? ').replace(' ', '')
        x, y = int(POSI[1]), int(POSI[3])

        if TYPE_COUP.lower() == 'd':
            jeu.déplacer_jeton(1, (x, y))
            print(jeu)
            time.sleep(0.6)
            reponse = jouer_coup(ID, 'D', (x, y))
        elif TYPE_COUP.lower() == 'mh':
            jeu.placer_mur(1, (x, y), 'horizontal')
            print(jeu)
            time.sleep(0.6)
            reponse = jouer_coup(ID, 'MH', (x, y))
        elif TYPE_COUP.lower() == 'mv':
            jeu.placer_mur(1, (x, y), 'vertical')
            print(jeu)
            time.sleep(0.6)
            reponse = jouer_coup(ID, 'MV', (x, y))
        jeu.pos2 = tuple(reponse['joueurs'][1]['pos'])
        jeu.hori = reponse['murs']['horizontaux']
        jeu.ver = reponse['murs']['verticaux']

        jeu.partie_terminée()

        jeu.état_partie()
        print(jeu)
        time.sleep(0.6)

#Mode automatique
if c.a and not (c.x or c.ax):
    jeu = Quoridor((c.idul, 'robot'))
    ID, etat = debuter_partie(c.idul)

    while True:
        jeu.jouer_coup(1)
        print(jeu)
        jeu.partie_terminée()
        time.sleep(0.6)
        reponse = jouer_coup(ID, 'D', jeu.pos1)
        jeu.pos2 = reponse['joueurs'][1]['pos']
        jeu.hori = reponse['murs']['horizontaux']
        jeu.ver = reponse['murs']['verticaux']

        jeu.partie_terminée()

        jeu.état_partie()
        print(jeu)
        time.sleep(0.6)

#Mode automatique graphique
if c.ax and not (c.x or c.a):
    jeu = QuoridorX((c.idul, 'robot'))
    ID, etat = debuter_partie(c.idul)

    while True:
        jeu.jouer_coup(1)
        jeu.afficher()
        jeu.partie_terminée()
        time.sleep(0.3)
        reponse = jouer_coup(ID, 'D', jeu.pos1)
        jeu.pos2 = reponse['joueurs'][1]['pos']
        jeu.hori = reponse['murs']['horizontaux']
        jeu.ver = reponse['murs']['verticaux']

        jeu.partie_terminée()

        jeu.état_partie()
        jeu.afficher()
        time.sleep(0.3)

#Mode manuel graphique
if c.x and not (c.ax and c.a):
    jeu = QuoridorX((c.idul, 'robot'))
    ID, etat = debuter_partie(c.idul)

    while True:
        TYPE_COUP = jeu.fen.textinput('Type de coup à jouer', 
                                        'Quel type de coup voulez-vous jouer? (D/MH/MV) ')
        POSI = jeu.fen.textinput('Position du coup à jouer', 
                                    'À quelle position (x,y) voulez-vous jouer ce coup ? ').replace(' ', '')
        x, y = int(POSI[1]), int(POSI[3])

        if TYPE_COUP.lower() == 'd':
            jeu.déplacer_jeton(1, (x, y))
            jeu.afficher()
            time.sleep(0.6)
            reponse = jouer_coup(ID, 'D', (x, y))
        elif TYPE_COUP.lower() == 'mh':
            jeu.placer_mur(1, (x, y), 'horizontal')
            jeu.afficher()
            time.sleep(0.6)
            reponse = jouer_coup(ID, 'MH', (x, y))
        elif TYPE_COUP.lower() == 'mv':
            jeu.placer_mur(1, (x, y), 'vertical')
            jeu.afficher()
            time.sleep(0.6)
            reponse = jouer_coup(ID, 'MV', (x, y))
        jeu.pos2 = tuple(reponse['joueurs'][1]['pos'])
        jeu.hori = reponse['murs']['horizontaux']
        jeu.ver = reponse['murs']['verticaux']

        jeu.partie_terminée()

        jeu.état_partie()
        jeu.afficher()
        time.sleep(0.6)
