import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import Circle
from pathlib import Path


# ==================================================
# 計算系の関数
# ==================================================

# 角速度ベクトルと位置ベクトルの外積から速度を計算する
def angular_velocity_cross_position(omega_z, position):
    omega = np.array([0.0, 0.0, omega_z])
    position_3d = np.array([position[0], position[1], 0.0])
    return np.cross(omega, position_3d)[:2]


# 時刻から回転中の点の位置を計算する
def calculate_position(omega_z, time, radius=1.0):
    theta = omega_z * time
    return radius * np.array([np.cos(theta), np.sin(theta)])


# ==================================================
# 描画系の関数
# ==================================================

# 日本語フォントを設定する
def setup_font():
    try:
        path = '/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc'
        plt.rcParams['font.family'] = fm.FontProperties(fname=path).get_name()
    except Exception:
        plt.rcParams['font.family'] = 'DejaVu Sans'


# グラフの軸・目盛り・タイトルなどを設定する
def configure_axis(ax):
    ax.set_aspect('equal')
    ax.set_xlim(-2.15, 2.15)
    ax.set_ylim(-2.15, 2.15)
    ax.set_xlabel('x [m]')
    ax.set_ylabel('y [m]')
    ax.grid(True, alpha=0.35)


# 回転中の点と、その瞬間の速度ベクトルを描画する
def draw_scene(ax, time, omega_z, radius=1.0):
    ax.clear()
    configure_axis(ax)
    ax.add_patch(Circle((0, 0), radius, fill=False, linestyle='--',
                        edgecolor='gray', linewidth=1.5))
    ax.plot(0, 0, 'ks', markersize=7, label='回転中心 O')

    position = calculate_position(omega_z, time, radius)
    velocity = angular_velocity_cross_position(omega_z, position)

    # 位置ベクトル r（中心 O から点 P へ）
    ax.annotate('', xy=position, xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', color='tab:blue', lw=2.5))
    r_label_pos = position * 0.50 + np.array([-0.22, 0.12])
    ax.text(*r_label_pos, '位置 r', color='tab:blue', fontsize=12, fontweight='bold')

    ax.plot(*position, 'o', color='tab:orange', markersize=9,
            label='回転する点 P')

    # 速度ベクトル v（円の接線方向。ω × r の結果）
    velocity_end = position + 0.32 * velocity
    ax.annotate('', xy=velocity_end, xytext=position,
                arrowprops=dict(arrowstyle='->', color='tab:green', lw=2.5))
    ax.text(*(velocity_end + np.array([0.06, 0.06])),
            '速度 v', color='tab:green', fontsize=12, fontweight='bold')

    theta_deg = np.degrees(omega_z * time) % 360
    ax.text(
        -2.05, 1.95,
        '角速度 ω は紙面の手前（こちら向き）\n'
        'ω = (0, 0, +2) rad/s',
        fontsize=10, va='top',
        bbox=dict(boxstyle='round,pad=0.35', facecolor='white', alpha=0.92),
    )
    ax.text(
        -2.05, -1.25,
        f'今の角度 θ = {theta_deg:.0f} 度\n'
        f'位置 r = ({position[0]:.2f}, {position[1]:.2f}) m\n'
        f'速度 v = ({velocity[0]:.2f}, {velocity[1]:.2f}) m/s\n'
        '※ v は r に垂直（円の接線）',
        fontsize=10, va='bottom',
        bbox=dict(boxstyle='round,pad=0.35', facecolor='white', alpha=0.92),
    )
    ax.set_title('点Pの速度は  v = ω × r  （角速度と位置の外積）')
    ax.legend(loc='lower right', fontsize=9)


# ==================================================
# 実行系
# ==================================================

# アニメーションの各フレームを更新する
def update(frame_index, ax, time_values, omega_z):
    draw_scene(ax, time_values[frame_index], omega_z)


# 外積による速度ベクトルをアニメーションGIFとして保存する
def create_animation():
    setup_font()
    omega_z = 2.0
    time_values = np.linspace(0.0, 2 * np.pi / omega_z, 49)
    fig, ax = plt.subplots(figsize=(8, 8))
    fig.suptitle('角速度ベクトルと外積の可視化', fontsize=14)
    fig.subplots_adjust(left=0.12, right=0.97, bottom=0.10, top=0.88)
    animation = FuncAnimation(
        fig, update, frames=len(time_values),
        fargs=(ax, time_values, omega_z), interval=100, repeat=True,
    )
    gif_path = Path(__file__).resolve().parent / 'angular_velocity_cross_product.gif'
    animation.save(gif_path, writer=PillowWriter(fps=10), dpi=90)
    plt.close(fig)
    print(f'作成完了: {gif_path}')


if __name__ == '__main__':
    create_animation()
