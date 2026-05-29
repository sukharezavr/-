import numpy as np
import matplotlib.pyplot as plt

print('ЭТАП 1')
# Данные из Таблицы 1

rho = 2700.0  # кг/м^3

# Скорости (м/с)
v1 = 6.24e3
v2 = 3.04e3
v3 = 3.04e3
v4 = 5.81e3
v5 = 2.92e3
v6 = 5.48e3
v7 = 3.01e3

# Измерения (ρv² в ГПа)
C11 = rho * v1**2 / 1e9
C66 = rho * v2**2 / 1e9
C55 = rho * v3**2 / 1e9
C22 = rho * v4**2 / 1e9
C44 = rho * v5**2 / 1e9
C33 = rho * v6**2 / 1e9
C12 = 0.5 * (C11 + C22) - 2 * rho * v7**2 / 1e9

# По условию задачи
C13 = 0.0
C23 = 0.0

# Матрица [C] в нотации Фойгта
C_matrix = np.array([
    [C11, C12, C13, 0.0, 0.0, 0.0],
    [C12, C22, C23, 0.0, 0.0, 0.0],
    [C13, C23, C33, 0.0, 0.0, 0.0],
    [0.0, 0.0, 0.0, C44, 0.0, 0.0],
    [0.0, 0.0, 0.0, 0.0, C55, 0.0],
    [0.0, 0.0, 0.0, 0.0, 0.0, C66]
])

print("Компоненты матрицы упругости (ГПа):")
print(f"C11 = {C11:.6f}")
print(f"C22 = {C22:.6f}")
print(f"C33 = {C33:.6f}")
print(f"C44 = {C44:.6f}")
print(f"C55 = {C55:.6f}")
print(f"C66 = {C66:.6f}")
print(f"C12 = {C12:.6f}")

print("\nМатрица [C] (ГПа):")
print(C_matrix)

# Проверка положительной определённости
eigvals = np.linalg.eigvals(C_matrix)
"""
print("\nСобственные значения (ГПа):")
for i, val in enumerate(eigvals):
    print(f"λ{i+1} = {val:.6f}")
"""

if np.all(eigvals > 0):
    print("\nМатрица положительно определена.")
else:
    print("\nВНИМАНИЕ: есть неположительные собственные значения!")

print('ЭТАП 2')
# Данные из Таблицы 2
# Координаты в мм, деформации в µε
points_data = [
    #   x    y    z   e11  e22  e33  e23  e13  e12
    [0, 0, 0, 120, -35, -40, 5, -3, 8],  # P1
    [5, 0, 25, 95, -28, -32, 3, -2, 6],  # P2
    [0, 5, 25, 88, -45, -25, 4, -1, 7],  # P3
    [-5, 0, 25, 102, -30, -38, 2, -4, 5],  # P4
    [0, 0, 50, 110, -42, -35, 6, -2, 9],  # P5
]

points = []  # координаты (мм)
epsilons = []  # векторы деформаций (безразмерные)

for data in points_data:
    x, y, z, e11, e22, e33, e23, e13, e12 = data

    points.append([x, y, z])

    # Вектор деформаций в нотации Фойгта (µε → безразмерные)
    epsilon = np.array([
        e11 * 1e-6,
        e22 * 1e-6,
        e33 * 1e-6,
        2 * e23 * 1e-6,
        2 * e13 * 1e-6,
        2 * e12 * 1e-6
    ])
    epsilons.append(epsilon)

points = np.array(points)
epsilons = np.array(epsilons)

print("Координаты точек (мм):")
print(points)
print("\nВекторы деформаций ε (безразмерные):")
for i, eps in enumerate(epsilons):
    print(f"P{i + 1}: {eps}")



print('\nЭТАП 3')

# Список для хранения результатов
results = []

