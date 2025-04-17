# Projet_MGA802
## Description du Projet
Ce projet, développé dans le cadre du cours **MGA802**, vise à optimiser des structures permettant de ralentir des satellites en phase de désorbitage en utilisant des algorithmes d'apprentissage et d'optimisation. 
Le code combine des techniques de génération, d'évaluation et d'amélioration de structures en fonction de critères spécifiques, tels que l'encombrement, le poids et la force. 
L'objectif principal est de produire des structures performantes selon les pondérations définies par l'utilisateur.

---

## Objectifs du Code
1. **Apprentissage des structures** : Générer et évaluer un ensemble de structures à travers plusieurs itérations d'apprentissage. Les meilleures structures sont conservées et modifiées pour itérer vers des solutions optimales.
2. **Optimisation des structures** : Améliorer une structure donnée à l'aide de l'algorithme Nelder-Mead pour maximiser les performances spécifiques (force, encombrement, poids).
3. **Visualisation** : Offrir une interface utilisateur interactive (via Streamlit) pour suivre les performances, visualiser les structures et évaluer les résultats.

---

## Comment Utiliser le Code
### Prérequis
**Python** : Assurez-vous que Python 3.8 ou une version ultérieure est installé.

      Installez les bibliothèques avec la commande suivante :

        python -m pip install -r requirements.txt

## Étapes pour Lancer le Projet
- Cloner le dépôt :

      git clone https://github.com/Zach-Yee-Haw/Projet_MGA802.git
      cd Projet_MGA802

- Lancer l'application Streamlit :

  - Ouvrez le fichier run.bat ou bien tapez la commande suivante :

        streamlit run __init__.py
  
- Configurer les paramètres via l'interface utilisateur :

  - Définir le nombre de points, les longueurs minimales et maximales, le nombre de structures, etc.
  - Cliquer sur Démarrer apprentissage pour lancer le processus.
  - (Optionnel) Activer l'optimisation pour améliorer les structures après l'apprentissage.

- Visualisation des résultats :

  - Suivre les graphiques et les visualisations en 3D directement dans l'application Streamlit.
    
## Stratégie Adoptée pour la Structure du Code
Le code est organisé en plusieurs modules pour garantir la modularité et la lisibilité :

- apprentissage.py :

  - Contient les fonctions pour l'apprentissage des structures.
  - Implémente une approche itérative où des structures sont générées, évaluées, triées et modifiées.
    
- optimisation.py :

  - Gère l'optimisation des structures en utilisant l'algorithme Nelder-Mead.
  - Permet de raffiner une structure pour maximiser un score basé sur des critères spécifiques.

- structure.py :

  - Définit la classe Structure, qui encapsule les propriétés et méthodes pour manipuler les structures géométriques.

- extra_fonctions.py :

  - Regroupe des fonctions utilitaires, comme le tri, le calcul des scores et le mélange des structures.

- __init__.py :

  - Point d'entrée principal du projet.
  - Configure l'interface utilisateur Streamlit pour permettre une interaction simple avec les différentes fonctionnalités du projet.
    
## Fonctionnalités Clés
- Apprentissage :

  - Génération de structures aléatoires avec des paramètres personnalisés.
  - Évaluation et tri des structures basés sur des scores pondérés.
  - Visualisation des progrès d'apprentissage via des graphiques.

- Optimisation :

  - Affinage des structures pour maximiser les performances.
  - Suivi des progrès de l'optimisation en temps réel.

- Interface Interactive :

  - Paramètres facilement ajustables via Streamlit.
  - Visualisation 3D des structures en cours d'apprentissage ou d'optimisation.

## Contributions
- Personnellement, je ne compte pas participer à d'autres modifications de ce projet.
- Cependant, vous pouvez faire ce que vous voulez dans une version clonée du projet.
- Ce qu'il reste à faire :

  - Vectoriser le calcul de force avec numpy dans structure.py.
  - Permettre à l’utilisateur de choisir une autre méthode d’optimisation.
  - Permettre à l’utilisateur de définir le matériau de la structure.
  - Améliorer l’interface (bloquer entrées, montrer meilleure structure de chaque itération, mettre plus d’informations, etc.).
  - Permettre à l’utilisateur de générer des boucles ou des embranchements.

## Licence
Ce projet est sous licence MIT. Vous êtes libre de l'utiliser, de le modifier et de le partager.

NB : Les commentaires et la documentation ont été rédigés avec l'assistance de la SIAG Microsoft Copilot.