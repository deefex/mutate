import ast

from base_mutator import BaseMutator


class ArithmeticOperatorMutator(BaseMutator):
    """
    Official (brief):  https://docs.python.org/2/library/ast.html
    Green Tree Snakes: http://greentreesnakes.readthedocs.org/

    Binary operator tokens = Add | Sub | Mult | Div | Mod | Pow

    The arithmetic mutator replaces the operators +, -, *, /, %, ** with their counterparts:

    '+'  is mutated to '-'
    '-'  is mutated to '+'
    '*'  is mutated to '/'
    '/'  is mutated to '*'
    '%'  is mutated to '**'
    '**' is mutated to '%'

    """
    def __init__(self, base_node):
        BaseMutator.__init__(self, base_node)
        self.original_bin_op = base_node.op

        if type(base_node.op) in [ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow]:
            if type(base_node.op) is ast.Add:
                # Don't perform the mutation for string concatenation (e.g. 'string' + 'concat')
                if (type(base_node.left) is not ast.Str) and (type(base_node.right) is not ast.Str):
                    self.mutations.append({"op": ast.Sub()})

            if type(base_node.op) is ast.Sub:
                self.mutations.append({"op": ast.Add()})

            if type(base_node.op) is ast.Mult:
                # Don't perform the mutation for string repetition (e.g. 'string' * 50)
                if (type(base_node.left) is not ast.Str) and (type(base_node.right) is not ast.Str):
                    self.mutations.append({"op": ast.Div()})

            if type(base_node.op) is ast.Div:
                self.mutations.append({"op": ast.Mult()})

            if type(base_node.op) is ast.Mod:
                # Don't perform the mutation for string format (e.g. 'strings are %s' % 'cool')
                if (type(base_node.left) is not ast.Str) and (type(base_node.right) is not ast.Str):
                    self.mutations.append({"op": ast.Pow()})

            if type(base_node.op) is ast.Pow:
                self.mutations.append({"op": ast.Mod()})

    def reset(self):
        self.base_node.op = self.original_bin_op

    def mutate(self, index):
        self.base_node.op = self.mutations[index]['op']
