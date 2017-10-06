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

## Required Features

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
