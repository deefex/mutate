import ast

from base_mutator import BaseMutator


class UnaryOperatorMutator(BaseMutator):
    """
    Official (brief):  https://docs.python.org/2/library/ast.html
    Green Tree Snakes: http://greentreesnakes.readthedocs.org/

    Unary operator tokens = Invert | Not | UAdd | USub

    The unary mutator replaces the operators +, -, with their counterparts:

    '+' is mutated to '-'
    '-' is mutated to '+'

    """
    def __init__(self, base_node):
        BaseMutator.__init__(self, base_node)
        self.original_unary_op = base_node.op

        if type(base_node.op) in [ast.UAdd, ast.USub]:
            if type(base_node.op) is ast.UAdd:
                self.mutations.append({"op": ast.USub()})

            if type(base_node.op) is ast.USub:
                self.mutations.append({"op": ast.UAdd()})

    def reset(self):
        self.base_node.op = self.original_unary_op

    def mutate(self, index):
        self.base_node.op = self.mutations[index]['op']