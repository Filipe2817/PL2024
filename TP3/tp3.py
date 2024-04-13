import sys
import re
import automaton

###############################################################################################

def findall_version(text):
    pattern = re.compile(r'on|off|=|[+-]?\d+(?:\.\d+)?', flags=re.IGNORECASE)
    tokens = pattern.findall(text)

    state = True
    value = 0

    for token in tokens:
        if token.lower() == 'on':
            state = True
        elif token.lower() == 'off':
            state = False
        elif token == '=':
            print("Sum:", value)
        elif state:
            value += int(token) if "." not in token else float(token)
    
###############################################################################################

def automaton_version(text):
    states = {'ON', 'OFF'}
    alphabet = {
        'on': r'(?i:on)',
        'off': r'(?i:off)',
        'equals': r'=',
        'number': r'[+-]?\d+(?:\.\d+)?'
    }
    transitions = {
        'ON': {'on': 'ON', 'off': 'OFF', 'equals': 'ON', 'number': 'ON'},
        'OFF': {'on': 'ON', 'off': 'OFF', 'equals': 'OFF', 'number': 'OFF'}
    }
    initial_state = 'ON'
    accepting_states = {'ON', 'OFF'}

    fsa = automaton.FiniteStateAutomaton(states, alphabet, transitions, initial_state, accepting_states)
    fsa.process_input(text)

###############################################################################################

def main():
    text = sys.stdin.read()

    # restore stdin
    sys.stdin.close()
    sys.stdin = open('/dev/tty')

    flag = True

    while flag:
        version = input("Enter the version:\n(1) Findall\n(2) Automaton\n(?) Any other key to exit\n> ")
        if version == '1':
            print("Running findall version...")
            findall_version(text)
        elif version == '2':
            print("Running automaton version...")
            automaton_version(text)
        else:
            flag = False

if __name__ == '__main__':
    main()

# Tokens:
# [on, -28, ON, =, 80, off, 2.5, ON, on, on, =, 23.5, 50, 40, 7, 15, 10, OFF, on, on, off, On, 6, 30, ON, =, -24.3, 99.8, oN, OfF, 4, 1.2, ON, -0.8, =]
# -28, print(-28), 52, print(52), 75.5, 125.5, 165.5, 172.5, 187.5, 197.5, 203.5, 233.5, print(233.5), 209.2, 309, 308.2, print(308.2)
