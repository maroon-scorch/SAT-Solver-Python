#!/bin/python3
import sys
from copy import copy, deepcopy
import random
from typing import List, Set

# Feel free to change the provided types and parsing code to match
# your preferred representation of formulas, clauses, and literals.

class Literal:
    def __init__(self, name, sign):
        self.name = name  # integer
        self.sign = sign  # boolean
        self.value = ("-" if not self.sign else "") + self.name #String

    def __repr__(self):
        return ("-" if not self.sign else "") + self.name

    def __eq__(self, other):
        if type(other) != Literal:
            return False
        return self.name == other.name and self.sign == other.sign

    def __hash__(self):
      return hash((self.name, self.sign))


class Clause:
    def __init__(self, id, literalSet):
        self.id = id
        self.literalSet = literalSet

    def __repr__(self):
        return f"{self.id}: {str(self.literalSet)}"

    def __eq__(self, other):
        if type(other) != Clause:
            return False
        return self.id == other.id


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
def printOutput(assignment):
    result = ""
    isSat = (assignment is not None)
    if isSat:
        for var in assignment:
            result += " " + var
            # result += " " + ("" if assignment[var] else "-") + var
            # str(var)

    print(f"s {'SATISFIABLE' if isSat else 'UNSATISFIABLE'}")
    if isSat:
        print(f"v{result} 0")


def findUnitClause(formula: List[Clause]) -> List[Clause]:
    unitClauseList = []
    for eachClause in formula:
        if len(eachClause.literalSet) == 1 :
            unitClauseList.append(eachClause)
    return unitClauseList

def isUnitCNeg(unitClause : Clause) -> bool:
    return (int(unitClause.literalSet[0].name) < 0)

def removeWithSpecified(formula: List[Clause], unitClauseList: List[Clause], specified: Literal):
    oppoSpecified = str(int(specified.value) * -1)

    for eachClause in formula:
        if eachClause not in unitClauseList and specified in eachClause.literalSet:
            formula.remove(eachClause)
    
    for ec in formula:
        for symbol in ec.literalSet:
            if symbol.value == oppoSpecified:
                ec.literalSet.remove(symbol)
    
        

def unitElim(formula: List[Clause], solutions: Set[str]):
    # print("Before Unit", formula)
    formulaCopy = formula.copy()
    unitClauseList = findUnitClause(formulaCopy)
    # print("Unit Clause list:", unitClauseList)
    for eachUnitClause in unitClauseList:
        if len(eachUnitClause.literalSet) == 0:
            continue
        else:
            specified = eachUnitClause.literalSet[0]
            oppoSpecified = str(int(specified.value) * -1)

            formulaCopy = list(filter(lambda eachClause:
                (specified not in eachClause.literalSet)
                or (eachClause in unitClauseList), formulaCopy))

            for i in range(0, len(formulaCopy)):
                ecId = formulaCopy[i].id
                ecClause = formulaCopy[i].literalSet
                formulaCopy[i] = Clause(ecId, list(filter(lambda eachSymbol:
                eachSymbol.value != oppoSpecified, ecClause)))
            
            # print("! ", formulaCopy)
            # formulaCopy.remove(eachUnitClause)
            solutions.add(specified.value)

    # print("Original Formula", formula)
    # print("Formula Copy", formulaCopy)
    # print(solutions)
    return formulaCopy
            # removeWithSpecified(formula, unitClauseList, specified)
            # solutions.add(specified.value)
            # formula.remove(eachUnitClause)

def findPure(formula: List[Clause]) -> List[str]:
    pureSet = set()
    seam = set()

    for eachClause in formula:
        for eachSymbol in eachClause.literalSet:
            seam.add(eachSymbol.value)
    
    for eachVal in seam:
        if eachVal in seam and str(-1 * int(eachVal)) not in seam:
            pureSet.add(eachVal)
    
    return pureSet

def removeVal(formula: List[Clause], elt: str):
    formulaCopy = formula.copy()
    # print("Formula Before", formulaCopy)
    formulaCopy = list(filter(lambda eachClause:
        elt not in map(lambda elt: elt.value, eachClause.literalSet), formulaCopy))
    # print("Formula After", formulaCopy)
    return formulaCopy



