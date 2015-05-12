import random, enchant, itertools

class PanDecrypt:
	"""docstring for Bdecrypt"""
	perhaps		= 'etaoinshrdlcumwfgypbvkjxqz'
	P   		= 'abcdefghijklmnopqrstuvwxyz'
	ciphertext	= ''
	letterDict	= {}
	wordsList	= ()
	init_key	= ''
	length		= 6

	def __init__(self):
		f = open('0x01-ciphertext.txt', 'r')
		self.ciphertext = f.read()
		f.close()
		pass

	def run(self):
		self.count_letter()
		self.get_wordList()
		self.get_init_key()
		pass

	def check_init_key(self):
		print('init_key is : ' + self.init_key)
		print('P(init_key) : ' + str(self.check(self.init_key)))

	def count_letter(self):
		for c in self.ciphertext:
			if c > 'z' or c < 'a':
				pass
			elif c in self.letterDict:
				self.letterDict[c] += 1
			else:
				self.letterDict.setdefault(c, 1)

	def all_is_letter(self, s):
		for c in s:
			if c > 'z' or c < 'a':
				return False

		return True

	def get_wordList(self):
		strs = self.ciphertext.split()

		for s in strs:
			if self.all_is_letter(s):
				if s not in self.wordsList:
					self.wordsList = self.wordsList + (s, )

	def get_init_key(self):
		letterList	= sorted(self.letterDict.items(), key = lambda e : e[1] , reverse=True)
		
		for x in range(len(letterList)):
			self.init_key = self.init_key + letterList[x][0]

	def check(self, trans):
		table = str.maketrans(trans, self.perhaps)

		T = enchant.Dict('en_US')
		succ_perhaps = 0 

		for x in self.wordsList:
			if T.check(x.translate(table)):
				succ_perhaps += 1

		return succ_perhaps * 1.0 / len(self.wordsList)


	def upgrade(self, str_statrt, str_middle, str_end):
		middle_list = sorted(str_middle)
		middle_strs = ''
		for i in range(len(middle_list)):
			middle_strs = middle_strs + middle_list[i]

		best_succ = 0
		best_strs = ''
		for x in list(itertools.permutations(middle_strs)):
			strs = ''
			for i in range(len(x)):
				strs = strs + x[i]

			if self.check(str_statrt + strs + str_end) > best_succ:
				best_succ = self.check(str_statrt + strs + str_end)
				best_strs = strs
				print(best_strs + ' ' + str(best_succ))

		return best_strs


	def auto_decrypt(self):
		best_pwd  = self.init_key
		best_suc  = self.check(self.init_key)

		for i in range(len(self.init_key) - self.length + 1):
			tstrs_start		= best_pwd[0: i]
			tstrs_middle 	= best_pwd[i: i + self.length]
			tstrs_end		= best_pwd[i + self.length:]
			
			print('The ' + str(i) + ' times:' + '\n')
			print(tstrs_start + ' ' + tstrs_middle + ' ' + tstrs_end + '\n')

			upgrade_middle = self.upgrade(tstrs_start, tstrs_middle, tstrs_end)
			best_pwd = tstrs_start + upgrade_middle + tstrs_end
			best_suc = 0

		return best_pwd

if __name__ == '__main__':
	D = PanDecrypt()
	D.run()
	D.check_init_key()

	pwd = D.auto_decrypt()
	f = open('0x01-decrypt.txt', 'w')
	f.write(D.perhaps + '\n')
	f.write(pwd)
	f.close()

