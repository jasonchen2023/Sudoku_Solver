# Jason Chen
# CS76 Fall21
# PA 5

import random
import copy

class SAT:

    def __init__(self, cnf_file):
        # choose random assignment (a model)
        self.variables = set()  # tracks all variables as ints
        self.clauses = set()    # tracks all claues
        self.ID_to_var = {} # dictionary tracking each variable to its numerical code
        self.var_to_ID = {}
        self.gsat_h = 0.1
        self.walksat_h = 0.3
        self.num_iterations = 0
        self.v = set()  # helper set to track the variables in their original format
        self.gsat_max_iterations = 2000
        self.walksat_max_iterations = 100000
        self.do_not_flip = set()   # a set of variables that you do not want to flip

        # self.clauses_testing = []

        i = 1

        f = open(cnf_file, "r")
        Lines = f.readlines()

        for line in Lines:
      
            clause = line.split()

            do_not_flip = False

            if len(clause) == 1:    # clause only has one variable, so variable should not be flipped

                do_not_flip = True

            clause_list = []
            c = []

            # create variables set
            for variable in clause: 


                if variable not in self.v and (int(variable) > 0):
                    self.v.add(variable)
                    negated_var = '-' + variable
                    self.variables.add(i)
                    self.ID_to_var[i] = variable
                    self.ID_to_var[-1*i] = negated_var
                    self.var_to_ID[variable] = i
                    self.var_to_ID[negated_var] = -i

                    i += 1 
                
                clause_list.append(self.var_to_ID[variable])
        
                if (do_not_flip == True):
                    self.do_not_flip.add(self.var_to_ID[variable])
                    do_not_flip = False

            self.clauses.add(tuple(clause_list))



    # GSAT algorithm
    def GSAT(self):

        # 1) choose a random assignment
        assignment = self.create_random_assignment()

        while True: 

            self.num_iterations += 1
            if (self.num_iterations > self.gsat_max_iterations):
                return False

            # 2) If the assignment satisfies all the clauses, stop.
 
            if self.check_satisfiability(assignment):
                self.assignment = assignment
                return True
            
            else:
                
                # 3) Pick a number between 0 and 1. If the number is greater than some threshold h, choose a variable uniformly at random and flip it; go back to step 2.
                if random.random() < self.gsat_h: 
                    random_var = random.choice(list(assignment))

                    while random_var in self.do_not_flip:   # do not flip
                        random_var = random.choice(list(assignment))
                    
                    self.flip_var(assignment, random_var)   # flip the variable chose
                    continue

                else:   # 3) Otherwise, for each variable, score how many clauses would be satisfied if the variable value were flipped.

                    max_score = 0
                    best_vars = []
                    for var in assignment:

                        if var in self.do_not_flip: # variable should not be flipped
                            continue

                        score = self.score_assignment(assignment, var)
                        # print(score, var)
                        if score == max_score:
                            best_vars.append(var)
                        elif score > max_score:
                            best_vars = [var]
                            max_score = score

                    # 4) Uniformly at random choose one of the variables with the highest score. Flip that variable. Go back to step 2.
                    random_num = random.randrange(len(best_vars))
                    self.flip_var(assignment, best_vars[random_num])


    # returns the solution with the original variables
    def build_solution(self, assignment):
        
        sol = []
        for var in assignment:
            sol.append(self.ID_to_var[var])

        return sol

    # writes the solution to a file
    def write_solution(self, file):
        f = open(file, "w")

        for var in self.assignment:
            string = self.ID_to_var[var] + '\n'
            f.write(string)
            
        f.close()

    # returns the score given assignment with flipped variable
    def score_assignment(self, assignment, var):
        
        score = 0
        
        for clause in self.clauses:

            for variable in list(clause):
                if variable == var:     # after variable is flipped, the variable will not make the clause true
                    continue
                elif variable == (-1 * var) or variable in assignment:    # clause would be satisfied if the variable value were flipped or if variable has same sign as assignment.

                    score += 1
                    break

        
        return score

    # retuens if assignment satisfies all clauses
    def check_satisfiability(self, assignment):

        # print("Assignment", assignment)

        for clause in self.clauses:
            satisfied = False

            for variable in list(clause):

                if variable in assignment:  # The variable is set to false in assignment
                    satisfied = True
                    break

            if not satisfied:   # no variables in clause set to false
                return False

        return True

    # WalkSAT first picks a clause which is unsatisfied by the current assignment, then flips a variable within that clause. The clause is picked at random among unsatisfied clauses. 
    def walksat(self):

        assignment = self.create_random_assignment()

        while True:

            self.num_iterations += 1
            if (self.num_iterations > self.walksat_max_iterations):
                return False

            # if assignment satisfies all clauses, return solution
            if self.check_satisfiability(assignment):
                self.assignment = assignment
                return True

            unsatisfied_clause = self.find_unsatisfied_clause(assignment) # find an unsatisfied clause

            unsatisfied_variables = []
            for unsatisfied_var in list(unsatisfied_clause):
                unsatisfied_variables.append(unsatisfied_var * -1)

            # 3) Pick a number between 0 and 1. If the number is greater than some threshold h, choose a variable uniformly at random and flip it; go back to step 2.
            if random.random() < self.walksat_h: 
                random_var = random.choice(tuple(unsatisfied_variables))

                while random_var in self.do_not_flip:   # variable should not be flipped
                    random_var = random.choice(tuple(unsatisfied_variables))
                    
                
                # flip the variable chose
                self.flip_var(assignment, random_var)
                continue

            else:

                max_score = 0
                best_vars = None

                for var in unsatisfied_variables:   # only calculate score if the variable is in the unsatisfied clause selected
                    
                    if var in self.do_not_flip: # variable should not be flipped
                        continue

                    score = self.score_assignment(assignment, var)

                    if score == max_score:
                        best_vars.append(var)
                    elif score > max_score:
                        best_vars = [var]
                        max_score = score

                # 4) Uniformly at random choose one of the variables with the highest score. Flip that variable. Go back to step 2.
                random_num = random.randrange(len(best_vars))
                self.flip_var(assignment, best_vars[random_num])


    # flips a variable in an assignment
    def flip_var(self, assignment, var):

        assignment[-1 * var] = None
        del assignment[var]


    # returns a set of unsatisfied clauses
    def find_unsatisfied_clause(self, assignment):

        unsatisfied = []
        for clause in self.clauses:
            satisfied = False

            for variable in list(clause):
                if variable in assignment:  # The variable is set to false in assignment
                    satisfied = True
                    break

            if not satisfied:   # add unsatisfied clause to the set
                unsatisfied.append(clause)

        rand = random.randrange(len(unsatisfied)) # choose a random clause from the list
        return unsatisfied[rand]


    # creates a random assignment
    def create_random_assignment(self):
        assignment = {}
        for var in self.variables:
            if random.random() >= 0.5:
                assignment[-1 * var] = None
            else:
                assignment[var] = None
        return assignment








