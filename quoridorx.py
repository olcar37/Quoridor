"""Module permettant d'afficher le jeu dans une fenêtre graphique."""


import turtle
import time
from quoridor import Quoridor


class QuoridorX(Quoridor):
    """Classe comprenant l'affichage graphique"""

    def __init__(self, joueurs, murs=None):
        """Initialise une fenêtre de jeu"""

        super().__init__(joueurs, murs)
        self.fen = turtle.Screen()
        self.fen.setup(width=1050, height=700)
        self.fen.title('Quoridor')
        self.tortue1, self.tortue2, self.tortue_murs = turtle.Turtle(
        ), turtle.Turtle(), turtle.Turtle()
        self.fen.bgpic('grid.png')
        self.tortue1.penup()
        self.tortue2.penup()
        self.tortue_murs.penup()
        self.tortue1.ht()
        self.tortue2.ht()
        self.tortue1.speed(10)
        self.tortue2.speed(10)
        self.tortue_murs.speed(10)
        self.tortue1.pencolor('green')
        self.tortue2.pencolor('red')
        self.tortue_murs.pencolor('yellow')
        self.tortue1.fillcolor('green')
        self.tortue2.fillcolor('red')
        self.tortue_murs.fillcolor('orange')
        self.tortue1.shape('circle')
        self.tortue2.shape('circle')
        self.tortue_murs.ht()
        murh = ((-5, 0), (-5, 114), (5, 114), (5, 0), (-5, 0))
        murv = ((25, -5), (-87, -5), (-87, 5), (25, 5), (25, -5))
        self.fen.addshape('murh', murh)
        self.fen.addshape('murv', murv)
        self.tortue1.goto(-79, -213)
        self.tortue2.goto(-79, 275)
        self.tortue1.st()
        self.tortue2.st()
        self.afficher()

    def afficher(self):
        """Mets à jour la fenêtre de jeu"""

        if self.hori != [] :
            self.tortue_murs.shape('murh')
            self.tortue_murs.setpos(-350 + 61 *
                                    (self.hori[-1][0] - 1), -244 + 61 * (self.hori[-1][1] - 1))
            self.tortue_murs.stamp()
        if self.ver != []:
            self.tortue_murs.shape('murv')
            self.tortue_murs.setpos(-354 + 61 *
                                    (self.ver[-1][0] - 1), -213 + 61 * (self.ver[-1][1] - 1))
            self.tortue_murs.stamp()
        time.sleep(0.1)
        self.tortue1.setpos(-323 + 61 *
                            (self.pos1[0] - 1), -213 + 61 * (self.pos1[1] - 1))
        self.tortue2.setpos(-323 + 61 *
                            (self.pos2[0] - 1), -213 + 61 * (self.pos2[1] - 1))
