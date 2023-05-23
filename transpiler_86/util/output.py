class StatementOutput(object):
    IDENT_SPACES = "    "
    
    VARIABLE_TYPES = {
        # Ints
        "byte": "int",
        "Byte": "int",
        "short": "int",
        "Short": "int",
        "int": "int",
        "Integer": "int",
        "long": "int",
        "Long": "int",
        
        # Floats
        "float": "float",
        "Float": "float",
        "double": "float",
        "Double": "float",

        # Strings
        "char": "str",
        "Char": "str",
        "String": "str",

        # Bools
        "boolean": "bool",
        "Boolean": "bool"
    }

    SPACE = " "
    COMMA = ","
    PERIOD = "."

    CLASS_KW = "class"
    PASS_KW = "pass"
    DEF_KW = "def"
    RETURN_KW = "return"
    IMPORT_KW = "import"
    IF_KW = "if"
    ELSE_KW = "else"
    WHILE_KW = "while"

    COLON = ":"
    OPEN_PAREN, CLOSE_PAREN = "(", ")"
    EQUALS_SIGN = "="
    COMMENT_STARTER = "#"
    PLUS_SIGN = "+"

    PRINT_FUNC_PY = "print"

    PRINTLN_FUNC_JAVA = "System.out.println"
    PRINT_FUNC_JAVA = "System.out.print"

    MATH_IMPORT_JAVA = "java.lang.Math"
    MATH_IMPORT_PY = "math"

    JAVA_IDENTS = {
        PRINTLN_FUNC_JAVA: PRINT_FUNC_PY,
        PRINT_FUNC_JAVA: PRINT_FUNC_PY,
        MATH_IMPORT_JAVA: MATH_IMPORT_PY,
    }

    def __init__(self, transpiler):
        self.transpiler = transpiler
        self.output = ""

    def add_output(self, string, delimiter=""):
        self.output += string + delimiter

    def add_newline(self, inc_ident = False, dec_ident=False):
        # Identation increases/decreases
        if inc_ident:
            self.transpiler.ident_level += 1
        
        if dec_ident:
            self.transpiler.ident_level -= 1
        
        # Add the newline and the appropriate identation
        # print("ADDED NEW LINE:", inc_ident, dec_ident, self.transpiler.ident_level)
        self.output += "\n" + (
            self.IDENT_SPACES * self.transpiler.ident_level)

    def get_output(self):
        return self.output
