import os, re


TOKEN_CLEAR   = 'CLS'
TOKEN_RETURN  = 'RET'
TOKEN_JUMP    = 'JP'
TOKEN_CALL    = 'CALL'
TOKEN_SKIP    = 'SE'
TOKEN_NSKIP   = 'SNE'
TOKEN_LOAD    = 'LD'
TOKEN_ADD     = 'ADD'
TOKEN_SUB     = 'SUB'
TOKEN_SHIFTR  = 'SHR'
TOKEN_SHIFTL  = 'SHL'
TOKEN_AND     = 'AND'
TOKEN_OR      = 'OR'
TOKEN_XOR     = 'XOR'
TOKEN_SKIPK   = 'SKP'
TOKEN_NSKIPK  = 'SKNP'
TOKEN_RANDOM  = 'RND'
TOKEN_DRAW    = 'DRW'

TOKEN_REG_V   = 'V'
TOKEN_REG_I   = 'I'
TOKEN_REG_DT  = 'DT'
TOKEN_REG_ST  = 'ST'
TOKEN_REG_B   = 'B'
TOKEN_REG_F   = 'F'

TOKEN_SYMBOL  = 'SYMBOL'
TOKEN_COMA    = ','
TOKEN_DECIMAL = 'DECIMAL'
TOKEN_HEX     = 'HEX'
TOKEN_END     = '\n'


TOKEN_KEYWORDS = [
	TOKEN_CLEAR,
	TOKEN_RETURN,
	TOKEN_JUMP,
	TOKEN_CALL,
	TOKEN_SKIP,
	TOKEN_NSKIP,
	TOKEN_LOAD,
	TOKEN_ADD,
	TOKEN_SUB,
	TOKEN_SHIFTR,
	TOKEN_SHIFTL,
	TOKEN_AND,
	TOKEN_OR,
	TOKEN_XOR,
	TOKEN_SKIPK,
	TOKEN_NSKIPK,
	TOKEN_RANDOM,
	TOKEN_DRAW,
	TOKEN_REG_V,
	TOKEN_REG_I,
	TOKEN_REG_DT,
	TOKEN_REG_ST,
	TOKEN_REG_B,
	TOKEN_REG_F
]


class Token:
	def __init__(self, token_name, value=None):
		self.token_name = token_name
		self.value = value

	def __str__(self):
		print(self.token_name,':',self.value)


class Lexer:
	def __init__(self, text):
		self.text = text
		self.index = 0

	def next_char(self):
		
		self.index += 1

	def tokenize(self):

tokens = []

with open('programs/loads.chip8') as code:
	code_line = 1
	for line in code:
		index = 0
		char_num = len(line)
		while(index < char_num):
			char = line[index]
			if char in [' ', '\t']:
				index += 1
			elif char == TOKEN_COMA:
				tokens.append(char)
				index += 1
			elif char == TOKEN_END:
				tokens.append('END')
				index += 1
			elif char == '$':
				acumulator_token = ''
				index += 1

				while(re.match('[0-9]', line[index])):
					acumulator_token = ''.join([acumulator_token, line[index]])
					index += 1

				tokens.append(':'.join([TOKEN_HEX, acumulator_token]))	

			elif re.match('[0-9]', char):
				print('HI')
				acumulator_token = ''

				while(re.match('[0-9]', line[index])):
					acumulator_token = ''.join([acumulator_token, line[index]])
					index += 1

				tokens.append(':'.join([TOKEN_DECIMAL, acumulator_token]))

			elif re.match('[a-zA-Z]', char):

				acumulator_token = ''

				while(re.match('[a-zA-Z]', line[index])):
					acumulator_token = ''.join([acumulator_token, line[index]])
					index += 1

				print(acumulator_token, index)

				if acumulator_token in TOKEN_KEYWORDS:
					tokens.append(acumulator_token)

			else:
				msg = ''
				for i in range(len(line)):
					if i == index:
						msg = msg + '*' + line[i] + '*'
					else:
						msg = msg + line[i]
				print('Line', code_line, ':', msg)
				break
		code_line += 1




path = 'out/lexer'
file_name = 'lexer_1.chip8.lex'
with open(os.path.join(path, file_name), 'w') as f:
	for i in tokens:
		f.write(str(i) + '\n')