def pureElim(formula: List[Clause], solutions: Set[str]):
    formulaCopy = formula.copy()
    pureSet = findPure(formulaCopy)
    # print("Pureset", pureSet)
    for eachPure in pureSet:
        formulaCopy = removeVal(formulaCopy, eachPure)
        solutions.add(eachPure)
    
    return formulaCopy
        # assign x consistent with its sign

def hasEmptyClause(formula: List[Clause]) -> bool:
    cond = False
    for eachClause in formula:
        if (len(eachClause.literalSet) == 0):
            cond = True
            break
    return cond

# Can change later just dont want to deal with now
def pickVar(formula: List[Clause]) -> str:
    eltSet = set()
    for eachClause in formula:
        for eachSymbol in eachClause.literalSet:
            eltSet.add(eachSymbol.name)
    return random.choice(tuple(eltSet))
    

def solve(formula: List[Clause], solution: Set[str]) -> (Set[str], bool):
    # print("Before Elim", formula)
    unitElimFormula = unitElim(formula, solution)
    #print("After Unit", unitElimFormula)
    currentFormula = pureElim(unitElimFormula, solution)
    # print("After 1 Solve", currentFormula)
    # print("Original", formula)
    # print("After Pure Elim", formula)
    # print("After Pure Elim SOlution", solution)

    if hasEmptyClause(currentFormula):
        return (set(), False)
    if len(currentFormula) == 0:
        return (solution.copy(), True)


    nextLit = pickVar(currentFormula)
    # print("Picked Var:", nextLit)

    posFormula = currentFormula.copy()
    posFormula.append(Clause(len(currentFormula), [Literal(nextLit, True)]))
    posSolution = solution.copy()
    posSolution.add(nextLit)

    posResult = solve(posFormula, posSolution)
    if posResult[1]:
        return posResult
    else:
        negFormula = currentFormula.copy()
        negFormula.append(Clause(len(currentFormula), [Literal(nextLit, False)]))
        negSolution = solution.copy()
        negSolution.add("-" + nextLit)
        # print("F ", solution)
  
        # print("FIRSTTTTTTTTTTTTTTTTTTTTT", nextLit)
        # print("FIRSTTTTTTTTTTTTTTTTTTTTT", nextLit)
        # print("FFFFF", negFormula)
        return solve(negFormula, negSolution)

'''
func solve(varAssignment, formula):
	// do unit clause elim and pure literal elim on the formula
	unitClauseElim(formula)
	pureLiteralElim(formula)

	if formula has empty clause
		return unsat
	if formula has no clauses
		sat -> return current varAssignment
	
	x := pickVar(formula) // do anything reasonable here
	if solve(varAssignment + {+x}, formula) is sat
		return result of solving with x assigned to true
	else
		return solve(varAssignment + {-x}, formula)
'''


if __name__ == "__main__":
    inputFile = sys.argv[1]
    varbset, clauseSet = readInput(inputFile)
    # print(varbset)
    # print("Before Elim: ", clauseSet)
    # # TODO: find a satisfying instance (or return unsat) and print it out
    # print(pickVar(clauseSet))


    # # Solution Set
    # solutions = set()

    # print(clauseSet)
    # clauseSet = list(filter(lambda ec: len(ec.literalSet) == 1, clauseSet))
    # print(clauseSet)


    # Unit Clause Step
    # print("Formula:", clauseSet)
    # newC = unitElim(clauseSet, solutions)
    # print("After Unit Elim :", newC)
    # newC1 = pureElim(newC, solutions)
    # print("After Pure Elim :", newC1)

    print("c solving", inputFile)
    preSolution = set()
    (solution, isSat) = solve(clauseSet, preSolution)

    # print('----')
    # print(isSat)
    # print(solution)

    if isSat:
        unsignedSolution = list(map(lambda s: str(abs(int(s))), solution.copy()))
        completeSolution = set(solution).union(set(varbset) - set(unsignedSolution))
        # print(completeSolution)
        printOutput(list(completeSolution))
    else:
        printOutput(None)


    '''
    for each unit clause {+/-x} in formula
	remove all non-unit clauses containing +/-x
	remove all instances of -/+x in every clause // flipped sign!
	assign x consistent with its sign in unit clause
    '''


