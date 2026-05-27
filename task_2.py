# Задание 2. Многоканальная СМО с неограниченной очередью

import math
import matplotlib.pyplot as plt

# НАЧАЛЬНЫЕ УСЛОВИЯ (в соответствии с вариантом)
LAMBDA_DAILY = 120          # Интенсивность поступления заявок в сутки
T_SERVICE_MIN = 8           # Среднее время обслуживания (минут)
ALPHA = 4                   # Коэффициент в функции затрат
N_QUEUE = 2                 # Число заявок в очереди для расчёта вероятности

# ФУНКЦИЯ РАСЧЁТА ХАРАКТЕРИСТИК МНОГОКАНАЛЬНОЙ СМО С НЕОГРАНИЧЕННОЙ ОЧЕРЕДЬЮ
def service_with_queue(lambda_rate, mu, k):
    """
    Возвращает для многоканальной СМО с неограниченной очередью:
    p0, L_оч, L_сист, T_оч, T_сист, probs (список p0...p_k).
    """
    rho = lambda_rate / mu
    if rho / k >= 1:
        raise ValueError("Система нестационарна: очередь будет расти до бесконечности")
    
    summ = 0.0
    for i in range(k):
        summ += (rho ** i) / math.factorial(i)
    last_term = (rho ** k) / math.factorial(k) * (1.0 / (1.0 - rho / k))
    p0 = 1.0 / (summ + last_term)
    
    L_och = (rho ** (k + 1) * p0) / (k * math.factorial(k) * (1 - rho / k) ** 2)
    L_sist = L_och + rho
    T_och = L_och / lambda_rate
    T_sist = L_sist / lambda_rate
    
    probs = [0.0] * (k + 1)
    probs[0] = p0
    for i in range(1, k + 1):
        probs[i] = (rho ** i / math.factorial(i)) * p0
    
    return p0, L_och, L_sist, T_och, T_sist, probs

# Функция поиска оптимального числа каналов kopt
def find_optimal_k(lambda_rate, t_service, kmin, alpha, kmax_offset=10):
    """
    Находит оптимальное число каналов по минимуму затрат
    """
    kmax_search = min(kmin + kmax_offset, 20)
    best_k = kmin
    best_C = float('inf')
    k_vals = []
    C_vals = []
    
    for k in range(kmin, kmax_search + 1):
        C_k = k / lambda_rate + alpha * t_service
        k_vals.append(k)
        C_vals.append(C_k)
        if C_k < best_C:
            best_C = C_k
            best_k = k
    return best_k, best_C, k_vals, C_vals

# Вывод характеристик для заданного k (используется для kmin и kopt)
def print_characteristics(k, p0, L_och, L_sist, T_och, T_sist):
    """Печатает основные показатели СМО для указанного числа каналов"""
    print(f"ХАРАКТЕРИСТИКИ ОБСЛУЖИВАНИЯ ПРИ k = {k}")
    print("-" * 70)
    print(f"    Вероятность свободного состояния p0 = {p0:.3f}")
    print(f"    Среднее число заявок в очереди L_оч = {L_och:.3f}")
    print(f"    Среднее число заявок в системе L_сист = {L_sist:.3f}")
    print(f"    Среднее время ожидания в очереди T_оч = {T_och:.3f} час = {T_och*60:.1f} мин")
    print(f"    Среднее время пребывания в системе T_сист = {T_sist:.3f} час = {T_sist*60:.1f} мин")
    print("-" * 70)

# Сравнение характеристик при kmin и kopt
def compare_characteristics(kmin, p0_min, L_och_min, T_och_min, T_sist_min,
                            kopt, p0_opt, L_och_opt, T_och_opt, T_sist_opt):
    """Выводит таблицу сравнения показателей."""
    print("\nСРАВНЕНИЕ ХАРАКТЕРИСТИК ПРИ kmin И kopt:")
    print("-" * 70)
    print(f"{'Показатель':<35} {'kmin = ' + str(kmin):<20} {'kopt = ' + str(kopt):<20}")
    print("-" * 70)
    print(f"{'Вероятность p0':<35} {p0_min:<20.3f} {p0_opt:<20.3f}")
    print(f"{'Средняя очередь L_оч':<35} {L_och_min:<20.3f} {L_och_opt:<20.3f}")
    print(f"{'Среднее время T_оч, мин':<35} {T_och_min*60:<20.1f} {T_och_opt*60:<20.1f}")
    print(f"{'Среднее время T_сист, мин':<35} {T_sist_min*60:<20.1f} {T_sist_opt*60:<20.1f}")
    print("-" * 70)

# Вероятность того, что в очереди не более N заявок
def prob_queue_not_more_than(k, p0, rho, N):
    """
    Вычисляет P(очередь ≤ N) для системы с k каналами,
    используя p0 и ρ.
    """
    max_state = k + N
    prob = 0.0
    # Вероятности для состояний 0..k (без очереди)
    for n_state in range(k + 1):
        if n_state <= k:
            prob += (rho ** n_state / math.factorial(n_state)) * p0
    # Для состояний k+1 .. k+N (с очередью)
    for n_state in range(k + 1, max_state + 1):
        r = n_state - k
        term = (rho ** n_state) / (math.factorial(k) * (k ** r)) * p0
        prob += term
    return prob

