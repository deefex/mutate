import ast

from mutators.logical_operator_mutator import LogicalOperatorMutator
from mutators.conditional_operator_boundary_mutator import ConditionalOperatorBoundaryMutator
from mutators.conditional_operator_negation_mutator import ConditionalOperatorNegationMutator
from mutators.arithmetic_operator_mutator import ArithmeticOperatorMutator
from mutators.bitwise_operator_mutator import BitwiseOperatorMutator
from mutators.unary_operator_mutator import UnaryOperatorMutator
from mutators.conditional_removal_mutator import ConditionalRemovalMutator
#from mutators.break_continue_mutator import BreakContinueMutator
from utils import *

'''
Possible additions/alternatives:
Statements
  visit_Assert
  visit_Assign
  visit_AugAssign
  visit_ImportFrom
  visit_Import
  visit_Expr
  visit_FunctionDef
  visit_ClassDef
  visit_If          *
  visit_For
  visit_While
  visit_With
  visit_Pass
  visit_Print
  visit_Delete
  visit_TryExcept
  visit_TryFinally
  visit_Global
  visit_Nonlocal
  visit_Return
  visit_Break       *
  visit_Continue    *
  visit_Raise
Expressions
  visit_Attribute
  visit_Call
  visit_Name
  visit_Str
  visit_Bytes
  visit_Num
  visit_Tuple
  visit_Dict
  visit_BinOp       *
  visit_BoolOp      *
  visit_Compare     *
  visit_UnaryOp     *
  visit_Subscript
  visit_Slice
  visit_ExtSlice
  visit_Yield
  visit_Lambda
  visit_Ellipsis
  visit_DictComp
  visit_IfExp
  visit_Starred
  visit_Repr
Helper
  visit_alias
  visit_comprehension
  visit_excepthandler
  visit_arguments
'''


class AstVisitor(ast.NodeVisitor):
    def __init__(self, filename):
        ast.NodeVisitor.__init__(self)
        self.filename = filename
        self.sample_source = get_file_as_string(self.filename)
        self.initial_tree = ast.parse(self.sample_source)
        self.genes = {}
        self.mutators = []
        self.visit(self.initial_tree)

    def visit_Compare(self, node):
        if 'Compare' not in self.genes:
            self.genes['Compare'] = []
        compare_op = ConditionalOperatorBoundaryMutator(node)
        self.mutators.append(compare_op)
        self.genes['Compare'].append(node)
        self.generic_visit(node)
        compare_op = ConditionalOperatorNegationMutator(node)
        self.mutators.append(compare_op)
        self.genes['Compare'].append(node)
        self.generic_visit(node)

    def visit_BoolOp(self, node):
        if 'BoolOp' not in self.genes:
            self.genes['BoolOp'] = []
        bool_op = LogicalOperatorMutator(node)
        self.mutators.append(bool_op)
        self.genes['BoolOp'].append(node)
        self.generic_visit(node)

    def visit_BinOp(self, node):
        if 'BinOp' not in self.genes:
            self.genes['BinOp'] = []
        bin_op = ArithmeticOperatorMutator(node)
        self.mutators.append(bin_op)
        self.genes['BinOp'].append(node)
        self.generic_visit(node)
        bin_op = BitwiseOperatorMutator(node)
        self.mutators.append(bin_op)
        self.genes['BinOp'].append(node)
        self.generic_visit(node)

    def visit_UnaryOp(self, node):
        if 'UnaryOp' not in self.genes:
            self.genes['UnaryOp'] = []
        unary_op = UnaryOperatorMutator(node)
        self.mutators.append(unary_op)
        self.genes['UnaryOp'].append(node)
        self.generic_visit(node)

    def visit_If(self, node):
        if 'If' not in self.genes:
            self.genes['If'] = []
        test = ConditionalRemovalMutator(node)
        self.mutators.append(test)
        self.genes['If'].append(node)
        self.generic_visit(node)

    # TODO - These mutators currently don't work as they need to replace an entire AST node (as opposed to
    # TODO - simply changing the attributes as the others do.

    '''def visit_Break(self, node):
        if 'Break' not in self.genes:
            self.genes['Break'] = []
        test = BreakContinueMutator(node)
        self.mutators.append(test)
        self.genes['Break'].append(node)
        self.generic_visit(node)

    def visit_Continue(self, node):
        if 'Continue' not in self.genes:
            self.genes['Continue'] = []
        test = BreakContinueMutator(node)
        self.mutators.append(test)
        self.genes['Continue'].append(node)
        self.generic_visit(node)'''