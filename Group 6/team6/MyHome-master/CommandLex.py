import ply.lex as lex

# -------------------------------
#
# S V O
#
# -------------------------------




# Reserved Token 
reserved = {
    'turn'    : 'TURN',
    'change'  : 'CHANGE',
    'channel' : 'CHANNEL',
    'volume'  : 'VOLUME',
    'speed'   : 'SPEED',
    'up'      : 'UP',
    'down'    : 'DOWN',
    'on'      : 'ON',
    'off'     : 'OFF',
}

tokens = list(reserved.values()) + [
    'WORD',
    'NUMBER'
]

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t
    
def t_WORD(t):
    r'[A-za-z][\w_]+'
    t.type = reserved.get(t.value, "WORD")
    return t


# A string containing ignored characters(spaces and tabs)
t_ignore = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character" + t.value[0])
    t.lexer.skip(1)

# Build the Lexer
lexer = lex.lex()