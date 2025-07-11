#
# textmodel.py
#
# TextModel project!
#

import string
import math
from porter import create_stem

class TextModel:
    """A class supporting complex models of text."""

    def __init__(self):
        """Create an empty TextModel."""
        # 
        # The text in the model, all in a single string--the original
        # and "cleaned" versions.
        #
        self.text = ''            # No text present yet
        self.cleanedtext = ''     # Nor any cleaned text yet
                                  # ..(cleaned == only letters, all lowercase)

        #
        # Create dictionaries for each characteristic
        #
        self.words = {}           # For counting words
        self.wordlengths = {}     # For counting word lengths
        self.stems = {}           # For counting stems
        self.sentencelengths = {} # For counting sentence lengths
        
        # Create another dictionary of your own
        #
        self.punctuation = {}     # For counting ___________

    def __repr__(self):
        """Display the contents of a TextModel."""
        s = f'Words:\n{str(self.words)}\n\n'
        s += f'Word lengths:\n{str(self.wordlengths)}\n\n'
        s += f'Stems:\n{str(self.stems)}\n\n'
        s += f'Sentence lengths:\n{str(self.sentencelengths)}\n\n'
        s += f'MY PUNCTUATION:\n{str(self.punctuation)}\n\n'
        s += '+'*55 + '\n'
        s += f'Text[:42]    {self.text[:42]}\n'
        s += f'Cleaned[:42] {self.cleanedtext[:42]}\n'
        s += '+'*55 + '\n\n'
        return s

    # We provide two text-adding methods (functions) here:
    def addRawText(self, text):
        """addRawText accepts self (the object itself)
                      and text, a string of raw text to add.
           Nothing is returned from this method, but
           the text _is_ added.
        """
        self.text += text 
        self.cleanedtext += self.cleanString(self.text) 

    # The second one adds text from a file:
    def addFileText(self, filename):
        """addFileText accepts a filename.
            
           Nothing is returned from this method, but
           the file is opened and its text _is_ added.

           If the file is not present, it will crash!
        """
        f = open(filename, 'r', encoding='latin1')
                               # The above may need utf-8 or utf-16, depending
        text = f.read()        # Read all of the contents into text 
        f.close()              # Close the file
        self.addRawText(text)  # Uses the previous method!

    def readTextFromFile(self, filename):
        """readTextFromFile accepts a filename (a string) and
        places all of the text in that file into self.textas a very large string."""
        f = open(filename)
        self.text = f.read()
        f.close()

    def makeSentenceLengths(self):
        """Creates the dictionary of sentence lengths
        should use self.text, because it needs the punctuation!
        """
        s = self.text
        allwords = s.split()
        d = self.sentencelengths
        c = 1
        for i in allwords:
            if i[-1] not in '.?!':
                c += 1
            else:
                if c in d:
                    d[c] += 1
                else:
                    d[c] = 1
                c = 1

    def cleanString(self, s):
        """Returns the string s, but
           with only ASCII characters, only lowercase, and no punctuation.
           See the description and hints in the problem!
        """
        s = s.lower()
        for p in string.punctuation:
            s = s.replace(p, '')
        return s
    
    def makeWordLengths(self):
        """Creates the dictionary of word lengths
        should use self.cleanedtext, because the punctuation needs to be removed!
        """
        s = self.cleanedtext
        allwords1 = s.split()
        d = self.wordlengths
        for i in allwords1:
            if len(i) in d:
                d[len(i)] += 1
            else:
                d[len(i)] = 1
    
    def makeWords(self):
        """Creates the dictionary of words
        should use self.cleanedtext, because the punctuation needs to be removed
        """
        s = self.cleanedtext
        allwords2 = s.split()
        d = self.words
        for i in allwords2:
            if i in d:
                d[i] += 1
            else:
                d[i] = 1
    
    def makeStems(self): 
        """except that it makes a dictionary of the stems of the words themselves (cleaned!)""" 
        s = self.cleanedtext
        allwords3 = s.split()
        d = self.stems
        for i in allwords3:
            stem = create_stem(i)
            if stem in d:
                d[stem] += 1
            else:
                d[stem] = 1
    
    def makePunctuation(self):
        """makePunctuation uses the text in self.text to createthe punctuation dictionary."""
        self.punctuation = {}
        c = 0
        LoS = list(self.text)
        for i in LoS:
            if i == ".":
                if "." in self.punctuation:
                    self.punctuation[i] += 1
                else:
                    self.punctuation[i] = 1
            if i == ",":
                if "," in self.punctuation:
                    self.punctuation[i] += 1
                else:
                    self.punctuation[i] = 1
            if i == "!":
                if "!" in self.punctuation:
                    self.punctuation[i] += 1
                else:
                    self.punctuation[i] = 1
            if i == "?":
                if "?" in self.punctuation:
                    self.punctuation[i] += 1
                else:
                    self.punctuation[i] = 1
            if i == ":":
                if ":" in self.punctuation:
                    self.punctuation[i] += 1
                else:
                    self.punctuation[i] = 1
            if i == ";":
                if ";" in self.punctuation:
                    self.punctuation[i] += 1
                else:
                    self.punctuation[i] = 1
            if i == "'":
                if "'" in self.punctuation:
                    self.punctuation[i] += 1
                else:
                    self.punctuation[i] = 1
            if i == '"':
                if '"' in self.punctuation:
                    self.punctuation[i] += 1
                else:
                    self.punctuation[i] = 1
        return self.punctuation
    
    def normalizeDictionary(self, d):
        """normalizeDictionary should accept any single one ofthe model dictionaries d and return a normalizedversion."""
        norm_dict = {}
        v = d.values()
        for k in d:
            norm_dict[k] = d[k] / sum(v)
        return norm_dict
    
    def smallestValue(self, nd1, nd2):
        """This function accepts any two model dictionaries nd1 and nd2 and 
        returns the smallest positive (that is, non-zero) value across them both.
        """
        L1 = list(nd1.values())
        L2 = list(nd2.values())
        L = L1 + L2
        # print(L)
        return min(L)
    
       
    def compareDictionaries(self, d, nd1, nd2):
        """compareDictionaries computes the log-probability that the dictionary d arose from the distribution of datain the normalized 
        dictionary nd1 and that in normalizeddictionary nd2."""
        total_log_prob = 0.0
        total_log_prob_2 = 0.0
        for k in d:
            if k in nd1:
                nd1[k]+= 1
            else:
                nd1[k]= 1
        for k in d:
            if k in nd2:
                nd2[k]+= 1
            else:
                nd2[k] = 1 
        nd1 = self.normalizeDictionary(nd1)
        nd2 = self.normalizeDictionary(nd2)
        for k in d:
            total_log_prob += d[k] * math.log(nd1[k])
            total_log_prob_2 += d[k] * math.log(nd2[k])
        comp = [total_log_prob, total_log_prob_2]
        return comp
    
    def createAllDictionaries(self):
        """Create out all five of self's
           dictionaries in full.
        """
        self.makeSentenceLengths()
        self.makeWords()
        self.makeStems()
        self.makeWordLengths()
        self.makePunctuation()
    
    def compareTextWithTwoModels(self, model1, model2):
        """This method should run the compareDictionaries method, described above,
        for each of the feature dictionaries in self against the corresponding (normalized!)
        dictionaries in model1 and model2.
        """
        m1 = 0
        m2 = 0
        nd1 = self.normalizeDictionary(model1.words)
        nd2 = self.normalizeDictionary(model2.words)
        LogProbs1 = self.compareDictionaries(self.words, nd1, nd2)
        print("LogProbs1 is", LogProbs1)
        nd1 = self.normalizeDictionary(model1.wordlengths)
        nd2 = self.normalizeDictionary(model2.wordlengths)
        LogProbs2 = self.compareDictionaries(self.wordlengths, nd1, nd2)
        print("LogProbs2 is", LogProbs2)
        nd1 = self.normalizeDictionary(model1.stems)
        nd2 = self.normalizeDictionary(model2.stems)
        LogProbs3 = self.compareDictionaries(self.stems, nd1, nd2)
        print("LogProbs3 is", LogProbs3)
        nd1 = self.normalizeDictionary(model1.sentencelengths)
        nd2 = self.normalizeDictionary(model2.sentencelengths)
        LogProbs4 = self.compareDictionaries(self.sentencelengths, nd1, nd2)
        print("LogProbs4 is", LogProbs4)
        nd1 = self.normalizeDictionary(model1.punctuation)
        nd2 = self.normalizeDictionary(model2.punctuation)
        LogProbs5 = self.compareDictionaries(self.punctuation, nd1, nd2)
        print("LogProbs5 is", LogProbs5)

        print(f" {'name':>20s} {'vsTM1':>10s} {'vsTM2':>10s} ")
        print(f" {'----':>20s} {'-----':>10s} {'-----':>10s} ")
        d_name1 = 'words'
        d_name2 = 'wordlengths'
        d_name3 = 'stem'
        d_name4 = 'sentencelengths'
        d_name5 = '1st & 2nd pronouns'

        print(f" {d_name1:>20s} {LogProbs1[0]:>10.2f} {LogProbs1[1]:>10.2f} ")
        print(f" {d_name2:>20s} {LogProbs2[0]:>10.2f} {LogProbs2[1]:>10.2f} ")
        print(f" {d_name3:>20s} {LogProbs3[0]:>10.2f} {LogProbs3[1]:>10.2f} ")
        print(f" {d_name4:>20s} {LogProbs4[0]:>10.2f} {LogProbs4[1]:>10.2f} ")
        print(f" {d_name5:>20s} {LogProbs5[0]:>10.2f} {LogProbs5[1]:>10.2f} ")
        print()

        LOL= [LogProbs1,LogProbs2,LogProbs3,LogProbs4,LogProbs5]
        for i in range(len(LOL)):
            if LOL[i][0]> LOL[i][1]:
                m1+=1
            elif LOL[i][0] < LOL[i][1]:
                m2+=1

        print("---> The Grinch wins",m1, "features")
        print("---> The tale of two Cities wins",m2, "features")
        print('Your preference is' ,int(m1/5*100), '% The Grinch and', int(m2/5*100), '% The tale of two Cities.')
        print()
        if m1>m2:
            print("+++++++++++ The Grinch is a better match! +++++++++++")
        elif m2>m1:
            print("+++++++++++ The tale of two Cities is a better match! +++++++++++")
        else:
            print("The Grinch and The tale of two Cities wins both are equal matches!")
        print()
        print()


