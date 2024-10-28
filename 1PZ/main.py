import string

# Шифр Цезаря
def caesar_cipher(text, shift, decrypt=False):
    # Изменяем направление сдвига, если дешифруем
    shift = -shift if decrypt else shift
    result = []
    for char in text:
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            result.append(chr((ord(char) + shift - offset) % 26 + offset))
        else:
            result.append(char)
    return ''.join(result)

# Шифр простой замены
def substitution_cipher(text, key, decrypt=False):
    alphabet = string.ascii_lowercase
    if decrypt:
        trans_table = str.maketrans(key, alphabet)
    else:
        trans_table = str.maketrans(alphabet, key)
    return text.translate(trans_table)

# Шифр Вижинера
def vigenere_cipher(text, keyword, decrypt=False):
    keyword = (keyword * (len(text) // len(keyword) + 1))[:len(text)]
    result = []
    for i, char in enumerate(text):
        if char.isalpha():
            shift = ord(keyword[i].lower()) - 97
            shift = -shift if decrypt else shift
            offset = 65 if char.isupper() else 97
            result.append(chr((ord(char) + shift - offset) % 26 + offset))
        else:
            result.append(char)
    return ''.join(result)

# Шифр простой перестановки
def transposition_cipher(text, key, decrypt=False):
    if decrypt:
        columns = [''] * len(key)
        col_len = len(text) // len(key)
        extra = len(text) % len(key)
        positions = sorted(range(len(key)), key=lambda x: key[x])
        start = 0
        for i, pos in enumerate(positions):
            end = start + col_len + (1 if i < extra else 0)
            columns[pos] = text[start:end]
            start = end
        return ''.join(''.join(x) for x in zip(*columns))
    else:
        columns = [''] * len(key)
        positions = sorted(range(len(key)), key=lambda x: key[x])
        for i, char in enumerate(text):
            columns[positions[i % len(key)]] += char
        return ''.join(columns)

# Шифр усложненной перестановки
def complex_transposition_cipher(text, key, decrypt=False):
    n = len(key)
    matrix = [''] * n
    if decrypt:
        ordered_key = sorted(range(n), key=lambda i: key[i])
        chunk_size = len(text) // n
        chunks = [text[i * chunk_size:(i + 1) * chunk_size] for i in range(n)]
        for i, index in enumerate(ordered_key):
            matrix[index] = chunks[i]
        return ''.join(''.join(x) for x in zip(*matrix))
    else:
        ordered_key = sorted(range(n), key=lambda i: key[i])
        for i, char in enumerate(text):
            matrix[i % n] += char
        return ''.join(matrix[i] for i in ordered_key)

def main():
    text = input("Введите текст: ")
    action = input("Выберите действие (шифровать/дешифровать): ").strip().lower()
    if action not in ["шифровать", "дешифровать"]:
        print("Неверное действие")
        return
    
    decrypt = action == "дешифровать"
    print("Методы шифрования:\n1. Шифр Цезаря\n2. Шифр простой замены\n3. Шифр Вижинера\n4. Шифр простой перестановки\n5. Шифр усложненной перестановки")
    choice = input("Выберите метод (1-5): ").strip()

    if choice == "1":
        shift = int(input("Введите сдвиг для шифра Цезаря: "))
        result = caesar_cipher(text, shift, decrypt)

    elif choice == "2":
        key = input("Введите 26-символьный ключ для простой замены: ").lower()
        if len(set(key)) != 26 or not all(c.isalpha() for c in key):
            print("Некорректный ключ. Должен содержать 26 уникальных букв.")
            return
        result = substitution_cipher(text, key, decrypt)

    elif choice == "3":
        keyword = input("Введите ключевое слово для шифра Вижинера: ").lower()
        result = vigenere_cipher(text, keyword, decrypt)

    elif choice == "4":
        key = input("Введите ключ (например, '3124' для 4-символьного ключа): ")
        if not key.isdigit():
            print("Некорректный ключ. Должен быть числовым.")
            return
        result = transposition_cipher(text, key, decrypt)

    elif choice == "5":
        key = input("Введите ключ (например, '3124' для 4-символьного ключа): ")
        if not key.isdigit():
            print("Некорректный ключ. Должен быть числовым.")
            return
        result = complex_transposition_cipher(text, key, decrypt)

    else:
        print("Некорректный выбор.")
        return

    print("Результат:", result)

if __name__ == "__main__":
    main()
