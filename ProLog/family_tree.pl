%family tree

% Facts

male(james).
male(robert).
male(michael).
male(david).
male(chris).
male(elly).
male(ronney).

female(eunice).
female(susan).
female(linda).
female(karen).
female(emily).
female(sophia).


% Parent Relationships
parent(eunice,ronney).
parent(elly, ronney).

parent(james, robert).
parent(susan, robert).

parent(james, linda).
parent(susan, linda).

parent(robert, michael).
parent(karen, michael).

parent(robert, emily).
parent(karen, emily).

parent(linda, david).
parent(chris, david).

parent(linda, sophia).
parent(chris, sophia).


% Rules 

father(X, Y) :-
    male(X),
    parent(X, Y).

mother(X, Y) :-
    female(X),
    parent(X, Y).

grandparent(X, Y) :-
    parent(X, Z),
    parent(Z, Y).

grandchild(X, Y) :-
    grandparent(Y, X).

child(X,Y) :-
    parent(Y,X).
    
sibling(X, Y) :-
    parent(Z, X),
    parent(Z, Y),
    X \= Y.

brother(X,Y) :-
    sibling(X,Y),
    male(X).

sister(X,Y) :-
    sibling(X,Y),
    female(X).

cousin(X, Y) :-
    parent(A, X),
    parent(B, Y),
    sibling(A, B).

uncle(X, Y) :-
    male(X),
    parent(Z, Y),
    sibling(X, Z).

aunt(X, Y) :-
    female(X),
    parent(Z, Y),
    sibling(X, Z).