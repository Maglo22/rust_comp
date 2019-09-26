# python rust_yacc.py [archivo_entrada]
# -> python rust_yacc.py ../tests/data_types.rs

# Imprime en consola un AST

import sys
if ".." not in sys.path: sys.path.insert(0,"..")

import ply.yacc as yacc
import rust_lex

tokens = rust_lex.tokens

inFile = sys.argv[1] # archivo de entrada

# -- Sintaxis en BNF -- #

# Statements
def p_statement(p):
    '''stmt : decl_stmt
            | expr_stmt
            | SEMICOLON '''
    if p[1] == ';':
        p[0] = ('STMT', 'SEMICOLON')
    else:
        p[0] = ('STMT', p[1])

# Declaraciones
def p_decl_stmt(p):
    '''decl_stmt : item
                 | let_decl'''
    p[0] = ('DECL_STMT', p[1])

# Expresiones
def p_expr_stmt(p):
    '''expr_stmt : expr SEMICOLON '''
    p[0] = ('EXPR_STMT', p[1], 'SEMICOLON')

# Items
def p_item(p):
    '''item : fn_item
            | const_item
            | static_item'''
    p[0] = ('ITEM', p[1])

# Funciones
def p_fn_item(p):
    '''fn_item : FN ID LPAREN RPAREN block_expr '''
    p[0] = ('FN_ITEM', 'FN', 'ID', 'LPAREN', 'RPAREN', p[5])

# Constantes
def p_const_item(p):
    '''const_item : CONST ID COLON type ASSIGN expr SEMICOLON '''
    p[0] = ('CONST_ITEM', 'CONST', 'ID', 'COLON', p[4], 'ASSIGN', p[6], 'SEMICOLON')

# Estáticos
def p_static_item(p):
    '''static_item : STATIC ID COLON type ASSIGN expr SEMICOLON '''
    p[0] = ('STATIC_ITEM', 'STATIC', 'ID', 'COLON', p[4], 'ASSIGN', p[6], 'SEMICOLON')

# Variables
def p_let_decl(p):
    '''let_decl : LET MUT ID COLON type init SEMICOLON
                | LET MUT ID COLON type SEMICOLON
                | LET MUT ID init SEMICOLON
                | LET MUT ID SEMICOLON
                | LET ID COLON type init SEMICOLON
                | LET ID COLON type SEMICOLON
                | LET ID init SEMICOLON
                | LET ID SEMICOLON '''
    if p[2] == 'MUT':
        if len(p) == 8:
            p[0] = ('LET_DECL', 'LET', 'MUT', 'ID', 'COLON', p[5], p[6], 'SEMICOLON')
        elif len(p) == 7:
            p[0] = ('LET_DECL', 'LET', 'MUT', 'ID', 'COLON', p[5], 'SEMICOLON')
        elif len(p) == 6:
            p[0] = ('LET_DECL', 'LET', 'MUT', 'ID', p[4], 'SEMICOLON')
        else:
            p[0] = ('LET_DECL', 'LET', 'MUT', 'ID', 'SEMICOLON')
    else:
        if len(p) == 7:
            p[0] = ('LET_DECL', 'LET', 'ID', 'COLON', p[4], p[5], 'SEMICOLON')
        elif len(p) == 6:
            p[0] = ('LET_DECL', 'LET', 'ID', 'COLON', p[4], 'SEMICOLON')
        elif len(p) == 5:
            p[0] = ('LET_DECL', 'LET', 'ID', p[3], 'SEMICOLON')
        else:
            p[0] = ('LET_DECL', 'LET', 'ID', 'SEMICOLON')

# Inicializar variable
def p_init(p):
    '''init : ASSIGN expr
            | expr'''
    if len(p) == 3:
        p[0] = ('INIT', 'ASSIGN', p[2])
    else:
        p[0] = ('INIT', p[1])

# Tipos de expresiones
def p_expr(p):
    '''expr : literal
            | block_expr
            | binop_expr
            | paren_expr
            | while_expr
            | loop_expr
            | break_expr
            | continue_expr
            | if_expr
            | return_expr '''
    p[0] = ('EXPR', p[1])

# Expresiones de bloque
def p_block_expr(p):
    '''block_expr : LBRACKET stmt expr RBRACKET
                  | LBRACKET item expr RBRACKET
                  | LBRACKET expr RBRACKET '''
    if len(p) == 5:
        p[0] = ('BLOCK_EXPR', 'LBRACKET', p[2], p[3], 'RBRACKET')
    else:
        p[0] = ('BLOCK_EXPR', 'LBRACKET', p[2], 'RBRACKET')

# Operadores binarios
def p_binop_expr(p):
    '''binop_expr : expr binop expr
                  | type_cast_expr
                  | assignment_expr
                  | compound_assignment_expr '''
    if len(p) == 4:
        p[0] = ('BINOP_EXPR', p[1], p[2], p[3])
    else:
        p[0] = ('BINOP_EXPR', p[1])

