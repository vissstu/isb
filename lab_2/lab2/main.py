import os

from test_nist import frequency_bitwise_test, identical_consecutive_bits, longest_tes_sequence


def load_sequences_from_files():
    """
    Загружает бинарные последовательности из двух файлов.
    Возвращает: Две строки, представляющие бинарные последовательности.
    """
    cpp_sequence = ""
    java_sequence = ""

    # Проверяем наличие обоих файлов перед продолжением
    if os.path.exists("cpp_binary_sequence.txt"):
        with open("cpp_binary_sequence.txt", "r") as file:
            cpp_sequence = file.read().strip()
    else:
        print("Файл 'cpp_binary_sequence.txt' не найден.")

    if os.path.exists("java_binary_sequence.txt"):
        with open("java_binary_sequence.txt", "r") as file:
            java_sequence = file.read().strip()
    else:
        print("Файл 'java_binary_sequence.txt' не найден.")

    return cpp_sequence, java_sequence


def save_results_to_file(filename, cpp_sequence, java_sequence):
    """
    Выполняет три теста NIST на предоставленные последовательности и записывает результаты в указанный файл.
    Параметры:
        filename (str): Имя файла, в который будут записаны результаты.
        cpp_sequence (str): Бинарная последовательность, созданная на C++.
        java_sequence (str): Бинарная последовательность, созданная на Java.
    """
    with open(filename, "w") as file:
        # Выполнение тестов для последовательности, созданной на C++
        freq_cpp = frequency_bitwise_test(cpp_sequence)
        ident_cpp = identical_consecutive_bits(cpp_sequence)
        longest_cpp = longest_tes_sequence(cpp_sequence)

        # Запись результатов для C++ последовательности
        file.write("Results for C++ sequence:\n")
        file.write(f"Frequency Bitwise Test: {freq_cpp:.8f}\n") #Частотный побитовый тест
        file.write(f"Identical Consecutive Bits Test: {ident_cpp:.8f}\n") #Тест на смежные одинаковые биты
        file.write(f"Longest TES Sequence Test: {longest_cpp:.8f}\n\n") #Тест на самую длинную последовательность единиц в блоке

        # Выполнение тестов для последовательности, созданной на Java
        freq_java = frequency_bitwise_test(java_sequence)
        ident_java = identical_consecutive_bits(java_sequence)
        longest_java = longest_tes_sequence(java_sequence)

        # Запись результатов для Java последовательности
        file.write("Results for Java sequence:\n")
        file.write(f"Frequency Bitwise Test: {freq_java:.8f}\n") #Частотный побитовый тест
        file.write(f"Identical Consecutive Bits Test: {ident_java:.8f}\n") #Тест на смежные одинаковые биты
        file.write(f"Longest TES Sequence Test: {longest_java:.8f}\n") #Тест на самую длинную последовательность единиц в блоке


def main():
    """
    Основная точка входа в программу.
    """
    cpp_sequence, java_sequence = load_sequences_from_files()

    # Проверяем, что обе последовательности успешно загружены
    if not cpp_sequence:
        print("Нет доступной последовательности для C++.")
    if not java_sequence:
        print("Нет доступной последовательности для Java.")

    if cpp_sequence and java_sequence:
        save_results_to_file("test_results.txt", cpp_sequence, java_sequence)
        print("Результаты успешно записаны в файл 'test_results.txt'.")


if __name__ == "__main__":
    main()
