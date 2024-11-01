import random
import string
import time
import itertools  # Импортируем itertools для перебора комбинаций

# Функция для генерации отчета о времени выполнения и количестве проверенных паролей
def generate_report(method, attempts, duration, found_password=None):
    with open("password_recovery_report.txt", "a") as report_file:
        report_file.write(f"Method: {method}\n")
        report_file.write(f"Total attempts: {attempts}\n")
        report_file.write(f"Duration: {duration:.2f} seconds\n")
        if found_password:
            report_file.write(f"Password found: {found_password}\n")
        report_file.write("\n")

# 1. Восстановление пароля с перебором
def password_recovery_brute_force(char_set, max_length, target_password):
    print("Starting brute-force recovery...")
    start_time = time.time()
    attempts = 0

    for length in range(1, max_length + 1):
        for password in ("".join(candidate) for candidate in itertools.product(char_set, repeat=length)):
            attempts += 1
            if password == target_password:  # Проверка угаданного пароля
                duration = time.time() - start_time
                generate_report("Brute-force", attempts, duration, found_password=password)
                print(f"Password '{password}' found after {attempts} attempts in {duration:.2f} seconds.")
                return password  # Возврат найденного пароля
            
            if attempts % 10000 == 0:  # Промежуточный отчет о попытках
                print(f"Attempts: {attempts}")
    
    duration = time.time() - start_time
    generate_report("Brute-force", attempts, duration)
    print("Password recovery completed. Password not found.")
    return None

# 2. Расчет минимальной длины пароля для заданной стойкости
def calculate_min_password_length(A, P, V, T):
    S_star = (V * T) / P
    L = 1
    while A ** L < S_star:
        L += 1
    return L

# 3. Генератор безопасных паролей
def generate_password(length, use_symbols=True):
    char_set = string.ascii_letters + string.digits
    if use_symbols:
        char_set += string.punctuation
    password = ''.join(random.choice(char_set) for _ in range(length))
    
    with open("generated_passwords.txt", "a") as file:
        file.write(password + "\n")
    
    return password

# 4. Пользовательский интерфейс
def user_interface():
    while True:
        print("\n--- Password Security Tool ---")
        print("1. Восстановление пароля (перебор)")
        print("2. Расчет минимальной длины пароля")
        print("3. Генератор пароля")
        print("4. Выход")
        
        choice = input("Выберите опцию: ")
        
        if choice == '1':
            char_set = string.ascii_letters + string.digits
            max_length = int(input("Введите максимальную длину пароля для перебора: "))
            target_password = input("Введите целевой пароль: ")
            password_recovery_brute_force(char_set, max_length, target_password)
        
        elif choice == '2':
            A = int(input("Введите мощность алфавита (количество символов): "))
            P = float(input("Введите вероятность подбора пароля: "))
            V = float(input("Введите скорость подбора паролей в секунду: "))
            T = float(input("Введите срок действия пароля в секундах: "))
            L = calculate_min_password_length(A, P, V, T)
            print(f"Минимальная длина пароля: {L}")
        
        elif choice == '3':
            length = int(input("Введите длину пароля: "))
            use_symbols = input("Использовать символы? (y/n): ").lower() == 'y'
            password = generate_password(length, use_symbols)
            print(f"Сгенерированный пароль: {password}")
        
        elif choice == '4':
            print("Выход из программы.")
            break
        
        else:
            print("Неверный ввод, попробуйте еще раз.")

# Запуск пользовательского интерфейса
if __name__ == "__main__":
    user_interface()
