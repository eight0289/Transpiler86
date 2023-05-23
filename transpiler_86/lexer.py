"""
This module contains all the lexical and token rules for the java
to python transpiler
"""

from ply.lex import TOKEN


# Keywords!! (and some literals)
reserved = {
    "true": "TRUE",  # Literal
    "false": "FALSE",  # Literal
    "null": "NULL",  # Literal
    "public": "PUBLIC",  # Modifier
    "private": "PRIVATE",  # Modifier
    "void": "VOID",  # Modifier
    "static": "STATIC",  # Modifier
    "class": "CLASS",  # Keyword
    "byte": "BYTE",  # Primitive
    "short": "SHORT",  # Primitive
    "char": "CHAR",  # Primitive
    "int": "INT",  # Primitive
    "long": "LONG",  # Primitive
    "float": "FLOAT",  # Primitive
    "double": "DOUBLE",  # Primitive
    "boolean": "BOOLEAN",  # Primitive
    "return": "RETURN",  # Keyword
    "new": "NEW",  # Keyword
    "package": "PACKAGE",  # Keyword
    "import": "IMPORT",  # Keyword
    "extends": "EXTENDS",  # Keyword
    "if": "IF",  # Keyword
    "else": "ELSE",  # Keyword
    "while": "WHILE",  # Keyword
}

literals = [
    "(", ")", "{", "}", "[", "]", ";", ".", ",",  # Separators
    "=", "<", ">", "!", "~", "?", ":", "+", "-", "*", "/", "%"
]

tokens = [
    "ID",  # Identifier
    "DEC_LIT",  # DecimalLiteral
    "FLOAT_LIT",  # FloatingPointLiteral
    "CHAR_LIT",  # CharacterLiteral
    "STR_LIT",  # StringLiteral
    "AND",
    "OR",
    "INC",
    "DEC",
    "MUL_INC",
    "DIV_DEC",
    "SINGLE_LINE_COMMENT",
    "MULTI_LINE_COMMENT",
] + list(reserved.values())

# Expressions
ID = r"[a-zA-Z_$][\da-zA-Z_$]*"
# OCT_LIT = r"0_*([0-7]([_0-7]*[0-7])?)+"
# BIN_LIT = r"0[bB]([0-1]([[_0-1]*[0-1])?)+"  # I dont feel like messing w/ this rn
# HEX_LIT = r"0[xX]([\da-fA-F]([_\da-fA-F]*[\da-fA-F])?)+"
DEC_LIT = r"([1-9]([_\d]*\d+)?|0)[lL]?"
FLOAT_LIT = r"(\d[_\d]*\d|\d)\.(\d[_\d]*\d|\d)?([eE][+-]?(\d[_\d]*\d|\d))?[fFdD]?"
SINGLE_LINE_COMMENT = r"//.*"

# Because I know you suck a regex, the question mark in the regexpr
# makes the expression lazy
MULTI_LINE_COMMENT = r"/\*[\s\S]*?\*/"

# Ignore spaces, tabs, returns, newlines, formfeed
# I think that's everything
t_ignore = " \t\r\n\f"


# Matches a single \ then 1 or more u's and finally 4 hexadecimal digits
# t_UNI_ESC = r"\\u+[\da-fA-F]{4}"
t_CHAR_LIT = r"'([^'\\]|\\[btnfr\"\'\\])'"
t_STR_LIT = r"\"([^\"\\]|\\[btnfr\"\'\\])*\""
t_AND = r"&&"
t_OR = r"\|\|"
t_INC = r"\+="
t_DEC = r"-="
t_MUL_INC = r"\*="
t_DIV_DEC = r"/="

@TOKEN(ID)
def t_ID(t):
    # First character set matches upper case letters, lower case letters,
    # underscores, or dollar signs. The second character set matches the
    # same as the first but also matches every digit

    t.type = reserved.get(t.value, "ID")
    return t

# The order of functions matter
@TOKEN(FLOAT_LIT)
def t_FLOAT_LIT(t):
    return t


@TOKEN(DEC_LIT)
def t_DEC_LIT(t):
    # Matches a singular 0 or a series of decimal digits with optional
    # underscores in between them
    return t


@TOKEN(SINGLE_LINE_COMMENT)
def t_SINGLE_LINE_COMMENT(t):
    # Removes the "//"
    t.value = t.value[2:]

    return t


@TOKEN(MULTI_LINE_COMMENT)
def t_MULTI_LINE_COMMENT(t):
    # Remove first 2 chars and last 2 chars
    t.value = t.value[2:]
    t.value = t.value[:-2]

    # Add the comment starters
    t.value = t.value.strip()
    t.value = t.value.replace("\n", "\n#")

    return t


# Temporary error handler. This will need to be elaborated upon
def t_error(t):
    print(f"Unknown Character {t.value}")
    t.lexer.skip(1)
