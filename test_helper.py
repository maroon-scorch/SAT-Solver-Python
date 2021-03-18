import unittest
from solver import *
from formula_constructor import constructFormula

# Testing for Individual Components of the Solver
class findUnitClauseTest(unittest.TestCase):
    def test_empty_formula(self):
        clauseSet=[]
        solution = findUnitClause(clauseSet)
        self.assertEqual(solution, [], "Empty list should return empty")

    def test_has_empty(self):
        clausedict={0: [1, 5], 1: [], 2: [-1, 6], 3: [5]}
        clauseSet = constructFormula(clausedict)
        solution = findUnitClause(clauseSet)
        self.assertEqual(solution, constructFormula({3: [5]}))

    def test_only_unit(self):
        clausedict={0: [1], 1: [3], 2: [-1]}
        clauseSet = constructFormula(clausedict)
        solution = findUnitClause(clauseSet)
        self.assertEqual(solution, clauseSet)
    
    def test_no_unit(self):
        clausedict={0: [1, 9, 8], 1: [3, 5], 2: [-1, 4]}
        clauseSet = constructFormula(clausedict)
        solution = findUnitClause(clauseSet)
        self.assertEqual(solution, [])

    def test_example(self):
        clausedict={0: [1, 9, 8], 1: [3, 5], 2: [-1], 3: [10], 4:[4]}
        clauseSet = constructFormula(clausedict)
        solution = findUnitClause(clauseSet)
        self.assertEqual(solution, constructFormula({2: [-1], 3: [10], 4:[4]}))

class unitElimTest(unittest.TestCase):
    def test_empty_formula(self):
        clauseSet=[]
        solution = set()
        formula = unitElim(clauseSet, solution)
        self.assertEqual(formula, [])
        self.assertEqual(solution, set())
    
    def test_example(self):
        clausedict={0: [1, 9, 8, 3], 1: [3], 2: [-1, -3], 3: [-10], 4:[4, -10, 6, 3], 5:[1, 2, 10]}
        clauseSet = constructFormula(clausedict)
        solution = set()

        formula = unitElim(clauseSet, solution)
        self.assertEqual(formula, constructFormula({1: [3], 2: [-1], 3:[-10], 5:[1, 2]}))
        self.assertEqual(solution, {'3', '-10'})

    def test_has_empty(self):
        clausedict={0: [1], 1: [], 2: [-1, 6], 3: [5, 6]}
        clauseSet = constructFormula(clausedict)
        solution = set()

        formula = unitElim(clauseSet, solution)
        self.assertEqual(formula, constructFormula({0: [1], 1: [], 2: [6], 3:[5, 6]}))
        self.assertEqual(solution, {'1'})

    def test_only_unit(self):
        clausedict={0: [1], 1: [3], 2: [1]}
        clauseSet = constructFormula(clausedict)
        solution = set()

        formula = unitElim(clauseSet, solution)
        self.assertEqual(formula, constructFormula({0: [1], 1: [3], 2: [1]}))
        self.assertEqual(solution, {'1', '3'})
    
    def test_no_unit(self):
        clausedict={0: [1, 9, 8], 1: [3, 5], 2: [-1, 4]}
        clauseSet = constructFormula(clausedict)
        solution = set()

        formula = unitElim(clauseSet, solution)
        self.assertEqual(formula, constructFormula(clausedict))
        self.assertEqual(solution, set())

    def test_opp_unit(self):
        clausedict={0: [1], 1: [3, 1, 5], 2: [-1], 3: [4, 5, -1]}
        clauseSet = constructFormula(clausedict)
        solution = set()

        formula = unitElim(clauseSet, solution)
        self.assertEqual(formula, constructFormula({0: [], 2: [], 3: [4, 5]}))
        self.assertEqual(solution, {'1', '-1'})

    def test_no_elim(self):
        clausedict={0: [1, 9, 8], 1: [3, 5], 2: [-1, 4], 3: [7, 6, -8, 9], 4: [15], 5: [1, 7, 5]}
        clauseSet = constructFormula(clausedict)
        solution = set()

        formula = unitElim(clauseSet, solution)
        self.assertEqual(formula, constructFormula(clausedict))
        self.assertEqual(solution, {'15'})

class findPureTest(unittest.TestCase):
    def test_empty_formula(self):
        clauseSet=[]
        answer = findPure(clauseSet)
        self.assertEqual(answer, set())
    
    def test_find_example(self):
        clausedict={0: [1, 9, 8], 1: [3, 1, 5], 2: [1, 4], 3: [-7, 6, -8, 1, 9], 4: [1, 7, 5]}
        clauseSet = constructFormula(clausedict)

        answer = findPure(clauseSet)
        self.assertEqual(answer, {'6', '3', '5', '9', '1', '4'})

    def test_no_pure_found(self):
        clausedict = {0: [-1, 4, 5], 1: [-4, 1], 2: [-5], 3: [3, -3]}
        clauseSet = constructFormula(clausedict)

        answer = findPure(clauseSet)
        self.assertEqual(answer, set())

    def test_one_pure(self):
        clausedict = {0: [-1, 4, 5], 1: [-4, 1], 2: [-5], 3: [3]}
        clauseSet = constructFormula(clausedict)

        answer = findPure(clauseSet)
        self.assertEqual(answer, {'3'})

