import ast
import copy
from base_mutator import BaseMutator


class ConditionalOperatorBoundaryMutator(BaseMutator):
    '''
    Official (brief):  https://docs.python.org/2/library/ast.html
    Green Tree Snakes: http://greentreesnakes.readthedocs.org/

    Comparison operator tokens = Eq | NotEq | Lt | LtE | Gt | GtE | Is | IsNot | In | NotIn

    The conditionals boundary mutator replaces the relational operators <, <=, >, >= with their counterparts:

    '<'  is mutated to '<='
    '<=' is mutated to '<'
    '>'  is mutated to '>='
    '>=' is mutated to '>'

    '''
    def __init__(self, base_node):
        BaseMutator.__init__(self, base_node)
        self.original_ops = base_node.ops

        index_count = 0
        for op in base_node.ops:

            if type(op) in [ast.Gt, ast.GtE, ast.Lt, ast.LtE]:
                if type(op) is ast.Gt:
                    ops_mutant_Gt = copy.deepcopy(base_node.ops)
                    ops_mutant_Gt[index_count] = ast.GtE()
                    self.mutations.append({"ops": ops_mutant_Gt})

                if type(op) is ast.GtE:
                    ops_mutant_GtE = copy.deepcopy(base_node.ops)
                    ops_mutant_GtE[index_count] = ast.Gt()
                    self.mutations.append({"ops": ops_mutant_GtE})

                if type(op) is ast.Lt:
                    ops_mutant_Lt = copy.deepcopy(base_node.ops)
                    ops_mutant_Lt[index_count] = ast.LtE()
                    self.mutations.append({"ops": ops_mutant_Lt})

                if type(op) is ast.LtE:
                    ops_mutant_LtE = copy.deepcopy(base_node.ops)
                    ops_mutant_LtE[index_count] = ast.Lt()
                    self.mutations.append({"ops": ops_mutant_LtE})

            index_count += 1

    def reset(self):
        self.base_node.ops = self.original_ops

    def mutate(self, index):
        self.base_node.ops = self.mutations[index]['ops']
