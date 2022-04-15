import sys
import string
import math 
import hashlib


# Name: Sean Hol
# Description: Feistel Cipher encoder and decoder 
#   A filepath for the text and string for the key must be specified, along with whether the user wishes an encoded or decoded output and the output filepath
#   This Feistel algorithm runs with F(R,K) function being the xor of the right side of the input and key for that round.
#   The keys are derived by creating sha256 functions of the prior key, with the first key being a sha256 hash of the inputted key. This way all keys are different.

#receives a string and output the binary of the unicode of each character
def toBinary(text):
  temp = []
  binaryText = ""
  for i in text:
    temp.append(ord(i))
  for j in temp:
    binaryText = binaryText + (format(int(bin(j)[2:])).zfill(8))
  return binaryText


#receives a binary string and returns the unicode characters for every binary byte
def fromBinary(text):
  stringOut = ''
  while (len(text)>=8):
      currChar = chr(int(text[:8],2))
      #print(currChar, int(text[:8],2))
      text = text[8:]
      stringOut = stringOut + currChar
  return stringOut

#returns the first half of the string (not including the centre, if exists)
def getLeft(string):
    return string[:len(string) // 2]

#returns the latter half of the string (including the centre, if exists)
def getRight(string):
    return string[len(string) // 2:]

#function to allow for xor operations on strings of binary text
def xor(i,j):
  out = int(i,2)^int(j,2)
  return bin(out)[2:].zfill(len(i))

#Encodes one block of the Feistel Cipher using xor, and flips the left and right
def encodeBlock(left, right, key):
  f = xor(right, key)
  newRight = xor(left, f)
  newLeft = right
  return newLeft, newRight

#Makes 4 unique keys based of the inputted keys and repeats or shaves them based on the required length
def makeKeys(inKey, keySize):
  k1, k2, k3, k4 = "","","",""
  k1 = str(hashlib.sha256(inKey.encode()).hexdigest())
  k2 = str(hashlib.sha256(k1.encode()).hexdigest())
  k3 = str(hashlib.sha256(k2.encode()).hexdigest())
  k4 = str(hashlib.sha256(k3.encode()).hexdigest())
  k1 = toBinary(k1)
  k2 = toBinary(k2)
  k3 = toBinary(k3)
  k4 = toBinary(k4)
  #adjusts the keys to the right length
  counter = 0
  newk1 = k1
  newk2 = k2
  newk3 = k3 
  newk4 = k4
  while len(newk1) < keySize:
    newk1 = newk1 + k1[counter:counter+8]
    newk2 = newk2 + k2[counter:counter+8]
    newk3 = newk3 + k3[counter:counter+8]
    newk4 = newk4 + k4[counter:counter+8]
    counter+=8
    if (counter+8)>len(k1):
      counter=0
  k1 = newk1[:keySize]
  k2 = newk2[:keySize]
  k3 = newk3[:keySize]
  k4 = newk4[:keySize]
    
  return k1,k2,k3,k4

#start of operations, imports text file and extracts string
fullstring = ""
#gets inputs from the command line when script is run
try:
  filepath = sys.argv[1]
  inKey = sys.argv[2]
  codeMode = sys.argv[3]
  #When decoded previously coded text, it will not work if it is simply the result printed into the terminal.
  #Therefore, an outputfilepath must be specified to place the encoded text into.
  outputfilepath = sys.argv[4]
except Exception as err:
  print("Input error. Command should look like:\npython FeistelCipher.py InputFilepath Key Codetype OutputFilepath\nRefer to README for usage instructions")
  quit()
if outputfilepath == "":
  print("Output filepath must be specified for encoding")
#reads file and throws an error if it doesn't work. newline being '' for all reads and writes ensures there are no missing \r or \n chars
try:
  with open(filepath, 'r',encoding="utf-8",newline='') as f:
      fullstring = f.read()
except Exception as err:
    print ("Could not read file:", filepath)
    quit()
if fullstring == "":
  print("textfile is empty")
  quit()
if len(fullstring)%2 == 1:
  fullstring = fullstring + " "
#string is made into binary, keysize is determined and keys are made
fullstringBin = toBinary(fullstring)
#fullstringBin = fullstring
keySize = int(len(fullstringBin)//2)
k1, k2, k3, k4 = makeKeys(inKey, keySize)
#keys are placed into a list for use (reversekeys allow for decoding)
keys = [k1,k2,k3,k4]
reversekeys = [k4,k3,k2,k1]
#depending on what the user inputted, encode or decode the text, and print the outcome
if codeMode == "encode":
  r = getRight(fullstringBin)
  l = getLeft(fullstringBin)
  for i in keys:
    l,r = encodeBlock(l,r,i)
  x = fromBinary(r+l)
  f = open(outputfilepath, "w", encoding="utf-8",newline = '')
  f.write(x)
  f.close()
  print("Output written to specified file. Please use this file to decode")
elif codeMode == "decode":
  r = getRight(fullstringBin)
  l = getLeft(fullstringBin)
  for i in reversekeys:
    l,r = encodeBlock(l,r,i)
  x = fromBinary(r+l)
  f = open(outputfilepath, "w", encoding="utf-8",newline='')
  f.write(x)
  f.close()
  print("Decoded text written to specified file")
else:
  print("coding type invalid. Please select encode or decode")

