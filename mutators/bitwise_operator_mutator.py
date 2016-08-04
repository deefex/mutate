import ast
import copy

from mutators.base_mutator import BaseMutator


class BitwiseOperatorMutator(BaseMutator):
    '''
    Official (brief):  https://docs.python.org/2/library/ast.html
    Green Tree Snakes: http://greentreesnakes.readthedocs.org/

    Binary operator tokens = LShift | RShift | BitOr | BitXor | BitAnd | FloorDiv

    The arithmetic mutator replaces the operators <<, >>, |, ^, &, / with their counterparts:

    '<<' is mutated to '>>'
    '>>' is mutated to '<<'
    '|'  is mutated to '&'
    '^'  is mutated to '/'
    '&'  is mutated to '|'
    '/'  is mutated to '^'

    '''
    def __init__(self, base_node):
        BaseMutator.__init__(self, base_node)
        self.original_bin_op = base_node.op

        if type(base_node.op) in [ast.LShift, ast.RShift, ast.BitOr, ast.BitXor, ast.BitAnd, ast.FloorDiv]:
            if type(base_node.op) is ast.LShift:
                self.mutations.append({"op": ast.RShift()})

            if type(base_node.op) is ast.RShift:
                self.mutations.append({"op": ast.LShift()})

            if type(base_node.op) is ast.BitOr:
                self.mutations.append({"op": ast.BitAnd()})

            if type(base_node.op) is ast.BitXor:
                self.mutations.append({"op": ast.FloorDiv()})

            if type(base_node.op) is ast.BitAnd:
                self.mutations.append({"op": ast.BitOr()})

            if type(base_node.op) is ast.FloorDiv:
                self.mutations.append({"op": ast.BitXor()})

    def reset(self):
        self.base_node.op = self.original_bin_op

    def mutate(self, index):
        self.base_node.op = self.mutations[index]['op']
