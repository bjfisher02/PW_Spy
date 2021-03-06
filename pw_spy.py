#!/usr/bin/env python3

import sys
import re
import operator
import argparse
from collections import Counter


parser = argparse.ArgumentParser()

parser.add_argument("-pot", "--potfile", dest = "potfile", help="Pot file")
parser.add_argument("-hash", "--hashlist", dest = "hashlist", help="Hash List")

args = parser.parse_args()
#repeated hashes (from full hashlist)
repeated_hashes = []

#plaintext passwords (from potfile)
plaintext_passwords = []

#cracked hashes (from potfile)
cracked_hashes = []

#letters
letters_regex = re.compile('[^a-zA-Z]')

#potfile
potfile = open(args.potfile) 

#potfile raw
potfile_raw = []

#full hashlists
if args.hashlist is not None:
  full_hashlist = open(args.hashlist)


print("""\
  ____ __          __   _____
 |  __ \ \        / /  / ____|
 | |__) \ \  /\  / /  | (___  _ __  _   _
 |  ___/ \ \/  \/ /    \___ \| '_ \| | | |
 | |      \  /\  /     ____) | |_) | |_| |
 |_|       \/  \/     |_____/| .__/ \__, |
                             | |     __/ |
                             |_|    |___/
                        """)

if len(sys.argv) < 3:
	print("Usage is: <full hashlist> <potfile>")
	sys.exit()

#split out the potfile to get hashes and plaintext passwords
def split_pot():
  print('###################### SPLITTING POT FILE ##################\n')
  for password in potfile:
     potfile_raw.append(password.strip())
     split_pw = password.split(":", 1)
     hash_string, pw_string = split_pw
     cracked_hashes.append(hash_string)
     plaintext_passwords.append(pw_string) 
  print('...DONE')

#Find how many times a password was reused
def pw_reuse():
  split_char = ":"
  split = 3
  print("\n\n\n###################### PASSWORD REUSE ######################\n")
  if args.hashlist is not None:
    for word in full_hashlist:
      stripped_hash = word.strip()
      ripped_hash   = stripped_hash.split(split_char)
      fixed_hash    = split_char.join(ripped_hash[split:])
      final_hash    = fixed_hash.split(":",1)
      repeated_hashes.append(final_hash[0])
    repeated = Counter(repeated_hashes).most_common()
    reused = []
    print('\n#### THIS IS SEPARATED AS <hash>:<number of occurances>')
    for occurance in repeated:
       occurance = [x for x in occurance if x != 1]
       if len(occurance) != 1:
           print(*occurance, sep=":")
           reused.append(occurance)
    if len(reused) == 0:
      print("No repeated hashes!")
  else:
    print("No hashlist supplied, skipping")
 


#Thanks Joshua Platz for his maskbuilder.py
def masks():
  print('\n\n\n###################### PASSWORD MASKS ######################\n')
  upper=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
  lower=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
  digit=["0","1","2","3","4","5","6","7","8","9"]
  masks={}
  words=0
  for word in plaintext_passwords:
    mask=""
    for char in word.rstrip('\r\n'):
      if char in upper:
        mask=mask+"?u"
      elif char in lower:
        mask=mask+"?l"
      elif char in digit:
        mask=mask+"?d"
      else:
        mask=mask+"?s"
    if mask not in masks:
        masks[mask] = 1
    else:
        masks[mask] += 1
        words+=1

  sorteddmask = sorted(masks.items(), key=operator.itemgetter(1), reverse=True)
  for mask in sorteddmask:
      if mask[1] >= 10:
        result = mask[0]+","+str(mask[1])+" Occurances,"+str((float(mask[1])/float(words))*100)+"%"
        print(result)


# Gets the basewords from the plaintext passwords and counts the number of occurances
def basewords_getter():
  print('\n\n\n###################### COMMON BASEWORDS  #########################\n')
  sorted_pws = []
  for word in plaintext_passwords:
    baseword = (letters_regex.sub('',word.rstrip()))
    sorted_pws.append(baseword)
  repeated = Counter(sorted_pws).most_common()
  print('\n###### THIS IS SEPARATED AS <baseword>:<number of occurances>#####')
  for occurance in repeated:
      occurance = [x for x in occurance if x != 1]
      if len(occurance) != 1:
          print(*occurance, sep=":")

# Looks for passwords without numbers or special characters
def weak_passwords():
  print("\n\n\n###################### WEAK PASSWORDS ######################\n")
  weak_pws = []
  for word in plaintext_passwords: 
     baseword = (letters_regex.sub('',word.rstrip()))
     if word.rstrip() == baseword:
       weak_pws.append(baseword)
  print('\n###### THESE ARE PASSWORDS THAT CONSIST OF ONLY LETTERS #####')
  weak_pws.sort()
  for occurance in weak_pws:
    print(occurance)

def pw_length_check():
  print("\n\n\n################### PASSWORD LENGTH CHECK ################\n")
  pw_length = []
  for word in plaintext_passwords:
     length = len(word)
     pw_length.append(length)
  pw_length.sort(reverse = True)

  pw_count = Counter(pw_length)
  for pw_length, count in pw_count.most_common():
      print(pw_length, ",", count)  

#Call the functions
split_pot()
basewords_getter()
pw_reuse()
masks()
weak_passwords()
pw_length_check()
