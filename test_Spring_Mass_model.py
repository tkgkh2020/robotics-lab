import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# バネマスシステムのパラメータ
m = 1.0  # 質量 [kg]
k = 10.0  # バネ定数 [N/m] 
c = 0.5   # 減衰係数 [Ns/m]

# 運動方程式
def spring_mass_system(state, t):
    x, v = state  # 変位と速度
    dx_dt = v
    dv_dt = (-k * x - c * v) / m
    return [dx_dt, dv_dt]

# 時間配列の生成
t = np.linspace(0, 10, 1000)  # 0から10秒まで1000点

# 初期条件
x0 = 1.0  # 初期変位 [m]
v0 = 0.0  # 初期速度 [m/s]
initial_state = [x0, v0]

# システムの時間応答を計算
solution = odeint(spring_mass_system, initial_state, t)

# 結果のプロット
plt.figure(figsize=(10, 6))
plt.plot(t, solution[:, 0], 'b-', label='変位')
plt.plot(t, solution[:, 1], 'r--', label='速度')
plt.grid(True)
plt.xlabel('時間 [s]')
plt.ylabel('変位 [m], 速度 [m/s]')
plt.title('バネマスシステムの時間応答')
plt.legend()
plt.show()
