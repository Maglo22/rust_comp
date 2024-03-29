import sys
if ".." not in sys.path: sys.path.insert(0,"..")

import ply.yacc as yacc
import rust_lex

tokens = rust_lex.tokens

precedence = (
    ('nonassoc', 'RETURN', 'BREAK'),
    ('right', 'ASSIGN'),
    ('left', 'EQUALS', 'NE', 'LT', 'GT', 'LE', 'GE'),
    ('left', 'OR'),
    ('left', 'XOR'),
    ('left', 'AND'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULT', 'DIVIDE', 'REMINDER'),
    ('left', 'DOT'),
)

# Clase genérica para un nodo del AST
class Node:
    def __init__(self, type, children=None, leaf=None):
        self.type = type
        if children:
            self.children = children
        else:
            self.children = [ ]
        self.leaf = leaf

    def __str__(self, level=0):
        ret = "\t" * level + repr(self.type)
        if self.leaf:
            ret += " => " + self.leaf + "\n"
        else:
            ret += "\n"
        
        for child in self.children:
            ret += child.__str__(level+1)
        return ret

# Clase para agregar nuevos alcances e IDs dentro de estos
class Table(dict):
    def __init__(self):
        self = dict()
    
    def add(self, key, value):
        self[key] = value

# Bloques de alcances (diccionarios)
scopes = Table()
scope_number = 0

# Primer alcance
s = Table()
scopes.add(scope_number, s)

# Checar si la llave ya se encuentra en alguna de las tablas de símbolos
def scope_check(key):
    for scope in range(0, scope_number + 1):
        #print('Comprobando ' + str(key) + ' en alcance ' + str(scope))
        if key in scopes[scope]:
            return True # ya está registrada en una tabla de símbolos
    
    return False # no se encuentra en ninguna tabla de símbolos

# -- Sintaxis en BNF -- #

def p_program(p):
    '''program : list_stmt '''
    p[0] = Node('program', [ p[1] ], None)

def p_list_stmt(p):
    '''list_stmt : stmt list_stmt
                 | stmt '''
    if len(p) == 3:
        p[0] = Node('list_stmt', [ p[1], p[2] ], None)
    else:
        p[0] = Node('list_stmt', [ p[1] ], None)

# Statements
def p_statement(p):
    '''stmt : decl_stmt
            | expr_stmt
            | SEMICOLON '''
    if p[1] == ';':
        p[0] = Node('stmt', None, ';')
    else:
        p[0] = Node('stmt', [ p[1] ], None)

# Declaraciones
def p_decl_stmt(p):
    '''decl_stmt : item
                 | let_decl'''
    p[0] = Node('decl_stmt', [ p[1] ], None)

# Expresiones
def p_expr_stmt(p):
    '''expr_stmt : expr SEMICOLON '''
    p[0] = Node('expr_stmt', [ p[1] ], ';')

# Items
def p_item(p):
    '''item : fn_item
            | const_item
            | static_item'''
    p[0] = Node('item', [ p[1] ], None)

# Funciones
def p_fn_item(p):
    '''fn_item : FN ID add_to_scope paren_expr_list block_expr '''
    p[0] = Node('fn_item', [ p[4], p[5] ], p[2])

# Acción para agregar función dentro de la tabla de símbolos
def p_add_to_scope(p):
    'add_to_scope :'
    if not scope_check(p[-1]):
        current_scope = scopes.get(scope_number)
        current_scope.add(p[-1], 'fn')

# Constantes
def p_const_item(p):
    '''const_item : CONST ID COLON type ASSIGN expr SEMICOLON '''
    p[0] = Node('const_item', [ p[4], p[6] ], p[2])
    if not scope_check(p[2]):
        current_scope = scopes.get(scope_number)
        current_scope.add(p[2], p[4].leaf)

# Estáticos
def p_static_item(p):
    '''static_item : STATIC ID COLON type ASSIGN expr SEMICOLON '''
    p[0] = Node('static_item', [ p[4], p[6] ], p[2])
    if not scope_check(p[2]):
        current_scope = scopes.get(scope_number)
        current_scope.add(p[2], p[4].leaf)

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
    if p[2] == 'mut':
        if len(p) == 8:
            p[0] = Node('let_decl', [ p[5], p[6] ], p[3])
            if not scope_check(p[3]):
                current_scope = scopes.get(scope_number)
                current_scope.add(p[3], p[5].leaf)
        elif len(p) == 7:
            p[0] = Node('let_decl', [ p[5] ], p[3])
            if not scope_check(p[3]):
                current_scope = scopes.get(scope_number)
                current_scope.add(p[3], p[5].leaf)
        elif len(p) == 6:
            p[0] = Node('let_decl', [ p[4] ], p[3])
            if not scope_check(p[3]):
                current_scope = scopes.get(scope_number)
                current_scope.add(p[3], 'var')
        else:
            p[0] = Node('let_decl', None, p[3])
            if not scope_check(p[3]):
                current_scope = scopes.get(scope_number)
                current_scope.add(p[3], 'var')
    else:
        if len(p) == 7:
            p[0] = Node('let_decl', [ p[4], p[5] ], p[2])
            if not scope_check(p[2]):
                current_scope = scopes.get(scope_number)
                current_scope.add(p[2], p[4].leaf)
        elif len(p) == 6:
            p[0] = Node('let_decl', [ p[4] ], p[2])
            if not scope_check(p[2]):
                current_scope = scopes.get(scope_number)
                current_scope.add(p[2], p[4].leaf)
        elif len(p) == 5:
            p[0] = Node('let_decl', [ p[3] ], p[2])
            if not scope_check(p[2]):
                current_scope = scopes.get(scope_number)
                current_scope.add(p[2], 'var')
        else:
            p[0] = Node('let_decl', None, p[2])
            if not scope_check(p[2]):
                current_scope = scopes.get(scope_number)
                current_scope.add(p[2], 'var')

# Inicializar variable
def p_init(p):
    '''init : ASSIGN expr
            | expr'''
    if len(p) == 3:
        p[0] = Node('init', [ p[2] ], '=')
    else:
        p[0] = Node('init', [ p[1] ], None)

# Tipos de expresiones
def p_expr(p):
    '''expr : literal
            | block_expr
            | method_call_expr
            | binop_expr
            | paren_expr
            | call_expr
            | while_expr
            | loop_expr
            | break_expr
            | continue_expr
            | if_expr
            | return_expr '''
    p[0] = Node('expr', [ p[1] ], None)

# Expresiones de bloque
def p_block_expr(p):
    '''block_expr : LBRACKET new_scope block_expr_a RBRACKET
                  | LBRACKET new_scope block_expr_b RBRACKET
                  | LBRACKET new_scope block_expr_c RBRACKET
                  | LBRACKET new_scope block_expr_d RBRACKET
                  | LBRACKET new_scope block_expr_e RBRACKET '''
    p[0] = Node('block', [ p[3] ], None)

# Acción para generar un nuevo bloque de alcance
def p_new_scope(p):
    'new_scope :'
    # Create a new scope for local variables
    s = Table()
    global scope_number
    scope_number += 1
    scopes.add(scope_number, s)

# Expresiones de apoyo para block_expr
def p_block_expr_a(p):
    '''block_expr_a : stmt block_expr_a
                    | empty '''
    if len(p) == 3:
        p[0] = Node('block_a', [ p[1], p[2] ], None)
    else:
        p[0] = Node('block_a', [ p[1] ], None)

def p_block_expr_b(p):
    '''block_expr_b : stmt block_expr_e
                    | item block_expr_e '''
    p[0] = Node('block_b', [ p[1], p[2] ], None)

def p_block_expr_c(p):
    '''block_expr_c : stmt block_expr_b '''
    p[0] = Node('block_c', [ p[1], p[2] ], None)

def p_block_expr_d(p):
    '''block_expr_d : item block_expr_b '''
    p[0] = Node('block_d', [ p[1], p[2] ], None)

def p_block_expr_e(p):
    '''block_expr_e : expr '''
    p[0] = Node('block_e', [ p[1] ], None)

# Llamada a un método
def p_method_call_expr(p):
    '''method_call_expr : expr DOT ID paren_expr_list '''
    p[0] = Node('method_call', [ p[1], p[4] ], p[3])

# Llamada a una función
def p_call_expr(p):
    '''call_expr : expr paren_expr_list '''
    p[0] = Node('call_expr', [ p[1], p[2] ], None)

# Parámetros en una función
def p_paren_expr_list(p):
    '''paren_expr_list : LPAREN expr_list RPAREN '''
    p[0] = Node('paren_expr_list', [ p[2] ], None)

# Lista de parámetros en una función
def p_expr_list(p):
    '''expr_list : expr
                 | expr e_list
                 | empty '''
    if len(p) == 3:
        p[0] = Node('expr_list', [ p[1], p[2] ], None)
    else:
        p[0] = Node('expr_list', [ p[1] ], None)

# Expresión de apoyo para lista de parámetros
def p_e_list(p):
    '''e_list : COMA expr_list '''
    p[0] = Node('e_list', [ p[2] ], p[1])

# Operadores binarios
def p_binop_expr(p):
    '''binop_expr : expr binop expr
                  | type_cast_expr
                  | assignment_expr
                  | compound_assignment_expr '''
    if len(p) == 4:
        p[0] = Node('binop_expr', [ p[1], p[2], p[3] ], None)
    else:
        p[0] = Node('binop_expr', [ p[1] ], None)

# Expresiones agrupadas
def p_paren_expr(p):
    '''paren_expr : LPAREN expr RPAREN '''
    p[0] = Node('paren_expr', [ p[2] ], None)

# While
def p_while_expr(p):
    '''while_expr : WHILE cond_expr block_expr '''
    p[0] = Node('while', [ p[2], p[3] ], None)

# Loop
def p_loop_expr(p):
    '''loop_expr : LOOP block_expr '''
    p[0] = Node('loop', [ p[2] ], None)

# Break
def p_break_expr(p):
    'break_expr : BREAK'
    p[0] = Node('break', None, 'break')

# Continue
def p_continue_expr(p):
    'continue_expr : CONTINUE'
    p[0] = Node('continue', None, 'continue')

# If
def p_if_expr(p):
    '''if_expr : IF cond_expr block_expr
               | IF cond_expr block_expr else_tail '''
    if len(p) == 5:
        p[0] = Node('if', [ p[2], p[3], p[4] ], None)
    else:
       p[0] = Node('if', [ p[2], p[3] ], None)

# Else
def p_else_tail(p):
    '''else_tail : ELSE if_expr 
                 | ELSE block_expr '''
    p[0] = Node('else', [ p[2] ], None)

# Return
def p_return_expr(p):
    '''return_expr : RETURN
                   | RETURN expr'''
    if len(p) == 3:
        p[0] = Node('return', [ p[2] ], None)
    else:
        p[0] = Node('return', None, 'return')

# Expresiones para Condicionales y Ciclos
def p_cond_expr(p):
    '''cond_expr : literal
                 | literal cond_op '''
    if len(p) == 3:
        p[0] = Node('cond_expr', [ p[1], p[2] ], None)
    else:
        p[0] = Node('cond_expr', [ p[1] ], None)

# Expresión de ayuda para condiciones
def p_cond_op(p):
    '''cond_op : binop cond_expr '''
    p[0] = Node('cond_op', [ p[1], p[2] ], None)

# Literales
def p_literal(p):
    '''literal : string_lit
               | char_lit
               | num_lit
               | bool_lit
               | id_lit '''
    p[0] = Node('literal', [ p[1] ], None)

# String
def p_string_lit(p):
    'string_lit : STRING'
    p[0] = Node('string_lit', None, p[1])

# Caracteres (char)
def p_char_lit(p):
    'char_lit : CHAR'
    p[0] = Node('char_lit', None, p[1])

# Números
def p_num_lit(p):
    '''num_lit : INTEGER
               | FLOAT '''
    p[0] = Node('num_lit', None, p[1])

# Booleanos
def p_bool_lit(p):
    '''bool_lit : TRUE
                | FALSE '''
    p[0] = Node('bool_lit', None, p[1])

# IDs
def p_id_lit(p):
    'id_lit : ID'
    p[0] = Node('id_lit', None, p[1])

# Operadores
def p_binop(p):
    '''binop : arith_op
             | bitwise_op
             | comp_op '''
    p[0] = Node('binop', [ p[1] ], None)

# Aritméticos
def p_arith_op(p):
    '''arith_op : PLUS
                | MINUS
                | MULT
                | DIVIDE
                | REMINDER '''
    p[0] = Node('arith_op', None, p[1])

# Bits
def p_bitwise_op(p):
    '''bitwise_op : AND
                  | OR
                  | XOR '''
    p[0] = Node('bitwise_op', None, p[1])

# Comparación
def p_comp_op(p):
    '''comp_op : EQUALS
               | NE
               | LT
               | GT
               | LE
               | GE '''
    p[0] = Node('comp_op', None, p[1])

# Casting
def p_type_cast_expr(p):
    '''type_cast_expr : ID AS type '''
    p[0] = Node('type_cast', [ p[3] ], p[1])

# Asignación
def p_assignment_expr(p):
    'assignment_expr : expr ASSIGN expr'
    p[0] = Node('assignment', [ p[1], p[3] ], '=')

# Asignación compuesta
def p_compound_assignment_expr(p):
    '''compound_assignment_expr : expr arith_op ASSIGN expr
                                | expr bitwise_op ASSIGN expr '''
    p[0] = Node('compound_assignment', [ p[1], p[2], p[4] ], '=')

# Tipos
def p_type(p):
    '''type : SIGNINTTYPE
            | UNSIGNINTTYPE
            | FLOATTYPE
            | BOOLTYPE
            | CHARTYPE '''
    p[0] = Node('type', None, p[1])

# Expresión vacía
def p_empty(p):
    'empty :'
    p[0] = Node('empty', None, None)

# -- Termina Sintaxis en BNF -- #

# Manejar errores (modo pánico)
def p_error(p):
    print("Error de sintaxis en '%s' (línea %s)" % (p.value, p.lexer.lineno))
    if not p:
        print("EOF")
        return
    
    while True:
        tok = parser.token() # siguiente token
        if not tok or tok.type == 'SEMICOLON':
            break
    parser.restart()

# Construir analizador
parser = yacc.yacc()

# Función para realizar análisis
def parse(data, debug=0, scope=False):
    parser.error = 0
    p = parser.parse(data, debug=debug)
    if parser.error:
        return None
    
    if scope:
        print(scopes)
    return p