class removeValTest(unittest.TestCase):
    def test_empty_formula(self):
        clauseSet=[]
        answer = removeVal(clauseSet, "6")
        self.assertEqual(answer, list())
    
    def test_formula_reduced_to_none(self):
        clausedict={0: [1, 9, 8], 1: [3, 1, 5], 2: [1, 4], 3: [7, 6, -8, 1, 9], 4: [1, 7, 5]}
        clauseSet = constructFormula(clausedict)

        formula = removeVal(clauseSet, "1")
        self.assertEqual(formula, [])

    def test_nothing_removed(self):
        clausedict={0: [1, 9, 8], 1: [3, 1, 5], 2: [1, 4], 3: [7, 6, -8, 1, 9], 4: [1, 7, 5]}
        clauseSet = constructFormula(clausedict)

        formula = removeVal(clauseSet, "-1")
        self.assertEqual(formula, constructFormula(clausedict))

    def test_partial_removed(self):
        clausedict={0: [1, 9, 8], 1: [3, 1, 5], 2: [1, 8, 4], 3: [7, 6, 8, 1, 9], 4: [1, 7, 5]}
        clauseSet = constructFormula(clausedict)

        formula = removeVal(clauseSet, "8")
        self.assertEqual(formula, constructFormula({1: [3, 1, 5], 4: [1, 7, 5]}))

    def test_remove_negative(self):
        clausedict={0: [1, -4, 8], 1: [3, 1, 5], 2: [1, 8, -4]}
        clauseSet = constructFormula(clausedict)

        formula = removeVal(clauseSet, "-4")
        self.assertEqual(formula, constructFormula({1: [3, 1, 5]}))

class pureElimTest(unittest.TestCase):
    def test_empty_formula(self):
        clauseSet=[]
        solution = set()

        formula = pureElim(clauseSet, solution)
        self.assertEqual(formula, [])
        self.assertEqual(solution, set())

    def test_example_pure_elim(self):
        clausedict={0: [1, 4, -8], 1: [3, 1, 5], 2: [8, -4]}
        clauseSet = constructFormula(clausedict)
        solution = set()

        formula = pureElim(clauseSet, solution)
        self.assertEqual(formula, constructFormula({2: [8, -4]}))
        self.assertEqual(solution, {'1', '3', '5'})

    def test_no_elim(self):
        clausedict={0: [1, 4, -8], 1: [3, -1, 5], 2: [8, -4], 4: [-3, -5]}
        clauseSet = constructFormula(clausedict)
        solution = set()

        formula = pureElim(clauseSet, solution)
        self.assertEqual(formula, constructFormula(clausedict))
        self.assertEqual(solution, set())

    def test_one_pure(self):
        clausedict={0: [1, 4, -8], 1: [3, -1, 2, 5], 2: [8, 2, -4], 4: [-3, -5], 5: [2]}
        clauseSet = constructFormula(clausedict)
        solution = set()

        formula = pureElim(clauseSet, solution)
        self.assertEqual(formula, constructFormula({0: [1, 4, -8], 4: [-3, -5] }))
        self.assertEqual(solution, {'2'})

class hasEmptyClauseTest(unittest.TestCase):
    def test_empty(self):
        formula = []
        self.assertFalse(hasEmptyClause(formula))

    def test_only_empty(self):
        formulaDict = {0: [], 1: []}
        formula = constructFormula(formulaDict)
        self.assertTrue(hasEmptyClause(formula))

    def test_has_empty(self):
        formulaDict = {0: [5, 6, 7], 1: [1, 2, 5], 2: [], 3: [5, 7, 1]}
        formula = constructFormula(formulaDict)
        self.assertTrue(hasEmptyClause(formula))

    def test_has_no_empty(self):
        formulaDict = {0: [5, 6, 7], 1: [1, 2, -5], 2: [6, 7, -1], 3: [-5, 7, 1]}
        formula = constructFormula(formulaDict)
        self.assertFalse(hasEmptyClause(formula))

class pickVarTest(unittest.TestCase):
    def test_one(self):
        formulaDict = {0: [1]}
        formula = constructFormula(formulaDict)
        self.assertEqual(pickVar(formula), '1')

    def test_negative_gives_positive(self):
        formulaDict = {0: [-1]}
        formula = constructFormula(formulaDict)
        self.assertEqual(pickVar(formula), '1')

    def test_example_is_one_value(self):
        formulaDict = {0: [-1], 1: [1], 2: [-1, 1]}
        formula = constructFormula(formulaDict)
        self.assertEqual(pickVar(formula), '1')

    def test_example(self):
        formulaDict = {0: [-1, 3, 2], 1: [1, 5, 6], 2: [4, 1]}
        formula = constructFormula(formulaDict)
        self.assertTrue(pickVar(formula) in {"1", "2", "3", "4", "5", "6"})

# Tests for the Main Solver (Integration Testing) is under test_solver.py

if __name__ == "__main__":
    unittest.main()