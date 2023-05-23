from __future__ import annotations

import enum
from typing import *
from dataclasses import dataclass


"""
This module contains components that are used in the transpiler and the
parser

This file is not split up like the cores are because it is <300 lines
"""


@dataclass
class ClassDeclaration(object):
    """
    comments_before is not exactly apart of class dec but it's easier
    to group it in with ClassDeclaration

    same goes for comments_after

    identifier refers to the name of the class
    
    class_body contains methods, fields, comments, etc.
    """

    identifier: Identifier
    class_body: ClassBody

    inherited_class: Optional[QualifiedIdentifier] = None   
    package_statement: Optional[PackageStatement] = None
    pre_class_declaration_list: Optional[PreClassDeclarationList] = None
    comments_after: Optional[Comment] = None


@dataclass
class VariableType(object):
    variable_type: Union[AnyStr, Identifier]


@dataclass
class PackageStatement(object):
    qualified_identifier: QualifiedIdentifier


@dataclass
class PreClassDeclarationList(object):
    statement: Union[PackageStatement, CommentList, None] = None
    additional_list: Optional[PreClassDeclarationList] = None


@dataclass
class CommentList(object):
    """
    In the BNF, additional_list is represented as comment_list
    """

    comment: Comment
    additional_list: Optional[CommentList] = None


@dataclass
class Comment(object):
    value: AnyStr
    is_statement: bool = False


@dataclass
class ImportStatement(object):
    qualified_identifier: QualifiedIdentifier


@dataclass
class Identifier(object):
    """
    Identifier has a string value.
    This class represents identifiers
    """
    
    value: AnyStr

    def __str__(self):
        return self.value


# No, this class is not redundant because eventually there will be
# fields added
@dataclass
class ClassBody(object):
    method_list: MethodList


@dataclass
class MethodList(object):
    method_or_comment: Union[Method, Comment, None] = None
    additional_list: Optional[MethodList] = None


@dataclass
class Method(object):
    identifier: Identifier
    parameter_list: ParameterList
    statement_list: StatementList

    comments_only: bool = True


@dataclass
class ParameterList(object):
    identifier: Optional[Identifier] = None
    additional_list: Optional[ParameterList] = None


@dataclass
class StatementList(object):
    statement: Optional[Statement] = None
    additional_list: Optional[StatementList] = None


@dataclass
class Statement(object):
    statement_body: Union[VariableInitialization, Expression, ReturnStatement]


@dataclass
class VariableDeclaration(object):
    variable_type: VariableType
    identifier: Identifier


@dataclass
class VariableInitialization(object):
    key_identifier: Identifier
    expression: Expression


@dataclass
class Expression(object):
    left_expression: Union[Factor, Expression, None] = None
    operator: Optional[Operator] = None
    right_expression: Union[Factor, Expression, None] = None
    is_statement: bool = False
    with_parenthesis: bool = False


class Operator(enum.Enum):
    PLUS = "+"
    MINUS = "-"
    MULTIPLY = "*"
    DIVIDE = "/"
    MODULUS = "%"


@dataclass
class Factor(object):
    """
    Factor's value can be a string or identifier
    """

    value: Union[AnyStr, Identifier]
    

@dataclass
class QualifiedIdentifier(object):
    identifier: Identifier
    qualified_identifier: Optional[QualifiedIdentifier] = None

    def __str__(self):
        if self.qualified_identifier is None:
            output = str(self.identifier)
        else:
            output = str(self.identifier) + "." + str(
                self.qualified_identifier)
        
        return output

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if isinstance(other, QualifiedIdentifier):
            if self.identifier.value == other.identifier:
                if self.qualified_identifier == other.qualified_identifier:
                    # This is actually recursive; None == None
                    # so no need to account for that

                    return True

        # If any of the checks don't hit, they don't match
        return False


@dataclass
class MethodCall(object):
    qualified_identifier: Union[QualifiedIdentifier, Identifier]
    argument_list: ArgumentList


@dataclass
class ArgumentList(object):
    argument: Optional[Factor] = None
    additional_list: Optional[ArgumentList] = None


@dataclass
class NewStatement(object):
    # Ex: new <qualified_identifier>(<argument_list>)
    # This refers to the class that the instance will be created from
    qualified_identifier: QualifiedIdentifier
    argument_list: ArgumentList


@dataclass
class ReturnStatement(object):
    expression: Union[Expression, Factor]


@dataclass
class VariableIncrement(object):
    identifier: Identifier
    amount: Union[Expression, AnyStr] = "1"


@dataclass
class IfStatement(object):
    comparison_expression: ComparisonExpression
    statement_list_or_empty: Optional[StatementList] = None
    else_statement_or_empty: Optional[StatementList] = None


@dataclass
class ComparisonExpression(object):
    left_expression: Union[ComparisonExpression, AnyStr]
    operator: Optional[ComparisonOperator] = None
    right_expression: Optional[ComparisonExpression] = None


class ComparisonOperator(enum.Enum):
    BOOL_EQ = "=="
    NOT_EQ = "!="
    GT_OR_EQ = ">="
    LT_OR_EQ = "<="
    GT = ">"
    LT = "<"


@dataclass
class WhileStatement(object):
    comparison_expression: ComparisonExpression
    statement_list_or_empty: Optional[StatementList] = None
