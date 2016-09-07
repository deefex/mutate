import ast
from base_mutator import BaseMutator


class LogicalOperatorMutator(BaseMutator):
    '''
    Official (brief):  https://docs.python.org/2/library/ast.html
    Green Tree Snakes: http://greentreesnakes.readthedocs.org/

    Boolean operator tokens = And | Or

    The conditionals negation mutator replaces the relational operators And, Or with their counterparts:

    'And' is mutated to 'Or'
    'Or'  is mutated to 'And'

    '''
    def __init__(self, base_node):
        BaseMutator.__init__(self, base_node)
        self.original_bool_op = base_node.op

        if type(base_node.op) is ast.Or:
            self.mutations.append(ast.And())

        if type(base_node.op) is ast.And:
            self.mutations.append(ast.Or())

    def reset(self):
        self.base_node.op = self.original_bool_op

    def mutate(self, index):
        self.base_node.op = self.mutations[index]
