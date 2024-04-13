import re

class FiniteStateAutomaton:
    def __init__(self, states, alphabet, transitions, initial_state, accepting_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.current_state = initial_state
        self.initial_state = initial_state
        self.accepting_states = accepting_states

    def reset(self):
        self.current_state = self.initial_state

    def tokenize(self, input_text): # findall would be better in terms of performance, but this solution with groups is really cool
        tokens = []
        pattern = '|'.join(f"(?P<{token_type}>{regex})" for token_type, regex in self.alphabet.items())

        for match in re.finditer(pattern, input_text):
            for token_type, token_value in match.groupdict().items():
                if token_value: # token or None
                    tokens.append((token_type, token_value))

        return tokens

    def process_input(self, input):
        tokens = iter(self.tokenize(input))
        error = False
        value = 0
        
        while not error and (element := next(tokens, False)):
            token_type, token_value = element
            if self.current_state not in self.transitions or token_type not in self.transitions[self.current_state]:
                error = True
                error_message = f"Error: there is no transition defined for state '{self.current_state}' with symbol '{token_type}'."
            else: # can't remove this else because self.current_state would be changed in case of error
                if token_type == 'number' and self.current_state == 'ON':
                    value += int(token_value) if "." not in token_value else float(token_value)
                elif token_type == 'equals':
                    print("Sum:", value)

                self.current_state = self.transitions[self.current_state][token_type]

        if error:
            return (False, error_message)
        
        if self.current_state in self.accepting_states:
            return (True, value)
        
        return (False, "Semantic error: the automaton did not reach a final state!")
