# Prédiction de liens dans des données liées
# Projet de systèmes à base de connaissances (SBC)

### Objectif de ce repository

L'objectif est d'utiliser une méthode d’apprentissage automatique pour entraîner un modèle qui permet de dire si une paire d’entités est liée par une relation particulière ou non à partir d’un jeu de données en RDF, d’un ensemble d’exemples positifs (des paires d’entités liées) et d’un ensemble d’exemples négatifs (des paires d’entités non liées).  
Plus précisément, nous cherchons à prédire des liens entre des médicaments et des gènes afin de savoir si un gène a un impact sur la réponse des individus à un médicament donné. Ceci permet en particulier de comprendre pourquoi deux individus qui ont une version différente d'un même gène réagissent différemment au même médicament.

### Fonctionnement des sources

Le fichier sparql.py contient trois éléments :  
* une fonction permettant de créer une requête SPARQL dont l'objectif est de trouver un lien dans le triple store entre un médicament et un gène donnés ;  
* une fonction qui envoie une requête http au serveur contenant le triple store (afin d'avoir la réponse à une requête SPARQL), un serveur local dans notre cas ;  
* une fonction qui permet de convertir les donnéees récupérées de la requête http (format JSON) en des données plus facilement utilisables.  

Le fichier recup_tsv.py permet de lire les fichiers TSV qui sont dans le dossier training.  
Enfin, le fichier complet_lstm.py permet quant à lui de lancer le LSTM sur les chemins de données récupérés entre les médicaments et les gènes.  

### Éléments inachevés

Les requêtes SPARQL ne fonctionnent pas sur tous les couples gène/médicament, donc il faudrait pouvoir prendre en compte tous les cas possibles.  
De plus, le code du LSTM est à adapter à notre problème car il ne peut pas actuellement donner des résultats.   
Enfin, il faudrait automatiser l'ensemble du processus afin de pouvoir facilement lancer le code.

### Lien vers la présentation

https://docs.google.com/a/esial.net/presentation/d/1acybXNnt1moMRbSgBa83Y9GFeH3mbFjhVPLYtv_yb_0/edit?usp=sharing

### Collaborateurs

Jean-Louis Cuartero  
Marc Delpech  
Julien Feuvrier  
Simon Hamant  
Matthieu Rousselle  

