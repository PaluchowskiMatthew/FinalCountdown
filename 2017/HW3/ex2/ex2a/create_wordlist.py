import itertools
import string


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

def create_wordlist(file_name, word_limit=6):
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

def main():
    create_wordlist('wordlist.txt', 6)

if __name__ == "__main__":
    main()
