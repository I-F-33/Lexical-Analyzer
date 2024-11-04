class Grammar:
    def __init__(self, productions):
        self.productions = productions
        self.first_sets = {}
        self.follow_sets = {}
        self.non_terminals = list(productions.keys())
        self.terminals = set()
        self.left_recursion_removed = {}

    # Calculate FIRST sets
    def calculate_first(self):
        for non_terminal in self.non_terminals:
            self.first_sets[non_terminal] = set()
        
        changed = True
        while changed:
            changed = False
            for non_terminal, production in self.productions.items():
                for prod in production:
                    for symbol in prod:
                        if symbol not in self.non_terminals:
                            if symbol not in self.first_sets[non_terminal]:
                                self.first_sets[non_terminal].add(symbol)
                                changed = True
                            break
                        else: 
                            if self.first_sets[symbol] - self.first_sets[non_terminal]:
                                self.first_sets[non_terminal].update(self.first_sets[symbol] - self.first_sets[non_terminal])
                                changed = True
                            if 'ε' in self.first_sets[symbol]:
                                continue
                            break
                    else:
                        if 'ε' not in self.first_sets[non_terminal]:
                            self.first_sets[non_terminal].add('ε')
                            changed = True
    
    # Calculate FOLLOW sets
    def calculate_follow(self):
        for non_terminal in self.non_terminals:
            self.follow_sets[non_terminal] = set()
        
        self.follow_sets[self.non_terminals[0]].add('$')

        changed = True
        while changed:
            changed = False
            for non_terminal, production in self.productions.items():
                for prod in production:
                    for symbol in prod:
                        if symbol in self.non_terminals:
                            index = prod.index(symbol)
                            if index + 1 < len(prod):
                                next_symbol = prod[index + 1]
                                if next_symbol in self.non_terminals:
                                    if self.first_sets[next_symbol] - self.follow_sets[symbol]:
                                        self.follow_sets[symbol].update(self.first_sets[next_symbol] - self.follow_sets[symbol])
                                        changed = True
                                    if 'ε' in self.first_sets[next_symbol]:
                                        if self.follow_sets[non_terminal] - self.follow_sets[symbol]:
                                            self.follow_sets[symbol].update(self.follow_sets[non_terminal] - self.follow_sets[symbol])
                                            changed = True
                                else:
                                    if next_symbol not in self.follow_sets[symbol]:
                                        self.follow_sets[symbol].add(next_symbol)
                                        changed = True
                            else:
                                if self.follow_sets[non_terminal] - self.follow_sets[symbol]:
                                    self.follow_sets[symbol].update(self.follow_sets[non_terminal] - self.follow_sets[symbol])
                                    changed = True
    # Remove left recursion
    def remove_left_recursion(self):
        new_productions = {}
        for non_terminal, production in self.productions.items():
            new_non_terminal = f"{non_terminal}'"
            alpha = []
            beta = []
            for prod in production:
                if prod[0] == non_terminal:
                    alpha.append(prod[1:])
                else:
                    beta.append(prod)
            if alpha:
                new_productions[non_terminal] = [*beta, [new_non_terminal]]
                new_productions[new_non_terminal] = [*alpha, ['ε']]
            else:
                new_productions[non_terminal] = beta

        self.left_recursion_removed = new_productions

    def display_results(self):
        print("FIRST sets:")
        for non_terminal, first in self.first_sets.items():
            print(f"FIRST({non_terminal}) = {{{', '.join(first)}}}")

        print("\nFOLLOW sets:")
        for non_terminal, follow in self.follow_sets.items():
            print(f"FOLLOW({non_terminal}) = {{{', '.join(follow)}}}")

        print("\nGrammar after removing left recursion:")
        for non_terminal, production in self.left_recursion_removed.items():
            prods = [' '.join(prod) for prod in production]
            print(f"{non_terminal} → {' | '.join(prods)}")


if __name__ == "__main__":
    # Define grammar
    grammar_productions = {
        'program': [['basic', 'main()', 'block']],
        'block': [['{', 'decls_stmts', '}']],
        'decls_stmts': [['decl', 'decls_stmts'], ['stmt', 'decls_stmts'], ['ε']],
        'decl': [['type', 'id', 'array_decl', 'init', ';']],
        'array_decl': [['[', 'expr', ']'], ['ε']],
        'init': [['=', 'initializer'], ['ε']],
        'initializer': [['{', 'expr_list', '}'], ['expr']],
        'expr_list': [['expr', 'expr_list_prime']],
        'expr_list_prime': [[',', 'expr', 'expr_list_prime'], ['ε']],
        'type': [['num', 'type_prime'], ['real', 'type_prime'], ['basic', 'type_prime']],
        'type_prime': [['[', 'num', ']', 'type_prime'], ['ε']],
        'stmt': [['if_stmt'], ['while', '(', 'bool', ')', 'stmt'], ['for', '(', 'for_init', ';', 'bool', ';', 'for_update', ')', 'stmt'], ['do', 'stmt', 'while', '(', 'bool', ')', ';'], ['break', ';'], ['continue', ';'], ['return', 'num', ';'], ['block'], ['loc', '=', 'bool', ';']],
        'if_stmt': [['if', '(', 'bool', ')', 'matched_stmt'], ['if', '(', 'bool', ')', 'unmatched_stmt']],
        'matched_stmt': [['stmt', 'else', 'stmt']],
        'unmatched_stmt': [['stmt']],
        'for_init': [['decl'], ['loc', '=', 'expr'], ['ε']],
        'for_update': [['loc', '=', 'expr'], ['increment'], ['decrement'], ['ε']],
        'loc': [['id', 'loc_prime']],
        'loc_prime': [['[', 'bool', ']', 'loc_prime'], ['ε']],
        'bool': [['join', 'bool_prime']],
        'bool_prime': [['||', 'join', 'bool_prime'], ['ε']],
        'join': [['equality', 'join_prime']],
        'join_prime': [['&&', 'equality', 'join_prime'], ['ε']],
        'equality': [['rel', 'equality_prime']],
        'equality_prime': [['==', 'rel', 'equality_prime'], ['!=', 'rel', 'equality_prime'], ['ε']],
        'rel': [['expr', 'rel_prime']],
        'rel_prime': [['<', 'expr'], ['<=', 'expr'], ['>=', 'expr'], ['>', 'expr'], ['ε']],
        'expr': [['term', 'expr_prime']],
        'expr_prime': [['+', 'term', 'expr_prime'], ['-', 'term', 'expr_prime'], ['ε']],
        'term': [['unary', 'term_prime']],
        'term_prime': [['*', 'unary', 'term_prime'], ['/', 'unary', 'term_prime'], ['ε']],
        'unary': [['!', 'unary'], ['-', 'unary'], ['factor'], ['increment'], ['decrement']],
        'factor': [['(', 'bool', ')'], ['loc'], ['num'], ['real'], ['true'], ['false']],
        'increment': [['loc', '++'], ['++', 'loc']],
        'decrement': [['loc', '--'], ['--', 'loc']]
    }

    grammar = Grammar(grammar_productions)
    grammar.calculate_first()
    grammar.calculate_follow()
    grammar.remove_left_recursion()
    grammar.display_results()
