# IQPlayground

Text Indexation &amp; Query Algorithms Playground

## Aim

Discovering Text Indexation &amp; Query Algorithms by implementing them 

## Prerequisites

Learn Python 3 :

+ [Quickstart](https://learnxinyminutes.com/docs/python3/)
+ [Style Guide](https://www.python.org/dev/peps/pep-0008/)
+ [Official Documentation](https://docs.python.org/3/)
+ [If you want to suffer](https://learncodethehardway.org/more-python/)

To test and use quickly without an IDE :

+ [Online code tester](https://tio.run/)

Use Pycharm :

+ [To install it quickly on Ubuntu](https://itsfoss.com/install-pycharm-ubuntu/)

## Feature Goals

### Indexing :

+ Parse pseudo-xml files into usable objects
+ Tokenization of each of the documents : use the [nltk Python library](http://www.nltk.org/api/nltk.tokenize.html)
+ Stemming : may help save place but is useless outside of this scope -> use a library. Allow user to activate or deactivate it.
+ Stop words removal : use a library. Allow user to activate or deactivate it.
+ Inverted file : Implement this mapping between vocabulary of terms (VOC) and posting lists (PL).
+ Merge-based algorithm To build the IF : to research and implement
+ PL Compression : to research and implement
+ Variable Byte : Implement following [this proposition](https://github.com/utahta/pyvbcode).
+ Score computation : To be implemented with variations that the user can play with.
+ Random indexing : Search pseudo-code and implement

### Querying :

+ Fagin’s top-k query algorithm (FA) : To implement with possibilities for variations.

### Graphical User interface

Simple graphical user interface with search bar(s), some checkboxes to activate some other options, and a text area where results can be displayed (list of articles with id, title, file name). When you click on it, displays

## First iteration 06/10/2017 -> 08/10/2017

- Alexis writes a basic implementation to get everyone started :

	+ Parse pseudo-xml files into usable objects without library : make each document into a separate object, removing all the XML markup and considering all the rest as text
	+ Simple tokenization of each of the documents using nltk (space-based rule with some exceptions managed by the library)
	+ Basic fully in-memory inverted file, with scores computed as the product of the term-frequency and inverse-document-frequency, with posting-lists ordered by DOCID
	+ For queries, input the query in terminal
	+ Parallel scan all posting-lists to find each DOCID that has all search terms at least once
	+ Consider all queries are only conjunctive and aggregate the scores as a simple sum of the score of each term for each document
	+ Sort document list by score and output DOCIDs of the 5 first ones in terminal

- All others learn Python through at least the QuickStart and the PEP8 (ideally with Learn Python the hard way if they can)

## First code review 09/10/2017 from 10 to 12 a.m.

+ Discussion around a nice cup of tea/chocolate/coffee.

+ Alexis presents the basic structure of the project and the strategy for expanding the different elements (packages, classes, functions, ...).

+ Affectation of the elements for the second iteration.

## Second iteration 09/10/2017 -> 15/10/2017

> Important note : For each feature, think about paraterizing it so that it is possible to play with it in the GUI (for example, change the ponderation of words that are in the document title when computing the inverted file).

+ Simple GUI using [PyGObject](https://pygobject.readthedocs.io/en/latest/), [Kivy](https://kivy.org/) or [PySide](http://wiki.qt.io/PySide)
	-> TODO By ...

+ Better parse the different XML elements of the file so that it is possible to ponderate the computation of the scores in the inverted file depending on whether the terms are the title or if they must agree with a particular date, ...
	-> TODO By ...

+ Deactivable (through UI) stemming and stop words removal that is going to influence th creation of the IF
	-> TODO By ...

+ Merge-based creation of the inverted file (see slide 24 of teacher's slideshow)
	-> TODO By ...

+ PL Compression (see slide 25 of teacher's slideshow)
	-> TODO By ...

+ Variable Byte Encoding (see slides 26 to 29 of teacher's slideshow)
	-> TODO By ...

## Second code review 16/10/2017 from 8 to 10 a.m.

+ Discussion around a nice cup of tea/chocolate/coffee.

+ Presentation of each person's work for 20 minutes max.

+ Affectation of the elements for the third iteration in the remaining time.

## Third iteration 16/10/2017 -> 19/10/2017

+ Fagin’s top-k query algorithm (FA) (see slides 16 to 18 of teacher's slideshow)
	-> TODO By ...

+ Fagin’s threshold algorithm (TA) (see slides 19 to 21 of teacher's slideshow)
	-> TODO By ...

+ Espilon-approximation of Top-K Answers (see slide 22 of teacher's slideshow)
	-> TODO By ...

+ Random Indexing (see slide 32 of teacher's slideshow)
	-> TODO By ...

## Third code review 19/10/2017 from 4:30 to 6:30 p.m.

+ Discussion around a nice cup of tea/chocolate/coffee.

+ Presentation of each person's work for 20 minutes max.

+ Bug fixes.

## Preparation of the presentation 19/10/2017 from 4:30 to 6:30 p.m.

+ Overall bug fixes

+ Preparation of slideshow and oral presentation.

## Preparation of the presentation 20/10/2017 from 10 to 17 a.m

+ Overall bug fixes

+ Preparation of slideshow and oral presentation.

## Presentation 20/10/2017 from 17 to 18 a.m

+ BE AWESOME ! :D