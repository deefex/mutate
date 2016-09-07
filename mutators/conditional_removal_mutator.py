import ast
from base_mutator import BaseMutator


class ConditionalRemovalMutator(BaseMutator):
    """
    Official (brief):  https://docs.python.org/2/library/ast.html
    Green Tree Snakes: http://greentreesnakes.readthedocs.org/

    The conditionals removal mutator replaces the original conditional with both True and False to execute protected
    statements in `if`, `elif` and `else` legs.

    """
    def __init__(self, base_node):
        BaseMutator.__init__(self, base_node)
        self.original_test = base_node.test

        if (base_node.__class__ == ast.If) and (base_node.test.__class__ == ast.BoolOp):

            # Mutate the original statement so that the protected statements *always* execute
            self.mutations.append({"test": ast.Name(id='True',
                                                    ctx=ast.Load(),
                                                    lineno=base_node.test.lineno,
                                                    col_offset=base_node.test.col_offset,
                                                    )
                                   })

            # Mutate the original statement so that the protected statements *never* execute
            # (and any 'else' statements *always* execute)
            self.mutations.append({"test": ast.Name(id='False',
                                                    ctx=ast.Load(),
                                                    lineno=base_node.test.lineno,
                                                    col_offset=base_node.test.col_offset,
                                                    )
                                   })

    def reset(self):
        self.base_node.test = self.original_test

    def mutate(self, index):
        self.base_node.test = self.mutations[index]['test']