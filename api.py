"""Module permettant de communiquer avec le serveur"""

import requests


URL_BASE = 'https://python.gel.ulaval.ca/quoridor/api/'


def lister_parties(idul):
    """Obtient la liste des parties en cours d'un utilisateur"""
    rep = requests.get(URL_BASE + 'lister/', params={'idul': idul})
    if rep.status_code == 200:
        rep = rep.json()
        if 'message' in rep:
            raise RuntimeError(rep['message'])
        return rep['parties']
    raise RuntimeError(f'{rep.status_code}')


def debuter_partie(idul):
    """Débute une partie"""
    rep = requests.post(URL_BASE + 'débuter/', data={'idul': idul})
    if rep.status_code == 200:
        rep = rep.json()
        if 'message' in rep:
            raise RuntimeError(rep['message'])
        return (rep['id'], rep['état'])
    raise RuntimeError(f'{rep.status_code}')


def jouer_coup(id_partie, type_coup, position):
    """Jouer un coup"""
    rep = requests.post(
        URL_BASE + 'jouer/', data={'id': id_partie, 'type': type_coup, 'pos': position})
    if rep.status_code == 200:
        rep = rep.json()
        if 'message' in rep:
            raise RuntimeError(rep['message'])
        elif 'gagnant' in rep:
            raise StopIteration(rep['gagnant'])
        return rep['état']
    raise RuntimeError(f'{rep.status_code}')
