import unittest
from solver import *

class PropertyBasedsolverTest(unittest.TestCase):
    def test_2clause(self):
        clauseSet=[]
        
        clausedict={0: [1, -3], 1: [2, 3, -1]}
        nextid=0
        for key in clausedict.keys():
            literalSet=[]
            for symbol in clausedict[key]:
                literalSet.append(Literal(str(abs(symbol)),(False if (symbol<0) else True)))
            clauseSet.append(Clause(nextid,literalSet))
            nextid=nextid+1
        preSolution=set()
        (solution, isSat) = solve(clauseSet, preSolution)
        self.assertTrue(isSat)

    def test_1clause_unsat(self):
        clauseSet=[]
        
        clausedict={0: [1], 1: [-1]}
        nextid=0
        for key in clausedict.keys():
            literalSet=[]
            for symbol in clausedict[key]:
                literalSet.append(Literal(str(abs(symbol)),(False if (symbol<0) else True)))
            clauseSet.append(Clause(nextid,literalSet))
            nextid=nextid+1
        preSolution=set()
        (solution, isSat) = solve(clauseSet, preSolution)
        self.assertFalse(isSat)

    def test_emptyclause_unsat(self):
        clauseSet=[]
        
        clausedict={0: [], 1: []}
        nextid=0
        for key in clausedict.keys():
            literalSet=[]
            for symbol in clausedict[key]:
                literalSet.append(Literal(str(abs(symbol)),(False if (symbol<0) else True)))
            clauseSet.append(Clause(nextid,literalSet))
            nextid=nextid+1
        preSolution=set()
        (solution, isSat) = solve(clauseSet, preSolution)
        self.assertFalse(isSat)
    
    def test_oneclause_sat(self):
        clauseSet=[]
        
        clausedict={0: [1]}
        nextid=0
        for key in clausedict.keys():
            literalSet=[]
            for symbol in clausedict[key]:
                literalSet.append(Literal(str(abs(symbol)),(False if (symbol<0) else True)))
            clauseSet.append(Clause(nextid,literalSet))
            nextid=nextid+1
        preSolution=set()
        (solution, isSat) = solve(clauseSet, preSolution)
        self.assertTrue(isSat)
    
    def test_allunit_sat(self):
        clauseSet=[]
        
        clausedict={0: [1],1: [2]}
        nextid=0
        for key in clausedict.keys():
            literalSet=[]
            for symbol in clausedict[key]:
                literalSet.append(Literal(str(abs(symbol)),(False if (symbol<0) else True)))
            clauseSet.append(Clause(nextid,literalSet))
            nextid=nextid+1
        preSolution=set()
        (solution, isSat) = solve(clauseSet, preSolution)
        self.assertTrue(isSat)

    def test_one_sol_sat(self):
        clauseSet=[]
        
        clausedict={0: [1],1: [-1,3]}
        nextid=0
        for key in clausedict.keys():
            literalSet=[]
            for symbol in clausedict[key]:
                literalSet.append(Literal(str(abs(symbol)),(False if (symbol<0) else True)))
            clauseSet.append(Clause(nextid,literalSet))
            nextid=nextid+1
        preSolution=set()
        (solution, isSat) = solve(clauseSet, preSolution)
        self.assertTrue((solution)==set(['1','3']))


if __name__ == "__main__":
    unittest.main()