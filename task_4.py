# Задание 4. СМО с ограничением на время ожидания в очереди («нетерпеливые» заявки)

import math

# НАЧАЛЬНЫЕ УСЛОВИЯ
LAMBDA = 0.3          # интенсивность поступления заявок, заявок/мин
T_SERVICE = 5.0       # среднее время обслуживания, мин
K = 1                 # число каналов
OMEGA = 15.0          # максимальное время ожидания в очереди, мин
C = 250.0             # доход от одной обслуженной заявки, у.е.
EPS = 0.01            # точность вычислений

# ФУНКЦИЯ РАСЧЁТА ХАРАКТЕРИСТИК ОДНОКАНАЛЬНОЙ СМО С ОГРАНИЧЕННЫМ ВРЕМЕНЕМ ОЖИДАНИЯ
def service_with_time_limit(lambda_rate, mu, beta, eps):
    """
    Расчёт характеристик одноканальной СМО с ограниченным временем ожидания
    Возвращает:
        p0, probs, k_bar, Q, P_uhod, L_och, L_sist, T_och, T_ob, T_sist, nu_uhod, loss
    """
    rho = lambda_rate / mu

    summ = 0.0
    term = rho / (1.0 + beta)          # m = 1
    m = 1
    while term > eps:
        summ += term
        m += 1
        term *= rho / (1.0 + m * beta)

    # Вероятность p0 
    p0 = 1.0 / (1.0 + rho + rho * summ)

    # Предельные вероятности состояний 
    probs = [p0]          # p0
    p1 = rho * p0
    probs.append(p1)      # p1
    term = rho / (1.0 + beta)
    m = 1
    while True:
        p_next = rho * term * p0
        if p_next < eps:
            break
        probs.append(p_next)
        m += 1
        term *= rho / (1.0 + m * beta)

    # Основные характеристики 
    k_bar = 1.0 - p0                     # среднее число занятых каналов
    Q = k_bar / rho                      # вероятность обслуживания
    P_uhod = 1.0 - Q                     # вероятность ухода
    L_och = (rho - k_bar) / beta         # средняя длина очереди
    L_ob = k_bar                         # среднее число заявок под обслуживанием
    L_sist = L_och + L_ob                # среднее число заявок в системе
    T_och = L_och / lambda_rate          # среднее время ожидания
    T_ob = L_ob / lambda_rate            # среднее время обслуживания
    T_sist = T_och + T_ob                # среднее время пребывания
    omega_int = beta * mu                # интенсивность ухода из очереди
    nu_uhod = omega_int * L_och          # интенсивность ухода заявок
    loss = C * nu_uhod                   # средние потери дохода в минуту

    return p0, probs, k_bar, Q, P_uhod, L_och, L_ob, L_sist, T_och, T_ob, T_sist, nu_uhod, loss


def main():
    mu = 1.0 / T_SERVICE                    
    omega_int = 1.0 / OMEGA     # интенсивность ухода заявки из очереди                 
    beta = omega_int / mu                       
    rho = LAMBDA / mu

    print("ОДНОКАНАЛЬНАЯ СМО С ОГРАНИЧЕННЫМ ВРЕМЕНЕМ ОЖИДАНИЯ")
    print("Исходные данные:")
    print(f"  lambda = {LAMBDA} заявок/мин")
    print(f"  t = {T_SERVICE} мин")
    print(f"  k = {K}")
    print(f"  omega = {OMEGA} мин")
    print(f"  C = {C} у.е./заявка")
    print(f"  eps = {EPS}")
    print(f"  mu = {mu:.5f} заявок/мин")
    print(f"  rho = λ/μ = {rho:.5f}")
    print(f"  omega_инт = {omega_int:.5f} заявок/мин")
    print(f"  beta = ω_инт/μ = {beta:.5f}")

    p0, probs, k_bar, Q, P_uhod, L_och, L_ob, L_sist, T_och, T_ob, T_sist, nu_uhod, loss = \
        service_with_time_limit(LAMBDA, mu, beta, EPS)

    print("-" * 70)
    print("ПРЕДЕЛЬНЫЕ ВЕРОЯТНОСТИ СОСТОЯНИЙ:")
    print("-" * 70)
    for i, p in enumerate(probs):
        if i == 0:
            desc = "канал свободен"
        elif i == 1:
            desc = "1 канал занят (очереди нет)"
        else:
            desc = f"{i} заявок в системе (1 канал + {i-1} в очереди)"
        print(f"  p{i} = {p:.3f}  – {desc}")
    print("-" * 70)

    print("ОСНОВНЫЕ ХАРАКТЕРИСТИКИ СМО:")
    print("-" * 70)
    print(f"  Вероятность обслуживания Q         = {Q:.3f}  ({Q*100:.3f}%)")
    print(f"  Вероятность ухода P_ух             = {P_uhod:.3f}  ({P_uhod*100:.3f}%)")
    print(f"  Среднее число занятых каналов k   = {k_bar:.3f}")
    print(f"  Среднее число заявок в очереди L_оч = {L_och:.3f}")
    print(f"  Среднее число заявок под обслуживанием L_об= {L_ob:.3f}")
    print(f"  Среднее число заявок в системе L_сист = {L_sist:.3f}")
    print(f"  Среднее время ожидания T_оч        = {T_och:.3f} мин")
    print(f"  Среднее время обслуживания T_об    = {T_ob:.3f} мин")
    print(f"  Среднее время пребывания T_сист    = {T_sist:.3f} мин")
    print(f"  Интенсивность ухода v_уход         = {nu_uhod:.3f} заявок/мин")
    print(f"  Средние потери дохода в минуту     = {loss:.3f} у.е./мин ({loss * 60:.3f} у.е./час)")

if __name__ == "__main__":
    main()