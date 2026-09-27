import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import FancyArrowPatch, Polygon


# ==================================================
# 計算系の関数
# ==================================================

# 2次元の同次変換行列を計算する
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


# 同次変換行列を使ってBody Frameの点をWorld Frameへ変換する
def transform_point(p_body, transform):
    p_body_h = to_homogeneous(p_body)
    p_world_h = transform @ p_body_h
    return p_world_h[:2]


# 同次変換行列から回転行列を取り出す
def extract_rotation(transform):
    return transform[:2, :2]


# 同次変換行列から平行移動ベクトルを取り出す
def extract_translation(transform):
    return transform[:2, 2]


# ロボットの三角形形状の頂点座標を計算する
def robot_triangle(origin, rotation, length=0.7, width=0.4):
    local_points = np.array([
        [length, 0.0],
        [-length * 0.4, width / 2],
        [-length * 0.4, -width / 2],
    ])
    return (rotation @ local_points.T).T + origin


# ==================================================
# 描画系の関数
# ==================================================

# 日本語フォントを設定する
def setup_font():
    try:
        path = '/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc'
        plt.rcParams['font.family'] = fm.FontProperties(
            fname=path
        ).get_name()
    except Exception:
        plt.rcParams['font.family'] = 'DejaVu Sans'
        plt.rcParams['font.sans-serif'] = [
            'Hiragino Sans', 'Yu Gothic', 'Meiryo', 'Takao',
            'IPAexGothic', 'IPAPGothic', 'VL PGothic',
            'Noto Sans CJK JP',
        ]


# 座標系のx軸・y軸を描画する
def draw_frame(ax, origin, rotation, axis_length, label,
               color_x='tab:red', color_y='tab:green'):
    x_axis = origin + rotation @ np.array([axis_length, 0.0])
    y_axis = origin + rotation @ np.array([0.0, axis_length])

    for endpoint, color in [(x_axis, color_x), (y_axis, color_y)]:
        ax.annotate(
            '', xy=endpoint, xytext=origin,
            arrowprops=dict(arrowstyle='->', color=color, lw=2),
        )

    ax.text(
        *(x_axis + 0.08 * (x_axis - origin)),
        f'{label}x', color=color_x, fontsize=11,
    )
    ax.text(
        *(y_axis + 0.08 * (y_axis - origin)),
        f'{label}y', color=color_y, fontsize=11,
    )


# グラフの軸・目盛り・タイトルなどを設定する
def configure_axis(ax, xlim, ylim, title):
    ax.set_aspect('equal')
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.grid(True, alpha=0.4)
    ax.set_xlabel('x [m]')
    ax.set_ylabel('y [m]')
    ax.set_title(title)


# Body Frame上のロボットと点を描画する
def draw_body_frame(ax, p_body):
    identity = np.eye(2)
    origin = np.zeros(2)

    draw_frame(ax, origin, identity, 1.2, 'B')

    ax.plot(
        0, 0, 'ks', markersize=8,
        label='ロボット原点 (Body)',
    )
    ax.plot(
        *p_body, 'o', color='tab:orange',
        markersize=10, label='点 p_B',
    )
    ax.plot(
        [0, p_body[0]], [0, p_body[1]],
        '--', color='tab:orange', lw=1.5,
    )
    ax.annotate(
        f'p_B = ({p_body[0]:.2f}, {p_body[1]:.2f})',
        p_body, textcoords='offset points',
        xytext=(8, 8), fontsize=10,
    )

    ax.add_patch(Polygon(
        robot_triangle(origin, identity),
        closed=True, facecolor='lightgray',
        edgecolor='black', alpha=0.8,
    ))

    configure_axis(ax, (-1.5, 2.0), (-1.5, 2.0), 'Body Frame')
    ax.legend(loc='upper left')


