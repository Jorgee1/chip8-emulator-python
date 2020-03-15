"""
    Tokens

    SYS - Not used
    CLS
    
    LD
    RND
    DRW

    PC movement:
        JP
        CALL
        SE
        SNE
        RET

    Keyboard:
        SKP
        SKNP

    Aritmetic:
        ADD
        SUB
        AND
        OR
        XOR
        SHR
        SUBN
        SHL

    Registers:
        I
        Vx
        DT
        ST

    Special Chars:
        F
        B
        K
"""
import re

TOKEN_NUMBER        = 'NUMBER'
TOKEN_COMMAND       = 'COMMAND'
TOKEN_REGISTER      = 'REGISTER'
TOKEN_END           = 'END'
TOKEN_COMA          = 'COMA'
TOKEN_LABEL         = 'LABEL'

# General
TOKEN_COMMAND_CLS   = 'CLS'
TOKEN_COMMAND_RND   = 'RND'
TOKEN_COMMAND_DRAW  = 'DRW'
TOKEN_COMMAND_LOAD  = 'LD'

# Keyboard
TOKEN_COMMAND_SKP   = 'SKP'
TOKEN_COMMAND_SKNP  = 'SKNP'

# PC Movement
TOKEN_COMMAND_JP    = 'JP'
TOKEN_COMMAND_CALL  = 'CALL'
TOKEN_COMMAND_SE    = 'SE'
TOKEN_COMMAND_SNE   = 'SNE'
TOKEN_COMMAND_RET   = 'RET'

# Operators
TOKEN_COMMAND_ADD   = 'ADD'
TOKEN_COMMAND_SUB   = 'SUB'
TOKEN_COMMAND_AND   = 'AND'
TOKEN_COMMAND_OR    = 'OR'
TOKEN_COMMAND_XOR   = 'XOR'
TOKEN_COMMAND_SHR   = 'SHR'
TOKEN_COMMAND_SUBN  = 'SUBN'
TOKEN_COMMAND_SHL   = 'SHL'

# Registers
TOKEN_REGISTER_I    = 'I'
TOKEN_REGISTER_V    = 'V'
TOKEN_REGISTER_DT   = 'DT'
TOKEN_REGISTER_ST   = 'ST'

# Special Characters
TOKEN_SPECIAL_F     = 'F'
TOKEN_SPECIAL_B     = 'B'
TOKEN_SPECIAL_K     = 'K'

NO_PARM_COMMANDS = [
    TOKEN_COMMAND_CLS,
    TOKEN_COMMAND_RET
]

SINGLE_PARM_COMMANDS = [
    TOKEN_COMMAND_JP,
    TOKEN_COMMAND_CALL
]

COMMANDS = [
    TOKEN_COMMAND_CLS   ,
    TOKEN_COMMAND_RND   ,
    TOKEN_COMMAND_DRAW  ,
    TOKEN_COMMAND_LOAD  ,
    TOKEN_COMMAND_SKP   ,
    TOKEN_COMMAND_SKNP  ,
    TOKEN_COMMAND_JP    ,
    TOKEN_COMMAND_CALL  ,
    TOKEN_COMMAND_SE    ,
    TOKEN_COMMAND_SNE   ,
    TOKEN_COMMAND_ADD   ,
    TOKEN_COMMAND_SUB   ,
    TOKEN_COMMAND_AND   ,
    TOKEN_COMMAND_OR    ,
    TOKEN_COMMAND_XOR   ,
    TOKEN_COMMAND_SHR   ,
    TOKEN_COMMAND_SUBN  ,
    TOKEN_COMMAND_SHL
]

REGISTERS = [
    TOKEN_REGISTER_I,
    TOKEN_REGISTER_V,
    TOKEN_REGISTER_DT,
    TOKEN_REGISTER_ST
]

class Error:
    def __init__(self, error_type, msg):
        self.error_type = error_type
        self.msg = msg

    def __repr__(self):
        return f'{self.error_type}: {self.msg}'

class InvalidToken(Error):
    def __init__(self, token):
        super().__init__('Invalid Token', f'Token "{token}" is not valid')


#######################
# TOKENS
#######################

class Token:
    def __init__(self, token_type, value=None):
        self.token_type = token_type
        self.value= value

    def __repr__(self):

        if self.value:
            return f'TOKEN[{self.token_type}:{self.value}]'
        else:
            return f'TOKEN[{self.token_type}]'

#######################
# LEXER
#######################

