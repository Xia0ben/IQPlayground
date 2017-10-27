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
+ [CheatSheet 1](http://overapi.com/python)
+ [CheatSheet 2](https://devhints.io/python)

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

> Important note : For each feature, think about parameterizing it so that it is possible to play with it in the GUI (for example, change the ponderation of words that are in the document title when computing the inverted file).

+ Simple GUI using [PyGObject](https://pygobject.readthedocs.io/en/latest/), [Kivy](https://kivy.org/) or [PySide](http://wiki.qt.io/PySide)
	-> SHOTGUN By Benoit :D

+ Better parse the different XML elements of the file so that it is possible to ponderate the computation of the scores in the inverted file depending on whether the terms are the title or if they must agree with a particular date, ...
	-> TODO By Zakaria

+ Deactivable (through UI) stemming and stop words removal that is going to influence the creation of the
	-> TODO By Omar

+ Merge-based creation of the inverted file (see slide 24 of teacher's slideshow)
	-> TODO By Alexis

+ PL Compression : Variable Byte Encoding (see slides 26 to 29 of teacher's slideshow)
	-> TODO By Bachir

## Second code review 16/10/2017 from 8 to 10 a.m.

+ Discussion around a nice cup of tea/chocolate/coffee.

+ Presentation of each person's work for 20 minutes max.

+ Affectation of the elements for the third iteration in the remaining time.

## Third iteration 16/10/2017 -> 19/10/2017

+ Fagin’s threshold algorithm (TA) (Top-k improvement, so we don't do the FA before) (see slides 16 to 18, then 19 to 21 of teacher's slideshow), with Espilon-approximation of Top-K Answers (see slide 22 of teacher's slideshow)
	-> TODO By Zakaria

+ Random Indexing (see slide 32 of teacher's slideshow)
	-> TODO By Bachir

+ Allow OR clause instead of only AND
	-> TODO By Alexis

+ Improvement of the GUI : Logging of queries ad associated results + performance indicators (processor time, memory used, number of reads of posting-lists...)
	-> SHOTGUN By Benoit :D

## Third code review 19/10/2017 from 4:30 to 6:30 p.m.

+ Discussion around a nice cup of tea/chocolate/coffee.

+ Presentation of each person's work for 20 minutes max.

+ Bug fixes.

## Preparation of the presentation 19/10/2017 from 6:30 to 8:30 p.m.

+ Overall bug fixes

+ Preparation of slideshow and oral presentation.

## Preparation of the presentation 20/10/2017 from 10 to 17 a.m

+ Overall bug fixes

+ Preparation of slideshow and oral presentation.

## Presentation 20/10/2017 from 17 to 18 a.m

+ BE AWESOME ! :D

## Description of the packages

+ Algorithm

    - Contains classes for each algorithm
    
    - Each algorithm is derived from the baseAlgorithm class
    
    - naiveAlgorithm : a naive query algorithm based on parallel scan of the posting lists
    
    - FA_Algorithm : Fagin's top-k query algorithm
    
    - TA_Algorithm : Fagin's thershold algorithm
    
+ Executable
    
    - Contains an executable class which act as a controller for the project
    
+ Files

    - Contains multiple classes which act with the memory and the hard drive
    
    - document : a memory based representation of a document
    
    - fileToPostingList : read a pl FILE to generate memory based posting lists when needed
    
    - invertedFile : memory based inverted file, which do a merge based creation of the posting lists
    
    - postingList : a memory based representation of the posting lists with 3 access :
        + randomaccess : return the score of a doc id in log(n) time
        + alphaaccess : return the doc_id and score ordered by doc_id
        + orderedaccess : return the doc_id and score ordered by score
    
    - reader : read a file and returns documents
        
    - stemmer : implementation of porter's algorithm
    
    - variableByte : encoding and decoding of variable byte integers
    
      ###### 1- Explaining Encoding :

        + Get the last seven bits from the binary code 1100001001 is 0001001,
        + Add 1 as the "head" bit (0001001 -> 10001001) 
        + Because there are still 3 bits left in the original binary code.
          Get the remain 3 bits, this time use 0 as the "head" bit (110 -> 00000110) 
        + Because there is no remain in the original binary code
          put these two bytes together 0000011010001001 is the VB code.

    
+ RandomIndexing
    
    - Contains classes used for the random indexing of terms
    - randomIndex : Contains a class with different functions to get context vector for a term
    - vectorsSimilarity : Contains functions to calculate Cosinus distance between context vectors
      this distance is in the interval [0-2]
    
+ Stats

    - Contains classes which allow to get stats ont indexing and querying
    
+ UI

    - Contains files used to generate the user interface

##RUNNING THE PROJECT:

+ Prerequisites
    
   - Python 3.6
   - Git
   
+ Installation

   - Import the Project : git pull https://github.com/Xia0ben/IQPlayground.git
   - Add the files directory "latimes" to the project repository
   - Add the folder pickles , and invertedfiles to the project repository
   - install nltk (using python interpreter): >>> import nltk
                                              >>> nltk.download()
   - install numpy package with pip : pip install numpy --index-url=http://pypi.python.org/simple/ --trusted-host pypi.python.org

   - install sortedcontainers library with pip: pip install sortedcontainers
   
+ Execution 

   - Console mode : 
        
        - access the project repository in the console  
        - run the console_mode_launch.py : python console_mode_launch.py
        
   - Graphical mode :
   
        - import gi , and install  PyGObject, GTK+ and their dependencies : http://pygobject.readthedocs.io/en/latest/getting_started.html
        - run the python file "test_gui.py" in the directory tests
        