# And let's test things out here...
TMintro = TextModel()

# Add a call that puts information into the model
TMintro.addRawText("""This is a small sentence. This isn't a small
sentence, because this sentence contains more than 10 words and a
number! This isn't a question, is it?""")

# Put the above triple-quoted string into a file named test.txt, then run this:
#  TMintro.addFileText("test.txt")   # "comment in" this line, once the file is created

# Print it out
print("TMintro is", TMintro)


# Add more calls - and more models - here:
TM = TextModel()
TM.addFileText("test.txt")      # Puts all text into TM.text
print(TM.makeSentenceLengths())

TM = TextModel()
TM.addFileText("test.txt")   # See makeSentenceLengths for the contents of this test.txt file
result = TM.cleanString(TM.text)
print(result)

# normalizeDictionary(self, d)
TM = TextModel()
d = {'a': 5, 'b':1, 'c':2}
nd = TM.normalizeDictionary(d)
print("The original dictionary is", d)
print("The normalized dictionary is", nd)


#smallestvalue test 
TM = TextModel()
d1 = {'a': 5, 'b':1, 'c':2}
nd1 = TM.normalizeDictionary(d1)
d2 = {'a': 15, 'd':1}
nd2 = TM.normalizeDictionary(d2)
print("The normalized dictionaries are:")
print(nd1)
print(nd2)
sm_va = TM.smallestValue(nd1, nd2)
print("and the smallest value between them is", sm_va)