print("\nРезультаты расчёта напряжений и упругой энергии:")
print("-" * 100)
print(
    f"{'Точка':<6} {'σ11 (ГПа)':<10} {'σ22 (ГПа)':<10} {'σ33 (ГПа)':<10} {'σ23 (ГПа)':<10} {'σ13 (ГПа)':<10} {'σ12 (ГПа)':<10} {'U (кДж/м³)':<12} {'σ1 (ГПа)':<10} {'σ2 (ГПа)':<10} {'σ3 (ГПа)':<10}")
print("-" * 100)

for i, eps in enumerate(epsilons):
    # 1. Напряжения σ = C · ε (ГПа)
    sigma = C_matrix @ eps

    # 2. Упругая энергия (кДж/м³): 1/2 * σ^T * ε * 10^6
    U = 0.5 * np.dot(sigma, eps) * 1e6

    # 3. Тензор напряжений 3×3
    sigma_tensor = np.array([
        [sigma[0], sigma[5], sigma[4]],
        [sigma[5], sigma[1], sigma[3]],
        [sigma[4], sigma[3], sigma[2]]
    ])

    # 4. Главные напряжения (сортируем по убыванию)
    principal_stresses = np.sort(np.linalg.eigvalsh(sigma_tensor))[::-1]

    # Сохраняем результаты
    results.append({
        'point': i + 1,
        'sigma': sigma,
        'U': U,
        'principal': principal_stresses
    })

    # Вывод
    print(
        f"P{i + 1:<5} {sigma[0]:<10.6f} {sigma[1]:<10.6f} {sigma[2]:<10.6f} {sigma[3]:<10.6f} {sigma[4]:<10.6f} {sigma[5]:<10.6f} {U:<12.2f} {principal_stresses[0]:<10.6f} {principal_stresses[1]:<10.6f} {principal_stresses[2]:<10.6f}")

print("-" * 100)

print("\nГлавные напряжения (ГПа) по точкам:")
for res in results:
    print(
        f"P{res['point']}: σ1 = {res['principal'][0]:.6f}, σ2 = {res['principal'][1]:.6f}, σ3 = {res['principal'][2]:.6f}")


# ========== ЭТАП 4: Интерполяция ==========

# Переводим матрицу упругости в МПа для удобства
C_MPa = C_matrix * 1000

# Вычисленные напряжения в МПа (у нас в results sigma в ГПа, переводим)
sigma_MPa = [res['sigma'] * 1000 for res in results]

# Исходные деформации в µε (из points_data)
eps_micro = np.array([data[3:] for data in points_data])

# Функция для напряжения по Мизесу
def von_mises(sigma_MPa):
    s11, s22, s33, s23, s13, s12 = sigma_MPa
    return np.sqrt(0.5 * ((s11 - s22)**2 + (s22 - s33)**2 + (s33 - s11)**2 +
                         6 * (s12**2 + s13**2 + s23**2)))

# Выбираем точку Q
Q = np.array([3.0, 2.0, 25.0])
print(f"\nТочка Q: ({Q[0]}, {Q[1]}, {Q[2]}) мм")

# Проверка принадлежности цилиндру (R=10, H=50)
if Q[0]**2 + Q[1]**2 <= 100 and 0 <= Q[2] <= 50:
    print("✓ Точка Q внутри образца")
else:
    print("✗ Точка Q вне образца!")

# Поиск трёх ближайших точек
distances = np.linalg.norm(points - Q, axis=1)
nearest_idx = np.argsort(distances)[:3]
print("\nТри ближайшие точки:")
for idx in nearest_idx:
    print(f"  P{idx+1}: расстояние = {distances[idx]:.2f} мм")

# Веса IDW
weights = 1.0 / distances[nearest_idx]
weights /= weights.sum()
print(f"Веса: {np.round(weights, 4)}")

# Интерполяция деформаций (в µε)
eps_Q_micro = np.zeros(6)
sigma_Q_MPa = np.zeros(6)
for w, idx in zip(weights, nearest_idx):
    eps_Q_micro += w * eps_micro[idx]
    sigma_Q_MPa += w * sigma_MPa[idx]

