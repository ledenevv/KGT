import math
from sympy import isprime, gcd

# Функция для проверки, является ли число простым
def check_prime(n):
    return isprime(n)

# Функция для вычисления функции Эйлера φ(n)
def euler_totient(p, q):
    return (p - 1) * (q - 1)

# Функция для поиска e, взаимно простого с φ(n)
def find_e(phi_n):
    e = 3
    while e < phi_n:
        if gcd(e, phi_n) == 1:
            return e
        e += 2  # обычно берут нечетные числа
    return None

# Расширенный алгоритм Евклида для нахождения мультипликативного обратного
def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    gcd_val, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd_val, x, y

# Функция для вычисления d
def find_d(e, phi_n):
    _, x, _ = extended_gcd(e, phi_n)
    return x % phi_n

# Функция для шифрования сообщения
def encrypt_message(message, e, n):
    encrypted_message = [(ord(char) - 65 + 1) ** e % n for char in message]
    return encrypted_message

# Функция для дешифрования сообщения
def decrypt_message(encrypted_message, d, n):
    decrypted_message = [chr((char ** d % n) + 65 - 1) for char in encrypted_message]
    return ''.join(decrypted_message).lower()

# Основная функция взаимодействия с пользователем
def main():
    print("RSA Шифратор / Дешифратор")
    
    # Выбор действия
    action = input("Выберите действие (шифровать / дешифровать): ").strip().lower()
    if action not in ["шифровать", "дешифровать"]:
        print("Некорректное действие. Пожалуйста, выберите 'шифровать' или 'дешифровать'.")
        return

    # Ввод чисел p и q и проверка их на простоту
    p = int(input("Введите простое число p: "))
    q = int(input("Введите простое число q: "))
    if not (check_prime(p) and check_prime(q)):
        print("Оба числа должны быть простыми. Пожалуйста, попробуйте снова.")
        return

    # Вычисление n и φ(n)
    n = p * q
    phi_n = euler_totient(p, q)

    # Поиск e и d
    e = find_e(phi_n)
    if not e:
        print("Не удалось найти подходящее значение для e.")
        return
    d = find_d(e, phi_n)

    # Вывод ключей
    print(f"Открытый ключ: (e={e}, n={n})")
    print(f"Закрытый ключ: (d={d}, n={n})")

    # Запрос на ввод сообщения
    if action == "шифровать":
        message = input("Введите сообщение для шифрования: ").upper()
        encrypted_message = encrypt_message(message, e, n)
        print("Зашифрованное сообщение:", encrypted_message)
    elif action == "дешифровать":
        encrypted_message = input("Введите зашифрованное сообщение (числа через пробел): ")
        encrypted_message = list(map(int, encrypted_message.split()))
        decrypted_message = decrypt_message(encrypted_message, d, n)
        print("Расшифрованное сообщение:", decrypted_message)

if __name__ == "__main__":
    main()
