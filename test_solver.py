import unittest
from solver import *
from formula_constructor import constructFormula, constructRandomFormula, solveFormula

# Testing for Solver as a Whole and the Oracle for Testing Property Based Test
# Run tests using 'python test_solver.py'

# Testing the Solver and Rechecking the Solution with solveFormula
class solverTest(unittest.TestCase):
    def test_2clause(self):
        clausedict={0: [1, -3], 1: [2, 3, -1]}
        clauseSet = constructFormula(clausedict)
        preSolution=set()
        (solution, isSat) = solve(clauseSet, preSolution)
        self.assertTrue(isSat)

        completeSolution = completeSolve({'1', '2', '3'}, solution)
        self.assertTrue(solveFormula(clauseSet, completeSolution))

    def test_1clause_unsat(self):
        clausedict={0: [1], 1: [-1]}
        clauseSet = constructFormula(clausedict)
        preSolution=set()
        (solution, isSat) = solve(clauseSet, preSolution)
        self.assertFalse(isSat)

    def test_emptyclause_unsat(self):
        clausedict={0: [], 1: []}
        clauseSet = constructFormula(clausedict)
        preSolution=set()
        (solution, isSat) = solve(clauseSet, preSolution)
        self.assertFalse(isSat)
    
    def test_oneclause_sat(self):
        clausedict={0: [1]}
        clauseSet = constructFormula(clausedict)
        preSolution=set()
        (solution, isSat) = solve(clauseSet, preSolution)
        self.assertTrue(isSat)
        self.assertEqual(solution, {'1'})
        
        completeSolution = completeSolve({'1'}, solution)
        self.assertTrue(solveFormula(clauseSet, completeSolution))
    
    def test_allunit_sat(self):
        clausedict={0: [1],1: [2]}
        clauseSet = constructFormula(clausedict)
        preSolution=set()
        (solution, isSat) = solve(clauseSet, preSolution)
        self.assertTrue(isSat)
        self.assertEqual(solution, {'1', '2'})
        
        completeSolution = completeSolve({'1', '2'}, solution)
        self.assertTrue(solveFormula(clauseSet, completeSolution))

    def test_one_sol_sat(self):
        clausedict={0: [1],1: [-1,3]}
        clauseSet = constructFormula(clausedict)
        preSolution=set()
        (solution, isSat) = solve(clauseSet, preSolution)
        self.assertTrue(isSat)
        self.assertTrue((solution)==set(['1','3']))

        completeSolution = completeSolve({'1', '3'}, solution)
        self.assertTrue(solveFormula(clauseSet, completeSolution))
        
    def test_empty(self):
        clausedict={}
        clauseSet = constructFormula(clausedict)
        preSolution=set()
        (solution, isSat) = solve(clauseSet, preSolution)
        self.assertTrue(isSat)
        self.assertEqual(solution, set())

    def test_has_empty(self):
        clausedict={0: [1],1: [-1,3], 2: [4, 5, -2], 3: [], 4: [6, 5, -4]}
        clauseSet = constructFormula(clausedict)
        preSolution=set()
        (solution, isSat) = solve(clauseSet, preSolution)
        self.assertFalse(isSat)

class completeSolveTest(unittest.TestCase):
    def test_example(self):
        varbset = ["1", "2", "3", "4", "5"]
        solution = {"-1", "2", "-4"}
        complete = completeSolve(varbset, solution)
        self.assertEqual(set(complete), {"-1", "2", "3", "-4", "5"})

    def test_empty_solution(self):
        varbset = ["1", "2", "3", "4", "5"]
        solution = {}
        complete = completeSolve(varbset, solution)
        self.assertEqual(set(complete), {"1", "2", "3", "4", "5"})

    def test_nothing_to_add(self):
        varbset = ["1", "2", "3", "4", "5"]
        solution = {"-1", "-2", "3", "4", "-5"}
        complete = completeSolve(varbset, solution)
        self.assertEqual(set(complete), {"-1", "-2", "3", "4", "-5"})

class constructRandomFormulaTest(unittest.TestCase):
    def test_construct_zero(self):
        (varbset, formula) = constructRandomFormula(0, 0)
        self.assertEqual(varbset, [])
        self.assertEqual(formula, [])
    
    def test_construct_zero_clause(self):
        (varbset, formula) = constructRandomFormula(4, 0)
        self.assertEqual(varbset, ["1", "2", "3", "4"])
        self.assertEqual(formula, [])

    def test_construct_zero_varbset(self):
        (varbset, formula) = constructRandomFormula(0, 4)
        self.assertEqual(varbset, [])
        self.assertEqual(formula, constructFormula({0: [], 1: [], 2: [], 3: []}))

    def test_varbset_always_in_range(self):
        numLoop = 100
        for i in range(0, numLoop):
            numLit = random.randint(1, 50)
            numClause = 0
            (varbset, formula) = constructRandomFormula(numLit, numClause)

            self.assertEqual(varbset, list(map(lambda elt: str(elt), list(range(1, numLit + 1)))))

    def test_clause_satisfy_property(self):
        numLoop = 100
        for i in range(0, numLoop):
            numLit = random.randint(1, 50)
            numClause = random.randint(1, 50)
            (varbset, formula) = constructRandomFormula(numLit, numClause)

            self.assertTrue(len(formula) == numClause)

            for eachClause in formula:
                litSet = eachClause.literalSet
                absLitSet = list(map(lambda elt: str(abs(int(elt.value))), litSet))
                self.assertTrue(len(litSet) <= len(varbset))
                self.assertTrue(set(absLitSet) <= set(varbset))

class PropertyBasedTestForSolver(unittest.TestCase):
    def test_formula_at_scale(self):
        numLoop = 100
        for i in range(0, numLoop):
            # Constructs the Formula
            numLit = random.randint(1, 50)
            numClause = random.randint(1, 50)
            (varbset, formula) = constructRandomFormula(numLit, numClause)
            # Solves the Formula
            preSolution=set()
            (solution, isSat) = solve(formula, preSolution)
            # Verify the solution is correct if isSat
            if isSat:
                completeSolution = completeSolve(varbset, solution)
                self.assertTrue(solveFormula(formula, completeSolution))

if __name__ == "__main__":
    unittest.main()