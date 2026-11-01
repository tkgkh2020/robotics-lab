import os

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.ticker import FuncFormatter


# ==================================================
# パラメータ
# ==================================================

L1 = 1.0             # リンク1の長さ [m]
L2 = 0.7             # リンク2の長さ [m]
N_SAMPLES = 10000    # 照合に使うランダム関節角の数
SEED = 0             # 乱数シード（結果を再現できるようにする）
TOLERANCE = 1e-12    # 「一致」とみなす誤差の上限 [m]

# 描画する代表姿勢 [deg]
THETA1_DEG = 40.0
THETA2_DEG = 60.0

FIGURE_PATH = os.path.join('figures', 'two_link_forward_kinematics.png')


# ==================================================
# 計算系の関数
# ==================================================

# 2次元の同次変換行列を計算する（回転 theta のあと平行移動 translation）
def homogeneous_transform_2d(theta, translation):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([
        [c, -s, translation[0]],
        [s,  c, translation[1]],
        [0,  0, 1],
    ])


# 2次元座標を同次座標へ変換する
def to_homogeneous(point):
    return np.append(point, 1.0)


# 同次変換の積で順運動学を計算する
#   T_W1 : World -> リンク1座標系（関節1で theta1 回転、原点はWorld原点）
#   T_12 : リンク1 -> リンク2座標系（リンク1の先端 (l1, 0) に移動し theta2 回転）
#   手先はリンク2座標系で (l2, 0) にある
def forward_kinematics_homogeneous(theta1, theta2, l1, l2):
    T_W1 = homogeneous_transform_2d(theta1, [0.0, 0.0])
    T_12 = homogeneous_transform_2d(theta2, [l1, 0.0])
    T_W2 = T_W1 @ T_12

    p_end_2 = to_homogeneous([l2, 0.0])
    p_end_W = (T_W2 @ p_end_2)[:2]

    # 肘（関節2）の位置は T_W2 の平行移動成分そのもの
    p_elbow_W = T_W2[:2, 2]
    return p_end_W, p_elbow_W, T_W1, T_W2


# 幾何（三角関数の式）で手先位置を計算する
def forward_kinematics_geometric(theta1, theta2, l1, l2):
    x = l1 * np.cos(theta1) + l2 * np.cos(theta1 + theta2)
    y = l1 * np.sin(theta1) + l2 * np.sin(theta1 + theta2)
    return np.array([x, y])


# ランダムな関節角で2つの方法を照合し、各サンプルの誤差を返す
def compare_random_angles(n_samples, l1, l2, seed):
    rng = np.random.default_rng(seed)
    thetas = rng.uniform(-np.pi, np.pi, size=(n_samples, 2))

    errors = np.empty(n_samples)
    for i, (theta1, theta2) in enumerate(thetas):
        p_h, _, _, _ = forward_kinematics_homogeneous(theta1, theta2, l1, l2)
        p_g = forward_kinematics_geometric(theta1, theta2, l1, l2)
        errors[i] = np.linalg.norm(p_h - p_g)
    return thetas, errors


# ==================================================
# 描画系の関数
# ==================================================

# 日本語フォントを設定する（macOSはヒラギノ、それ以外は見つかったものを使う）
def setup_font():
    plt.rcParams['axes.unicode_minus'] = False  # 日本語フォントでマイナス記号が化けないようにする
    mac_path = '/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc'
    if os.path.exists(mac_path):
        fm.fontManager.addfont(mac_path)
        plt.rcParams['font.family'] = fm.FontProperties(fname=mac_path).get_name()
        return

    candidates = [
        'Hiragino Sans', 'Yu Gothic', 'Meiryo', 'IPAexGothic',
        'Noto Sans CJK JP', 'WenQuanYi Zen Hei',
    ]
    available = {f.name for f in fm.fontManager.ttflist}
    for name in candidates:
        if name in available:
            plt.rcParams['font.family'] = name
            return


