# Задание 1. Многоканальная СМО с отказами

import math
import matplotlib.pyplot as plt

# НАЧАЛЬНЫЕ УСЛОВИЯ (задаются в соответствии с вариантом)
ALPHA = 3.0                 # Среднее время обслуживания одной заявки (часы)
N_DAILY = 24                # Количество заявок, поступающих в сутки
K = 4                       # Число каналов для расчёта 
TARGET_Q = 0.95             # Требуемая относительная пропускная способность

# ФУНКЦИЯ РАСЧЁТА ВЕРОЯТНОСТИ ОТКАЗА ПО ФОРМУЛЕ ЭРЛАНГА
def erlang(rho, n):
    """
    Возвращает вероятность отказа P_отк и вероятность свободного состояния p0
    для многоканальной СМО с отказами.
    """
    # Сумма ряда для p0
    summ = 0.0
    for k in range(n + 1):
        summ += (rho ** k) / math.factorial(k)

    # Вероятность свободного состояния системы
    p0 = 1.0 / summ

    # Вероятность отказа (все каналы заняты)
    potk = (rho ** n / math.factorial(n)) * p0
    return potk, p0

# ОСНОВНАЯ ПРОГРАММА
def main():
    # 1. Расчёт параметров системы
    mu = 1.0 / ALPHA                     # интенсивность обслуживания (заяв/час)
    lambda_rate = N_DAILY / 24.0         # интенсивность входящего потока (заяв/час)
    rho = lambda_rate / mu               # приведённая интенсивность (трафик)

    print("МНОГОКАНАЛЬНАЯ СМО С ОТКАЗАМИ (аналитический расчёт)")
    print(f"Исходные данные:")
    print(f"    a = {ALPHA} час – среднее время обслуживания")
    print(f"    n = {N_DAILY} заявок/сутки – интенсивность поступления")
    print(f"    k = {K} – число каналов для анализа")
    print(f"    Требование: Q >= {TARGET_Q}")
    print("-" * 70)
    print(f"Расчётные параметры:")
    print(f"    lambda = {lambda_rate:.5f} заяв/час")
    print(f"    mu = {mu:.5f} заяв/час")
    print(f"    rho = {rho:.5f}")
    print("-" * 70)

    # 2. Нахождение минимального числа каналов n_min, при котором Q >= 0.95
    n_min = 1
    while True:
        potk_n, _ = erlang(rho, n_min)
        Q_n = 1 - potk_n
        if Q_n >= TARGET_Q:
            break
        n_min += 1

    print("\nРЕЗУЛЬТАТ ПОИСКА МИНИМАЛЬНОГО ЧИСЛА КАНАЛОВ:")
    print("-" * 70)
    print(f"    При n = {n_min-1}: Q = {1 - erlang(rho, n_min-1)[0]:.5f} (< {TARGET_Q})")
    print(f"    При n = {n_min}:   Q = {1 - erlang(rho, n_min)[0]:.5f} (>= {TARGET_Q})")
    print(f"\nМинимальное число каналов для обеспечения Q >= {TARGET_Q}: n_min = {n_min}")
    print("-" * 70)

    # 3. Расчёт характеристик для заданного числа каналов K = 4
    potk, p0 = erlang(rho, K)
    Q = 1 - potk
    A = lambda_rate * Q
    k_avg = rho * Q
    k_zag = k_avg / K

    print("\nРЕЗУЛЬТАТЫ РАСЧЁТА ДЛЯ ЗАДАННОГО ЧИСЛА КАНАЛОВ k =", K)
    print("-" * 70)
    print(f"    Вероятность отказа P_отк = {potk:.3f} ({potk*100:.2f}%)")
    print(f"    Относительная пропускная способность Q = {Q:.3f} ({Q*100:.2f}%)")
    print(f"    Абсолютная пропускная способность A = {A:.3f} заяв/час")
    print(f"    Среднее число занятых каналов k = {k_avg:.3f}")
    print(f"    Коэффициент загрузки каналов k_заг = {k_zag:.3f}")
    print("-" * 70)

    # 4. Предельные вероятности состояний системы (для k = 4)
    print("\nПРЕДЕЛЬНЫЕ ВЕРОЯТНОСТИ СОСТОЯНИЙ СИСТЕМЫ (n =", K, "):")
    print("-" * 70)
    print(f"    p0 = {p0:.3f}  – вероятность того, что все каналы свободны")
    prob_sum = p0
    for k in range(1, K + 1):
        # p_k = (ρ^k / k!) * p0
        pk = (rho ** k / math.factorial(k)) * p0
        prob_sum += pk
        # Выбор правильного склонения для комментария
        state_desc = f"{k} канал занят" if k == 1 else f"{k} канала занято" if k <= 4 else f"{k} каналов занято"
        print(f"    p{k} = {pk:.3f}  – вероятность того, что {state_desc}")
    print(f"\nКонтроль суммы вероятностей: Ep_k = {prob_sum:.3f} (должно быть равно 1)")

    # 5. Построение графика зависимости Q(n) для n от 1 до 12
    n_values = list(range(1, 13))
    Q_values = []
    for n in n_values:
        potk_n, _ = erlang(rho, n)      # P_отк для n каналов
        Q_values.append(1 - potk_n)     # Q(n)

    plt.figure(figsize=(8, 5))
    plt.plot(n_values, Q_values, 'bo-', linewidth=2, markersize=6, label='Q(n)')
    plt.axhline(y=TARGET_Q, color='r', linestyle='--', linewidth=1.5, label=f'Q = {TARGET_Q}')
    plt.axvline(x=n_min, color='g', linestyle='--', linewidth=1.5, label=f'n_min = {n_min}')
    plt.plot(K, Q, 'rD', markersize=8, label=f'k = {K} (заданное)')
    plt.xlabel('Число каналов n')
    plt.ylabel('Относительная пропускная способность Q')
    plt.title(f'Зависимость Q от числа каналов (rho = {rho:.3f})')
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()