TM = TextModel()
d = {'a':2, 'b':1, 'c':1, 'd':1, 'e':1}
print("The unnormalized dictionary is", d)
print("\n")
d1 = {'a': 5, 'b':1, 'c':2}
nd1 = TM.normalizeDictionary(d1)
d2 = {'a': 15, 'd':1}
nd2 = TM.normalizeDictionary(d2)
print("The normalized comparison dictionaries are:")
print(nd1)
print(nd2)

List_of_log_probs = TM.compareDictionaries(d, nd1, nd2)
print("The list of log probs is")
print(List_of_log_probs)


print(" +++++++++++ Model1 +++++++++++ ")
TM1 = TextModel()
TM1.addFileText("grinch.txt")
TM1.createAllDictionaries()  # provided in hw description
print(TM1)

print(" +++++++++++ Model2 +++++++++++ ")
TM2 = TextModel()
TM2.addFileText("cities.txt")
TM2.createAllDictionaries()  # provided in hw description
print(TM2)


print(" +++++++++++ Unknown text +++++++++++ ")

TM_Unk1 = TextModel()
TM_Unk1.addFileText("percy.txt")
TM_Unk1.createAllDictionaries() # provided in hw description
TM_Unk2 = TextModel()
TM_Unk2.addFileText("harry.txt")
TM_Unk2.createAllDictionaries()

#the main comparison method 
TM_Unk1.compareTextWithTwoModels(TM1, TM2)
TM_Unk2.compareTextWithTwoModels(TM1, TM2)