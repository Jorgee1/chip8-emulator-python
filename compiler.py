from random import randint
import binascii
import sys
import re
class Compilation_error(LookupError):
    pass

def compiler(cmd):
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
	elif re.match(r'JP 0x[0-9]{3}', cmd):
		addr = re.search('[0-9]{3}', cmd).group(0)
		code = '1'+addr
		print(cmd, '->', ('%0*X' % (4,int('0x'+code, 0)) ))
		return binascii.unhexlify(code)
	elif re.match(r'CALL 0x[0-9]{3}', cmd):
		addr = re.search('[0-9]{3}', cmd).group(0)
		code = '2'+addr
		print(cmd, '->', ('%0*X' % (4,int('0x'+code, 0)) ))
		return binascii.unhexlify(code)
	elif re.match(r'SE V[0-9], 0x[0-9]{2}', cmd):
		x = re.search('V[0-9]', cmd).group(0).replace('V','')
		kk = re.search('0x[0-9]{2}', cmd).group(0).replace('0x','')
		code = '3' + x + kk
		print(cmd, '->', ('%0*X' % (4,int('0x'+code, 0)) ))
		return binascii.unhexlify(code)
	elif re.match(r'SNE V[0-9], 0x[0-9]{2}', cmd):
		x = re.search('V[0-9]', cmd).group(0).replace('V','')
		kk = re.search('0x[0-9]{2}', cmd).group(0).replace('0x','')
		code = '4' + x + kk
		print(cmd, '->', ('%0*X' % (4,int('0x'+code, 0)) ))
		return binascii.unhexlify(code)
	else:
		raise Compilation_error("No se reconoce el comando: "+ cmd)


with open('Programs/Test.Chip8', 'r') as f:
	with open('Out/TEST', 'wb') as out:
		for i in f:
			line = i.strip("\n")
			if line[0] != '#':
				out.write(compiler(line))
			else:
				print('Comment', line)