"""
    Tokens

    SYS - Not used
    CLS
    RET
    LD
    RND
    DRW

    PC movement:
        JP
        CALL
        SE
        SNE

    Keyboard:
        SKP
        SKNP

    Aritmetic:
        ADD
        OR
        AND
        XOR
        SUB
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

TOKEN_NUMBER      = 'NUMBER'
TOKEN_COMMAND     = 'COMMAND'
TOKEN_REGISTER    = 'REGISTER'
TOKEN_END         = 'END'
TOKEN_COMA        = 'COMA'
TOKEN_LABEL       = 'LABEL'
TOKEN_LOAD        = 'LD'
TOKEN_ADD         = 'ADD'
TOKEN_SUB         = 'SUB'
TOKEN_REGISTER_I  = 'I'
TOKEN_REGISTER_V  = 'V'
TOKEN_REGISTER_DT = 'DT'
TOKEN_REGISTER_ST = 'ST'

COMMANDS = [
    TOKEN_LOAD,
    TOKEN_ADD,
    TOKEN_SUB
]

REGISTER = [
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


class Token:
    def __init__(self, token_type, value=None):
        self.token_type = token_type
        self.value= value

    def __repr__(self):

        if self.value:
            return f'{self.token_type}:{self.value}'
        else:
            return f'{self.token_type}'

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
            

class NumberNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return self.value

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

class CommandFactorFactorNode:
    def __init__(self, command, first_node, second_node):
        self.command = command
        self.first_node = first_node
        self.second_node = second_node
    
    def __repr__(self):
        return f'{self.command.value}({self.first_node} - {self.second_node})'


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
