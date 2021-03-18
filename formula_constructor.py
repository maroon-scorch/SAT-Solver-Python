from solver import *
from typing import List, Dict
import random

"""
    Constructs a formula with a given dictionary of id to List of integers
""" 
def constructFormula(clausedict: Dict[int, List[int]]) -> List[Clause]:
    clauseSet = []
    nextid=0
    for key in clausedict.keys():
        literalSet=[]
        for symbol in clausedict[key]:
            literalSet.append(Literal(str(abs(symbol)),(False if (symbol<0) else True)))
        clauseSet.append(Clause(key,literalSet))
    return clauseSet

"""
    Constructs a random formula with numLit literals and numClause clauses
""" 
def constructRandomFormula(numLit: int, numClause: int) -> (List[str], List[Clause]):
    varSet = list(range(1, numLit + 1))
    varCopy = varSet.copy()
    for i in range(0, len(varCopy)):
        varCopy[i] = str(varCopy[i])

    formulaDict = {}

    for i in range(0, numClause):
        n = random.randint(0, numLit)
        litList = random.sample(varSet, n)
        listForDict = list()
        for eachLit in litList:
            listForDict.append(eachLit) if (bool(random.getrandbits(1))) else listForDict.append(-1*eachLit)
        formulaDict[i] = listForDict

    formula = constructFormula(formulaDict)
    return (varCopy, formula)

"""
    Given a solution and a formula, solves the formula with that solution
""" 
def solveFormula(formula : List[Clause], solution : List[str]) -> bool:
    boolDict = {}
    # Convert the solution to a dictionary of integer to true or false
    for eachS in solution:
        numSol = int(eachS)
        absSol = abs(numSol)
        boolDict[absSol] = (numSol > 0)
        boolDict[(-1 * absSol)] = not boolDict[absSol]
    
    answer = True
    # Apply the solution to the formula
    for eachClause in formula:
        eachClauseVal = False
        for eachLit in eachClause.literalSet:
            eachVal = int(eachLit.value)
            eachClauseVal = eachClauseVal or boolDict[eachVal]
        
        answer = answer and eachClauseVal
    return answer