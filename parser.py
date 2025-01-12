import vendor.lex as lex
import vendor.yacc as yacc

debug = False
#debug = True

#-------------------------------------------------- 
#-- Ply Lexer setup ------------------------------- 
#-------------------------------------------------- 
# List of all of our tokens
tokens = (
    'STATE_MACHINE_NAME',
    'STARTING_STATE',
    'STATE_DEFINITION_NAME',
    'STATE_DEFINITION_BEGIN',
    'STATE_TRANSITION_INPUT',
    'STATE_TRANSITION_ARROW',
    'STATE_TRANSITION_TARGET',
    'STATE_DEFINITION_END',
    'DOC_COMMENT',
    'COMMENT'
)

# List of all of our states for token processing
states = (
   ('states','exclusive'),
   ('input','exclusive'),
   ('target','exclusive'),
)

#-------------------------------------------------- 
#-- Define regexs for all of our token types ------ 
#-------------------------------------------------- 
# We will ignore tabs 
t_ANY_ignore = ' \t'

# Token STATE_MACHINE_NAME in the INITIAL state
def t_INITIAL_STATE_MACHINE_NAME(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    return t

# Token STATE_MACHINE_NAME in the INITIAL state
def t_INITIAL_STARTING_STATE(t):
    r'\([A-Za-z_][A-Za-z0-9_]*\)'
    # Remove the parentheses
    t.value = t.value[1:-1]
    # We got our header so start processing states
    t.lexer.begin('states')
    return t

def t_states_STATE_DEFINITION_NAME(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    return t

def t_states_STATE_DEFINITION_BEGIN(t):
    r'\{'
    t.lexer.begin('input')
    return t

def t_input_STATE_DEFINITION_END(t):
    r'\},*'
    t.lexer.begin('states')
    return t

def t_input_STATE_TRANSITION_INPUT(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    return t

def t_input_STATE_TRANSITION_ARROW(t):
    r'=>'
    t.lexer.begin('target')
    return t

def t_target_STATE_TRANSITION_TARGET(t):
    r'[A-Za-z_][A-Za-z0-9_]*,*'
    # If theres a comma at the end remove it
    if (t.value[-1] == ','):
        t.value = t.value[:-1]
    t.lexer.begin('input')
    return t

def t_ANY_DOC_COMMENT(t):
    r'//!.*'
    return t

def t_ANY_COMMENT(t):
    r'//.*'
    pass  # Ignore comments

def t_ANY_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

def t_input_error(t):
    print(f"input: Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

def t_states_error(t):
    print(f"states: Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

def t_target_error(t):
    print(f"target: Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# We will save all data here
state_machine = {
    'name': None,
    'initial_state': None,
    'states': {}
}

#-------------------------------------------------- 
#-- Ply Parser setup ------------------------------ 
#-------------------------------------------------- 
# Our config file should have the state name with its initial state followed by all of
#   its states and transitions
def p_sm(p):
    '''sm : name all_states'''
    pass

# Here we are parsing the state machine name as well as the initial state
def p_name(p):
    '''name : STATE_MACHINE_NAME STARTING_STATE'''
    state_machine['name'] = p[1]
    state_machine['initial_state'] = p[2]

# This is essentially a recursive definition for the list of states.
def p_all_states(p):
    '''all_states : all_states state
                     | state'''
    pass

# This will parse a single state. We will handle the case where it is either doc commented or not
def p_state(p):
    '''state : STATE_DEFINITION_NAME STATE_DEFINITION_BEGIN all_transitions STATE_DEFINITION_END 
                    | DOC_COMMENT STATE_DEFINITION_NAME STATE_DEFINITION_BEGIN all_transitions STATE_DEFINITION_END'''
    # Handle DOC comment
    if (len(p) == 6):
        state_doc = p[1]
        state_name = p[2]
        transitions = p[4]
        state_machine['states'][state_name] = dict()
        state_machine['states'][state_name]['transitions'] = transitions
        state_machine['states'][state_name]['doc'] = state_doc[3:].strip()
    # Handle undocumented case
    elif (len(p) == 5):
        state_name = p[1]
        transitions = p[3]
        state_machine['states'][state_name] = dict()
        state_machine['states'][state_name]['transitions'] = transitions
        state_machine['states'][state_name]['doc'] = None

# This defines that a state can have one or multiple transitions
def p_all_transitions(p):
    '''all_transitions : all_transitions transition
                          | transition'''
    if len(p) == 3:
        p[0] = p[1]
        p[0].append(p[2])
    else:
        p[0] = [p[1]]

def p_transition(p):
    '''transition : STATE_TRANSITION_INPUT STATE_TRANSITION_ARROW STATE_TRANSITION_TARGET
                    | DOC_COMMENT STATE_TRANSITION_INPUT STATE_TRANSITION_ARROW STATE_TRANSITION_TARGET'''
    # Handle uncommented case
    if (len(p) == 4):
        doc_str = None
        sm_input = p[1]
        transition_target = p[3]
        p[0] = (sm_input,transition_target,None)
    # Handle commented case
    elif (len(p) == 5):
        doc_str = p[1][3:].strip()
        sm_input = p[2]
        transition_target = p[4]
        p[0] = (sm_input,transition_target,doc_str)

def p_error(p):
    print(f"Syntax error at '{p.value}' '{p}'")

def parse(input_file,debug=False):
    sm_definition_src = ""

    # Read out the source file
    with open(input_file, "r") as f:
        sm_definition_src = f.read()

    # Build the lexer
    lexer = lex.lex()

    # Build the parser
    parser = yacc.yacc(debug=debug)

    if debug:
        lexer.input(sm_definition_src)
        for tok in lexer:
            print(tok)

        # Initialize the lexer back to the INITIAL state
        lexer.begin('INITIAL')

    parser.parse(sm_definition_src, debug=0)

    # Validate state machine
    if debug:
        print("NAME: {}".format(state_machine["name"]))
        print("INITIAL_STATE: {}".format(state_machine["initial_state"]))
    for s in state_machine["states"]:
        if debug:
            print(s)
        for t in state_machine["states"][s].keys():
            if debug:
                print("   ",t,":")
            if state_machine["states"][s][t] is not None and type(state_machine["states"][s][t]) is not str:
                for i in state_machine["states"][s][t]:
                    if debug:
                        print("      ",i)
            else:
                if debug:
                    print("      ",state_machine["states"][s][t])
            continue

    return state_machine
