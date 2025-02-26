from rply import ParserGenerator
from .conversion import conversion_dict

class Parser:

    expected_tokens = {
        None: ['dinein'],  # Program must start with 'dinein'
        'dinein': ['pasta', 'pinch', 'skim', 'bool', 'recipe', 'full', 'hungry', 'chef'],  # After 'dinein', allow all top-level declarations
        # general expected tokens based solely on the current token type
        'chef': ['pinch'],
        ('pinch', 'pinch', 'chef'): ['dish'],  # specific rule when the last reserved word is chef for pinch
        'dish': ['('],
        ('(', 'dish'): [')'],  # specific rule when the last reserved word is dish for (
        (')', 'dish'): ['{'],  # specific rule when the last reserved word is dish for )
        '{': ['pasta', 'pinch', 'skim', 'bool', 'recipe', 'taste', 'make', 'serve', 'for', 'simmer', 'chop', 'identifier', 'spit'],  # dish and full
        ('spit', 'dish'): ['pinchliterals'],  # specific rule when the for spit inside the dish function to be updated with literals...
        ('pinchliterals', 'spit'): [';'],  # specific rule when the last reserved word is spit for pinchliterals

        # Variable Declaration
        'pasta': ['identifier'],
        'pinch': ['identifier'],
        'skim': ['identifier'],
        'bool': ['identifier'],
        
        # Variable Declaration to Variable Initialization
        ('identifier', 'pasta'): [',', ';', '='],
        ('identifier', 'pinch'): [',', ';', '='],
        ('identifier', 'skim'): [',', ';', '='],
        ('identifier', 'bool'): [',', ';', '='],
        (';', 'pasta'): ['pasta', 'pinch', 'skim', 'bool', 'recipe', 'full', 'hungry', 'chef'],
        (';', 'pinch'): ['pasta', 'pinch', 'skim', 'bool', 'recipe', 'full', 'hungry', 'chef'],
        (';', 'skim'): ['pasta', 'pinch', 'skim', 'bool', 'recipe', 'full', 'hungry', 'chef'],
        (';', 'bool'): ['pasta', 'pinch', 'skim', 'bool', 'recipe', 'full', 'hungry', 'chef'],

        # Declaration Tail
        ',': ['identifier'],
        ('identifier', 'pasta', ',', 'identifier'): [',', ';'],
        ('identifier', 'pinch', ',', 'identifier'): [',', ';'],
        ('identifier', 'skim', ',', 'identifier'): [',', ';'],
        ('identifier', 'bool', ',', 'identifier'): [',', ';'],

        # Variable Initialization
        ('=', 'pasta'): ['pastaliterals'],
        ('=', 'pinch'): ['pinchliterals', 'nepinch'],
        ('=', 'skim'): ['skimliterals', 'neskim'],
        ('=', 'bool'): ['yum', 'bleh'],
        ('=', 'yum'): ['yum', 'bleh'],
        ('=', 'bleh'): ['yum', 'bleh'],
        ('identifier', 'pasta', ','): ['='],
        ('identifier', 'pinch', ','): ['='],
        ('identifier', 'skim', ','): ['='],
        ('identifier', 'bleh', ','): ['='],
        ('identifier', 'yum', ','): ['='],
        (',', 'pasta', 'pastaliterals', '='): ['identifier'],
        (',', 'pinch', 'pinchliterals', '='): ['identifier'],
        (',', 'pinch', 'nepinch', '='): ['identifier'],
        (',', 'skim', 'skimliterals', '='): ['identifier'],
        (',', 'skim', 'skimliterals', '='): ['identifier'],
        (',', 'bool', 'bleh', '='): ['identifier'],
        (',', 'bool', 'yum', '='): ['identifier'],

        # Variable Initialization to Initialize Tail
        ('pastaliterals', 'pasta'): [',', ';'],
        ('pinchliterals', 'pinch'): [',', ';'],
        ('nepinch', 'pinch'): [',', ';'],
        ('skimliterals', 'skim'): [',', ';'],
        ('neskim', 'skim'): [',', ';'],
        ('yum', 'yum'): [',', ';'],
        ('bleh', 'bleh'): [',', ';'],
        (';', 'bleh'): ['pasta', 'pinch', 'skim', 'bool', 'recipe', 'full', 'hungry', 'chef'],
        (';', 'yum'): ['pasta', 'pinch', 'skim', 'bool', 'recipe', 'full', 'hungry', 'chef'],

        # Array Declaration
        'recipe': ['pasta', 'pinch', 'skim', 'bool'],
        ('identifier', 'pasta', 'recipe'): ['['],
        ('identifier', 'pinch', 'recipe'): ['['],
        ('identifier', 'skim', 'recipe'): ['['],
        ('identifier', 'bool', 'recipe'): ['['],
        '[': ['identifier', 'pinchliterals'],
        ('identifier', 'pasta', '['): [']'],
        ('identifier', 'pinch', '['): [']'],
        ('identifier', 'skim', '['): [']'],
        ('identifier', 'bool', '['): [']'],
        ('pinchliterals', 'pasta', '['): [']'],
        ('pinchliterals', 'pinch', '['): [']'],
        ('pinchliterals', 'skim', '['): [']'],
        ('pinchliterals', 'bool', '['): [']'],
        ']': [';', '='],

        # Array Initialization
        ('=', 'pasta', ']'): ['{'],
        ('=', 'pinch', ']'): ['{'],
        ('=', 'skim', ']'): ['{'],
        ('=', 'bool', ']'): ['{'],
        ('{', 'pasta', '='): ['pastaliterals'],
        ('{', 'pinch', '='): ['pinchliterals', 'nepinch'],
        ('{', 'skim', '='): ['skimliterals', 'neskim'],
        ('{', 'bool', '='): ['BOOLLITERAL'],
        ('pastaliterals', 'pasta', '{'): [','],
        ('pinchliterals', 'pinch', '{'): [','],
        ('nepinch', 'pinch', '{'): [','],
        ('skimliterals', 'skim', '{'): [','],
        ('neskim', 'skim', '{'): [','],
        ('bleh', 'bleh', '{'): [','],
        ('yum', 'yum', '{'): [','],
        (',', 'pasta', 'pastaliterals'): ['pastaliterals'],
        (',', 'pinch', 'pinchliterals'): ['pinchliterals', 'nepinch'],
        (',', 'pinch', 'nepinch'): ['pinchliterals', 'nepinch'],
        (',', 'skim', 'skimliterals'): ['skimliterals', 'neskim'],
        (',', 'skim', 'skimliterals'): ['skimliterals', 'neskim'],
        (',', 'bool', 'bleh'): ['bleh', 'yum'],
        (',', 'bool', 'yum'): ['bleh', 'yum'],
        ('pastaliterals', 'pasta', ','): [',', '}'],
        ('pinchliterals', 'pinch', ','): [',', '}'],
        ('nepinch', 'pinch', ','): [',', '}'],
        ('skimliterals', 'skim', ','): [',', '}'],
        ('neskim', 'skim', ','): [',', '}'],
        ('bleh', 'bleh', ','): [',', '}'],
        ('yum', 'yum', ','): [',', '}'],
        ('}', 'pasta'): [';'],
        ('}', 'pinch'): [';'],
        ('}', 'skim'): [';'],
        ('}', 'bool'): [';'],
        ('}', 'bleh'): [';'],
        ('}', 'yum'): [';'],

        # Function Definition
        'full': ['pasta', 'pinch', 'skim', 'bool'],
        ('identifier', 'pasta', 'full'): ['('],
        ('identifier', 'pinch', 'full'): ['('],
        ('identifier', 'skim', 'full'): ['('],
        ('identifier', 'bool', 'full'): ['('],
        '(': ['pasta', 'pinch', 'skim', 'bool'],
        ('identifier', 'pasta', 'pasta', 'full'): [',', ')'],
        ('identifier', 'pinch', 'pinch', 'full'): [',', ')'],
        ('identifier', 'skim', 'skim', 'full'): [',', ')'],
        ('identifier', 'bool', 'bool', 'full'): [',', ')'],
        (',', 'pasta', 'identifier', 'full'): ['pasta', 'pinch', 'skim', 'bool'],
        (',', 'pinch', 'identifier', 'full'): ['pasta', 'pinch', 'skim', 'bool'],
        (',', 'skim', 'identifier', 'full'): ['pasta', 'pinch', 'skim', 'bool'],
        (',', 'bool', 'identifier', 'full'): ['pasta', 'pinch', 'skim', 'bool'],
        (')', 'pasta'): ['{'],
        (')', 'pinch'): ['{'],
        (')', 'skim'): ['{'],
        (')', 'bool'): ['{'],
        ('identifier', 'pasta', 'pasta', 'pasta', 'full'): [',', ';', '='],
        ('identifier', 'pasta', 'pasta', 'pinch', 'full'): [',', ';', '='],
        ('identifier', 'pasta', 'pasta', 'skim', 'full'): [',', ';', '='],
        ('identifier', 'pasta', 'pasta', 'bool', 'full'): [',', ';', '='],
        ('identifier', 'pinch', 'pinch', 'pasta', 'full'): [',', ';', '='],
        ('identifier', 'pinch', 'pinch', 'pinch', 'full'): [',', ';', '='],
        ('identifier', 'pinch', 'pinch', 'skim', 'full'): [',', ';', '='],
        ('identifier', 'pinch', 'pinch', 'bool', 'full'): [',', ';', '='],
        ('identifier', 'skim', 'skim', 'pasta', 'full'): [',', ';', '='],
        ('identifier', 'skim', 'skim', 'pinch', 'full'): [',', ';', '='],
        ('identifier', 'skim', 'skim', 'skim', 'full'): [',', ';', '='],
        ('identifier', 'skim', 'skim', 'bool', 'full'): [',', ';', '='],
        ('identifier', 'bool', 'bool', 'pasta', 'full'): [',', ';', '='],
        ('identifier', 'bool', 'bool', 'pinch', 'full'): [',', ';', '='],
        ('identifier', 'bool', 'bool', 'skim', 'full'): [',', ';', '='],
        ('identifier', 'bool', 'bool', 'bool', 'full'): [',', ';', '='],
        (',', 'pasta', 'identifier', 'pasta', 'full'): ['identifier'],
        (',', 'pasta', 'identifier', 'pinch', 'full'): ['identifier'],
        (',', 'pasta', 'identifier', 'skim', 'full'): ['identifier'],
        (',', 'pasta', 'identifier', 'bool', 'full'): ['identifier'],
        (',', 'pinch', 'identifier', 'pasta', 'full'): ['identifier'],
        (',', 'pinch', 'identifier', 'pinch', 'full'): ['identifier'],
        (',', 'pinch', 'identifier', 'skim', 'full'): ['identifier'],
        (',', 'pinch', 'identifier', 'bool', 'full'): ['identifier'],
        (',', 'skim', 'identifier', 'pasta', 'full'): ['identifier'],
        (',', 'skim', 'identifier', 'pinch', 'full'): ['identifier'],
        (',', 'skim', 'identifier', 'skim', 'full'): ['identifier'],
        (',', 'skim', 'identifier', 'bool', 'full'): ['identifier'],
        (',', 'bool', 'identifier', 'pasta', 'full'): ['identifier'],
        (',', 'bool', 'identifier', 'pinch', 'full'): ['identifier'],
        (',', 'bool', 'identifier', 'skim', 'full'): ['identifier'],
        (',', 'bool', 'identifier', 'bool', 'full'): ['identifier'],
        ('identifier', 'pasta', 'pasta', 'recipe'): ['['],
        ('identifier', 'pinch', 'pinch', 'recipe'): ['['],
        ('identifier', 'skim', 'skim', 'recipe'): ['['],
        ('identifier', 'bool', 'bool', 'recipe'): ['['],
        (';', 'pasta', 'full'): ['pasta', 'pinch', 'skim', 'bool', 'recipe', 'taste', 'make', 'serve', 'for', 'simmer', 'identifier', 'spit', '}'],
        (';', 'pinch', 'full'): ['pasta', 'pinch', 'skim', 'bool', 'recipe', 'taste', 'make', 'serve', 'for', 'simmer', 'identifier', 'spit', '}'],
        (';', 'skim', 'full'): ['pasta', 'pinch', 'skim', 'bool', 'recipe', 'taste', 'make', 'serve', 'for', 'simmer', 'identifier', 'spit', '}'],
        (';', 'bool', 'full'): ['pasta', 'pinch', 'skim', 'bool', 'recipe', 'taste', 'make', 'serve', 'for', 'simmer', 'identifier', 'spit', '}'],
        ('spit', 'spit'): ['pastaliterals', 'pinchliterals', 'neatliterals', 'skimliterals', 'neskim', 'bleh', 'yum', 'identifier'],
        # spit [expr, func_call, type_cast, esc_sequence]
        
        ('pastaliterals', 'spit'): [';'],
        ('pinchliterals', 'spit'): [';'],
        ('skimliterals', 'spit'): [';'],
        ('neskim', 'spit'): [';'],
        ('yum', 'yum', 'spit'): [';'],
        ('bleh', 'bleh', 'spit'): [';'],
        (';', 'spit'): ['}'],
        (';', 'yum', 'full'): ['}'],
        (';', 'bleh', 'full'): ['}'],
        ('}', 'spit'): ['full', 'hungry', 'chef'],

        # Hungry function transitions
        'Hungry': ['identifier'],
        ('identifier', 'hungry'): ['('],
        ('identifier', 'pasta', 'hungry'): [',', ')'],
        ('identifier', 'pinch', 'hungry'): [',', ')'],
        ('identifier', 'skim', 'hungry'): [',', ')'],
        ('identifier', 'bool', 'hungry'): [',', ')'],
        (',', 'pasta', 'hungry'): ['pasta', 'pinch', 'skim', 'bool'],
        (',', 'pinch', 'hungry'): ['pasta', 'pinch', 'skim', 'bool'],
        (',', 'skim', 'hungry'): ['pasta', 'pinch', 'skim', 'bool'],
        (',', 'bool', 'hungry'): ['pasta', 'pinch', 'skim', 'bool'],
        ('{', 'pasta', 'hungry'): ['pasta', 'pinch', 'skim', 'bool', 'recipe', 'taste', 'make', 'serve', 'for', 'simmer', 'identifier'],
        ('{', 'pinch', 'hungry'): ['pasta', 'pinch', 'skim', 'bool', 'recipe', 'taste', 'make', 'serve', 'for', 'simmer', 'identifier'],
        ('{', 'skim', 'hungry'): ['pasta', 'pinch', 'skim', 'bool', 'recipe', 'taste', 'make', 'serve', 'for', 'simmer', 'identifier'],
        ('{', 'bool', 'hungry'): ['pasta', 'pinch', 'skim', 'bool', 'recipe', 'taste', 'make', 'serve', 'for', 'simmer', 'identifier'],
        ('identifier', 'pasta', 'pasta', 'pasta', 'hungry'): [',', ';', '='],
        ('identifier', 'pasta', 'pasta', 'pinch', 'hungry'): [',', ';', '='],
        ('identifier', 'pasta', 'pasta', 'skim', 'hungry'): [',', ';', '='],
        ('identifier', 'pasta', 'pasta', 'bool', 'hungry'): [',', ';', '='],
        ('identifier', 'pinch', 'pinch', 'pasta', 'hungry'): [',', ';', '='],
        ('identifier', 'pinch', 'pinch', 'pinch', 'hungry'): [',', ';', '='],
        ('identifier', 'pinch', 'pinch', 'skim', 'hungry'): [',', ';', '='],
        ('identifier', 'pinch', 'pinch', 'bool', 'hungry'): [',', ';', '='],
        ('identifier', 'skim', 'skim', 'pasta', 'hungry'): [',', ';', '='],
        ('identifier', 'skim', 'skim', 'pinch', 'hungry'): [',', ';', '='],
        ('identifier', 'skim', 'skim', 'skim', 'hungry'): [',', ';', '='],
        ('identifier', 'skim', 'skim', 'bool', 'hungry'): [',', ';', '='],
        ('identifier', 'bool', 'bool', 'pasta', 'hungry'): [',', ';', '='],
        ('identifier', 'bool', 'bool', 'pinch', 'hungry'): [',', ';', '='],
        ('identifier', 'bool', 'bool', 'skim', 'hungry'): [',', ';', '='],
        ('identifier', 'bool', 'bool', 'bool', 'hungry'): [',', ';', '='],
        (',', 'pasta', 'identifier', 'pasta', 'hungry'): ['identifier'],
        (',', 'pasta', 'identifier', 'pinch', 'hungry'): ['identifier'],
        (',', 'pasta', 'identifier', 'skim', 'hungry'): ['identifier'],
        (',', 'pasta', 'identifier', 'bool', 'hungry'): ['identifier'],
        (',', 'pinch', 'identifier', 'pasta', 'hungry'): ['identifier'],
        (',', 'pinch', 'identifier', 'pinch', 'hungry'): ['identifier'],
        (',', 'pinch', 'identifier', 'skim', 'hungry'): ['identifier'],
        (',', 'pinch', 'identifier', 'bool', 'hungry'): ['identifier'],
        (',', 'skim', 'identifier', 'pasta', 'hungry'): ['identifier'],
        (',', 'skim', 'identifier', 'pinch', 'hungry'): ['identifier'],
        (',', 'skim', 'identifier', 'skim', 'hungry'): ['identifier'],
        (',', 'skim', 'identifier', 'bool', 'hungry'): ['identifier'],
        (',', 'bool', 'identifier', 'pasta', 'hungry'): ['identifier'],
        (',', 'bool', 'identifier', 'pinch', 'hungry'): ['identifier'],
        (',', 'bool', 'identifier', 'skim', 'hungry'): ['identifier'],
        (',', 'bool', 'identifier', 'bool', 'hungry'): ['identifier'],
        (';', 'pasta', 'identifier', 'hungry'): ['pasta', 'pinch', 'skim', 'bool', 'recipe', 'taste', 'make', 'serve', 'for', 'simmer', 'identifier', '}'],
        (';', 'pinch', 'identifier', 'hungry'): ['pasta', 'pinch', 'skim', 'bool', 'recipe', 'taste', 'make', 'serve', 'for', 'simmer', 'identifier', '}'],
        (';', 'skim', 'identifier', 'hungry'): ['pasta', 'pinch', 'skim', 'bool', 'recipe', 'taste', 'make', 'serve', 'for', 'simmer', 'identifier', '}'],
        (';', 'bool', 'identifier', 'hungry'): ['pasta', 'pinch', 'skim', 'bool', 'recipe', 'taste', 'make', 'serve', 'for', 'simmer', 'identifier', '}'],
        (';', 'pasta', 'pastaliterals', 'hungry'): ['pasta', 'pinch', 'skim', 'bool', 'recipe', 'taste', 'make', 'serve', 'for', 'simmer', 'identifier', '}'],
        (';', 'pinch', 'pinchliterals', 'hungry'): ['pasta', 'pinch', 'skim', 'bool', 'recipe', 'taste', 'make', 'serve', 'for', 'simmer', 'identifier', '}'],
        (';', 'pinch', 'nepinch', 'hungry'): ['pasta', 'pinch', 'skim', 'bool', 'recipe', 'taste', 'make', 'serve', 'for', 'simmer', 'identifier', '}'],
        (';', 'skim', 'skimliterals', 'hungry'): ['pasta', 'pinch', 'skim', 'bool', 'recipe', 'taste', 'make', 'serve', 'for', 'simmer', 'identifier', '}'],
        (';', 'skim', 'neskim', 'hungry'): ['pasta', 'pinch', 'skim', 'bool', 'recipe', 'taste', 'make', 'serve', 'for', 'simmer', 'identifier', '}'],
        (';', 'cap', 'hungry'): ['pasta', 'pinch', 'skim', 'bool', 'recipe', 'taste', 'make', 'serve', 'for', 'simmer', 'identifier', '}'],
        (';', 'nocap', 'hungry'): ['pasta', 'pinch', 'skim', 'bool', 'recipe', 'taste', 'make', 'serve', 'for', 'simmer', 'identifier', '}'],
        (';', 'pasta', 'hungry'): ['pasta', 'pinch', 'skim', 'bool', 'recipe', 'taste', 'make', 'serve', 'for', 'simmer', 'identifier', '}'],
        (';', 'pinch', 'hungry'): ['pasta', 'pinch', 'skim', 'bool', 'recipe', 'taste', 'make', 'serve', 'for', 'simmer', 'identifier', '}'],
        (';', 'skim', 'hungry'): ['pasta', 'pinch', 'skim', 'bool', 'recipe', 'taste', 'make', 'serve', 'for', 'simmer', 'identifier', '}'],
        # (';', 'pasta', 'hungry'): ['pasta', 'pinch', 'skim', 'bool', 'recipe', 'taste', 'make', 'serve', 'for', 'simmer', 'identifier', '}'],
        # (',', 'pastaliterals', '{'): ['sample']
        # ('}', 'pasta', ';', 'pastaliterals'): ['full', 'hungry', 'chef..'],
        # closing bracket of void func



        # chef pinch dish() {
        (';', 'pinch', 'chef'): ['pasta', 'pinch', 'skim', 'bool', 'recipe', 'taste', 'make', 'serve', 'for', 'simmer', 'identifier', 'spit'],
        (';', 'pasta', 'chef'): ['pasta', 'pinch', 'skim', 'bool', 'recipe', 'taste', 'make', 'serve', 'for', 'simmer', 'identifier', 'spit'],
        (';', 'skim', 'chef'): ['pasta', 'pinch', 'skim', 'bool', 'recipe', 'taste', 'make', 'serve', 'for', 'simmer', 'identifier', 'spit'],
        (';', 'bleh', 'chef'): ['pasta', 'pinch', 'skim', 'bool', 'recipe', 'taste', 'make', 'serve', 'for', 'simmer', 'identifier', 'spit'],
        (';', 'yum', 'chef'): ['pasta', 'pinch', 'skim', 'bool', 'recipe', 'taste', 'make', 'serve', 'for', 'simmer', 'identifier', 'spit'],
        ('pinch', 'pinch', 'chef'): ['identifier'],

        # Make Stmt
        'make': ['('],
        ('(', 'make'): ['identifier'],

        #('identifier', 'make', '('): [')'],
        ('identifier', 'make'): ['[', ')'],
        ('identifier', 'make', '['): [']'],
        ('pinchliterals', 'make'): [']'],
        (']', 'make'): [')'],
        (')', 'make'): [';'],
        (';', 'make'): ['taste', 'make', 'serve', 'for', 'simmer', 'identifier', 'spit'],
        (';', 'make', 'hungry'): ['taste', 'make', 'serve', 'for', 'simmer', 'identifier', '}'],
 
        # serve statement
        ('identifier', 'serve'): [')', '~'],
        ('(', 'serve'): ['identifier', 'pastaliterals', 'pinchliterals', 'nepinch', 'skimliterals', 'neskim', 'bleh', 'yum'],
        ('identifier', 'serve'): [')', '~'],
        ('pastaliterals', 'serve'): [')', '~'],
        ('pinchliterals', 'serve'): [')', '~'],
        ('nepinch', 'serve'): [')', '~'],
        ('skimliterals', 'serve'): [')', '~'],
        ('neskim', 'serve'): [')', '~'],
        ('bleh', 'bleh', '('): [')', '~'],
        ('yum', 'yum', '('): [')', '~'],
        ('~', 'serve'): ['identifier', 'pastaliterals', 'pinchliterals', 'nepinch', 'skimliterals', 'neskim', 'bleh', 'yum'],
        ('~', 'bleh'): ['identifier', 'pastaliterals', 'pinchliterals', 'nepinch', 'skimliterals', 'neskim', 'bleh', 'yum'],
        ('~', 'yum'): ['identifier', 'pastaliterals', 'pinchliterals', 'nepinch', 'skimliterals', 'neskim', 'bleh', 'yum'],
        ('yum', 'yum', '~'): [')', '~'],
        ('bleh', 'bleh', '~'): [')', '~'],
        (')', 'serve'): [';'],
        (')', 'bleh'): [';'],
        (')', 'yum'): [';'],
        (';', 'serve'): ['taste', 'make', 'serve', 'for', 'simmer', 'identifier', 'spit'],
        (';', 'serve', 'hungry'): ['taste', 'make', 'serve', 'for', 'simmer', 'identifier', '}'],
        (';', 'bleh', 'serve'): ['taste', 'make', 'serve', 'for', 'simmer', 'identifier', 'spit'],
        (';', 'yum', 'serve'): ['taste', 'make', 'serve', 'for', 'simmer', 'identifier', 'spit'],
        (';', 'yum', 'yum'): ['taste', 'make', 'serve', 'for', 'simmer', 'identifier', 'spit'],
        (';', 'yum', 'bleh'): ['taste', 'make', 'serve', 'for', 'simmer', 'identifier', 'spit'],
        (';', 'bleh', 'bleh'): ['taste', 'make', 'serve', 'for', 'simmer', 'identifier', 'spit'],
        (';', 'bleh', 'yum'): ['taste', 'make', 'serve', 'for', 'simmer', 'identifier', 'spit'],

        
        # For Stmt
        'for': ['('],
        ('(', 'for'): ['pinch', 'skim'],
        ('identifier', 'pinch', 'for'): ['='],
        ('identifier', 'skim', 'for'): ['='],
        ('pinchliterals', 'pinch', 'for'): [';'],
        ('nepinch', 'pinch', 'for'): [';'],
        ('skimliterals', 'skim', 'for'): [';'],
        ('neskim', 'skim', 'for'): [';'],
        (';', 'pinch', 'for'): ['identifier', 'pinchliterals', 'nepinch', 'skimliterals', 'neskim'],
        (';', 'skim', 'for'): ['identifier', 'pinchliterals', 'nepinch', 'skimliterals', 'neskim'],
        ('identifier', 'pinch', ';', 'pinchliterals'): ['<', '>', '<=', '>=', '==', '!='],
        ('identifier', 'pinch', ';', 'nepinch'): ['<', '>', '<=', '>=', '==', '!='],
        ('identifier', 'skim', ';', 'skimliterals'): ['<', '>', '<=', '>=', '==', '!='],
        ('identifier', 'skim', ';', 'neskim'): ['<', '>', '<=', '>=', '==', '!='],
        ('pinchliterals', 'pinch', ';', 'pinchliterals'): ['<', '>', '<=', '>=', '==', '!='],
        ('pinchliterals', 'pinch', ';', 'nepinch'): ['<', '>', '<=', '>=', '==', '!='],
        ('pinchliterals', 'skim', ';', 'skimliterals'): ['<', '>', '<=', '>=', '==', '!='],
        ('pinchliterals', 'skim', ';', 'neskim'): ['<', '>', '<=', '>=', '==', '!='],
        ('nepinch', 'pinch', ';', 'pinchliterals'): ['<', '>', '<=', '>=', '==', '!='],
        ('nepinch', 'pinch', ';', 'nepinch'): ['<', '>', '<=', '>=', '==', '!='],
        ('nepinch', 'skim', ';', 'skimliterals'): ['<', '>', '<=', '>=', '==', '!='],
        ('nepinch', 'skim', ';', 'neskim'): ['<', '>', '<=', '>=', '==', '!='],
        ('skimliterals', 'pinch', ';', 'pinchliterals'): ['<', '>', '<=', '>=', '==', '!='],
        ('skimliterals', 'pinch', ';', 'nepinch'): ['<', '>', '<=', '>=', '==', '!='],
        ('skimliterals', 'skim', ';', 'skimliterals'): ['<', '>', '<=', '>=', '==', '!='],
        ('skimliterals', 'skim', ';', 'neskim'): ['<', '>', '<=', '>=', '==', '!='],
        ('neskim', 'pinch', ';', 'pinchliterals'): ['<', '>', '<=', '>=', '==', '!='],
        ('neskim', 'pinch', ';', 'nepinch'): ['<', '>', '<=', '>=', '==', '!='],
        ('neskim', 'skim', ';', 'skimliterals'): ['<', '>', '<=', '>=', '==', '!='],
        ('neskim', 'skim', ';', 'neskim'): ['<', '>', '<=', '>=', '==', '!='],
        ('<', 'pinch'): ['identifier', 'pinchliterals', 'nepinch', 'skimliterals', 'neskim'],
        ('<', 'skim'): ['identifier', 'pinchliterals', 'nepinch', 'skimliterals', 'neskim'],
        ('>', 'pinch'): ['identifier', 'pinchliterals', 'nepinch', 'skimliterals', 'neskim'],
        ('>', 'skim'): ['identifier', 'pinchliterals', 'nepinch', 'skimliterals', 'neskim'],
        ('<=', 'pinch'): ['identifier', 'pinchliterals', 'nepinch', 'skimliterals', 'neskim'],
        ('<=', 'skim'): ['identifier', 'pinchliterals', 'nepinch', 'skimliterals', 'neskim'],
        ('>=', 'pinch'): ['identifier', 'pinchliterals', 'nepinch', 'skimliterals', 'neskim'],
        ('>=', 'skim'): ['identifier', 'pinchliterals', 'nepinch', 'skimliterals', 'neskim'],
        ('==', 'pinch'): ['identifier', 'pinchliterals', 'nepinch', 'skimliterals', 'neskim'],
        ('==', 'skim'): ['identifier', 'pinchliterals', 'nepinch', 'skimliterals', 'neskim'],
        ('!=', 'pinch'): ['identifier', 'pinchliterals', 'nepinch', 'skimliterals', 'neskim'],
        ('!=', 'skim'): ['identifier', 'pinchliterals', 'nepinch', 'skimliterals', 'neskim'],
        ('identifier', 'pinch', '<'): [';'],
        ('identifier', 'pinch', '>'): [';'],
        ('identifier', 'pinch', '<='): [';'],
        ('identifier', 'pinch', '>='): [';'],
        ('identifier', 'pinch', '=='): [';'],
        ('identifier', 'pinch', '!='): [';'],
        ('identifier', 'skim', '<'): [';'],
        ('identifier', 'skim', '>'): [';'],
        ('identifier', 'skim', '<='): [';'],
        ('identifier', 'skim', '>='): [';'],
        ('identifier', 'skim', '=='): [';'],
        ('identifier', 'skim', '!='): [';'],
        (';', 'pinch', 'identifier', 'for', 'chef'): ['identifier'],
        (';', 'skim', 'identifier', 'for', 'chef'): ['identifier'],
        (';', 'pinch', 'identifier', 'for', 'hungry'): ['identifier'],
        (';', 'skim', 'identifier', 'for', 'hungry'): ['identifier'],
        (';', 'pinch', 'identifier', 'for', 'full'): ['identifier'],
        (';', 'skim', 'identifier', 'for', 'full'): ['identifier'],
        ('identifier', 'pinch', ';', 'for', 'chef'): ['+=', '-='],
        ('identifier', 'skim', ';', 'for', 'chef'): ['+=', '-='],
        ('identifier', 'pinch', ';', 'for', 'hungry'): ['+=', '-='],
        ('identifier', 'skim', ';', 'for', 'hungry'): ['+=', '-='],
        ('identifier', 'pinch', ';', 'for', 'full'): ['+=', '-='],
        ('identifier', 'skim', ';', 'for', 'full'): ['+=', '-='],
        ('+=', 'pinch', 'for'): ['identifier', 'pinchliterals', 'nepinch', 'skimliterals', 'neskim'],
        ('-=', 'pinch', 'for'): ['identifier', 'pinchliterals', 'nepinch', 'skimliterals', 'neskim'],
        ('+=', 'skim', 'for'): ['identifier', 'pinchliterals', 'nepinch', 'skimliterals', 'neskim'],
        ('-=', 'skim', 'for'): ['identifier', 'pinchliterals', 'nepinch', 'skimliterals', 'neskim'],
        #('identifier', 'pinch', '+='): ['sss'],
        #...
        
        # Flip (switch) initialization
        'flip': ['('],  # flip must be followed by (
        ('(', 'flip'): ['identifier'],  # only identifier can be evaluated in flip
        ('identifier', 'flip'): [')'],  # must close parenthesis after identifier
        (')', 'flip'): ['{'],  # must open block after flip condition
        ('{', 'flip'): ['case', 'default'],  # after opening flip block, expect case or default

        # Case statements
        'case': ['pastaliterals', 'pinchliterals', 'nepinch', 'skimliterals', 'neskim'],  # case must be followed by a literal
        ('pastaliterals', 'case'): [':'],
        ('pinchliterals', 'case'): [':'],
        ('nepinch', 'case'): [':'],
        ('skimliterals', 'case'): [':'],
        ('neskim', 'case'): [':'],
        (':', 'case'): ['taste', 'make', 'serve', 'for', 'simmer', 'identifier', 'spit', 'case', 'default'],  # after case:, allow statements or another case/default

        # Default statement
        'default': [':'],  # default must be followed by :
        (':', 'default'): ['taste', 'make', 'serve', 'for', 'simmer', 'identifier', 'spit'],  # after default:, allow statements

        # Breaks
        ('spit', 'case'): [';'],  # spit must be followed by ;
        ('spit', 'default'): [';'],
        (';', 'spit', 'case'): ['case', 'default', '}'],  #
        (';', 'spit', 'default'): ['}'],  #

        # End of flip block
        ('}', 'flip'): ['taste', 'make', 'serve', 'for', 'simmer', 'identifier', 'spit'],  # after closing flip, allow normal statements
        
        # Add rules for program end
        '}': ['takeout'],  # After the last closing brace, expect 'takeout'
        'takeout': [], 
    }
    
    def __init__(self):
        self.pg = ParserGenerator(
            # List of token names (same as before)
            ['DINEIN', 'TAKEOUT', 'CHEF', 'PINCH', 'DISH', 'LPAREN', 'RPAREN', 
             'LBRACE', 'RBRACE', 'IDENTIFIER', 'SEMI', 'PASTA', 'SKIM', 
             'BOOL', 'RECIPE', 'COMMA', 'EQUALS', 'PINCHLITERALS', 'SKIMLITERALS',
             'PASTALITERALS', 'YUM', 'BLEH', 'FULL', 'HUNGRY', 'MAKE', 'SERVE',
             'TASTE', 'ELIF', 'MIX', 'FLIP', 'CASE', 'DEFAULT', 'CHOP', 'FOR',
             'SIMMER', 'KEEPMIX', 'SPIT', 'PLUS', 'MINUS', 'MUL', 'DIV', 'MOD',
             'EQ', 'NE', 'LT', 'GT', 'LE', 'GE', 'AND', 'OR', 'NOT', 'PLUSPLUS',
             'MINUSMINUS', 'PLUSEQ', 'MINUSEQ', 'MULEQ', 'DIVEQ', 'MODEQ',
             'LBRACKET', 'RBRACKET'],
            precedence=[
                ('left', ['OR']),
                ('left', ['AND']),
                ('left', ['EQ', 'NE']),
                ('left', ['LT', 'GT', 'LE', 'GE']),
                ('left', ['PLUS', 'MINUS']),
                ('left', ['MUL', 'DIV', 'MOD']),
                ('right', ['NOT']),
            ]
        )
        self.define_rules()

    def define_rules(self):
        # Previous rules remain the same...

        # Recipe Array Elements
        @self.pg.production('recipe_size : IDENTIFIER LBRACKET PINCHLITERALS RBRACKET')
        def recipe_size(p):
            return ('recipe_size', p[0], p[2])

        @self.pg.production('pinch_elements : EQUALS LBRACE PINCHLITERALS pinch_elementtail RBRACE')
        @self.pg.production('pinch_elements : ')
        def pinch_elements(p):
            if not p:
                return None
            return ('pinch_elements', p[2], p[3])

        @self.pg.production('pinch_elementtail : COMMA PINCHLITERALS pinch_elementtail')
        @self.pg.production('pinch_elementtail : ')
        def pinch_elementtail(p):
            if not p:
                return None
            return ('pinch_elementtail', p[1], p[2])

        # Similar rules for skim_elements and pasta_elements...

        # Expression Rules
        @self.pg.production('expression : negate_op operand operator negate_op operand more_expression')
        @self.pg.production('expression : LPAREN negate_op operand operator negate_op operand more_expression RPAREN')
        def expression(p):
            if len(p) == 6:
                return ('expression', p[0], p[1], p[2], p[3], p[4], p[5])
            return ('expression_paren', p[1], p[2], p[3], p[4], p[5], p[6])

        @self.pg.production('more_expression : operator negate_op operand more_expression')
        @self.pg.production('more_expression : ')
        def more_expression(p):
            if not p:
                return None
            return ('more_expression', p[0], p[1], p[2], p[3])

        # Operators
        @self.pg.production('operator : arith_operator')
        @self.pg.production('operator : relational_operator')
        @self.pg.production('operator : logical_operator')
        def operator(p):
            return ('operator', p[0])

        @self.pg.production('arith_operator : PLUS')
        @self.pg.production('arith_operator : MINUS')
        @self.pg.production('arith_operator : MUL')
        @self.pg.production('arith_operator : DIV')
        @self.pg.production('arith_operator : MOD')
        def arith_operator(p):
            return ('arith_operator', p[0])

        # Conditional Statements
        @self.pg.production('conditional_statement : taste_statement')
        @self.pg.production('conditional_statement : flip_statement')
        def conditional_statement(p):
            return ('conditional', p[0])

        @self.pg.production('taste_statement : TASTE LPAREN condition RPAREN LBRACE statements RBRACE conditional_tail')
        def taste_statement(p):
            return ('taste', p[2], p[5], p[7])

        @self.pg.production('conditional_tail : ELIF LPAREN condition RPAREN LBRACE statements RBRACE conditional_tail')
        @self.pg.production('conditional_tail : MIX LBRACE statements RBRACE')
        @self.pg.production('conditional_tail : ')
        def conditional_tail(p):
            if not p:
                return None
            if p[0].name == 'ELIF':
                return ('elif', p[2], p[5], p[7])
            return ('mix', p[2])

        # Loop Statements
        @self.pg.production('looping_statement : for_statements')
        @self.pg.production('looping_statement : simmer_statements')
        @self.pg.production('looping_statement : keepmix_statement')
        def looping_statement(p):
            return ('loop', p[0])

        @self.pg.production('for_statements : FOR for_initial LBRACE statements RBRACE')
        def for_statements(p):
            return ('for', p[1], p[3])

        @self.pg.production('for_initial : LPAREN for_initialize SEMICOLON condition SEMICOLON for_iterate RPAREN')
        def for_initial(p):
            return ('for_initial', p[1], p[3], p[5])

        @self.pg.production('for_initialize : PINCH IDENTIFIER EQUALS PINCHLITERALS')
        def for_initialize(p):
            return ('for_init', p[1], p[3])

        # Input/Output Statements
        @self.pg.production('input_statement : MAKE LPAREN input_field RPAREN')
        def input_statement(p):
            return ('input', p[2])

        @self.pg.production('input_field : IDENTIFIER')
        @self.pg.production('input_field : access_element')
        def input_field(p):
            return ('input_field', p[0])

        @self.pg.production('output_statement : SERVE LPAREN output_field RPAREN')
        def output_statement(p):
            return ('output', p[2])

        @self.pg.production('output_field : output output_tail')
        def output_field(p):
            return ('output_field', p[0], p[1])

        # Unary Statements
        @self.pg.production('unary_statements : pre_unary')
        @self.pg.production('unary_statements : post_unary')
        def unary_statements(p):
            return ('unary', p[0])

        @self.pg.production('pre_unary : unary_operator IDENTIFIER')
        @self.pg.production('pre_unary : LPAREN unary_operator IDENTIFIER RPAREN')
        def pre_unary(p):
            if len(p) == 2:
                return ('pre_unary', p[0], p[1])
            return ('pre_unary_paren', p[1], p[2])

        # Error handling remains the same...

    def get_parser(self):
        return self.pg.build()
        
    def _add_productions(self):
        @self.pg.production('program : dinein chef pinch dish  takeout')
        def program(p):
            print("parsing program")
#from lexical import tokens
#from syntax.lexer import lexer
from rply import ParserGenerator