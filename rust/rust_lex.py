import sys
if ".." not in sys.path: sys.path.insert(0,"..")

import ply.lex as lex

# -- Tokens -- #
# Funciones en caso de acciones especiales para el token

# Tipos
def t_SIGNINTTYPE(t):
    r'i8|i16|i32|i64|i128|isize'
    return t

def t_UNSIGNINTTYPE(t):
    r'u8|u16|u32|u64|u128|usize'
    return t

def t_FLOATTYPE(t):
    r'f32|f64'
    return t

def t_BOOLTYPE(t):
    r'bool'
    return t

def t_CHARTYPE(t):
    r'char'
    #r':\s?char'
    return t

# IDs (variables)
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value,'ID') # Checar palabras reservadas
    return t

# Comentarios (ignorados)
def t_COMMENT(t):
    r'(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)|(//.*)'
    pass

# Expresiones regulares de cada token

# Operadores aritméticos
t_PLUS          = r'\+'
t_MINUS         = r'-'
t_MULT          = r'\*'
t_DIVIDE        = r'/'
t_REMINDER      = r'\%'
t_ASSIGN        = r'='
# Operadores de comparación
t_EQUALS        = r'=='
t_NE            = r'!='
t_LT            = r'<'
t_GT            = r'>'
t_LE            = r'<='
t_GE            = r'>='
# Operadores de bits
t_AND           = r'\&'
t_OR            = r'\|'
t_XOR           = r'\^'
# Símbolos
t_LPAREN        = r'\('
t_RPAREN        = r'\)'
t_LBRACKET      = r'\{'
t_RBRACKET      = r'\}'
t_DOT           = r'\.'
t_COMA          = r','
t_COLON         = r':'
t_SEMICOLON     = r';'
t_QUOTE         = r'\''
t_DOBLEQUOTE    = r'\"'
# Números
t_INTEGER       = r'\d+'
t_FLOAT         = r'((\d*\.\d+)(E[\+-]?\d+)?|([1-9]\d*E[\+-]?\d+))'
t_CHAR          = r'\'.?\''
t_STRING        = r'\".*?\"'
# Cualquier cosa que no sea salto de línea (\n)
#t_NONEOL        = r'.'

t_ignore        = " \t" # ignorar espacios

# Palabras reservadas
reserved = {
    'as'        : 'AS',         # casting primitivo | quitar ambiguedad de item | renombrar items
    'break'     : 'BREAK',      # salir de loop
    'const'     : 'CONST',      # definir constantes
    'continue'  : 'CONTINUE',   # continuar a siguiente iteración de loop
    'crate'     : 'CRATE',      # ligar crate o macro externa
    'dyn'       : 'DYN',        # dynamic dispatch (a objeto de rasgo)
    'else'      : 'ELSE',       # parte del flujo de control de if
    'enum'      : 'ENUM',       # definir enumaración
    'extern'    : 'EXTERN',     # ligar una crate, función o variable externa
    'false'     : 'FALSE',      # literal booleano falso
    'fn'        : 'FN',         # definir función o puntero tipo función
    'for'       : 'FOR',        # ciclar sobre items con un iterador
    'if'        : 'IF',         # expresión condicional
    'impl'      : 'IMPL',       # implementar funcionalidad inherente o de rasgo
    'in'        : 'IN',         # parte de la sintaxis de for
    'let'       : 'LET',        # definir una variable
    'loop'      : 'LOOP',       # ciclo sin condición (necesita salida explicita)
    'match'     : 'MATCH',      # igualar un valor a patrones
    'mod'       : 'MOD',        # definir un módulo
    'move'      : 'MOVE',       # hacer que una closure se haga cargo de todas sus capturas
    'mut'       : 'MUT',        # denotar mutabilidad
    'pub'       : 'PUB',        # denotar visibilidad pública
    'ref'       : 'REF',        # ligar por referencia
    'return'    : 'RETURN',     # regresar de función
    'self'      : 'SELF',       # método sujeto | módulo actual
    'static'    : 'STATIC',     # variable global
    'struct'    : 'STRUCT',     # definir estructura
    'super'     : 'SUPER',      # módulo padre del actual
    'trait'     : 'TRAIT',      # definir un rasgo
    'true'      : 'TRUE',       # literal booleano verdadero
    'type'      : 'TYPE',       # definir un alias de tipo
    'unsafe'    : 'UNSAFE',     # denotar código inseguro
    'use'       : 'USE',        # traer símbolos a alcance
    'where'     : 'WHERE',      # denota cláusulas que restringen un tipo
    'while'     : 'WHILE'       # ciclo condicional basado en el resultado de una expresión
}

tokens = [
            'SIGNINTTYPE',
            'UNSIGNINTTYPE',
            'FLOATTYPE',
            'BOOLTYPE',
            'CHARTYPE',
            'ID',
            'COMMENT',
            'PLUS',
            'MINUS',
            'MULT',
            'DIVIDE',
            'REMINDER',
            'ASSIGN',
            'EQUALS',
            'NE',
            'LT',
            'GT',
            'LE',
            'GE',
            'AND',
            'OR',
            'XOR',
            'LPAREN',
            'RPAREN',
            'LBRACKET',
            'RBRACKET',
            'DOT',
            'COMA',
            'COLON',
            'SEMICOLON',
            'QUOTE',
            'DOBLEQUOTE',
            'INTEGER',
            'FLOAT',
            'CHAR',
            'STRING',
            #'NONEOL',
        ] + list(reserved.values())

# Saber números de línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

# Manejo de errores
def t_error(t):
    print("Caracter ilegal '%s'" % t.value[0])
    t.lexer.skip(1)

# Construir el lexer
lex.lex()



# -- Probar sólo el lex -- #
#lexer = lex.lex()
#inFile = sys.argv[1]

#with open(inFile,'r') as file:
#    data = file.read()
#lex.input(data)

#while True:
#    tok = lexer.token()
#    if not tok:
#        break
#    print(tok)
