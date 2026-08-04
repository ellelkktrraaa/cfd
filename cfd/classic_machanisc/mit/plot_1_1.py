"""
P 1.1 绘图:球在平方阻力下的运动 (x, y, v_x, v_y)
公式来自 1.revise.md(y 轴向下、原点在抛出点、地面 y = h)
"""
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ---------- 物理常数 ----------
C1 = 3.1e-4    # kg/(s m)  粘性项系数(本题已忽略)
C2 = 0.85      # kg/m^3    压力项系数
r  = 0.5       # m         球半径
g  = 10.0      # m/s^2
v0 = 5.0       # m/s       水平初速度
h  = 10.0      # m         地面位置(y 向下)

# 注意:题目没给质量 m,这里按笔记里隐含的 m = 1 kg
m = 1.0

K     = C2 * r**2 / m          # K = C2 r^2 / m
alpha = np.sqrt(g / K)         # 终端速度 v_term = sqrt(g/K)

# ---------- 解析解(和笔记里的 boxed 公式一致) ----------
def v_x(t):  return v0 / (1 + K * v0 * t)
def x(t):    return np.log(1 + K * v0 * t) / K
def v_y(t):  return alpha * np.tanh(np.sqrt(g * K) * t)
def y(t):    return np.log(np.cosh(np.sqrt(g * K) * t)) / K

# ---------- 二分法求落地时间: y(t) = h ----------
def bisect(func, lo, hi, tol=1e-12):
    """在 [lo, hi] 上找 func 的零点(要求 func 单调,端点异号)"""
    for _ in range(200):
        mid = (lo + hi) / 2
        if func(mid) * func(lo) > 0:   # mid 与 lo 同号 -> 零点在右边
            lo = mid
        else:
            hi = mid
        if hi - lo < tol:
            break
    return (lo + hi) / 2

hi = 10.0
while y(hi) < h:          # 把上界翻倍,直到 y(t) 超过地面
    hi *= 2
t_land = bisect(lambda t: y(t) - h, 0.0, hi)

print(f"v_term = {alpha:.2f} m/s")
print(f"t_land = {t_land:.3f} s,  x_land = {x(t_land):.2f} m")

# ---------- 画图 ----------
t = np.linspace(0, t_land, 500)

# 无阻力对照: x = v0 t,  y = 1/2 g t^2(同原点、同 y 向下)
t_free = t[t <= np.sqrt(2 * h / g)]
y_free = 0.5 * g * t_free**2

fig, axes = plt.subplots(2, 2, figsize=(10, 8))

# 1) 轨迹(纵轴画离地高度 h - y, y 向下量)
ax = axes[0, 0]
ax.plot(x(t), h - y(t), 'b-', lw=2, label='with drag')
ax.plot(v0 * t_free, h - y_free, 'r--', lw=2, label='free fall')
ax.plot(x(t_land), 0, 'ko', ms=8, label='landing')
ax.set_xlabel('x (m)')
ax.set_ylabel('height (m)')
ax.set_title('trajectory')
ax.legend()
ax.grid(alpha=0.3)
ax.axis('equal')

# 2) 高度随时间
ax = axes[0, 1]
ax.plot(t, h - y(t), 'b-', lw=2, label='with drag')
ax.plot(t_free, h - y_free, 'r--', lw=2, label='free fall')
ax.set_xlabel('t (s)')
ax.set_ylabel('height (m)')
ax.set_title('height vs time')
ax.legend()
ax.grid(alpha=0.3)

# 3) 水平速度
ax = axes[1, 0]
ax.plot(t, v_x(t), 'b-', lw=2)
ax.axhline(0, color='gray', lw=0.8)
ax.set_xlabel('t (s)')
ax.set_ylabel('v_x (m/s)')
ax.set_title('horizontal velocity')
ax.grid(alpha=0.3)

# 4) 竖直速度 + 终端速度参考线
ax = axes[1, 1]
ax.plot(t, v_y(t), 'b-', lw=2, label='v_y')
ax.axhline(alpha, color='r', ls='--', lw=1,
           label=f'v_term = {alpha:.2f} m/s')
ax.set_xlabel('t (s)')
ax.set_ylabel('v_y (m/s)')
ax.set_title('vertical velocity')
ax.legend()
ax.grid(alpha=0.3)

fig.tight_layout()
out = Path(__file__).parent / 'assets' / 'traj_1_1.png'
out.parent.mkdir(exist_ok=True)
fig.savefig(out, dpi=150)
print(f"figure saved -> {out}")
