import ply.lex as lex
import ply.yacc as yacc

# 1. LISTA DE TOKENS
# Es obligatorio declarar una tupla con los nombres de los tokens.
tokens = (
    "NUMERO",
    "SUMA",
    "RESTA",
    "MULT",
    "DIV",
    "LPAREN",  # Paréntesis izquierdo (
    "RPAREN",  # Paréntesis derecho )
)

# 2. REGLAS DE EXPRESIONES REGULARES (REGEX)
# El nombre de la variable debe ser 't_' seguido del nombre del token.

t_SUMA = r"\+"
t_RESTA = r"-"
t_MULT = r"\*"
t_DIV = r"/"
t_LPAREN = r"\("
t_RPAREN = r"\)"

# Ignorar caracteres como espacios y tabulaciones
t_ignore = " \t"


# 3. REGLAS COMPLEJAS (FUNCIONES)
# Usamos funciones cuando necesitamos procesar el dato (ej. convertir texto a int)
def t_NUMERO(t):
    r"\d+"
    t.value = int(t.value)  # Convertimos el lexema "10" al entero 10
    return t


# Manejo de saltos de línea (para llevar la cuenta de líneas)
def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


# Manejo de errores (caracteres ilegales)
def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}'")
    t.lexer.skip(1)


# 4. CONSTRUIR EL LEXER
lexer = lex.lex()


# 1. PRECEDENCIA (Jerarquía de operaciones)
# Esto le dice a Yacc: "Calcula multiplicación antes que suma"
# Se define de menor a mayor prioridad.
precedence = (
    ("left", "SUMA", "RESTA"),
    ("left", "MULT", "DIV"),
)

# 2. REGLAS GRAMATICALES
# La sintaxis es: p[0] = p[1] OPERADOR p[3]
# p es una lista: p[0] es el resultado, p[1] el primer elemento, etc.


def p_expresion_operacion(p):
    """expression : expression SUMA expression
    | expression RESTA expression
    | expression MULT expression
    | expression DIV expression"""
    # p[0]   p[1]      p[2]    p[3]
    # RES  = NUM (5) + SUMA +  NUM (2)

    if p[2] == "+":
        p[0] = p[1] + p[3]
    elif p[2] == "-":
        p[0] = p[1] - p[3]
    elif p[2] == "*":
        p[0] = p[1] * p[3]
    elif p[2] == "/":
        p[0] = p[1] / p[3]


def p_expresion_grupo(p):
    """expression : LPAREN expression RPAREN"""
    p[0] = p[2]  # El valor es lo que está DENTRO de los paréntesis


def p_expresion_numero(p):
    """expression : NUMERO"""
    p[0] = p[1]  # Si es solo un número, el valor es el número mismo


# Manejo de errores de sintaxis
def p_error(p):
    print("Error de sintaxis en la entrada!")


# 3. CONSTRUIR EL PARSER
parser = yacc.yacc()

while True:
    try:
        s = input("calc > ")
    except EOFError:
        break
    if not s:
        continue

    # Aquí ocurre la magia:
    resultado = parser.parse(s)
    print(resultado)
