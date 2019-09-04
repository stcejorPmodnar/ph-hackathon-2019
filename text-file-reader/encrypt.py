import math
import itertools
import random
import os


cwd = os.getcwd()
user_name = cwd.split('/')[1]

chars = [',', ';', '#', '%', '*', '`', '~', '}', ']']
keys = [
    'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f',
    'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm', 'Q', 'W',
    'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'A', 'S', 'D', 'F', 'G', 'H',
    'J', 'K', 'L', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', '', '1', '2', '3', '4',
    '5', '6', '7', '8', '9', '0', '!', '@', '#', '$', '%', '^', '&', '*', '(',
    ')', '-', '_', '+', '=', '[', ']', '{', '}', '\n', '\t', '|', ':', ';',
    '\'', '"', '<', ',', '.', '>', '/', '?', '`', '~', '\\', ' '
    ]


def insert(list1, list2):
    indexes = [i for i in range(len(list2))]
    lists = [list1]

    for i in list2:
        number = random.choice(indexes)
        b = lists[-1][:]
        b.insert(number, i)
        lists.append(b)

    return ''.join([str(i) for i in lists[-1]])


def convert(number, base):
    """ Converts the number from base 10 to any base less than 10 """
    try:
        first_exp = int(math.log(number, base))
    except ValueError:
        first_exp = int(str(math.log(number, base)).split('.')[0])
    exp = sorted(range(int(first_exp)+1), reverse=True)
    r = number
    values = []
    if number == 0:
        values = [0]
    elif number == 1:
        values = [1]
    else:
        for i in exp:
            values.append(r // base ** i)
            r = r % (base ** i)
    return int(''.join([str(i) for i in values]))


def undo_convert(number, base):
    """ Converts a number in any base less than 10 to base 10 """
    digits = [int(i) for i in list(str(number))]
    base10 = 0
    places = sorted(range(len(digits)), reverse=True)
    for i in range(len(digits)):
        base10 += (base**places[i]) * digits[i]
    return base10


def encrypt(message):
    """ Self-developed encryption method that uses base conversion """
    base = random.randint(3, 9)
    number_list = []
    for i in message:
        number_list.append(keys.index(i)+1)
    converted_number_list = []
    for i in number_list:
        converted_number_list.append(convert(i, base))
    encryption_list = []
    for number in converted_number_list:
        cur = []
        for digit in str(number):
            cur.append(chars[int(digit)])
        encryption_list.append(cur)
    string_encryption_list = []
    for i in encryption_list:
            string_encryption_list.append(''.join([str(x) for x in i]))
    converted_base_number = convert(123, base)
    encrypted_base_list = []
    for i in str(converted_base_number):
        if i == '0':
            encrypted_base_list.append('?')
        elif i == '1':
            encrypted_base_list.append('{')
        elif i == '2':
            encrypted_base_list.append('[')
        elif i == '3':
            encrypted_base_list.append('/')
        elif i == '4':
            encrypted_base_list.append('$')
        elif i == '6':
            encrypted_base_list.append('@')
        elif i == '7':
            encrypted_base_list.append('>')
    return insert(list('|'.join(string_encryption_list)), encrypted_base_list)

def decrypt(message):
    """ decrypts any message encrypted with the encrypt(message) function """
    message_list = list(message)
    number_chars = []
    for i in message_list:
        if i in ['?', '{', '[', '/', '$', '@', '>']:
            number_chars.append(i)
    arrangements = [i for i in itertools.permutations(number_chars, len(number_chars))]
    base = 0
    if ('{', '$', '@') in arrangements:
        base = 9
    elif ('{', '>', '/') in arrangements:
        base = 8
    elif ('[', '/', '$') in arrangements:
        base = 7
    elif ('/', '[', '/') in arrangements:
        base = 6
    elif ('$', '$', '/') in arrangements:
        base = 5
    elif ('{', '/', '[', '/') in arrangements:
        base = 4
    elif ('{', '{', '{', '[', '?') in arrangements:
        base = 3
    for i in number_chars:
        message_list.remove(i)
    chars_list = ''.join(message_list).split('|')
    chars_list_list = [list(i) for i in chars_list]
    char_numbers = []
    for i in chars_list_list:
        char_numbers.append([chars.index(x) for x in i])
    base10_char_numbers = []
    for i in char_numbers:
        base10_char_numbers.append(undo_convert(int(''.join([str(x) for x in i])), base))
    decrypted_list = [keys[i-1] for i in base10_char_numbers]
    return ''.join(decrypted_list)