# Expresiones agrupadas
def p_paren_expr(p):
    '''paren_expr : LPAREN expr RPAREN '''
    p[0] = ('PAREN_EXPR', 'LPAREN', p[2], 'RPAREN')

# While
def p_while_expr(p):
    '''while_expr : WHILE no_struct_literal_expr block_expr '''
    p[0] = ('WHILE_EXPR', 'WHILE', p[2], p[3])

# Loop
def p_loop_expr(p):
    '''loop_expr : LOOP block_expr '''
    p[0] = ('LOOP', p[2])

# Break
def p_break_expr(p):
    'break_expr : BREAK'
    p[0] = ('BREAK')

# Continue
def p_continue_expr(p):
    'continue_expr : CONTINUE'
    p[0] = ('CONTINUE')

# If
def p_if_expr(p):
    '''if_expr : IF no_struct_literal_expr block_expr
               | IF no_struct_literal_expr block_expr else_tail '''
    if len(p) == 5:
        p[0] = ('IF_EXPR', 'IF', p[2], p[3], p[4])
    else:
       p[0] = ('IF_EXPR', 'IF', p[2], p[3])

# Else
def p_else_tail(p):
    '''else_tail : ELSE if_expr 
                 | ELSE block_expr '''
    p[0] = ('ELSE_TAIL', p[2])

# Return
def p_return_expr(p):
    '''return_expr : RETURN
                   | RETURN expr'''
    if len(p) == 2:
        p[0] = ('RETURN')
    else:
        p[0] = ('RETURN', p[2])

def p_no_struct_literal_expr(p):
    '''no_struct_literal_expr : literal
                              | literal binop literal 
                              | literal binop literal binop literal'''
    if len(p) == 6:
        p[0] = ('NO_STRUCT_LITERAL_EXPR', p[1], p[2], p[3], p[4], p[5])
    elif len(p) == 4:
        p[0] = ('NO_STRUCT_LITERAL_EXPR', p[1], p[2], p[3])
    else:
        p[0] = ('NO_STRUCT_LITERAL_EXPR', p[1])

# Literales
def p_lit_suffix(p):
    'lit_suffix : ID'
    p[0] = ('LIT_SUFFIX', 'ID')

def p_literal(p):
    '''literal : num_lit
               | bool_lit
               | lit_suffix '''
    p[0] = ('LITERAL', p[1])

# Números
def p_num_lit(p):
    '''num_lit : INTEGER
               | FLOAT '''
    p[0] = ('NUM_LIT', p[1])

# Booleanos
def p_bool_lit(p):
    '''bool_lit : TRUE
                | FALSE '''
    p[0] = ('BOOL_LIT', p[1])

# Operadores
def p_binop(p):
    '''binop : arith_op
             | bitwise_op
             | comp_op '''
    p[0] = ('BINOP', p[1])

# Aritméticos
def p_arith_op(p):
    '''arith_op : PLUS
                | MINUS
                | MULT
                | DIVIDE
                | REMINDER '''
    p[0] = ('ARITH_OP', p[1])

# Bits
def p_bitwise_op(p):
    '''bitwise_op : AND
                  | OR
                  | XOR '''
    p[0] = ('BITWISE_OP', p[1])

# Comparación
def p_comp_op(p):
    '''comp_op : EQUALS
               | NE
               | LT
               | GT
               | LE
               | GE '''
    p[0] = ('COMP_OP', p[1])

# Casting
def p_type_cast_expr(p):
    '''type_cast_expr : ID AS type '''
    p[0] = ('TYPE_CAST_EXPR', 'ID', 'AS', p[3])

# Asignación
def p_assignment_expr(p):
    'assignment_expr : expr ASSIGN expr'
    p[0] = ('ASSIGNMENT_EXPR', p[1], 'ASSIGN', p[3])

# Asignación compuesta
def p_compound_assignment_expr(p):
    '''compound_assignment_expr : expr arith_op ASSIGN expr
                               | expr bitwise_op ASSIGN expr '''
    p[0] = ('COMPOUND_ASSIGNMENT_EXPR', p[1], p[2], 'ASSIGN', p[4])

# Tipos
def p_type(p):
    '''type : SIGNINTTYPE
            | UNSIGNINTTYPE
            | FLOATTYPE
            | BOOLTYPE
            | CHARTYPE '''
    p[0] = ('TYPE', p[1])



# Manejar errores (modo pánico)
def p_error(p):
    print("Error de sintaxis en '%s' " % p.value)
    if not p:
        print("EOF")
        return
    
    while True:
        tok = parser.token() # siguiente token
        if not tok or tok.type == 'RBRACKET':
            break
        parser.restart()

# Construir analizador
parser = yacc.yacc()

# Leer archivo de entrada
with open(inFile,'r') as file:
    data = file.read()

result = parser.parse(data)
print(result) # Imprimir resultado en consola