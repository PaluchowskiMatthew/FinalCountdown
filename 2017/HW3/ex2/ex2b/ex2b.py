import hashlib
import itertools
import copy

password_hashes = ['fa686d5bb544d6ff480a2f44ea93ff73a410852404ce80e611bd26d99c616f82',
                   '4742b74c53d128418a731fe6e02afe40ebfb1b78e25d79f5895fb96d814ff634',
                   '9cedad0f9d6e35d9b6c92b0993a191ffd31c9b5f6cdc664c81af523a16df45d6',
                   'e0c6ad42ec4a5303f063ac1df4cb4ddf96e0df622d3954eab0ac7b860be749db',
                   '2b02453faa881bca83cfce25fd5f3b5a3f43d161dc609d62e0b712f32d846fda',
                   '8dd4e19bfb397affe3347906ce0e756550d502cb59106aae653c0d568a81fd99',
                   'd3cf0c242ab91bfb516d5a658b340df60a9bccf5f4a73e3826d84310500876b0',
                   '572b728572b9d736c2ef58d5a9612c38e7ee66085f76eca46f923495246d573e',
                   '0ee504b19e581c6594819210dd61c19d4f5459419b0be208ff05dce513a1406d',
                   '1111816024baff12c7f1c59e6f4b4d96f5dba089e23aec939b084c1490463182']

def sha256_hex(text):
    return hashlib.sha256(text).hexdigest()

def find_occurances(string, chr):
    return [i for i, letter in enumerate(string) if letter == chr]

def all_letters_to_number(word, letter, number):
    letter_occurances = find_occurances(word, letter)
    word_chars = list(word)
    for ind in letter_occurances:
        word_chars[ind] = str(number)
    return ["".join(word_chars)]

def letter_to_number(word, letter, number):
    word_occurances = find_occurances(word, letter)

    all_combinations = []
    for L in range(1, len(word_occurances)+1):
      for subset in itertools.combinations(word_occurances, L):
        # all_combinations.append(subset)
        word_chars = list(word)
        for ind in list(subset):
            word_chars[ind] = str(number)
        all_combinations.append("".join(word_chars))
    return all_combinations

def word_modifications(word):
    modified_words = [word, word.title()]

    words_to_modify = copy.deepcopy(modified_words)
    for word in words_to_modify:
        modified_words += all_letters_to_number(word, 'e', 3)

    words_to_modify = copy.deepcopy(modified_words)
    for to_modify in words_to_modify:
        modified_words += all_letters_to_number(to_modify, 'o', 0)

    words_to_modify = copy.deepcopy(modified_words)
    for to_modify in words_to_modify:
        modified_words += all_letters_to_number(to_modify, 'i', 1)

    titleized = []
    for word in modified_words:
        titleized.append(word.title())
    final = list(set(modified_words + titleized))

    return final

def main():

    wordlist = open('rockyou.txt', 'r')
    passwords_dict = dict.fromkeys(password_hashes, '')

    for word in wordlist:
        word_raw = word.rstrip()

        if not word_raw.isalnum():
            continue

        modified_words = word_modifications(word_raw)

        for moded_word in modified_words:
            word_hash = sha256_hex(moded_word.encode('utf-8'))

            if word_hash in passwords_dict:
                print('hash: ', word_hash)
                print('word: ', moded_word)
                passwords_dict[word_hash] = moded_word

            if '' not in passwords_dict.values():
                break
    return passwords_dict


if __name__ == "__main__":
    main()