# 座標系のx軸・y軸を描画する
def draw_frame(ax, transform, axis_length, label,
               color_x='tab:red', color_y='tab:green'):
    origin = transform[:2, 2]
    rotation = transform[:2, :2]
    x_axis = origin + rotation @ np.array([axis_length, 0.0])
    y_axis = origin + rotation @ np.array([0.0, axis_length])

    for endpoint, color in [(x_axis, color_x), (y_axis, color_y)]:
        ax.annotate(
            '', xy=endpoint, xytext=origin,
            arrowprops=dict(arrowstyle='->', color=color, lw=1.8),
        )
    ax.text(*(x_axis + 0.05 * (x_axis - origin) / axis_length),
            f'{label}x', color=color_x, fontsize=10)
    ax.text(*(y_axis + 0.05 * (y_axis - origin) / axis_length),
            f'{label}y', color=color_y, fontsize=10)


# 代表姿勢のアームと各座標系を描画する
def draw_arm_pose(ax, theta1, theta2, l1, l2):
    p_end_h, p_elbow, T_W1, T_W2 = forward_kinematics_homogeneous(
        theta1, theta2, l1, l2)
    p_end_g = forward_kinematics_geometric(theta1, theta2, l1, l2)

    draw_frame(ax, np.eye(3), 0.5, 'W', color_x='gray', color_y='gray')
    draw_frame(ax, T_W1, 0.35, '1')
    draw_frame(ax, T_W2, 0.35, '2')

    # リンク
    xs = [0.0, p_elbow[0], p_end_h[0]]
    ys = [0.0, p_elbow[1], p_end_h[1]]
    ax.plot(xs, ys, '-', color='tab:blue', lw=5, alpha=0.6,
            solid_capstyle='round', label='リンク')
    ax.plot(xs[:2], ys[:2], 'ko', markersize=8, label='関節')

    # 手先：同次変換（○）と幾何（×）を重ねて描く
    ax.plot(*p_end_h, 'o', color='tab:orange', markersize=12,
            markerfacecolor='none', mew=2, label='手先（同次変換 T_W1 T_12）')
    ax.plot(*p_end_g, 'x', color='black', markersize=10, mew=2,
            label='手先（幾何の式）')
    ax.annotate(
        f'({p_end_h[0]:.3f}, {p_end_h[1]:.3f})', p_end_h,
        textcoords='offset points', xytext=(10, -15), fontsize=9,
    )

    # 関節角の注記
    ax.text(0.12, 0.02, f'θ1={np.rad2deg(theta1):.0f}°', fontsize=9)
    ax.text(p_elbow[0] + 0.08, p_elbow[1] - 0.08,
            f'θ2={np.rad2deg(theta2):.0f}°', fontsize=9)

    # 到達可能領域の境界（外側 l1+l2、内側 |l1-l2|）
    circle = np.linspace(0, 2 * np.pi, 200)
    for r in (l1 + l2, abs(l1 - l2)):
        ax.plot(r * np.cos(circle), r * np.sin(circle),
                ':', color='gray', lw=1)

    reach = l1 + l2
    ax.set_aspect('equal')
    ax.set_xlim(-reach - 0.1, reach + 0.1)
    ax.set_ylim(-reach - 0.1, reach + 0.1)
    ax.grid(True, alpha=0.4)
    ax.set_xlabel('x [m]')
    ax.set_ylabel('y [m]')
    ax.set_title(f'2リンクアームの姿勢（l1={l1}, l2={l2}）')
    ax.legend(loc='lower left', fontsize=8)


