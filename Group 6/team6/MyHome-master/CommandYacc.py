import ply.yacc as yacc

from CommandLex import tokens

start = 'command'

def p_command(p):
    '''
    command : svo_cmd
               | sv_cmd
    '''
    p[0] = p[1]

def p_sv_cmd(p):
    
    '''
    sv_cmd : WORD action1
    '''
    # find the S in database, if in the database then  
    command = {
        'device_name' : p[1],
        'action' : p[2],
        'number' : '',
    }
    p[0] = command

def p_svo_cmd(p):
    '''
    svo_cmd : WORD action2 NUMBER
    '''
    command = {
        'device_name' : p[1],
        'action' : p[2],
        'number' : p[3]
    }
    p[0] = command

def p_action1(p):
    '''
    action1 : TURN ON
           | TURN OFF
           | VOLUME UP
           | VOLUME DOWN
           | SPEED UP
           | SPEED DOWN
    '''
    p[0] = p[1] + " " + p[2]

def p_action2(p):
    '''
    action2 : CHANGE CHANNEL
    '''
    p[0] = p[1] + " " + p[2]

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in ", p.value)


CommandParser = yacc.yacc()

if __name__ == '__main__':
    
    while True:
        try:
            s = raw_input('cmd> ')
        except EOFError:
            break

        if not s:
            continue
        s = s.lower()
        result = CommandParser.parse(s)
        print 'Result:=>', result
    
    # print 'type', type(tokens)
    # print 'token', tokens