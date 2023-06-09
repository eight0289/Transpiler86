"""
This file covers stuff that is used everywhere and doesn't have 
a place to go
"""

from transpiler_86.util import components as comp
from transpiler_86.util.output import StatementOutput


def transpiler_comment_list(transpiler, current: comp.CommentList):
    out = StatementOutput(transpiler)

    out.add_output(transpiler.traverse(current.comment))

    # Separator
    out.add_newline()

    # Check for additional comments
    if current.additional_list is not None:
        out.add_output(transpiler.traverse(current.additional_list))

    return out.get_output()


def transpiler_comment(transpiler, current: comp.Comment):
    out = StatementOutput(transpiler)

    out.add_output(out.COMMENT_STARTER)
    out.add_output(current.value)

    # Only add newlines for statemetn
    if current.is_statement:
        out.add_newline()

    return out.get_output()


def transpiler_variable_type(transpiler, current: comp.VariableType):
    # If the variable type is an instance of an identifier,
    # traverse, but otherwise just return it as is
    if isinstance(current.variable_type, comp.Identifier):

        # There may be a bug in the future, so you could move
        # this if-statement into the Idenfiier section if it is
        # necessary
        if current.variable_type.value in StatementOutput.VARIABLE_TYPES.keys():
            return StatementOutput.VARIABLE_TYPES[current.variable_type.value]

        return transpiler.traverse(current.variable_type)

    # Return the proper type hint
    if current.variable_type in StatementOutput.VARIABLE_TYPES.keys():
        return StatementOutput.VARIABLE_TYPES[current.variable_type]
    
    return current.variable_type


def transpiler_identifier(transpiler, current: comp.Identifier):
    # Identifier.value is just a string.
    # There is an issue here though because of the differences in
    # naming conventions; Java allows the use of "$" in
    # indentifiers while Python does not allow its use.
    return current.value


def transpiler_qualified_identifier(transpiler, current: comp.QualifiedIdentifier):
    out = StatementOutput(transpiler)
    
    current_as_str = str(current)
    if current_as_str in out.JAVA_IDENTS:
        # If an identifier has a direct translation in Python,
        # Add that instead of the other
        out.add_output(out.JAVA_IDENTS[current_as_str])
    else:

        # Traverse the current identifier
        out.add_output(transpiler.traverse(current.identifier))

        # Add the additional qualified_identifier is there is one
        if current.qualified_identifier is not None:
            
            # Remember that QualifiedIdentifier could just be a single
            # identifier so periods will be added when there are
            # multiple identifiers
            out.add_output(out.PERIOD)
            out.add_output(transpiler.traverse(current.qualified_identifier))

    return out.get_output()
