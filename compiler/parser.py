import os, json

path = 'out/lexer'
file_name = 'lexer_1.chip8.lex'


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



START_TOKENS = [
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
	TOKEN_DRAW
]

lexer_tokens = []
with open(os.path.join(path, file_name)) as f:
	statments = []
	for i in f:
		lexer_tokens.append(i.replace('\n', ''))



total_tokens = len(lexer_tokens)

index = 0

parser_tree = []
while(index < total_tokens):
	token = lexer_tokens[index]
	if token in START_TOKENS:
		print(token)
		if token == TOKEN_LOAD:
			while(token != TOKEN_END):
				index += 1
				token = lexer_tokens[index]
				print(token)
			print('END')
		else:
			index += 1
				
	else:
		print('Error, Invalid start token', token)
		break


for i in parser_tree:
	print(json.dumps(i,   sort_keys=True, indent=4))