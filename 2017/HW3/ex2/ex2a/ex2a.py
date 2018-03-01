import hashlib
import os
import itertools
import string


password_hashes = ['bc4fd60d1dfb47aa5a0885adfe27a4198fb319732b6713b5f8eb3b385300e638',
                    'af97f3be82d357c58201763b37f1a4747f6a73bcf50ab65d99cf261b3a119831',
                    'e7af1d32f9ae67f8599e62bcf433a9953ba91d20715f18f6e3bb725379585de3',
                    'cc8c74c535bf8f2e7aa3b3caad1245cb4690cf2be516be9651f431fe34d27c19',
                    '1bea3e9d7e3c065e716294d572ea86aeba7f7a3572f4736703b26e61c3019aa5',
                    '8815adb95cc1d1d760860a3b29ab775d67f62b8660f2229a29bdeaf3b7c807bc',
                    'f8ad59e7f6259b8f0f071d761b510928d0c2fde63b2d6de2fcdbedec11f25a27',
                    'c0c4b3ba2a95bc58cc62e1c6e238c98f6cb0ac09e5544df0ef1d91baa94f109c',
                    '5166d25564e249bbbdf5cec58eacf0d0f5e1a5936378cb1c044c78b2cbd8a2ea',
                    'dda9a2a10e9d6f4975f5db2170d62a5ccefd7359b544c8c81d4980929201bde3']

charset_space = 'abcdefghijklmnopqrstuvwxyz0123456789'

def _word_generator(limit):
  """Generates a list of words up to length specified by 'limit'.
  Parameters:
    - limit: The upper limit of the range of the word length.
  Yields:
    - A range of words with a maximum length given 'limit'.
  """
  for length in range(4, limit+1):
    for char in itertools.product(charset_space, repeat=length):
      yield "".join(char)

def _create_wordlist(file_name, word_limit=6):
  """Generates a wordlist plaintext file.
  Parameters:
    - file_name: The name to give the wordlist file.
    - word_limit: The upper limit of the range of the word length. Passed to
      "_word_generator"; default=8.
    - digit_limit: The upper limit of the range of digits to append to the word.
      Passed to "digit_generator"; default=0.
  """
  try:
    with open(file_name, "w") as output:
      for word in _word_generator(word_limit):
        print(word, file=output)

  except IOError as err:
    print("File error: %s",str(err))


def sha256_hex(text):
    return hashlib.sha256(text).hexdigest()

def create_wordlist():
    if os.path.isfile('wordlist.txt'):
        wordlist = open('wordlist.txt', 'r')
    else:
        _create_wordlist('wordlist.txt', 6) #takes some time...

        wordlist = open('wordlist.txt', 'r')
    return wordlist

def main():

    wordlist = create_wordlist()
    passwords_dict = dict.fromkeys(password_hashes, '')

    for word in wordlist:
        word_raw = word.rstrip()
        word_hash = sha256_hex(word_raw.encode('utf-8'))

        if word_hash in passwords_dict:
            print('hash: ', word_hash)
            print('word: ', word_raw)
            passwords_dict[word_hash] = word_raw

        if '' not in passwords_dict.values():
            break
    return passwords_dict


if __name__ == "__main__":
    main()
