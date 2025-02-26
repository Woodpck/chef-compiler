from rply import ParserGenerator
from src.syntax.conversion import conversion_dict
# from ast_1 import *
# Remove " . " from ast_1 kapag sa main.py magrun 
# from ast_1 import *

class Parser:

    expected_tokens = {
        None: ['pasta', 'pinch', 'skim', 'bool', 'recipe', 'full', 'hungry', 'chef'],
        # General expected tokens based solely on the current token type
        'chef': ['pinch'],
        # 'pinch': ['dish'],
        ('pinch', 'pinch', 'chef'): ['dish'], # Specific rule when the last reserved word is chef for pinch
        'dish': ['('],
        # '(': [')'],
        ('(', 'dish'): [')'], # Specific rule when the last reserved word is dish for (
        # ')': ['{'],
        (')', 'dish'): ['{'], # Specific rule when the last reserved word is dish for )
        '{': ['pasta', 'pinch', 'skim', 'bool', 'recipe', 'taste', 'make', 'serve', 'for', 'simmer', 'identifier', 'spit'], # dish and full
        # 'spit': ['PINCHLITERAL'],
        ('spit', 'dish'): ['PINCHLITERAL'], # Specific rule when the for spit inside the dish function to be updated with statements...
        # 'PINCHLITERAL': [';'],
        ('PINCHLITERAL', 'spit'): [';'], # Specific rule when the last reserved word is spit for PINCHLITERAL

        # Context-specific expected tokens based on the current token and last reserved word
        # Bali yung mga possible terminals na expected based sa last token and reserved word
        # ('{', 'dish'): ['pasta', 'pinch', 'skim', 'bool', 'recipe', 'spit'],  # Specific rule when the last reserved word is 'dish'

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
        ('=', 'pasta'): ['PASTALITERAL'],
        ('=', 'pinch'): ['PINCHLITERAL', 'NEALITERAL'],
        ('=', 'skim'): ['SKIMLITERAL', 'NEHLITERAL'],
        ('=', 'bool'): ['yum', 'bleh'],
        ('=', 'yum'): ['yum', 'bleh'],
        ('=', 'bleh'): ['yum', 'bleh'],
        ('identifier', 'pasta', ','): ['='],
        ('identifier', 'pinch', ','): ['='],
        ('identifier', 'skim', ','): ['='],
        ('identifier', 'bleh', ','): ['='],
        ('identifier', 'yum', ','): ['='],
        (',', 'pasta', 'PASTALITERAL', '='): ['identifier'],
        (',', 'pinch', 'PINCHLITERAL', '='): ['identifier'],
        (',', 'pinch', 'NEALITERAL', '='): ['identifier'],
        (',', 'skim', 'SKIMLITERAL', '='): ['identifier'],
        (',', 'skim', 'SKIMLITERAL', '='): ['identifier'],
        (',', 'bool', 'bleh', '='): ['identifier'],
        (',', 'bool', 'yum', '='): ['identifier'],
        
        # identifier<recipe element>, <expr>, <pasta_concat>, <func_call>, <type_cast>, <esc_Sequence>
        
        # Variable Initialization to Initialize Tail
        ('PASTALITERAL', 'pasta'): [',', ';'],
        ('PINCHLITERAL', 'pinch'): [',', ';'],
        ('NEALITERAL', 'pinch'): [',', ';'],
        ('SKIMLITERAL', 'skim'): [',', ';'],
        ('NEHLITERAL', 'skim'): [',', ';'],
        ('yum', 'yum'): [',', ';'],
        ('bleh', 'bleh'): [',', ';'],
        (';', 'bleh'): ['pasta', 'pinch', 'skim', 'bool', 'recipe', 'full', 'hungry', 'chef'],
        (';', 'yum'): ['pasta', 'pinch', 'skim', 'bool', 'recipe', 'full', 'hungry', 'chef'],

        # recipe Declaration
        'recipe': ['pasta', 'pinch', 'skim', 'bool'],
        ('identifier', 'pasta', 'recipe'): ['['],
        ('identifier', 'pinch', 'recipe'): ['['],
        ('identifier', 'skim', 'recipe'): ['['],
        ('identifier', 'bool', 'recipe'): ['['],
        '[': ['identifier', 'PINCHLITERAL'],
        ('identifier', 'pasta', '['): [']'],
        ('identifier', 'pinch', '['): [']'],
        ('identifier', 'skim', '['): [']'],
        ('identifier', 'bool', '['): [']'],
        ('PINCHLITERAL', 'pasta', '['): [']'],
        ('PINCHLITERAL', 'pinch', '['): [']'],
        ('PINCHLITERAL', 'skim', '['): [']'],
        ('PINCHLITERAL', 'bool', '['): [']'],
        ']': [';', '='],

        # recipe Initialization
        ('=', 'pasta', ']'): ['{'],
        ('=', 'pinch', ']'): ['{'],
        ('=', 'skim', ']'): ['{'],
        ('=', 'bool', ']'): ['{'],
        ('{', 'pasta', '='): ['PASTALITERAL'],
        ('{', 'pinch', '='): ['PINCHLITERAL', 'NEALITERAL'],
        ('{', 'skim', '='): ['SKIMLITERAL', 'NEHLITERAL'],
        ('{', 'bool', '='): ['BOOLLITERAL'],
        ('PASTALITERAL', 'pasta', '{'): [','],
        ('PINCHLITERAL', 'pinch', '{'): [','],
        ('NEALITERAL', 'pinch', '{'): [','],
        ('SKIMLITERAL', 'skim', '{'): [','],
        ('NEHLITERAL', 'skim', '{'): [','],
        ('bleh', 'bleh', '{'): [','],
        ('yum', 'yum', '{'): [','],
        (',', 'pasta', 'PASTALITERAL'): ['PASTALITERAL'],
        (',', 'pinch', 'PINCHLITERAL'): ['PINCHLITERAL', 'NEALITERAL'],
        (',', 'pinch', 'NEALITERAL'): ['PINCHLITERAL', 'NEALITERAL'],
        (',', 'skim', 'SKIMLITERAL'): ['SKIMLITERAL', 'NEHLITERAL'],
        (',', 'skim', 'SKIMLITERAL'): ['SKIMLITERAL', 'NEHLITERAL'],
        (',', 'bool', 'bleh'): ['bleh', 'yum'],
        (',', 'bool', 'yum'): ['bleh', 'yum'],
        ('PASTALITERAL', 'pasta', ','): [',', '}'],
        ('PINCHLITERAL', 'pinch', ','): [',', '}'],
        ('NEALITERAL', 'pinch', ','): [',', '}'],
        ('SKIMLITERAL', 'skim', ','): [',', '}'],
        ('NEHLITERAL', 'skim', ','): [',', '}'],
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
        ('spit', 'spit'): ['PASTALITERAL', 'PINCHLITERAL', 'NEALITERAL', 'SKIMLITERAL', 'NEHLITERAL', 'bleh', 'yum', 'identifier'],
        # spit [expr, pasta_concat, func_call, type_cast, esc_sequence]
        
        ('PASTALITERAL', 'spit'): [';'],
        ('NEALITERAL', 'spit'): [';'],
        ('SKIMLITERAL', 'spit'): [';'],
        ('NEHLITERAL', 'spit'): [';'],
        ('yum', 'yum', 'spit'): [';'],
        ('bleh', 'bleh', 'spit'): [';'],
        (';', 'spit'): ['}'],
        (';', 'yum', 'full'): ['}'],
        (';', 'bleh', 'full'): ['}'],
        ('}', 'spit'): ['full', 'hungry', 'chef'],

        # hungry Function
        'hungry': ['identifier'],
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
        (';', 'pasta', 'PASTALITERAL', 'hungry'): ['pasta', 'pinch', 'skim', 'bool', 'recipe', 'taste', 'make', 'serve', 'for', 'simmer', 'identifier', '}'],        
        (';', 'pinch', 'PINCHLITERAL', 'hungry'): ['pasta', 'pinch', 'skim', 'bool', 'recipe', 'taste', 'make', 'serve', 'for', 'simmer', 'identifier', '}'], 
        (';', 'pinch', 'NEALITERAL', 'hungry'): ['pasta', 'pinch', 'skim', 'bool', 'recipe', 'taste', 'make', 'serve', 'for', 'simmer', 'identifier', '}'], 
        (';', 'skim', 'SKIMLITERAL', 'hungry'): ['pasta', 'pinch', 'skim', 'bool', 'recipe', 'taste', 'make', 'serve', 'for', 'simmer', 'identifier', '}'], 
        (';', 'skim', 'NEHLITERAL', 'hungry'): ['pasta', 'pinch', 'skim', 'bool', 'recipe', 'taste', 'make', 'serve', 'for', 'simmer', 'identifier', '}'], 
        (';', 'bleh', 'hungry'): ['pasta', 'pinch', 'skim', 'bool', 'recipe', 'taste', 'make', 'serve', 'for', 'simmer', 'identifier', '}'], 
        (';', 'yum', 'hungry'): ['pasta', 'pinch', 'skim', 'bool', 'recipe', 'taste', 'make', 'serve', 'for', 'simmer', 'identifier', '}'], 
        (';', 'pasta', 'hungry'): ['pasta', 'pinch', 'skim', 'bool', 'recipe', 'taste', 'make', 'serve', 'for', 'simmer', 'identifier', '}'],
        (';', 'pinch', 'hungry'): ['pasta', 'pinch', 'skim', 'bool', 'recipe', 'taste', 'make', 'serve', 'for', 'simmer', 'identifier', '}'],
        (';', 'skim', 'hungry'): ['pasta', 'pinch', 'skim', 'bool', 'recipe', 'taste', 'make', 'serve', 'for', 'simmer', 'identifier', '}'],
        #(';', 'pasta', 'hungry'): ['pasta', 'pinch', 'skim', 'bool', 'recipe', 'taste', 'make', 'serve', 'for', 'simmer', 'identifier', '}'],
        # (',', 'PASTALITERAL', '{'): ['sample']
        # ('}', 'pasta', ';', 'PASTALITERAL'): ['full', 'hungry', 'chef..'],
        # closing bracket of void func 


        # chef pinch dish () {
        (';', 'pasta', 'chef'): ['pasta', 'pinch', 'skim', 'bool', 'recipe', 'taste', 'make', 'serve', 'for', 'simmer', 'identifier', 'spit'],
        (';', 'pinch', 'chef'): ['pasta', 'pinch', 'skim', 'bool', 'recipe', 'taste', 'make', 'serve', 'for', 'simmer', 'identifier', 'spit'],
        (';', 'skim', 'chef'): ['pasta', 'pinch', 'skim', 'bool', 'recipe', 'taste', 'make', 'serve', 'for', 'simmer', 'identifier', 'spit'],
        (';', 'bleh', 'chef'): ['pasta', 'pinch', 'skim', 'bool', 'recipe', 'taste', 'make', 'serve', 'for', 'simmer', 'identifier', 'spit'],
        (';', 'yum', 'chef'): ['pasta', 'pinch', 'skim', 'bool', 'recipe', 'taste', 'make', 'serve', 'for', 'simmer', 'identifier', 'spit'],
        ('pinch', 'pinch', 'chef'): ['identifier'],


        # make Stmt
        'make': ['('],
        ('(', 'make'): ['identifier'],
        #('identifier', 'make', '('): [')'],
        ('identifier', 'make'): ['[', ')'],
        ('identifier', 'make', '['): [']'],
        ('PINCHLITERAL', 'make'): [']'],
        (']', 'make'): [')'],   
        (')', 'make'): [';'],   
        (';', 'make'): ['taste', 'make', 'serve', 'for', 'simmer', 'identifier', 'spit'], 
        (';', 'make', 'hungry'): ['taste', 'make', 'serve', 'for', 'simmer', 'identifier', '}'], 

        # serve Stmt
        'serve': ['('],
        ('(', 'serve'): ['identifier', 'PASTALITERAL', 'PINCHLITERAL', 'NEALITERAL', 'SKIMLITERAL', 'NEHLITERAL', 'bleh', 'yum'],
        ('identifier', 'serve'): [')', '~'],
        ('PASTALITERAL', 'serve'): [')', '~'],
        ('PINCHLITERAL', 'serve'): [')', '~'],
        ('NEALITERAL', 'serve'): [')', '~'],
        ('SKIMLITERAL', 'serve'): [')', '~'],
        ('NEHLITERAL', 'serve'): [')', '~'],
        ('bleh', 'bleh', '('): [')', '~'],
        ('yum', 'yum', '('): [')', '~'],
        ('~', 'serve'): ['identifier', 'PASTALITERAL', 'PINCHLITERAL', 'NEALITERAL', 'SKIMLITERAL', 'NEHLITERAL', 'bleh', 'yum'],
        ('~', 'bleh'): ['identifier', 'PASTALITERAL', 'PINCHLITERAL', 'NEALITERAL', 'SKIMLITERAL', 'NEHLITERAL', 'bleh', 'yum'],
        ('~', 'yum'): ['identifier', 'PASTALITERAL', 'PINCHLITERAL', 'NEALITERAL', 'SKIMLITERAL', 'NEHLITERAL', 'bleh', 'yum'],
        ('yum', 'yum', '~'): [')', '~'],
        ('bleh', 'bleh', '~'): [')', '~'],
        (')', 'serve'): [';'],
        (')', 'bleh'): [';'],
        (')', 'yum'): [';'],
        (';', 'serve'): ['taste', 'make', 'serve', 'for', 'simmer', 'identifier', 'spit'], 
        (';', 'serve', 'hungry'): ['taste', 'make', 'serve', 'for', 'simmer', 'identifier', 'spit'],
        (';', 'bleh', 'serve'): ['taste', 'make', 'serve', 'for', 'simmer', 'identifier', 'spit'],
        (';', 'yum', 'serve'): ['taste', 'make', 'serve', 'for', 'simmer', 'identifier', 'spit'],
        (';', 'yum', 'yum'): ['taste', 'make', 'serve', 'for', 'simmer', 'identifier', 'spit'],
        (';', 'yum', 'bleh'): ['taste', 'make', 'serve', 'for', 'simmer', 'identifier', 'spit'],
        (';', 'bleh', 'bleh'): ['taste', 'make', 'serve', 'for', 'simmer', 'identifier', 'spit'],
        
        # for Stmt
        'for': ['('],
        ('(', 'for'): ['pinch', 'skim'],
        ('identifier', 'pinch', 'for'): ['='],
        ('identifier', 'skim', 'for'): ['='],
        ('PINCHLITERAL', 'pinch', 'for'): [';'],
        ('NEALITERAL', 'pinch', 'for'): [';'],
        ('SKIMLITERAL', 'skim', 'for'): [';'],
        ('NEHLITERAL', 'skim', 'for'): [';'],
        (';', 'pinch', 'for'): ['identifier', 'PINCHLITERAL', 'NEALITERAL', 'SKIMLITERAL', 'NEHLITERAL'],
        (';', 'skim', 'for'): ['identifier', 'PINCHLITERAL', 'NEALITERAL', 'SKIMLITERAL', 'NEHLITERAL'],
        ('identifier', 'pinch', ';', 'PINCHLITERAL'): ['<', '>', '<=', '>=', '==', '!='],
        ('identifier', 'pinch', ';', 'NEALITERAL'): ['<', '>', '<=', '>=', '==', '!='],
        ('identifier', 'skim', ';', 'SKIMLITERAL'): ['<', '>', '<=', '>=', '==', '!='],
        ('identifier', 'skim', ';', 'NEHLITERAL'): ['<', '>', '<=', '>=', '==', '!='],
        ('PINCHLITERAL', 'pinch', ';', 'PINCHLITERAL'): ['<', '>', '<=', '>=', '==', '!='],
        ('PINCHLITERAL', 'pinch', ';', 'NEALITERAL'): ['<', '>', '<=', '>=', '==', '!='],
        ('PINCHLITERAL', 'skim', ';', 'SKIMLITERAL'): ['<', '>', '<=', '>=', '==', '!='],
        ('PINCHLITERAL', 'skim', ';', 'NEHLITERAL'): ['<', '>', '<=', '>=', '==', '!='],
        ('NEALITERAL', 'pinch', ';', 'PINCHLITERAL'): ['<', '>', '<=', '>=', '==', '!='],
        ('NEALITERAL', 'pinch', ';', 'NEALITERAL'): ['<', '>', '<=', '>=', '==', '!='],
        ('NEALITERAL', 'skim', ';', 'SKIMLITERAL'): ['<', '>', '<=', '>=', '==', '!='],
        ('NEALITERAL', 'skim', ';', 'NEHLITERAL'): ['<', '>', '<=', '>=', '==', '!='],
        ('SKIMLITERAL', 'pinch', ';', 'PINCHLITERAL'): ['<', '>', '<=', '>=', '==', '!='],
        ('SKIMLITERAL', 'pinch', ';', 'NEALITERAL'): ['<', '>', '<=', '>=', '==', '!='],
        ('SKIMLITERAL', 'skim', ';', 'SKIMLITERAL'): ['<', '>', '<=', '>=', '==', '!='],
        ('SKIMLITERAL', 'skim', ';', 'NEHLITERAL'): ['<', '>', '<=', '>=', '==', '!='],
        ('NEHLITERAL', 'pinch', ';', 'PINCHLITERAL'): ['<', '>', '<=', '>=', '==', '!='],
        ('NEHLITERAL', 'pinch', ';', 'NEALITERAL'): ['<', '>', '<=', '>=', '==', '!='],
        ('NEHLITERAL', 'skim', ';', 'SKIMLITERAL'): ['<', '>', '<=', '>=', '==', '!='],
        ('NEHLITERAL', 'skim', ';', 'NEHLITERAL'): ['<', '>', '<=', '>=', '==', '!='],
        ('<', 'pinch'): ['identifier', 'PINCHLITERAL', 'NEALITERAL', 'SKIMLITERAL', 'NEHLITERAL'],
        ('<', 'skim'): ['identifier', 'PINCHLITERAL', 'NEALITERAL', 'SKIMLITERAL', 'NEHLITERAL'],
        ('>', 'pinch'): ['identifier', 'PINCHLITERAL', 'NEALITERAL', 'SKIMLITERAL', 'NEHLITERAL'],
        ('>', 'skim'): ['identifier', 'PINCHLITERAL', 'NEALITERAL', 'SKIMLITERAL', 'NEHLITERAL'],
        ('<=', 'pinch'): ['identifier', 'PINCHLITERAL', 'NEALITERAL', 'SKIMLITERAL', 'NEHLITERAL'],
        ('<=', 'skim'): ['identifier', 'PINCHLITERAL', 'NEALITERAL', 'SKIMLITERAL', 'NEHLITERAL'],
        ('>=', 'pinch'): ['identifier', 'PINCHLITERAL', 'NEALITERAL', 'SKIMLITERAL', 'NEHLITERAL'],
        ('>=', 'skim'): ['identifier', 'PINCHLITERAL', 'NEALITERAL', 'SKIMLITERAL', 'NEHLITERAL'],
        ('==', 'pinch'): ['identifier', 'PINCHLITERAL', 'NEALITERAL', 'SKIMLITERAL', 'NEHLITERAL'],
        ('==', 'skim'): ['identifier', 'PINCHLITERAL', 'NEALITERAL', 'SKIMLITERAL', 'NEHLITERAL'],
        ('!=', 'pinch'): ['identifier', 'PINCHLITERAL', 'NEALITERAL', 'SKIMLITERAL', 'NEHLITERAL'],
        ('!=', 'skim'): ['identifier', 'PINCHLITERAL', 'NEALITERAL', 'SKIMLITERAL', 'NEHLITERAL'],
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
        ('+=', 'pinch', 'for'): ['identifier', 'PINCHLITERAL', 'NEALITERAL', 'SKIMLITERAL', 'NEHLITERAL'],
        ('-=', 'pinch', 'for'): ['identifier', 'PINCHLITERAL', 'NEALITERAL', 'SKIMLITERAL', 'NEHLITERAL'],
        ('+=', 'skim', 'for'): ['identifier', 'PINCHLITERAL', 'NEALITERAL', 'SKIMLITERAL', 'NEHLITERAL'],
        ('-=', 'skim', 'for'): ['identifier', 'PINCHLITERAL', 'NEALITERAL', 'SKIMLITERAL', 'NEHLITERAL'],
        #('identifier', 'pinch', '+='): ['sss'],

        #...
      
    }

    def __init__(self, lexer):
        self.lexer = lexer
        self.pg = ParserGenerator(
            ['LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET', 'LBRACE', 'RBRACE', 'SEMI','COLON', 'COMMA', 'UNDERSCORE', 'TILDE', 'BACKSLASH',
             'IDENTIFIER', 'PINCH', 'PASTA', 'SKIM', 'BOOL', 'MAKE', 'SERVE', 'TASTE', 'MIX', 'ELIF', 'FLIP', 'CASE', 'DEFAULT',
             'FOR', 'SIMMER', 'CHOP', 'SPIT', 'YUM', 'BLEH', 'DISH', 'HUNGRY', 'CHEF', 'FULL', 'RECIPE',
             'PINCHLITERAL','BOOLLITERAL','PASTALITERAL', 'SKIMLITERAL', 'NEALITERAL', 'NEHLITERAL',
             'EQUALS', 'PLUSEQUAL', 'MINUSEQUAL', 'STAREQUAL', 'SLASHEQUAL', 'PERCENTEQUAL', 
             'PLUS', 'MINUS', 'STAR', 'SLASH', 'PERCENT', 'LT', 'GT', 'EQ', 'NEQ', 'LTE', 'GTE', 
             'AND', 'OR', 'NOT', 'TAB', 'NEWLINE', 'DOUBLE_QUOTE']
        )

        self.pg.precedence = [
            ('left', ['OR']),
            ('left', ['AND']),
            ('right', ['NOT']),
            ('left', ['LT', 'LTE', 'GT', 'GTE', 'EQ', 'NEQ']),
            ('left', ['PLUS', 'MINUS']),
            ('left', ['STAR', 'SLASH', 'PERCENT']),
            ('left', ['TILDE']),
            ('right', ['EQUALS', 'PLUSEQUAL', 'MINUSEQUAL', 'STAREQUAL', 'SLASHEQUAL', 'PERCENTEQUAL']),
        ]

        self._add_productions()
        self.parser = self.pg.build()

        # self.parse()

    def parse(self, text):
        tokens = self.lexer.lex(text)
        try:
            self.parser.parse(tokens)
            print(f"No syntax error/s")
            return (f"No syntax error/s")
        except ValueError as e:
            print(f"Syntax error: {str(e)}")
            return (f"{str(e)}")
        
    def _add_productions(self):
        @self.pg.production('program : global_declarations functions CHEF PINCH DISH LPAREN RPAREN LBRACE body SPIT PINCHLITERAL SEMI RBRACE')
        def program(p):
            print("parsing program")

        @self.pg.production('global_declarations : declarations')
        def global_declarations(p):
            print("parsing global_declarations")
            

        @self.pg.production('declarations : declares declarations')
        @self.pg.production('declarations : ')
        def declarations(p):
            print("parsing declarations")
            

        @self.pg.production('declares : variable_decls')
        @self.pg.production('declares : stmt')
        @self.pg.production('declares : recipe_decl')
        @self.pg.production('declares : recipe_init')
        @self.pg.production('declares : ')
        def declares(p):
            print("parsing declares")
        

        @self.pg.production('variable_decls : variable_decl')
        @self.pg.production('variable_decls : variable_initialization')
        def variable_decls(p):
            print("parsing variable_decls")
            

        @self.pg.production('variable_decl : data_type IDENTIFIER decl_tail SEMI')
        def variable_decl(p):
            print("parsing variable_decl")


        @self.pg.production('decl_tail : COMMA IDENTIFIER decl_tail')
        @self.pg.production('decl_tail : ')
        def decl_tail(p):
            print("parsing decl_tail")


        @self.pg.production('variable_initialization : data_type IDENTIFIER EQUALS value initialize_tail SEMI')
        def variable_initialization(p):
            print("parsing variable_initialization")


        @self.pg.production('initialize_tail : COMMA IDENTIFIER EQUALS value initialize_tail')
        @self.pg.production('initialize_tail : ')
        def initialize_tail(p):
            print("parsing initialize_tail")

        @self.pg.production('data_type : PINCH')
        @self.pg.production('data_type : PASTA') 
        @self.pg.production('data_type : SKIM')
        @self.pg.production('data_type : BOOL')
        def data_type(p):
            print("parsing data_type")


        @self.pg.production('recipe_decl : RECIPE data_type IDENTIFIER LBRACKET PINCHLITERAL RBRACKET SEMI')
        def recipe_decl(p):
            print("parsing recipe_decl")


        @self.pg.production('recipe_init : RECIPE data_type IDENTIFIER LBRACKET PINCHLITERAL RBRACKET EQUALS LBRACE recipe_elements RBRACE SEMI')
        def recipe_init(p):
            print("parsing recipe_init")

        @self.pg.production('recipe_elements : value COMMA recipe_elements')
        @self.pg.production('recipe_elements : value')
        def recipe_elements(p):
            print("parsing recipe_elements")

        @self.pg.production('value : identifier LBRACKET expr RBRACKET')
        def value_recipe_access(p):
            print("parsing value_recipe_access")


        @self.pg.production('value : identifier')
        @self.pg.production('value : literal')
        @self.pg.production('value : expr')
        # @self.pg.production('value : pasta_concat')
        @self.pg.production('value : func_call')
        @self.pg.production('value : type_cast')
        @self.pg.production('value : esc_sequence')
        @self.pg.production('value : bool_literal')
        def value(p):
            print("parsing value")


        @self.pg.production('type_cast : data_type LPAREN value RPAREN')
        def type_cast(p):
            print("parsing type_cast")


        @self.pg.production('literal : PINCHLITERAL')
        @self.pg.production('literal : SKIMLITERAL')
        @self.pg.production('literal : NEALITERAL')
        @self.pg.production('literal : NEHLITERAL')
        @self.pg.production('literal : PASTALITERAL')
        def literal(p):
            print("parsing literal")


        @self.pg.production('identifier : IDENTIFIER')
        def identifier(p):
            print("parsing identifier")


        @self.pg.production('functions : function_definition functions')
        @self.pg.production('functions : ')
        def functions(p):
            print("parsing functions")


        @self.pg.production('function_definition : FULL data_type IDENTIFIER LPAREN parameters RPAREN LBRACE full_body RBRACE')
        @self.pg.production('function_definition : HUNGRY IDENTIFIER LPAREN parameters RPAREN LBRACE voidbody RBRACE')
        def function_definition(p):
            print("parsing function_definition")

            
        @self.pg.production('full_body : declarations stmts SPIT value SEMI')
        @self.pg.production('full_body : declarations SPIT value SEMI')
        def full_body(p):
            print("parsing full_body")

    
        @self.pg.production('func_call : IDENTIFIER LPAREN args RPAREN')
        def func_call(p):
            print("parsing func_call")

        @self.pg.production('parameters : param parameters_tail')
        @self.pg.production('parameters : ')
        def parameters(p):
            print("parsing parameters")


        @self.pg.production('parameters_tail : COMMA param parameters_tail')
        @self.pg.production('parameters_tail : ')
        def parameters_tail(p):
            print("parsing parameters_tail")


        @self.pg.production('param : data_type IDENTIFIER')
        def param(p):
            pass
    

        @self.pg.production('args : value args_tail')
        @self.pg.production('args : ')
        def args(p):
            print("parsing args")


        @self.pg.production('args_tail : COMMA value args_tail')
        @self.pg.production('args_tail : ')
        def args_tail(p):
            print("parsing args_tail")


        @self.pg.production('body : declarations stmts')
        def body(p):
            print("parsing body")


        @self.pg.production('voidbody : declarations void_stmts')
        def voidbody(p):
            print("parsing voidbody")

        @self.pg.production('void_stmts : void_stmt void_stmts')
        @self.pg.production('void_stmts : ')
        def void_stmts(p):
            print("parsing void_stmts")


        @self.pg.production('void_stmt : make_stmt SEMI')
        @self.pg.production('void_stmt : serve_stmt SEMI')
        @self.pg.production('void_stmt : void_for_stmt')
        @self.pg.production('void_stmt : void_simmer_stmt')
        @self.pg.production('void_stmt : assignment_stmt SEMI')
        @self.pg.production('void_stmt : func_call SEMI')
        @self.pg.production('void_stmt : break_stmt SEMI')
        # @self.pg.production('void_stmt : continue_stmt SEMI')
        def void_stmt(p):
            print("parsing void_stmt")


        @self.pg.production('stmts : stmt stmts')
        @self.pg.production('stmts : ')
        def stmts(p):
            print("parsing stmts")


        @self.pg.production('stmt : make_stmt SEMI')
        @self.pg.production('stmt : serve_stmt SEMI')
        @self.pg.production('stmt : for_stmt')
        @self.pg.production('stmt : simmer_stmt')
        @self.pg.production('stmt : assignment_stmt SEMI')
        @self.pg.production('stmt : func_call SEMI')
        @self.pg.production('stmt : pasta_concat SEMI')
        @self.pg.production('stmt : bool_expr SEMI')
        @self.pg.production('stmt : taste_stmt')  # Add this line to allow taste_stmt as stmt
        @self.pg.production('stmt : break_stmt SEMI')
        # @self.pg.production('stmt : continue_stmt SEMI')
        def stmt(p):
            print("parsing stmt")


        @self.pg.production('break_stmt : CHOP')
        def break_stmt(p):
            print("parsing break_stmt")


        # @self.pg.production('continue_stmt : GORA')
        # def continue_stmt(p):
        #     print("parsing continue_stmt")


        @self.pg.production('next_stmts : dish_stmt next_stmts')
        @self.pg.production('next_stmts : ')
        def next_stmts(p):
            print("parsing next_stmts")


        @self.pg.production('spit_stmt : SPIT value SEMI')
        def spit_stmt(p):
            print("parsing spit_stmt")

        @self.pg.production('dish_stmt : stmt')
        @self.pg.production('dish_stmt : taste_stmt')
        def dish_stmt(p):
            print("parsing dish_stmt")

        @self.pg.production('make_stmt : MAKE LPAREN IDENTIFIER RPAREN')
        def make_stmt(p):
            print("parsing make_stmt")

        @self.pg.production('serve_stmt : SERVE LPAREN pasta_concat RPAREN')
        @self.pg.production('serve_stmt : SERVE LPAREN value RPAREN')
        def serve_stmt(p):
            print("parsing serve_stmt")

        @self.pg.production('for_stmt : FOR LPAREN PINCH IDENTIFIER EQUALS value SEMI rel_expr SEMI assignment_stmt RPAREN LBRACE stmts RBRACE')
        def for_stmt(p):
            print("parsing for_stmt")


        @self.pg.production('simmer_stmt : SIMMER LPAREN condition RPAREN LBRACE stmts RBRACE')
        def simmer_stmt(p):
            print("parsing simmer_stmt")


        @self.pg.production('assignment_stmt : IDENTIFIER LBRACKET expr RBRACKET EQUALS value')
        @self.pg.production('assignment_stmt : IDENTIFIER EQUALS value')
        @self.pg.production('assignment_stmt : IDENTIFIER PLUSEQUAL value')
        @self.pg.production('assignment_stmt : IDENTIFIER MINUSEQUAL value')
        @self.pg.production('assignment_stmt : IDENTIFIER STAREQUAL value')
        @self.pg.production('assignment_stmt : IDENTIFIER SLASHEQUAL value')
        @self.pg.production('assignment_stmt : IDENTIFIER PERCENTEQUAL value')
        @self.pg.production('assignment_stmt : IDENTIFIER COMMA identifier_list EQUALS func_call')
        def assignment_stmt(p):
            print("parsing assignment_stmt")

        @self.pg.production('identifier_list : IDENTIFIER COMMA identifier_list')
        @self.pg.production('identifier_list : IDENTIFIER')
        def identifier_list(p):
            pass

        @self.pg.production('expr : bool_expr')
        @self.pg.production('expr : term expr_tail')
        def expr(p):
            print("parsing expr")



        @self.pg.production('expr_tail : PLUS term expr_tail')
        @self.pg.production('expr_tail : MINUS term expr_tail')
        @self.pg.production('expr_tail : ')
        def expr_tail(p):
            print("parsing expr_tail")


        @self.pg.production('term : factor term_tail')
        def term(p):
            print("parsing term")


        @self.pg.production('term_tail : STAR factor term_tail')
        @self.pg.production('term_tail : SLASH factor term_tail')
        @self.pg.production('term_tail : PERCENT factor term_tail')
        @self.pg.production('term_tail : ')
        def term_tail(p):
            print("parsing term_tail")



        @self.pg.production('factor : NOT factor')
        @self.pg.production('factor : IDENTIFIER LBRACKET expr RBRACKET')
        @self.pg.production('factor : IDENTIFIER')
        @self.pg.production('factor : PINCHLITERAL')
        @self.pg.production('factor : SKIMLITERAL')
        @self.pg.production('factor : PASTALITERAL')
        @self.pg.production('factor : bool_literal')
        @self.pg.production('factor : LPAREN expr RPAREN')
        @self.pg.production('factor : data_type LPAREN factor RPAREN')
        def factor(p):
            print("parsing factor")



        @self.pg.production('taste_stmt : TASTE LPAREN condition RPAREN LBRACE stmts RBRACE mul_elif')
        def taste_stmt(p):
            print("parsing taste_stmt")

        @self.pg.production('mul_elif : elif_stmt mul_elif')
        @self.pg.production('mul_elif : mix_stmt')
        @self.pg.production('mul_elif : ')
        def mul_elif(p):
            print("parsing mul_elif")


        @self.pg.production('elif_stmt : ELIF LPAREN condition RPAREN LBRACE stmts RBRACE')
        def elif_stmt(p):
            print("parsing elif_stmt")


        @self.pg.production('mix_stmt : MIX LBRACE stmts RBRACE')
        def mix_stmt(p):
            print("parsing mix_stmt")


        @self.pg.production('condition : expr')
        def condition(p):
            print("parsing condition")


        @self.pg.production('bool_expr : rel_expr')
        @self.pg.production('bool_expr : bool_expr AND bool_expr')
        @self.pg.production('bool_expr : NOT bool_expr')
        @self.pg.production('bool_expr : bool_expr OR bool_expr')
        def bool_expr(p):
            print("parsing bool_expr")



        @self.pg.production('rel_expr : expr rel_op expr')
        def rel_expr(p):
            print("parsing rel_expr")

        # Relational operators
        @self.pg.production('rel_op : LT')
        @self.pg.production('rel_op : GT')
        @self.pg.production('rel_op : LTE')
        @self.pg.production('rel_op : GTE')
        @self.pg.production('rel_op : EQ')
        @self.pg.production('rel_op : NEQ')
        def rel_op(p):
            print("parsing rel_op")


        @self.pg.production('void_for_stmt : FOR LPAREN PINCH IDENTIFIER EQUALS value SEMI rel_expr SEMI assignment_stmt RPAREN LBRACE void_stmts RBRACE')
        def void_for_stmt(p):
            print("parsing void_for_stmt")



        @self.pg.production('void_simmer_stmt : SIMMER LPAREN rel_expr RPAREN LBRACE void_stmts RBRACE')
        def void_simmer_stmt(p):
            print("parsing void_simmer_stmt")


        @self.pg.production('pasta_concat : value TILDE pasta_concat')
        @self.pg.production('pasta_concat : value TILDE value')
        def pasta_concat(p):
            print("parsing pasta_concat")


        @self.pg.production('pasta_operand : IDENTIFIER')
        @self.pg.production('pasta_operand : PASTALITERAL')
        def pasta_operand(p):
            print("parsing pasta_operand")


        @self.pg.production('bool_literal : YUM')
        @self.pg.production('bool_literal : BLEH')
        def bool_literal(p):
            print("parsing bool_literal")


        @self.pg.production('esc_sequence : TAB')
        @self.pg.production('esc_sequence : NEWLINE')
        @self.pg.production('esc_sequence : BACKSLASH')
        @self.pg.production('esc_sequence : DOUBLE_QUOTE')
        def esc_sequence(p):
            print("parsing esc_sequence")


        
        @self.pg.error
        def error_handle(token):
            # Use lexer to access the previous token in case of an error
            function = self.lexer.get_function()
            last_reserved_word = self.lexer.get_last_reserved_keyword()
            previous_token = self.lexer.get_previous_token()
            seclast_reserved_keyword = self.lexer.get_seclast_reserved_keyword() # second to the last reserved keyword
            secprev_token = self.lexer.get_secprevious_token() # second to the previous token

            if token.gettokentype() == '$end':
                raise ValueError("Syntax error: Unexpected end of input\n")
            else:            
                expected = list_expected_tokens(previous_token, last_reserved_word, seclast_reserved_keyword, secprev_token, function)

                # error_message = f"Function: {function.getstr()}\n2nd prev Token: {secprev_token.getstr()}\nPrev Token: {previous_token.getstr()}\nLast RW: {last_reserved_word.getstr()}\n2nd prev RW: {seclast_reserved_keyword.getstr()}\nUnexpected token: {[token.getstr()]} at line number {token.getsourcepos().lineno}\nExpected Token\s: {expected}\n"
                
                error_message = f"Unexpected token: {[token.getstr()]} at line number {token.getsourcepos().lineno}\nExpected Token\s: {expected}\n"
                raise ValueError(error_message)
        
        # Function to convert tokens
        def convert_token(token_type):
            return conversion_dict.get(token_type, token_type)
        
        def list_expected_tokens(token, last_reserved_word, seclast_reserved_word, secprev_token, function):

            token_type = convert_token(token.gettokentype()) if token else None
            last_reserved_word = convert_token(last_reserved_word.gettokentype()) if last_reserved_word else None
            seclast_reserved_word = convert_token(seclast_reserved_word.gettokentype()) if seclast_reserved_word else None
            secprev_token = convert_token(secprev_token.gettokentype()) if secprev_token else None
            function = convert_token(function.gettokentype()) if function else None

            # Context Keys
            full_context = (token_type, last_reserved_word, secprev_token, seclast_reserved_word, function)
            four_context = (token_type, last_reserved_word, secprev_token, seclast_reserved_word)
            three_context = (token_type, last_reserved_word, secprev_token)
            three_context_function = (token_type, last_reserved_word, function)
            three_context_alt = (token_type, last_reserved_word, seclast_reserved_word)
            two_context = (token_type, last_reserved_word)

            # context_key = (token_type, last_reserved_word.gettokentype()) if last_reserved_word else token_type

            # Fetch expected tokens based on the token type or the context-specific key
            # return self.expected_tokens.get(context_key, self.expected_tokens.get(token_type, ['unknown']))

            return self.expected_tokens.get(
                full_context,
                self.expected_tokens.get(
                    four_context,
                    self.expected_tokens.get(
                        three_context,
                        self.expected_tokens.get(
                                three_context_function,
                                self.expected_tokens.get(
                                    three_context_alt,
                                    self.expected_tokens.get(
                                        two_context,
                                        self.expected_tokens.get(
                                            token_type,
                                            ['unkown'],
                                    )
                                )
                            )
                        )    
                    )
                )
            )

            
# from lexical_analyzer import tokens
from rply import ParserGenerator

    # def get_parser(self):
    #     return self.pg.build()