"""
    class Lexer:
        def __init__(self, text_line):
            self.text_line  = text_line
            self.max_index = len(text_line) - 1
            self.char_index = 0
            self.lexer_sw = True
        
        def next(self):
            if (self.char_index < self.max_index):
                self.char_index += 1
            else:
                self.lexer_sw = False

        def get_char(self):
            if (self.char_index <= self.max_index):
                return self.text_line[self.char_index]
            else:
                return None

        def get_next_char(self):
            next_index = self.char_index + 1
            if (next_index <= self.max_index):
                return self.text_line[next_index]
            else:
                return None

        def compare_char(self, regex_search, char):
            if char:
                if re.search(regex_search, char):
                    return True
                else:
                    return False
            else:
                return False

        def get_word(self, regex_search):
            temp_word = self.get_char()
            while(True):
                next_char = self.get_next_char()
                if self.compare_char(regex_search, next_char):
                    temp_word = temp_word + next_char
                    self.next()
                else:
                    break
            
            return temp_word

        def get_tokens(self):
            tokens = []
            error = None
            while(self.lexer_sw):
                selected_char = self.get_char()
                if self.compare_char('[a-zA-Z]', selected_char):
                    acc_char = self.get_word('[a-zA-Z]')
                    if acc_char in COMMANDS:
                        tokens.append(Token(TOKEN_COMMAND, acc_char))
                    elif acc_char in REGISTER:
                        tokens.append(Token(TOKEN_REGISTER, acc_char))
                    else:
                        #tokens.append(Token(TOKEN_LABEL, acc_char))
                        error = InvalidToken(acc_char)
                        self.lexer_sw = False
                    #print(acc_char)
                elif selected_char == ',':
                    tokens.append(Token(TOKEN_COMA))
                elif self.compare_char('[0-9]', selected_char):
                    acc_char = self.get_word('[0-9]')
                    tokens.append(Token(TOKEN_NUMBER, acc_char))
                    #print(acc_char)
                elif selected_char in ' \n\t':
                    pass
                else:
                    error = InvalidToken(selected_char)
                    self.lexer_sw = False

                self.next()
            tokens.append(Token(TOKEN_END))
            return tokens, error
"""        

class Lexer:
    def __init__(self, code):
        self.reset_lexer(code)
        self.code_to_tokens()

    def reset_lexer(self, code):
        self.tokens = []
        self.code = code
        self.char_nums = len(self.code)
        self.lexer_switch = True
        self.index = 0

    def word_assambly(self, regex_query):
        temp_num = ''
        current_char = self.code[self.index]
        while re.match(regex_query, current_char):
            temp_num = ''.join([temp_num, current_char])
            self.index += 1

            if self.index >= self.char_nums:
                break
            else:
                current_char = self.code[self.index]

        return temp_num

    def code_to_tokens(self):
        while self.lexer_switch:
            current_char = self.code[self.index]
            

            if current_char == ' ':
                self.index += 1

            elif current_char == '\n':
                self.tokens.append(Token(TOKEN_END))
                self.index += 1

            elif current_char == ',':
                self.tokens.append(Token(TOKEN_COMA))
                self.index += 1

            elif re.match(r'\d', current_char):
                temp_num = self.word_assambly(r'\d')
                self.tokens.append(Token(TOKEN_NUMBER, temp_num))

            elif re.match(r'[a-zA-Z]', current_char):
                temp_word = self.word_assambly(r'[a-zA-Z]')
                
                for command in COMMANDS:
                    if temp_word == command:
                        self.tokens.append(Token(command))
                        break
                else:
                    for register in REGISTERS:
                        if temp_word == register:
                            self.tokens.append(Token(register))
                            break
                    else:
                        # Debe tirar error
                        self.lexer_switch = False
                        print('ERROR', temp_word)

            else:
                # Debe tirar error
                self.lexer_switch = False
                print('ERROR', current_char, self.index)

            
            if self.index >= self.char_nums:
                self.lexer_switch = False

    def __repr__(self):
        text = 'LEXER:\n'
        for i, token in enumerate(self.tokens):
            text = ''.join([text, str(i), ':', str(token), '\n'])

        return text


#######################
# PARSER NODES
#######################

class NumberNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'Node({self.value})'

class RegisterNode:
    def __init__(self, register):
        self.register = register

    def __repr__(self):
        return self.register

class VNode:
    def __init__(self, register_index):
        self.register_index = register_index
    
    def __repr__(self):
        return f'V({self.register_index})'


class CommandFactorFactorFactorNode:
    def __init__(self, command, first_factor_node, second_factor_node, third_factor_node):
        self.command = command
        self.first_factor_node = first_factor_node
        self.second_factor_node = second_factor_node
        self.third_factor_node = third_factor_node
    
    def __repr__(self):
        return f'{self.command.value}({self.first_factor_node} - {self.second_factor_node} - {self.third_factor_node})'

class CommandFactorFactorNode:
    def __init__(self, command, first_factor_node, second_factor_node):
        self.command = command
        self.first_factor_node = first_factor_node
        self.second_factor_node = second_factor_node
    
    def __repr__(self):
        return f'{self.command.value}({self.first_factor_node} - {self.second_factor_node})'