# Построение графика затрат C(k)
def plot_cost(k_vals, C_vals, best_k, lambda_rate, alpha):
    """Строит график C(k) и отмечает точку оптимума"""
    plt.figure(figsize=(8, 5))
    plt.plot(k_vals, C_vals, 'bo-', linewidth=2, markersize=6, label='C(k)')
    plt.axvline(x=best_k, color='r', linestyle='--', linewidth=1.5, label=f'kopt = {best_k}')
    plt.xlabel('Число каналов k')
    plt.ylabel('Затраты C(k)')
    plt.title(f'Зависимость затрат от числа каналов (lambda = {lambda_rate:.3f} час, alpha = {alpha})')
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.show()

# ОСНОВНАЯ ПРОГРАММА
def main():
    # 1. Перевод величин в часы
    lambda_rate = LAMBDA_DAILY / 24.0
    mu = 60.0 / T_SERVICE_MIN
    rho = lambda_rate / mu
    t_service_hours = T_SERVICE_MIN / 60.0   

    # 2. Минимальное число каналов
    kmin = int(math.floor(rho)) + 1

    # Вывод исходных данных
    print("МНОГОКАНАЛЬНАЯ СМО С НЕОГРАНИЧЕННОЙ ОЧЕРЕДЬЮ")
    print("Исходные данные:")
    print(f"    lambda = {LAMBDA_DAILY} заявок/сутки = {lambda_rate:.5f} заявок/час")
    print(f"    t_обсл = {T_SERVICE_MIN} мин = {T_SERVICE_MIN/60:.5f} час")
    print(f"    mu = {mu:.5f} заявок/час")
    print(f"    rho = {rho:.5f}")
    print(f"    alpha = {ALPHA}")
    print(f"    n (для вероятности в очереди) = {N_QUEUE}")
    print("-" * 70)
    print(f"Минимальное число каналов: kmin = {kmin}")
    print("-" * 70)

    # 3. Расчёт характеристик при kmin
    p0_min, L_och_min, L_sist_min, T_och_min, T_sist_min, probs_min = service_with_queue(lambda_rate, mu, kmin)
    print_characteristics(kmin, p0_min, L_och_min, L_sist_min, T_och_min, T_sist_min)

    # 4. Предельные вероятности состояний (для kmin)
    print("ПРЕДЕЛЬНЫЕ ВЕРОЯТНОСТИ СОСТОЯНИЙ (k =", kmin, "):")
    print("-" * 70)
    prob_sum = 0.0
    for i, p in enumerate(probs_min):
        if i == 0:
            desc = "все каналы свободны"
        elif i == 1:
            desc = "1 канал занят"
        else:
            desc = f"{i} канала занято" if i <= 4 else f"{i} каналов занято"
        print(f"    p{i} = {p:.3f}  – вероятность того, что {desc}")
        prob_sum += p
    print("-" * 70)

    # 5. Оптимизация
    print("ОПТИМИЗАЦИЯ ПО ФУНКЦИИ ЗАТРАТ")
    print("Минимизируем C(k) = k / lambda + alpha * T_обсл")
    print(f"lambda = {lambda_rate:.3f} заявок/час, alpha = {ALPHA}")
    print("=>")
    best_k, best_C, k_vals, C_vals = find_optimal_k(lambda_rate, t_service_hours, kmin, ALPHA)
    print(f"Оптимальное число каналов: kopt = {best_k}")
    print(f"Минимальное значение затрат C = {best_C:.3f}")

    # 6. Характеристики при kopt
    if best_k == kmin:
        print("\nХарактеристики при kopt совпадают с характеристиками при kmin")
        p0_opt, L_och_opt, L_sist_opt, T_och_opt, T_sist_opt = p0_min, L_och_min, L_sist_min, T_och_min, T_sist_min
    else:
        p0_opt, L_och_opt, L_sist_opt, T_och_opt, T_sist_opt, _ = service_with_queue(lambda_rate, mu, best_k)
        print_characteristics(best_k, p0_opt, L_och_opt, L_sist_opt, T_och_opt, T_sist_opt)

    # 7. Сравнение характеристик
    compare_characteristics(kmin, p0_min, L_och_min, T_och_min, T_sist_min,
                            best_k, p0_opt, L_och_opt, T_och_opt, T_sist_opt)

    # 8. Вероятность очереди не более N_QUEUE заявок (при kopt)
    prob = prob_queue_not_more_than(best_k, p0_opt, rho, N_QUEUE)
    print("ВЕРОЯТНОСТНЫЕ ХАРАКТЕРИСТИКИ ОЧЕРЕДИ")
    print("-" * 70)
    print(f"При kopt = {best_k} вероятность того, что в очереди находится не более {N_QUEUE} заявок:")
    print(f"    P(очередь <= {N_QUEUE}) = {prob:.3f} ({prob*100:.1f}%)")

    # 9. Построение графика
    plot_cost(k_vals, C_vals, best_k, lambda_rate, ALPHA)


if __name__ == '__main__':
    main()