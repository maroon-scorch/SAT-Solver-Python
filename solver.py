#!/bin/python3
import sys
from copy import copy, deepcopy
import random
from typing import List, Set

# Feel free to change the provided types and parsing code to match
# your preferred representation of formulas, clauses, and literals.

# Run program using 'python solver.py [directory to file]'

# IO Implementation to handle the File Input (Provided by Assignment):

# Class representing a Literal:
class Literal:
    def __init__(self, name, sign):
        self.name = name  # integer
        self.sign = sign  # boolean
        # The String Representation of the value of the Literal
        self.value = ("-" if not self.sign else "") + self.name #String

    def __repr__(self):
        return ("-" if not self.sign else "") + self.name

    def __eq__(self, other):
        if type(other) != Literal:
            return False
        return self.name == other.name and self.sign == other.sign

    def __hash__(self):
      return hash((self.name, self.sign))

# Class representing a Clause:
class Clause:
    def __init__(self, id, literalSet):
        self.id = id
        self.literalSet = literalSet

    def __repr__(self):
        return f"{self.id}: {str(self.literalSet)}"

    def __eq__(self, other):
        if type(other) != Clause:
            return False
        return (self.id == other.id) and (self.literalSet == other.literalSet)


# Read and parse a cnf file, returning the variable set and clause set
def readInput(cnfFile):
    variableSet = []
    clauseSet = []
    nextCID = 0
    with open(cnfFile, "r") as f:
        for line in f.readlines():
            tokens = line.strip().split()
            if tokens and tokens[0] != "p" and tokens[0] != "c":
                literalSet = []
                for lit in tokens[:-1]:
                    sign = lit[0] != "-"
                    variable = lit.strip("-")

                    literalSet.append(Literal(variable, sign))
                    if variable not in variableSet:
                        variableSet.append(variable)

                clauseSet.append(Clause(nextCID, literalSet))
                nextCID += 1
    
    return variableSet, clauseSet


# Print the result in DIMACS format
# Assignment is a set of Strings with each String being a non-zero
# integer that is either positive or negative
def printOutput(assignment):
    result = ""
    isSat = (assignment is not None)
    if isSat:
        for var in assignment:
            result += " " + var

    print(f"s {'SATISFIABLE' if isSat else 'UNSATISFIABLE'}")
    if isSat:
        print(f"v{result} 0")

"""
    Finds all Unit Clauses within a given formula.
""" 
def findUnitClause(formula: List[Clause]) -> List[Clause]:
    unitClauseList = []
    for eachClause in formula:
        if len(eachClause.literalSet) == 1 :
            unitClauseList.append(eachClause)
    return unitClauseList        

"""
    Performs Unit Elimination on the Given Formula:
    * For all Unit Clauses found:
    1. Removes all Clauses with that Exact Clause
    2. Remove all instances of the converse of the Unit Clause
    3. Assign the Unit Clause to the solution set.
""" 
def unitElim(formula: List[Clause], solutions: Set[str]) -> List[Clause]:
    # Copy the Formula to avoid Mutability Issues
    formulaCopy = formula.copy()

    # Finds the list of Unit Clauses
    unitClauseList = findUnitClause(formulaCopy)

    # For each Unit Clause in the list:
    for eachUnitClause in unitClauseList:
        # Occurs when a Unit Clause and its Converse both exist as
        # individual clauses, the one that comes after the first will be
        # removed.
        if len(eachUnitClause.literalSet) == 0:
            continue
        else:
            # Specified Value (ex. Unit Clause of +x -> +x)
            specified = eachUnitClause.literalSet[0]
            # (ex. If specified is +x, opposite is -x)
            oppoSpecified = str(int(specified.value) * -1)

            # Remove the non-unit-Clauses containing the unit clause
            formulaCopy = list(filter(lambda eachClause:
                (specified not in eachClause.literalSet)
                or (eachClause in unitClauseList), formulaCopy))

            # Remove instances of the negation of the unit cluase
            # in all Clauses
            for i in range(0, len(formulaCopy)):
                ecId = formulaCopy[i].id
                ecClause = formulaCopy[i].literalSet
                formulaCopy[i] = Clause(ecId, list(filter(lambda eachSymbol:
                eachSymbol.value != oppoSpecified, ecClause)))
            
            # Add the Specified Value to the Solution
            solutions.add(specified.value)
    return formulaCopy

"""
    Finds all Pure Clauses in a given formula.
""" 
def findPure(formula: List[Clause]) -> Set[str]:
    pureSet = set()
    seam = set()

    for eachClause in formula:
        for eachSymbol in eachClause.literalSet:
            seam.add(eachSymbol.value)
    
    for eachVal in seam:
        if eachVal in seam and str(-1 * int(eachVal)) not in seam:
            pureSet.add(eachVal)
    
    return pureSet

