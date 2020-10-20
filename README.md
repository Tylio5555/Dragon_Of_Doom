# Dragon Of Doom

Dragon of Doom est un mini-jeu de combat de Dragons.

Votre but est d'entrainer un Dragon pour lui faire affronter le boss de l'arène, le Dragon of Doom!
Soyez gagnant et alors votre Dragon deviendra le nouveau boss à retourner affronter.
Chaque victoire vous apporte des Victory Token a dépenser en améliorations.

Dragon of Doom est un jeu de paris. Est ce que mon dragon peut tuer son Dragon?



Détails sur les Dragons:

- il ya plusieurs types elementaires de dragon, ceux-ci sont classés en 3 rangs:
    - Rang 1:
    	Fire, Water, Air, Earth
    - Rang 2:
    	Metal, Lightning, Ice, Nature
    - Rang 3:
    	Spirit, Darkness, Light

La reproduction de dragons permet d'obtenir des dragons du rang supérieurs dont les combinaisons seront à vous de trouver.


- Le Rating est la facon dont vont evoluer ses stats:
    Pour l'instant les stats suivent une equation de second degré : X² + a*x +b ou a est la valeur de rating compris entre 1 et 10 
    Un dragon qui commence avec une faible attaque mais un bon rating deviendra meilleur qu'un dragon avec une forte attaque mais un faible rating.

- Gagner un combat dans l'arène fait directement gagner un level au dragon gagnant mais
  battre un adversaire dont le dragon est un level au dessus du notre fait gagner directement 2 level en plus.

- Dégat d'attaque:
    Calculer selon la formule suivante:
        ((level*0.4 + 2)*Atk)/enemy_def
        l'attaque et la defense sont choisi entre normal et spécial dépandant si le dragon qui attaque à
        son attaque spé plus forte que son attaque normal et qu'il lui reste des mp pour pouvoir l'utiliser.

- Autosave:
    Le jeu possède un system d'autosave qui sauvegarde la progression du joueur juste avant la selection d'une action dans la ville principale
    Ce n'est pas une feature sur laquelle il faut dependre mais en cas de crash le joueur doit directement relancer et faire Load et mettre en nom de fichier à load: "autosave"
