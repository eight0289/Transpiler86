from ply import lex, yacc


def tokenizer(lexer):
    built_lexer = lex.lex(module=lexer)

    while True:
        data = input(">>> ")
        built_lexer.input(data)
        
        while True:
            token = built_lexer.token()

            if token is None:
                break

            print(token)


def test_parse(lexer, yacc_parser):
    # Build the ply components
    built_lexer = lex.lex(module=lexer)
    built_parser = yacc.yacc(module=yacc)

    while True:
        try:
            s = input(">>> ")
        except EOFError:
            break

        if s is None:
            continue

        result = built_parser.parse(s, lexer=built_lexer)
        print(result)


def sample(sample_file, lexer, yacc_parser):
    with open(sample_file[1], "r") as f:
        data = f.read()

        built_lexer = lex.lex(module=lexer)
        built_parser = yacc.yacc(module=yacc_parser)
        
        result = built_parser.parse(data, lexer=built_lexer)
        
        # When presenting, do not print
        print(result)

        with open("samples/sample.py", "w") as out_f:
            out_f.write(result)


def simple(text, lexer, yacc_parser):
    built_lexer = lex.lex(module=lexer)
    built_parser = yacc.yacc(module=yacc_parser)
    
    result = built_parser.parse(text, lexer=built_lexer)

    print(result)
