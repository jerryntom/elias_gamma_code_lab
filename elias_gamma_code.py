import math


def calculate_n(m):
    """
    Calculates the smallest integer n such that 2^n >= m.

    :param m: The integer to calculate n for.
    :return: The smallest integer n such that 2^n >= m.
    """

    if m < 1:
        return -1

    return int(math.log(m, 2))


def unary(num):
    """
    Generate a unary representation of a number.

    :param num: The number to represent in unary.
    :return: The unary representation of the number.
    """

    unary_code = ""

    for i in range(0, num - 1):
        unary_code += "0"

    unary_code += "1"

    return unary_code


def binary(num):
    """
    Generate a binary representation of a number.

    :param num: The number to represent in binary.
    :return: The binary representation of the number.
    """

    binary_code = ""

    while num > 0:
        binary_code += str(num % 2)
        num //= 2

    binary_code = binary_code[::-1]

    return binary_code


def truncated_binary(m):
    """
    Generate a truncated binary representation of a number.

    :param m: The number to represent in binary.
    :return: The truncated binary representation of the number.
    """

    binary_code = binary(m)
    truncated_bin = binary_code[1::]
    return truncated_bin


def gamma_code(m):
    """
    Generate a gamma code for a number.

    :param m: The number to represent in gamma code.
    :return: The gamma code for the number.
    """

    return unary(calculate_n(m) + 1) + truncated_binary(m)


def text_entropy(text):
    """
    Calculates the entropy of a text string.

    :param text: The text string to calculate the entropy for.
    :return: The entropy of the text string.
    """

    ascii_symbols = set(text)
    ascii_counter = {}

    for ascii_symbol in ascii_symbols:
        ascii_counter[ascii_symbol] = 0

    for ascii_symbol in text:
        ascii_counter[ascii_symbol] += 1

    text_len = len(text)

    entropy_val = 0

    for k, v in ascii_counter.items():
        entropy_val += (v / text_len) * math.log2(text_len / v)

    return entropy_val


# testing calculation of entropy
print(f"Entropy of 'Ala ma kota, a to lis!' {text_entropy('Ala ma kota, a to lis!'):.2f}")


def gamma_encode(text):
    """
    Encodes a text string using gamma coding.

    :param text: The text string to encode.
    :return: The encoded text string and the list of symbols.
    """

    ascii_symbols = set(text)
    ascii_counter = {}

    for ascii_symbol in ascii_symbols:
        ascii_counter[ascii_symbol] = 0

    for ascii_symbol in text:
        ascii_counter[ascii_symbol] += 1

    characters = [key for key in ascii_counter.keys()]
    values = []

    for key in characters:
        values.append(ascii_counter[key])

    size = len(characters)

    change = False

    for i in range(size - 1):
        for j in range(size - i - 1):
            if values[j] < values[j+1] or (values[j] == values[j+1] and characters[j] > characters[j+1]):
                characters[j], characters[j+1] = characters[j+1], characters[j]
                values[j], values[j+1] = values[j+1], values[j]
                change = True
        if not change:
            break

    encoded_string_gamma = []

    for ascii_symbol in text:
        encoded_string_gamma.append(gamma_code(characters.index(ascii_symbol) + 1))

    len_sum_code = 0

    for encoded_ascii_symbol in encoded_string_gamma:
        len_sum_code += len(encoded_ascii_symbol)

    print("Total number of bits:", len_sum_code)
    print(f"Average number of bits: {len_sum_code / len(encoded_string_gamma):.2f}")

    return encoded_string_gamma, characters


def gamma_decode(encoded_text_gamma):
    """
    Decodes a text string that has been encoded using gamma coding.

    :param encoded_text_gamma: The encoded text string and the list of symbols.
    :return: The decoded text string.
    """

    decoded_text = ""

    for gamma_symbol in encoded_text_gamma[0]:
        decoded_text += encoded_text_gamma[1][gamma_symbol_decode(gamma_symbol) - 1]

    return decoded_text


def gamma_symbol_decode(gamma_code):
    """
    Decodes a gamma code symbol.

    :param gamma_code: The gamma code symbol to decode.
    :return: The decoded symbol.
    """

    first_one_index = gamma_code.index('1')
    gamma_code = gamma_code[first_one_index::]
    num = int(gamma_code, 2)

    return num


# testing gamma encoding and decoding on example of simple sentence

print("Result of gamma encode for 'Ala ma kota, a to lis!':")
res_gamma_encode = gamma_encode("Ala ma kota, a to lis!")

print("Gamma code:")
for i in range(0, len(res_gamma_encode[0])):
    print(res_gamma_encode[0][i])

print('\nCharacters:')
for i in range(0, len(res_gamma_encode[1])):
    if res_gamma_encode[1][i] == ' ':
        print('(space)')
        continue

    print(res_gamma_encode[1][i])


print(f"Result of gamma decode: {gamma_decode(res_gamma_encode)} \n")

# testing gamma encoding and decoding on example of text file
with open("dickens.txt", "r", encoding="utf-8") as f:
    file_text = f.read()

print("Result for dickens.txt")
print(f"Entropy of text file: {text_entropy(file_text):.2f}")
res_gamma_encode_dickens = gamma_encode(file_text)
decoded_text_file = gamma_decode(res_gamma_encode_dickens)
print("Part of decoded text:", decoded_text_file[0:100])
