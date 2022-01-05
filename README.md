# Sudoku Solver

A program that solves sudokus using the **GSAT** and **WalkSAT** algorithms. The sudoku is represented as a propositional logic satisfiability problem. 

**GSAT** – GSAT starts by assigning a random value to each variable. If the assignments satisfies all clauses, we return the assignment. Otherwise, it either a). chooses a random variable to flip, or b). flips the variable that maximizes the number of satisfied variables.

**WalkSAT** – WalkSAT runs similarly to GSAT, but instead either a). picks an unsatisfied clause and flips a variable within that clause or b). picks an unsatisfied clause and flips the variable within that clause that maximizes the score (number of satisfied variables). WalkSAT is more efficient than GSAT because it considers fewer variables when determining which variable to flip.

### Usage
To run tests, enter in terminal `python3 solve_sudoku.py /tests/[puzzle].cnf`, where "puzzle" is the name of the puzzle.
