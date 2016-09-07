import ast
import copy
from base_mutator import BaseMutator


class ConditionalOperatorNegationMutator(BaseMutator):
    '''
    Official (brief):  https://docs.python.org/2/library/ast.html
    Green Tree Snakes: http://greentreesnakes.readthedocs.org/

    Comparison operator tokens = Eq | NotEq | Lt | LtE | Gt | GtE | Is | IsNot | In | NotIn

    The conditionals negation mutator replaces the relational operators ==, != <, <=, >, >= with their counterparts:

    '=='     is mutated to '!='
    '!='     is mutated to '=='
    '<='     is mutated to '>'
    '>='     is mutated to '<'
    '<'      is mutated to '>='
    '>'      is mutated to '<='
    'is'     is mutated to 'is not'
    'is not' is mutated to 'is'
    'in'     is mutated to 'not in'
    'not in' is mutated to 'in'

    '''
    def __init__(self, base_node):
        BaseMutator.__init__(self, base_node)
        self.original_ops = base_node.ops

        index_count = 0
        for op in base_node.ops:

            if type(op) in [ast.Gt, ast.GtE, ast.Lt, ast.LtE, ast.Eq, ast.NotEq, ast.Is, ast.IsNot, ast.In, ast.NotIn]:
                if type(op) is ast.Eq:
                    ops_mutant_Eq = copy.deepcopy(base_node.ops)
                    ops_mutant_Eq[index_count] = ast.NotEq()
                    self.mutations.append({"ops": ops_mutant_Eq})

                if type(op) is ast.NotEq:
                    ops_mutant_NotEq = copy.deepcopy(base_node.ops)
                    ops_mutant_NotEq[index_count] = ast.Eq()
                    self.mutations.append({"ops": ops_mutant_NotEq})

                if type(op) is ast.LtE:
                    ops_mutant_LtE = copy.deepcopy(base_node.ops)
                    ops_mutant_LtE[index_count] = ast.Gt()
                    self.mutations.append({"ops": ops_mutant_LtE})

                if type(op) is ast.GtE:
                    ops_mutant_GtE = copy.deepcopy(base_node.ops)
                    ops_mutant_GtE[index_count] = ast.Lt()
                    self.mutations.append({"ops": ops_mutant_GtE})

                if type(op) is ast.Lt:
                    ops_mutant_Lt = copy.deepcopy(base_node.ops)
                    ops_mutant_Lt[index_count] = ast.GtE()
                    self.mutations.append({"ops": ops_mutant_Lt})

                if type(op) is ast.Gt:
                    ops_mutant_Gt = copy.deepcopy(base_node.ops)
                    ops_mutant_Gt[index_count] = ast.LtE()
                    self.mutations.append({"ops": ops_mutant_Gt})

                if type(op) is ast.Is:
                    ops_mutant_Is = copy.deepcopy(base_node.ops)
                    ops_mutant_Is[index_count] = ast.IsNot()
                    self.mutations.append({"ops": ops_mutant_Is})

                if type(op) is ast.IsNot:
                    ops_mutant_IsNot = copy.deepcopy(base_node.ops)
                    ops_mutant_IsNot[index_count] = ast.Is()
                    self.mutations.append({"ops": ops_mutant_IsNot})

                if type(op) is ast.In:
                    ops_mutant_In = copy.deepcopy(base_node.ops)
                    ops_mutant_In[index_count] = ast.NotIn()
                    self.mutations.append({"ops": ops_mutant_In})

                if type(op) is ast.NotIn:
                    ops_mutant_NotIn = copy.deepcopy(base_node.ops)
                    ops_mutant_NotIn[index_count] = ast.In()
                    self.mutations.append({"ops": ops_mutant_NotIn})

            index_count += 1

    def reset(self):
        self.base_node.ops = self.original_ops

    def mutate(self, index):
        self.base_node.ops = self.mutations[index]['ops']
