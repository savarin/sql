# sql

*This project was completed as a part of Bradfield's [Databases](https://bradfieldcs.com/courses/databases) class.*

## Introduction

sql is a simple implementation of a relational database management system (RDBMS).

## Components

**executor - basic query executor that supports single table queries**
* filescan - reads the input file 1 page (4,096 bytes) at a time i.e. FROM clause
* selection - returns rows that satisfy a predicate function i.e. WHERE clause
* projection - returns a subset of columns i.e. SELECT clause
* sort - returns row in sorted order (with heapsort) i.e. ORDER BY clause
* distinct - returns distinct rows i.e. DISTINCT clause
* aggregate - performs aggregation i.e. GROUP BY clause

**join - supports queries over multiple tables**
* nested loop join - simple but slow
* hash join - faster, requires hash table fit in memory
* sort-merge join (not implemented) - faster, requires entries be sorted

**index - for fast lookup times**
* b+ tree - analogous to binary search tree but with more branching at each node, as shallow trees makes better use of caches