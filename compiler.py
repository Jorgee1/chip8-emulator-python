from random import randint
import binascii
import sys
import re

"""
NOP
CALL x
SE Vx, x
SE Vx, Vx

"""

class Compilation_error(LookupError):

    pass

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
		raise Compilation_error("No se reconoce el comando: "+ cmd)



def type_addr(code, cmd):
	addr = re.search(num_match+'{3}', cmd).group(0)
	return 'code'+addr

num_match = '[0-9a-f]'

def NOP(cmd):
	return binascii.unhexlify('0000')


def CLS(cmd):
	return binascii.unhexlify('00E0')


def RET(cmd):
	return binascii.unhexlify('00EE')


def JP(cmd):
	return binascii.unhexlify('0000')


def CALL(cmd):
	return binascii.unhexlify(type_addr('2', cmd))


def SE(cmd):
	return binascii.unhexlify('0000')


def SNE(cmd):
	return binascii.unhexlify('0000')


def LD(cmd):
	return binascii.unhexlify('0000')


def ADD(cmd):
	return binascii.unhexlify('0000')


def OR(cmd):
	return binascii.unhexlify('0000')


def AND(cmd):
	return binascii.unhexlify('0000')


def XOR(cmd):
	return binascii.unhexlify('0000')


def SUB(cmd):
	return binascii.unhexlify('0000')


def SHR(cmd):
	return binascii.unhexlify('0000')


def SUBN(cmd):
	return binascii.unhexlify('0000')


def SHL(cmd):
	return binascii.unhexlify('0000')


def RND(cmd):
	return binascii.unhexlify('0000')


def DRW(cmd):
	return binascii.unhexlify('0000')


def SKP(cmd):
	return binascii.unhexlify('0000')


def SKNP(cmd):
	return binascii.unhexlify('0000')




def compiler2(cmd):
	words = {
		"CLS" : CLS, "RET":RET, "JP"  :  JP, "NOP" : NOP,
		"CALL":CALL, "SE" : SE, "SNE" : SNE, "LD"  :  LD,
		"ADD" : ADD, "OR" : OR, "AND" : AND, "XOR" : XOR,
		"SUB" : SUB, "SHR":SHR, "SUBN":SUBN, "SHL" : SHL,
		"RND" : RND, "DRW":DRW, "SKP" : SKP, "SKNP":SKNP,
	}

	word = cmd.split(' ')[0]
	print(word)
	try:
		return words[word](cmd)
	except KeyError:
		raise Compilation_error("No se reconoce el comando: "+ cmd)


with open('Programs/Test.Chip8', 'r') as f:
	with open('Out/TEST', 'wb') as out:
		for i in f:
			line = i.strip("\n")
			if line[0] != '#':
				out.write(compiler2(line))
			else:
				print('Comment', line)





"""


def CLS(cmd){
	return binascii.unhexlify('0000')
}

def RET(cmd){
	return binascii.unhexlify('0000')
}

def SYS(cmd){
	return binascii.unhexlify('0000')
}

def JP(cmd){
	return binascii.unhexlify('0000')
}

def CALL(cmd){
	return binascii.unhexlify('0000')
}

def SE(cmd){
	return binascii.unhexlify('0000')
}

def SNE(cmd){
	return binascii.unhexlify('0000')
}

def LD(cmd){
	return binascii.unhexlify('0000')
}

def ADD(cmd){
	return binascii.unhexlify('0000')
}

def OR(cmd){
	return binascii.unhexlify('0000')
}

def AND(cmd){
	return binascii.unhexlify('0000')
}

def XOR(cmd){
	return binascii.unhexlify('0000')
}

def SUB(cmd){
	return binascii.unhexlify('0000')
}

def SHR(cmd){
	return binascii.unhexlify('0000')
}

def SUBN(cmd){
	return binascii.unhexlify('0000')
}

def SHL(cmd){
	return binascii.unhexlify('0000')
}

def RND(cmd){
	return binascii.unhexlify('0000')
}

def DRW(cmd){
	return binascii.unhexlify('0000')
}

def SKP(cmd){
	return binascii.unhexlify('0000')
}

def SKNP(cmd){
	return binascii.unhexlify('0000')
}





"""