print("\nРезультаты интерполяции в точке Q:")
print("Деформации (µε):")
print(f"  ε11 = {eps_Q_micro[0]:.2f}, ε22 = {eps_Q_micro[1]:.2f}, ε33 = {eps_Q_micro[2]:.2f}")
print(f"  ε23 = {eps_Q_micro[3]:.2f}, ε13 = {eps_Q_micro[4]:.2f}, ε12 = {eps_Q_micro[5]:.2f}")
print("Напряжения (МПа):")
print(f"  σ11 = {sigma_Q_MPa[0]:.4f}, σ22 = {sigma_Q_MPa[1]:.4f}, σ33 = {sigma_Q_MPa[2]:.4f}")
print(f"  σ23 = {sigma_Q_MPa[3]:.4f}, σ13 = {sigma_Q_MPa[4]:.4f}, σ12 = {sigma_Q_MPa[5]:.4f}")

# Упругая энергия в Q (кДж/м³)
# Нужен вектор в нотации Фойгта с удвоенными сдвигами
eps_Q_voigt = eps_Q_micro.copy()
eps_Q_voigt[3:] *= 2   # 2ε23, 2ε13, 2ε12
eps_Q_voigt *= 1e-6    # в безразмерные
U_Q = 0.5 * np.dot(sigma_Q_MPa, eps_Q_voigt) * 1e-3
U_Q = 0.5 * np.dot(sigma_Q_MPa, eps_Q_voigt) * 500
print(f"\nУпругая энергия в Q: U = {U_Q:.6f} кДж/м³")

# Напряжение по Мизесу в Q
vm_Q = von_mises(sigma_Q_MPa)
print(f"Напряжение по Мизесу в Q: σ_vM = {vm_Q:.4f} МПа")

# Градиент ∂σ11/∂x по точкам P2 и P4
# Найдём индексы точек P2 и P4 (в массиве points)
idx_P2 = 1   # P2 - второй в списке
idx_P4 = 3   # P4 - четвёртый
sigma11_P2 = sigma_MPa[idx_P2][0]
sigma11_P4 = sigma_MPa[idx_P4][0]
x_P2 = points[idx_P2][0]
x_P4 = points[idx_P4][0]
grad_s11 = (sigma11_P2 - sigma11_P4) / (x_P2 - x_P4)
print(f"\nГрадиент ∂σ₁₁/∂x ≈ {grad_s11:.6f} МПа/мм")

# ========== ЭТАП 5: Визуализация ==========

# Отбираем точки с z = 25 мм
z_target = 25.0
section_points = []
section_vm = []
for i, coord in enumerate(points):
    if abs(coord[2] - z_target) < 0.1:
        section_points.append([coord[0], coord[1]])
        vm = von_mises(sigma_MPa[i])
        section_vm.append(vm)
        print(f"P{i+1}: x={coord[0]}, y={coord[1]}, σ_vM = {vm:.4f} МПа")

# Добавляем точку Q (если её z=25)
if abs(Q[2] - z_target) < 0.1:
    section_points.append([Q[0], Q[1]])
    section_vm.append(vm_Q)
    print(f"Q: x={Q[0]}, y={Q[1]}, σ_vM = {vm_Q:.4f} МПа")

section_points = np.array(section_points)
section_vm = np.array(section_vm)

# Построение
plt.figure(figsize=(8, 7))
scatter = plt.scatter(section_points[:, 0], section_points[:, 1],
                      c=section_vm, cmap='jet', s=200, edgecolors='black', linewidth=1.5)
plt.colorbar(scatter, label='σ_vM (МПа)')
plt.xlabel('x (мм)', fontsize=12)
plt.ylabel('y (мм)', fontsize=12)
plt.title(f'Напряжение по Мизесу на сечении z = {z_target} мм\n'
          f'max = {np.max(section_vm):.4f} МПа, min = {np.min(section_vm):.4f} МПа',
          fontsize=11)
plt.grid(True, alpha=0.3)
plt.axis('equal')
plt.tight_layout()
plt.show()