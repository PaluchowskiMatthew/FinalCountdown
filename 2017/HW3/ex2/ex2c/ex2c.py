import hashlib
import itertools
import copy

password_hashes = ['a39b2f73b58b1b9a822a061bc11497c0df8a5d52be39d61a4e34fa318fbda796',
                   '3e60aa26d2e6a43af15b38f0d30ec4c32d569772664f1ab241b488a9137a3c7e',
                   'd899970d6b5829a10455df736499edb65dba34c557e4e9e648e824dea9970007',
                   '25e8b47e5852eeea060b04e4499ba1a125e700d365820007bae7a3042c3d3433',
                   '82687c758c56b7355d0376d2ca73538b8bfdb2a4ca5dfaa436a0dce40abc5064',
                   'e36a677f15c8615793ca770570ad37f9abbb211d3b191a1ae8bd50327aed6520',
                   '0ca21a4f23a716c8ce65a19367148532420db6390389b083aaf2bc6d569ab9bf',
                   'fd05789594abc93c74d756e4de0ee37ccbce5324fa12d960d2ec81a60ddefba5',
                   '13fe7430b5adc879dbf9323480a120b097c637a81c8363aa024224ee4f529496',
                   'bf34bf328383e82b5a4e1633950d5ab3064442c58c693d5680dddbd8fb6f71e6']


salts = ['96', 'ed', '57', '4b', 'a7', '7d', '3d', '76', '65', '4f']


def sha256_hex(text):
    return hashlib.sha256(text).hexdigest()

def word_salting(word):
    return [word + salt for salt in salts]

def main():

    wordlist = open('../rockyou.txt', 'r')
    passwords_dict = dict.fromkeys(password_hashes, '')

    for word in wordlist:
        word_raw = word.rstrip()

        if not word_raw.isalnum():
            continue

        salted_words = word_salting(word_raw)

        for ind, salted_word in enumerate(salted_words):
            word_hash = sha256_hex(salted_word.encode('utf-8'))

            if word_hash in passwords_dict:
                if password_hashes[ind] == word_hash:
                    print('hash: ', word_hash)
                    print('word: ', salted_word)
                    passwords_dict[word_hash] = salted_word

            if '' not in passwords_dict.values():
                break
    return passwords_dict


if __name__ == "__main__":
    main()
