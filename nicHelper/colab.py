# AUTOGENERATED! DO NOT EDIT! File to edit: colab.ipynb (unless otherwise specified).

__all__ = ['saveAwsPw', 'loadAwsPw', 'setUpAws', 'autoSetupAws']

# Cell
from .encrypt import encryptPasswordAes, decryptPasswordAes
from beartype import beartype
from getpass import getpass
from functools import partial
from typing import Tuple, Optional
from getpass import getpass
import subprocess, pickle, os

# Cell
@beartype
def saveAwsPw(awskey:bytes, awssecret:bytes,
              path:str = '/content/drive/MyDrive/.awskey', password:bytes = b''):
  '''
    save your aws password in your
  '''
  # get password
  if not password:
    password = getpass('input the password').encode()

  # encrypt with aes
  encrypt = partial(encryptPasswordAes, password)
  cryptkey, keynonce = encrypt(awskey)
  cryptsecret, secretnonce = encrypt(awssecret)

  # save file as pickle
  with open (path ,'wb') as f:
    pickle.dump((cryptkey, cryptsecret, keynonce, secretnonce),f)


# Cell
@beartype
def loadAwsPw(path = '/content/drive/MyDrive/.awskey',
              password:Optional[bytes] = None )->Optional[Tuple[bytes,bytes]]:
  '''
    load key and secret from path
  '''
  if not password: password = getpass().encode()

  with open (path, 'rb') as f:
    cryptkey, cryptsecret, keynonce, secretnonce = pickle.load(f)
  decryptedKey = decryptPasswordAes(cryptkey,password,keynonce)
  decryptedSecret = decryptPasswordAes(cryptsecret, password, secretnonce)
  return decryptedKey, decryptedSecret


# Cell
@beartype
def setUpAws(awsKey:str, awsSecret:str,
             profile:Optional[str] = None, region:str = 'ap-southeast-1')->Tuple[str,str,str]:
  '''
    this code generate a string to be executed to the shell
    you can do this with, however, its not a bad idea to check before executing

    (exec(c) for c in setUpAws(...))

    response:
      (setupKey, setupSecret, setupRegion)

  '''
  if profile:  profileParameter = f'--profile {profile} '
  else: profileParameter = ''

  setupPrefix = f'aws configure {profileParameter}'
  setupKey = f'{setupPrefix}set aws_access_key_id {awsKey}'
  setupSecret = f'{setupPrefix}set aws_secret_access_key {awsSecret}'
  setupRegion = f'{setupPrefix}set default.region {region}'


  return setupKey, setupSecret, setupRegion


# Cell
def autoSetupAws(path, profile=None, region='ap-southeast-1', mockup = False, password:Optional[bytes] = None):
  key, secret = loadAwsPw(path, password=password) # key and secret in bytes
  try:
    key, secret = key.decode(), secret.decode()
  except:
    print('cant decode key and secret, maybe the password is wrong')
    return

#   print(key,secret)
  setupStrings = setUpAws(awsKey=key,
                          awsSecret=secret,
                          profile=profile,
                          region=region)
  # check if reunning in colab
  isColab =  'google.colab' in str(get_ipython())

  if isColab:
    print('Running on CoLab')
  else:
    print('Not running on colab')


  if mockup:
    return setupStrings
  for setupString in setupStrings:
    if isColab:
      print(f'executing {setupString[:-5]}')
      os.system(setupString)
    else:
      print('Not running on CoLab')
      print(setupString[:=5])

