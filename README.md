FRANCAIS:

Ce projet consiste à lire un fichier au format CoNLL-U (https://universaldependencies.org/format.html) pour générer un fichier au format JSON (https://fr.wikipedia.org/wiki/JavaScript_Object_Notation) contenant diverses statistiques et index hiérarchiques de n-grammes.

Objectifs
Lire un fichier CoNLL-U et générer un fichier JSON avec les propriétés suivantes :

nbToks : Nombre total de tokens.
nbSents : Nombre total de phrases.
nbForms : Nombre total de formes.
nbPuncts : Nombre total de ponctuations.
nbTypes : Nombre total de types.
averageSentLength : Nombre moyen de formes par phrase.
averageFormLength : Nombre moyen de caractères par forme.
noun2freq : Index hiérarchique des noms triés par fréquence décroissante.
verb2freq : Index hiérarchique des verbes triés par fréquence décroissante.
adj2freq : Index hiérarchique des adjectifs triés par fréquence décroissante.
adv2freq : Index hiérarchique des adverbes triés par fréquence décroissante.
lem2freq : Index hiérarchique des lemmes triés par fréquence décroissante.
ngrams : Index hiérarchiques des n-grammes de longueur 3, 4, 5, 6, etc.
Décrire en pseudo-code l'algorithme de calcul des index hiérarchiques des n-grammes et estimer sa complexité.

Décrire et implémenter un algorithme de déduplonnage des fragments de n-grammes en appliquant la règle suivante :

Si un n-gramme X de taille n est contenu dans un n-gramme Y de taille n+1, et que freq(X) <= seuil_dedoublonnage * freq(Y), alors X est éliminé.

Extraire les fréquences associées à des patterns (p.ex. NOUN ADP NOUN, ADJ NOUN) listées dans un fichier patterns.json.
Extraire les fréquences pour des skip-grams à un gap.


ENGLISH:

This project involves reading a file in CoNLL-U format (https://universaldependencies.org/format.html) to generate a file in JSON format (https://fr.wikipedia.org/wiki/JavaScript_Object_Notation) containing various statistics and hierarchical indexes of n-grams.

Objectives
Read a CoNLL-U file and generate a JSON file with the following properties:

nbToks: Total number of tokens.
nbSents: Total number of phrases.
nbForms: Total number of forms.
nbPuncts: Total number of punctuation marks.
nbTypes: Total number of types.
averageSentLength: Average number of forms per sentence.
averageFormLength: Average number of characters per form.
noun2freq: Hierarchical index of nouns sorted by decreasing frequency.
verb2freq: Hierarchical index of verbs sorted by descending frequency.
adj2freq: Hierarchical index of adjectives sorted by descending frequency.
adv2freq: Hierarchical index of adverbs sorted by descending frequency.
lem2freq: Hierarchical index of lemmas sorted by descending frequency.
ngrams: Hierarchical index of n-grams of length 3, 4, 5, 6, etc.
Describe in pseudo-code the algorithm for calculating the hierarchical indexes of n-grams and estimate its complexity.

Describe and implement an algorithm for deduplicating fragments of n-grams by applying the following rule:

If an n-gram X of size n is contained in an n-gram Y of size n+1, and freq(X) <= deduplication_threshold * freq(Y), then X is eliminated.

Extract frequencies associated with patterns (e.g. NOUN ADP NOUN, ADJ NOUN) listed in a patterns.json file.
Extract frequencies for skip-grams at a gap.