# ランダム関節角での誤差の分布を描画する
def draw_errors(ax, errors, tolerance):
    # 誤差がちょうど0のサンプルは対数軸に載らないので、下端に別色で描く
    zero = errors == 0.0
    floor = 1e-18
    idx = np.arange(len(errors))
    ax.semilogy(idx[~zero], errors[~zero], '.', markersize=2,
                color='tab:blue', alpha=0.5, label='誤差 > 0')
    ax.semilogy(idx[zero], np.full(zero.sum(), floor), '.', markersize=2,
                color='tab:gray', alpha=0.5,
                label=f'誤差 = 0（完全一致）{zero.sum()} 件')
    ax.axhline(tolerance, color='tab:red', ls='--', lw=1,
               label=f'許容値 {tolerance:.0e} m')
    ax.axhline(errors.max(), color='tab:orange', ls='-', lw=1,
               label=f'最大誤差 {errors.max():.2e} m')
    # 目盛りを 1e-16 のような文字で表示する（フォントによる記号化けを避ける）
    ax.yaxis.set_major_formatter(
        FuncFormatter(lambda v, _: f'1e{int(round(np.log10(v)))}'))
    ax.set_ylim(floor / 3, tolerance * 30)
    ax.set_xlabel('サンプル番号')
    ax.set_ylabel('|p_同次 - p_幾何| [m]')
    ax.set_title(f'ランダム関節角 {len(errors)} 通りでの誤差')
    ax.grid(True, which='major', alpha=0.3)
    ax.legend(loc='center right', fontsize=8, markerscale=4)


# ==================================================
# 実行系の関数
# ==================================================

def main():
    setup_font()

    # 1. 代表姿勢で同次変換行列を表示する
    theta1 = np.deg2rad(THETA1_DEG)
    theta2 = np.deg2rad(THETA2_DEG)
    p_end_h, p_elbow, T_W1, T_W2 = forward_kinematics_homogeneous(
        theta1, theta2, L1, L2)
    p_end_g = forward_kinematics_geometric(theta1, theta2, L1, L2)

    np.set_printoptions(precision=4, suppress=True)
    print('=== 代表姿勢 ===')
    print(f'theta1 = {THETA1_DEG} deg, theta2 = {THETA2_DEG} deg')
    print('T_W1 =\n', T_W1)
    print('T_W2 = T_W1 @ T_12 =\n', T_W2)
    print(f'肘の位置   = {p_elbow}')
    print(f'手先（同次変換） = {p_end_h}')
    print(f'手先（幾何）     = {p_end_g}')
    # T_W2 の回転部分は theta1+theta2 の回転になっているはず
    angle_W2 = np.arctan2(T_W2[1, 0], T_W2[0, 0])
    print(f'T_W2 の回転角 = {np.rad2deg(angle_W2):.4f} deg '
          f'(theta1+theta2 = {THETA1_DEG + THETA2_DEG} deg)')

    # 2. ランダムな関節角で照合する
    thetas, errors = compare_random_angles(N_SAMPLES, L1, L2, SEED)
    i_max = int(np.argmax(errors))
    print('\n=== ランダム照合 ===')
    print(f'サンプル数 = {N_SAMPLES}, 関節角の範囲 = [-180, 180] deg')
    print(f'最大誤差   = {errors.max():.3e} m '
          f'(theta = {np.rad2deg(thetas[i_max]).round(1)} deg)')
    print(f'平均誤差   = {errors.mean():.3e} m')
    print(f'誤差0の件数 = {(errors == 0).sum()} / {N_SAMPLES}')
    print(f'最大誤差 / 機械イプシロン = {errors.max() / np.finfo(float).eps:.2f}')
    print(f'判定       = {"一致" if errors.max() < TOLERANCE else "不一致"} '
          f'(許容値 {TOLERANCE:.0e} m)')
    assert errors.max() < TOLERANCE

    # 3. グラフを描く
    fig, axes = plt.subplots(1, 2, figsize=(13, 6))
    draw_arm_pose(axes[0], theta1, theta2, L1, L2)
    draw_errors(axes[1], errors, TOLERANCE)
    fig.suptitle('同次変換の積による順運動学と幾何の式の照合', fontsize=14)
    fig.tight_layout()

    os.makedirs(os.path.dirname(FIGURE_PATH), exist_ok=True)
    fig.savefig(FIGURE_PATH, dpi=120)
    print(f'\nグラフを保存しました: {FIGURE_PATH}')
    plt.show()


if __name__ == '__main__':
    main()
