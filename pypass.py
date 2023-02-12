import os
import hashlib
import string
import random
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from getpass import getpass

def encrypt(key, filename):
    chunksize = 64 * 1024
    output_file = filename
    iv = os.urandom(16)
    encryptor = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend()).encryptor()
    with open('/tmp/decrypted', 'rb') as infile:
        with open(output_file, 'wb') as outfile:
            outfile.write(iv)
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - len(chunk) % 16)
                outfile.write(encryptor.update(chunk))
            outfile.write(encryptor.finalize())

def decrypt(key, filename):
    chunksize = 64 * 1024
    output_file = '/tmp/decrypted'
    with open(filename, 'rb') as infile:
        iv = infile.read(16)
        decryptor = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend()).decryptor()
        with open(output_file, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.update(chunk))
            outfile.write(decryptor.finalize())

def get_key(password):
    hashed = hashlib.sha256(password.encode()).digest()
    return hashed
def inputpass():
    while True:
        p1=getpass('  Enter password:')
        p2=getpass('Reenter password:')
        if p1==p2:
           break
        else:
           print('')
           print('Password and confirming is not equal.')
           print('')
    return p1

def secdel(p):
    digits = random.sample("123456789",4)
    rd=(str("".join(digits)))
    print('Enter '+rd+' to delete file.')
    cfm=input()
    if cfm==rd:
       stats = os.stat(p)
       s=stats.st_size
       letters = string.ascii_lowercase
       rand_string = ''.join(random.choice(letters) for i in range(s))
       f=open(p,'w')
       f.write(rand_string)
       f.close()
       os.remove(p)
    else:
       print('Incorrect confirmation. Delete cancelled.')
def cleartmp():
    stats = os.stat('/tmp/decrypted')
    s=stats.st_size
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for i in range(s))
    f=open('/tmp/decrypted','w')
    f.write(rand_string)
    f.close()
    os.remove('/tmp/decrypted')

while True:
   print("\033c", end="") # clear the terminal
   print("List of notes:")
   print("==================================================")
   un=os.environ.get("USER")
   path='/home/'+un+'/.pypass'
   content = os.listdir(path)
   l=len(content)


   for i in range(l):
       ls=str(i)+'. '+content[i]
       print(ls)

   print("==================================================")
   print("Enter: number of note to read it,  a to add note, e to edit note, r to rename, d to delete note and q to exit")
   print('')
   cmd = input('>>>  ')
   cmd=cmd.lower()
   if cmd.isdigit() is True:
      try:
          filepath=path+'/'+content[int(cmd)]
      except Exception:
          input('Wrong number. Press enter to continue.')
          continue

      passw=getpass('Enter password: ')
      dkey = get_key(passw)
      try:
         decrypt(dkey, filepath)
         f=open('/tmp/decrypted','r')
         s=f.read()
         f.close()
      except Exception:
         s='Wrong password or note is corrupt.'
      print("\033c", end="") # clear the terminal
      print(s)
      print('')
      print('')
      cleartmp()
      input('Press Enter to continue')
   else:
      if cmd=='e':
         edn=input('Enter number of note to edit: ')
         filepath=path+'/'+content[int(edn)]
         passw=getpass('Enter password: ')
         dkey = get_key(passw)
         try:
            decrypt(dkey, filepath)
            print('File will edit by nano. After edit press Ctrl+O and Ctrl+X. Waning: do not edit name of file')
            input('Press Enter to continue.')
            os.system('nano /tmp/decrypted')
            encrypt(dkey,filepath)
            cleartmp()
         except Exception:
            print('Wrong password or note is corrupt.')
      if cmd=='r':
         print ("Enter number of note:\n")
         n=input(">>> ")
         print ("Enter new name of the note:\n")
         newname=input(">>> ")
         newname=newname.replace('/','')
         
         try:
             filepath=path+'/'+content[int(n)]+' '
             filepathnew=path+'/'+newname
             cmd='mv '+filepath+filepathnew
             os.system(cmd)
             
         except Exception:
             input('Wrong number. Press enter to continue.')
             continue

      if cmd=='d':
         dtd=input('Enter number of note to delete: ')
         filepath=path+'/'+content[int(dtd)]
         secdel(filepath)
      if cmd=='q':

         break

      if cmd=='a':
         notename=input('Enter note name: ')
         passw=inputpass()
         filepath=path+'/'+notename
         text = ""
         while True:
            print("\033c", end="") # clear the terminal
            print("Enter ~ to save your note. Enter cw to clear your note.")
            print("========================================================")
            if text == "cw\n":
               text=""
            print(text)
            line = input(">>> ")
            if line == "cw":
                text=""
            elif line == "~":
                with open("/tmp/decrypted", "w") as f:
                   f.write(text)
                break
            text += line + "\n"
         ekey=get_key(passw)
         encrypt(ekey, filepath)
         cleartmp()
