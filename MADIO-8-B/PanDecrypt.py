import itertools, enchant

class PanDecrypt:
    """docstring for PanDecrypt"""
    perhaps 	= 'etaoinshrdlcumwfgypbvkjxqz'
    P 		= 'abcdefghijklmnopqrstuvwxyz'
    
    def __init__(self, ciphertext, length = 6):
        self.ciphertext = ciphertext
        self.length     = length
        self.wordSet    = {x for x in self.ciphertext.split() if x.isalpha()}
        
        self.letterDict = self.getLetterDict(self.ciphertext)
        self.init_key   = self.getInitKey(self.letterDict)
        
        
    def getLetterDict(self, ciphertext):
        letterDict = {x: 0 for x in self.P}
        
        for x in ciphertext:
            if x in letterDict:
                letterDict[x] += 1
                
        return letterDict
        
    def getInitKey(self, letterDict):
        letterList = sorted(letterDict.items(), key = lambda e : e[1] , reverse=True)
        return str().join([x[0] for x in letterList])
        
    def check(self, trans):
        table = str.maketrans(trans, self.perhaps)
        T = enchant.Dict('en_US')
        
        accept_count = 0
        for x in self.wordSet:
            if T.check(x.translate(table)):
                accept_count += 1
            
        return accept_count
                
    
    def upgrade(self, strs_start, strs_middle, strs_end):
        best_middle = str().join(sorted(strs_middle))
        best_accept = 0
        
        for x in itertools.permutations(sorted(strs_middle)):
            new_middle = str().join(x)
            accepts = self.check(strs_start + new_middle + strs_end)
            if accepts > best_accept:
                best_accept = accepts
                best_middle = new_middle
                self.logSuccess(best_middle, accepts)
                
        return best_middle
        
    def autoDecrypt(self):
        print('AutoDecrypt start......')
        
        best_pwd  = self.init_key
        
        for i in range(len(self.init_key) - self.length + 1):
            tstrs_start     = best_pwd[0: i]
            tstrs_middle    = best_pwd[i: i + self.length]
            tstrs_end       = best_pwd[i + self.length: ]
            
            print('\nThe ' + str(i) + ' times:')
            print(tstrs_start + ' ' + tstrs_middle + ' ' + tstrs_end)
            
            upgrade_middle = self.upgrade(tstrs_start, tstrs_middle, tstrs_end)
            best_pwd = tstrs_start + upgrade_middle + tstrs_end
            
        return best_pwd
        
    def logSuccess(self, current_middle, accept_count):
        succ = accept_count / len(self.wordSet)
        print(current_middle + ' ' + str(succ))
    
    
if __name__ == '__main__':
    f = open('0x01-ciphertext.txt', 'r')
    ciphertext = f.read().lower()
    f.close()
    
    D = PanDecrypt(ciphertext)
    pwd = D.autoDecrypt()
    f = open('0x01-decrypt.txt', 'w')
    f.write(D.perhaps + '\n')
    f.write(pwd)
    f.close()
