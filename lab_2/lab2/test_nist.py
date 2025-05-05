import math

from scipy.special import gammaincc as igamc


def frequency_bitwise_test(sequence: str) -> float:
    """
    Выполняет частотный побитовый тест для заданной последовательности.

    Параметры:
        sequence (str): Строка, состоящая из нулей и единиц.
    Возвращает: float: P-значение теста.
    """
    s_n = 0
    n = len(sequence)
    for val in sequence:
        if val == "1":
            s_n += 1 / math.sqrt(n)
        else:
            s_n -= 1 / math.sqrt(n)

    p_value = math.erfc(abs(s_n) / math.sqrt(2))
    return p_value


def identical_consecutive_bits(sequence: str) -> float:
    """
    Выполняет тест на одинаковые подряд идущие биты для заданной последовательности.

    Параметры:
        sequence (str): Строка, состоящая из нулей и единиц.

    Возвращает:
        float: P-значение теста.
    """
    n = len(sequence)
    s_n = sum(val == '1' for val in sequence) / n

    if abs(s_n - 0.5) >= 2 / math.sqrt(n):
        return 0.0

    v_n = sum(sequence[i] != sequence[i + 1] for i in range(n - 1))
    p_value = math.erfc((abs(v_n - 2 * n * s_n * (1 - s_n))) / (2 * math.sqrt(2 * n) * s_n * (1 - s_n)))

    return p_value


def longest_tes_sequence(sequence: str) -> float:
    """
    Выполняет тест на самую длинную последовательность единиц в блоке для заданной последовательности.

    Параметры:
        sequence (str): Строка, состоящая из нулей и единиц.

    Возвращает:
        float: P-значение теста.
    """
    n = len(sequence)
    v = [0, 0, 0, 0]  # v0, v1, v2, v3
    blocks = [sequence[i:i + 8] for i in range(0, n, 8)]
    pi = [0.2148, 0.3672, 0.2305, 0.1875]

    for block in blocks:
        max_block = 0
        max_val = 0
        for val in block:
            if val == "1":
                max_val += 1
                max_block = max(max_val, max_block)
            else:
                max_val = 0

        if max_block <= 1:
            v[0] += 1
        elif max_block == 2:
            v[1] += 1
        elif max_block == 3:
            v[2] += 1
        else:  # если max_block >= 4
            v[3] += 1

    chi_square = sum(((v[i] - 16 * pi[i]) ** 2) / (16 * pi[i]) for i in range(4))
    p_value = igamc(3 / 2, chi_square / 2)
    return p_value
