import ast

from base_mutator import BaseMutator


class BreakContinueMutator(BaseMutator):
    """
    Official (brief):  https://docs.python.org/2/library/ast.html
    Green Tree Snakes: http://greentreesnakes.readthedocs.org/

    The break-continue mutator negates the statements in the code:

    'break'    is mutated to 'continue'
    'continue' is mutated to 'break'

    """
    def __init__(self, base_node):
        BaseMutator.__init__(self, base_node)
        self.original_node = base_node

        # TODO - This doesn't work - AST node needs replaced
        if base_node.__class__ is ast.Break:
            self.mutations.append(ast.Continue(lineno=base_node.lineno,
                                               col_offset=base_node.col_offset
                                               )
                                  )
        # TODO - This doesn't work - AST node needs replaced
        if base_node.__class__ is ast.Continue:
            self.mutations.append(ast.Break(lineno=base_node.lineno,
                                            col_offset=base_node.col_offset
                                            )
                                  )

    def reset(self):
        self.base_node = self.original_node

    def mutate(self, index):
        self.base_node = self.mutations[index]