"""
    Removes all clauses containing a given value (+x or -x)
""" 
def removeVal(formula: List[Clause], elt: str) -> List[Clause]:
    formulaCopy = formula.copy()
    # print("Formula Before", formulaCopy)
    formulaCopy = list(filter(lambda eachClause:
        elt not in map(lambda elt: elt.value, eachClause.literalSet), formulaCopy))
    # print("Formula After", formulaCopy)
    return formulaCopy

"""
    Performs Pure Elimination on the Formula:
    * For all Pure Clauses Found
    1. Eliminate all Clauses containing the Pure Clause
    2. Add the Pure Clause to the Solution
""" 
def pureElim(formula: List[Clause], solutions: Set[str]) -> List[Clause]:
    # Make a copy of the Formula to avoid Mutability Issues
    formulaCopy = formula.copy()
    # Find the set of Pure Clauses
    pureSet = findPure(formulaCopy)

    # For each Pure Clause:
    for eachPure in pureSet:
        # Eliminate all Clauses containing it
        formulaCopy = removeVal(formulaCopy, eachPure)
        # Add it to the solution
        solutions.add(eachPure)
    
    return formulaCopy

"""
    Checks if the Formula has an empty clause.
""" 
def hasEmptyClause(formula: List[Clause]) -> bool:
    cond = False
    for eachClause in formula:
        if (len(eachClause.literalSet) == 0):
            cond = True
            break
    return cond

"""
    Select a Literal in the Formula to recur on.
""" 
def pickVar(formula: List[Clause]) -> str:
    eltSet = set()
    for eachClause in formula:
        for eachSymbol in eachClause.literalSet:
            eltSet.add(eachSymbol.name)
    # The implementation choice here is to randomly pick a literal.
    return random.choice(tuple(eltSet))
    
"""
    Given a formula and a solution set (initially empty),
    either returns the solution that satisfies the formula or
    determine the formula to be unsat.
""" 
def solve(formula: List[Clause], solution: Set[str]) -> (Set[str], bool):
    # Performs Unit Elimination on the Formula
    unitElimFormula = unitElim(formula, solution)
    # Performs Pure Elimination on the Formula
    currentFormula = pureElim(unitElimFormula, solution)

    # If the Formula has an empty clauses - no solution
    if hasEmptyClause(currentFormula):
        return (set(), False)
    # If the Formula itself is empty, we found a solution!
    if len(currentFormula) == 0:
        return (solution.copy(), True)

    # Chooses the next Literal
    nextLit = pickVar(currentFormula)

    # Constructs the Positive Formula
    posFormula = currentFormula.copy()
    posFormula.append(Clause(len(currentFormula), [Literal(nextLit, True)]))
    posSolution = solution.copy()
    posSolution.add(nextLit)

    posResult = solve(posFormula, posSolution)
    # If positive Formula is SAT, returns the answer
    if posResult[1]:
        return posResult
    # Else, recur on the negative case
    else:
        # Constructs the Negative Formula
        negFormula = currentFormula.copy()
        negFormula.append(Clause(len(currentFormula), [Literal(nextLit, False)]))
        negSolution = solution.copy()
        negSolution.add("-" + nextLit)

        return solve(negFormula, negSolution)

"""
    Completes the Incomplete Solution given in
""" 
def completeSolve(varbset : List[str], incompleteSol: Set[str]) -> List[str]:
    unsignedSolution = list(map(lambda s: str(abs(int(s))), incompleteSol.copy()))
    completeSolution = set(incompleteSol).union(set(varbset) - set(unsignedSolution))
    return list(completeSolution)

# The Main Method to execute:
if __name__ == "__main__":
    inputFile = sys.argv[1]
    varbset, clauseSet = readInput(inputFile)

    # TODO: find a satisfying instance (or return unsat) and print it out
    print("c solving", inputFile)
    # Constructs the Initial Empty Set of Solution
    preSolution = set()
    # Retrieves the Result from the Solver
    (solution, isSat) = solve(clauseSet, preSolution)

    # If the solution is SAT, there is a possibility that the solution set
    # does not contain all literals. This is because some literals, regardless
    # of what their value is assigned, is entirely irrelevant to the outcome of
    # satisfiability. These Literals are default assigned with true.
    if isSat:
        printOutput(completeSolve(varbset, solution))
    # If the solution is UNSAT, pass None to the printOutput
    else:
        printOutput(None)