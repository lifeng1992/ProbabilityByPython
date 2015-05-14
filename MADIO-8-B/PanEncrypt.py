import os, random

class Password():
	"""docstring for Password"""

	def __init__(self):
		pass

	def create(self):
		S = 'abcdefghijklmnopqrstuvwxyz'
		P = 'etaoinshrdlcumwfgypbvkjxqz'
		W = [c for c in P]
		random.shuffle(W)
		
		password = ''
		for c in W:
			password = password + c

		f = open('0x01-password.txt', 'w')
		f.write(P + '\n')
		f.write(password)
		f.close()

		return password


class PanEncrypt:
	"""docstring for bcrypt"""
	P = 'etaoinshrdlcumwfgypbvkjxqz'
	plaintext	= ''
	ciphertext	= ''

	def __init__(self, password):
		self.password = password

		f = open('0x01.txt', 'r')
		self.plaintext = f.read().lower()
		f.close()

	def run(self):
		self.encrypt()
		f = open('0x01-ciphertext.txt', 'w')
		f.write(self.ciphertext)
		f.close()

	def encrypt(self):
		self.table = str.maketrans(self.P, self.password)
		self.ciphertext = self.plaintext.translate(self.table)

	
if __name__ == '__main__':
	pwd = Password().create()
	encrypt = PanEncrypt(pwd).run()
	