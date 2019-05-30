from os import path, makedirs
from src.compiler.compiler import Compiler

"""
NOP
CALL x
SE Vx, x
SE Vx, Vx

"""


"""
def compiler(cmd):
	instructions = ['NOP', 'CLS', 'RET', 'JP', 'CALL']
	num_match = '[0-9a-f]'

	if cmd == 'NOP':
		print(cmd, '->', ('%0*X' % (4,0) ))
		return binascii.unhexlify('0000')
	elif cmd == 'CLS':
		code = '00E0'
		print(cmd, '->', ('%0*X' % (4,int('0x'+code, 0)) ))
		return binascii.unhexlify(code)
	elif cmd == 'RET':
		code = '00EE'
		print(cmd, '->', ('%0*X' % (4,int('0x'+code, 0)) ))
		return binascii.unhexlify(code)
	elif re.match(r'JP 0x'+num_match+'{3}', cmd):
		addr = re.search(''+num_match+'{3}', cmd).group(0)
		code = '1'+addr
		print(cmd, '->', ('%0*X' % (4,int('0x'+code, 0)) ))
		return binascii.unhexlify(code)
	elif re.match(r'CALL 0x'+num_match+'{3}', cmd):
		addr = re.search(''+num_match+'{3}', cmd).group(0)
		code = '2'+addr
		print(cmd, '->', ('%0*X' % (4,int('0x'+code, 0)) ))
		return binascii.unhexlify(code)
	elif re.match(r'SE V'+num_match+', 0x'+num_match+'{2}', cmd):
		x = re.search('V'+num_match+'', cmd).group(0).replace('V','')
		kk = re.search('0x'+num_match+'{2}', cmd).group(0).replace('0x','')
		code = '3' + x + kk
		print(cmd, '->', ('%0*X' % (4,int('0x'+code, 0)) ))
		return binascii.unhexlify(code)
	elif re.match(r'SNE V'+num_match+', 0x'+num_match+'{2}', cmd):
		x = re.search('V'+num_match+'', cmd).group(0).replace('V','')
		kk = re.search('0x'+num_match+'{2}', cmd).group(0).replace('0x','')
		code = '4' + x + kk
		print(cmd, '->', ('%0*X' % (4,int('0x'+code, 0)) ))
		return binascii.unhexlify(code)
	elif re.match(r'SE V'+num_match+', V'+num_match+'', cmd):
		x = re.findall(r'V'+num_match+'', cmd)[0].replace('V','')
		y = re.findall(r'V'+num_match+'', cmd)[1].replace('V','')
		code = '5' + x + y + '0'
		print(cmd, '->', ('%0*X' % (4,int('0x'+code, 0)) ))
		return binascii.unhexlify(code)
	elif re.match(r'LD V'+num_match+', 0x'+num_match+'{2}', cmd):
		x = re.search('V'+num_match+'', cmd).group(0).replace('V','')
		kk = re.search('0x'+num_match+'{2}', cmd).group(0).replace('0x','')
		code = '6' + x + kk
		print(cmd, '->', ('%0*X' % (4,int('0x'+code, 0)) ))
	elif re.match(r'ADD V'+num_match+', 0x'+num_match+'{2}', cmd):
		x = re.search('V'+num_match+'', cmd).group(0).replace('V','')
		kk = re.search('0x'+num_match+'{2}', cmd).group(0).replace('0x','')
		code = '7' + x + kk
		print(cmd, '->', ('%0*X' % (4,int('0x'+code, 0)) ))
	elif re.match(r'SNE V'+num_match+', V'+num_match+'', cmd):
		x = re.findall(r'V'+num_match+'', cmd)[0].replace('V','')
		y = re.findall(r'V'+num_match+'', cmd)[1].replace('V','')
		code = '9' + x + y + '0'
		print(cmd, '->', ('%0*X' % (4,int('0x'+code, 0)) ))
	elif re.match(r'LD, 0x'+num_match+'{3}', cmd):
		addr = re.search(''+num_match+'{3}', cmd).group(0)
		code = 'a'+addr
		print(cmd, '->', ('%0*X' % (4,int('0x'+code, 0)) ))
	elif re.match(r'JP V0, 0x'+num_match+'{3}', cmd):
		addr = re.search(''+num_match+'{3}', cmd).group(0)
		code = 'b'+addr
		print(cmd, '->', ('%0*X' % (4,int('0x'+code, 0)) ))
	elif re.match(r'JP V0, 0x'+num_match+'{3}', cmd):
		addr = re.search(''+num_match+'{3}', cmd).group(0)
		code = 'c'+addr
		print(cmd, '->', ('%0*X' % (4,int('0x'+code, 0)) ))
	else:
		print("Error")
"""


compiler = Compiler()

if not path.exists(compiler.output_folder):
	makedirs(compiler.output_folder)

with open('Programs/WordAndParm.chip8') as f,\
	 open(path.join(compiler.output_folder, 'TEST'), 'wb') as out:
	for i in f:
		line = i.strip("\n")
		if line:
			print("Command:", line)
			if line[0] != '#':
				out.write(compiler.compile(line))
			else:
				print('Comment', line)