# World Frame上で座標変換の過程と結果を描画する
def draw_world_frame(ax, p_rotated, p_world, t_world,
                     rotation, theta_deg):
    identity = np.eye(2)

    draw_frame(ax, np.zeros(2), identity, 1.4, 'W')
    draw_frame(ax, t_world, rotation, 1.0, 'B')

    ax.add_patch(Polygon(
        robot_triangle(t_world, rotation),
        closed=True, facecolor='lightgray',
        edgecolor='black', alpha=0.8, label='ロボット',
    ))

    # 回転後の点を描画する
    ax.plot(
        *p_rotated, 'x', color='tab:blue',
        markersize=9, label='回転後 R p_B',
    )
    ax.annotate(
        '回転',
        xy=p_rotated,
        xytext=(0.2, p_rotated[1] + 0.35),
        arrowprops=dict(
            arrowstyle='->', color='tab:blue'
        ),
        color='tab:blue', fontsize=9,
    )

    # 平行移動後の最終座標を描画する
    ax.plot(
        *p_world, 'o', color='tab:orange',
        markersize=10, label='点 p_W',
    )
    ax.plot(
        [t_world[0], p_world[0]],
        [t_world[1], p_world[1]],
        '--', color='tab:orange', lw=1.5,
    )
    ax.annotate(
        f'p_W = ({p_world[0]:.2f}, {p_world[1]:.2f})',
        p_world, textcoords='offset points',
        xytext=(8, 8), fontsize=10,
    )

    # 回転後の点から平行移動後の点への矢印を描画する
    ax.add_patch(FancyArrowPatch(
        p_rotated, p_world,
        arrowstyle='->', mutation_scale=12,
        color='tab:purple', lw=1.5, linestyle='--',
    ))

    midpoint = 0.5 * (p_rotated + p_world)
    ax.text(
        *(midpoint + np.array([0.05, 0.15])),
        '平行移動 +t_W',
        color='tab:purple', fontsize=9,
    )

    # ロボットの位置と姿勢を表示する
    ax.plot(*t_world, 'ks', markersize=8)
    ax.annotate(
        f't_W = ({t_world[0]:.1f}, {t_world[1]:.1f})\n'
        f'θ = {theta_deg:.0f}°',
        t_world, textcoords='offset points',
        xytext=(-55, -35), fontsize=9,
    )

    configure_axis(
        ax, (-0.5, 5.0), (-0.5, 4.0),
        'World Frame  (p_W = T_WB p_B)',
    )
    ax.legend(loc='upper left')


# ==================================================
# 実行系の関数
# ==================================================

# 計算結果をコンソールに出力する
def print_results(p_body, t_world, theta_deg, transform, p_world):
    rotation = extract_rotation(transform)

    print('=== Body Frame -> World Frame ===')
    print(f'Body Frame 上の点 p_B     = {p_body}')
    print(f'ロボット位置 t_W          = {t_world}')
    print(f'ロボット姿勢 theta        = {theta_deg:.1f} deg')

    print('\n同次変換行列 T_WB =')
    print(transform)

    print('\n回転行列 R =')
    print(rotation)

    print(f'\nWorld Frame 上の点 p_W    = {p_world}')


# 座標変換の計算・検証・出力・描画を実行する
def main():
    setup_font()

    p_body = np.array([1.0, 0.5])
    theta_deg = 30.0
    theta = np.deg2rad(theta_deg)
    t_world = np.array([2.0, 1.0])

    # 回転と平行移動を1つの同次変換行列にまとめる
    transform = homogeneous_transform_2d(theta, t_world)

    # 同次変換行列を使ってBody FrameからWorld Frameへ変換する
    p_world = transform_point(p_body, transform)

    # 同次変換行列から描画に必要な情報を取り出す
    rotation = extract_rotation(transform)

    # 従来の計算結果と一致することを検証する
    p_rotated = rotation @ p_body
    p_expected = p_rotated + t_world
    assert np.allclose(p_world, p_expected)

    print_results(
        p_body, t_world, theta_deg,
        transform, p_world,
    )

    # 2つの座標系を描画する
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    draw_body_frame(axes[0], p_body)
    draw_world_frame(
        axes[1], p_rotated, p_world,
        t_world, rotation, theta_deg,
    )

    fig.suptitle(
        'Body Frame から World Frame への座標変換',
        fontsize=14,
    )
    fig.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()