class CommandFactorNode:
    def __init__(self, command, factor_node):
        self.command = command
        self.factor_node = factor_node
    
    def __repr__(self):
        return f'{self.command.value}({self.factor_node})'

class CommandNode:
    def __init__(self, command):
        self.command = command
    
    def __repr__(self):
        return f'{self.command.value}'

class CommandFactorNode:
    def __init__(self, command, first_node):
        self.command = command
        self.first_node = first_node
    
    def __repr__(self):
        return f'{self.command.value}({self.first_node} - {self.second_node})'

class CommandNode:
    def __init__(self, command, first_node):
        self.command = command
        self.first_node = first_node
    
    def __repr__(self):
        return f'{self.command.value}({self.first_node})'

#######################
# PARSER
#######################

"""
    class Parser:
        def __init__(self, tokens):
            self.tokens = tokens
            self.token_index = 0
            self.parse_sw = True

        def get_token(self):
            if self.token_index < len(self.tokens):
                token = self.tokens[self.token_index]
                self.token_index += 1
                if self.token_index == len(self.tokens)-1:
                    self.parse_sw = False
                return token
            else:
                self.parse_sw = False
                return None

        def parse(self):
            parse_tree = []
            while(self.parse_sw):

                parse_tree.append(self.statement())

            return parse_tree

        def factor(self):
            current_token = self.get_token()
            if current_token.token_type is TOKEN_NUMBER:
                return NumberNode(current_token)
            elif current_token.token_type is TOKEN_REGISTER:
                if current_token.value is TOKEN_REGISTER_V:
                    v_index = self.get_token()
                    if v_index.token_type is TOKEN_NUMBER:
                        return VNode(v_index)
                    else:
                        print('Error1')
                else:
                    return RegisterNode(current_token)
            else:
                print('Error2')

        def statement(self):
            current_token = self.get_token()
            if current_token.token_type is TOKEN_COMMAND:
                first_factor = self.factor()
                separator_token = self.get_token()
                if separator_token.token_type is TOKEN_COMA:
                    second_factor = self.factor()
                    end_token = self.get_token()
                    if end_token.token_type is TOKEN_END:
                        return CommandFactorFactorNode(current_token, first_factor, second_factor)
                    else:
                        print('Error3')
                else:
                    print('Error4')
            else:
                print('Error5')
"""

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tokens_nums = len(self.tokens)
        self.index = 0
        self.parser_switch = True
        self.tree = []


    def get_token(self):
        token = self.tokens[self.index]
        self.index += 1

        if self.index >= self.tokens_nums:
            self.parser_switch = False

        return token


    def check_next_token(self):
        if self.index + 1 < self.tokens_nums:
            return self.index[self.index + 1]
        else:
            return None

    def node(sel):
        

    def factor(self):
        if check_next_token:
            current_token = self.get_token()
            if current_token.token_type == TOKEN_END:
                return None
            elif current_token.token_type in REGISTERS:
                if current_token.token_type == TOKEN_REGISTER_V:
                    if check_next_token:
                        current_token = self.get_token()
                        if current_token.token_type == TOKEN_NUMBER:

                        else:
                            print('Error')
                            return None
                    else:
                        print('Error')
                        return None
                else:
                    return RegisterNode(current_token)
        else:
            return None

    def build_tree(self):
        while self.parser_switch:
            current_token = self.get_token()

            if self.parser_switch:
                if current_token.token_type in COMMANDS:
                    temp_statemet = None

                    temp_command = current_token

                    first_factor  = self.factor()
                    second_factor = None

                    if first_factor:
                        second_factor = self.factor()

                    if first_factor and second_factor:
                        self.tree.append(CommandFactorFactorNode(temp_command, first_factor, second_factor))
                    elif first_factor:
                        self.tree.append(CommandFactorNode(temp_command, first_factor))
                    else:
                        self.tree.append(CommandNode(temp_command))


                    print(current_token)
                    self.index += 1
                else:
                    print('Error', current_token)
                    self.parser_switch = False
                



"""
    def run(file_name):
        tokens = []
        error_flag = False
        with open(file_name) as file:
            for line in file:
                temp_token, error = Lexer(line).get_tokens()

                if error:
                    error_flag = True
                    print(error)
                else:
                    tokens = tokens + temp_token


        if not error_flag:
            print('Tokens:', tokens)

            parse_tree = Parser(tokens).parse()

            print('Parsing tree:', parse_tree)

    run('test.chip8')
"""


text = ''
with open('test.chip8') as f:
    for line in f:
        text = ''.join([text, line])


lexer = Lexer(text)

parser = Parser(lexer.tokens)

parser.build_tree()

