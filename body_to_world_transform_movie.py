import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import FancyArrowPatch, Polygon
from matplotlib.animation import FuncAnimation, PillowWriter


# ==================================================
# 計算系の関数
# ==================================================

# 2次元の回転行列を計算する
def rotation_matrix_2d(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, -s], [s, c]])


# Body Frame上の点を回転・平行移動してWorld Frameへ変換する
def transform_point(p_body, rotation, translation):
    p_rotated = rotation @ p_body
    p_world = p_rotated + translation
    return p_rotated, p_world


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


# 座標系のx軸・y軸を描画する
def draw_frame(ax, origin, rotation, axis_length, label,
               color_x='tab:red', color_y='tab:green'):
    x_axis = origin + rotation @ np.array([axis_length, 0.0])
    y_axis = origin + rotation @ np.array([0.0, axis_length])

    for endpoint, color in [(x_axis, color_x), (y_axis, color_y)]:
        ax.annotate(
            '', xy=endpoint, xytext=origin,
            arrowprops=dict(
                arrowstyle='->',
                color=color,
                lw=2,
            ),
        )

    ax.text(
        *(x_axis + 0.08 * (x_axis - origin)),
        f'{label}x',
        color=color_x,
        fontsize=11,
    )
    ax.text(
        *(y_axis + 0.08 * (y_axis - origin)),
        f'{label}y',
        color=color_y,
        fontsize=11,
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


# Body Frame側の固定された描画を作成する
def draw_body_frame(ax, p_body):
    identity = np.eye(2)
    origin = np.zeros(2)

    draw_frame(ax, origin, identity, 1.2, 'B')

    ax.plot(
        0, 0, 'ks',
        markersize=8,
        label='ロボット原点 (Body)',
    )
    ax.plot(
        *p_body, 'o',
        color='tab:orange',
        markersize=10,
        label='点 p_B',
    )
    ax.plot(
        [0, p_body[0]],
        [0, p_body[1]],
        '--',
        color='tab:orange',
        lw=1.5,
    )
    ax.annotate(
        f'p_B = ({p_body[0]:.2f}, {p_body[1]:.2f})',
        p_body,
        textcoords='offset points',
        xytext=(8, 8),
        fontsize=10,
    )

    ax.add_patch(Polygon(
        robot_triangle(origin, identity),
        closed=True,
        facecolor='lightgray',
        edgecolor='black',
        alpha=0.8,
    ))

    configure_axis(
        ax,
        (-1.5, 2.0),
        (-1.5, 2.0),
        'Body Frame',
    )
    ax.legend(loc='upper left')


# World Frame側の1フレームを描画する
def draw_world_frame(ax, p_rotated, p_world, t_world,
                     rotation, theta_deg):
    identity = np.eye(2)

    draw_frame(ax, np.zeros(2), identity, 1.4, 'W')
    draw_frame(ax, t_world, rotation, 1.0, 'B')

    ax.add_patch(Polygon(
        robot_triangle(t_world, rotation),
        closed=True,
        facecolor='lightgray',
        edgecolor='black',
        alpha=0.8,
        label='ロボット',
    ))

    # 回転後の点を描画する
    ax.plot(
        *p_rotated, 'x',
        color='tab:blue',
        markersize=9,
        label='回転後 R p_B',
    )
    ax.annotate(
        '回転',
        xy=p_rotated,
        xytext=(0.2, p_rotated[1] + 0.35),
        arrowprops=dict(
            arrowstyle='->',
            color='tab:blue',
        ),
        color='tab:blue',
        fontsize=9,
    )

    # 平行移動後の最終座標を描画する
    ax.plot(
        *p_world, 'o',
        color='tab:orange',
        markersize=10,
        label='点 p_W',
    )
    ax.plot(
        [t_world[0], p_world[0]],
        [t_world[1], p_world[1]],
        '--',
        color='tab:orange',
        lw=1.5,
    )
    ax.annotate(
        f'p_W = ({p_world[0]:.2f}, {p_world[1]:.2f})',
        p_world,
        textcoords='offset points',
        xytext=(8, 8),
        fontsize=10,
    )

    # 回転後の点から平行移動後の点への矢印を描画する
    ax.add_patch(FancyArrowPatch(
        p_rotated,
        p_world,
        arrowstyle='->',
        mutation_scale=12,
        color='tab:purple',
        lw=1.5,
        linestyle='--',
    ))

    midpoint = 0.5 * (p_rotated + p_world)
    ax.text(
        *(midpoint + np.array([0.05, 0.15])),
        '平行移動 +t_W',
        color='tab:purple',
        fontsize=9,
    )

    # ロボットの位置と姿勢を表示する
    ax.plot(*t_world, 'ks', markersize=8)
    ax.annotate(
        f't_W = ({t_world[0]:.1f}, {t_world[1]:.1f})\n'
        f'θ = {theta_deg:.0f}°',
        t_world,
        textcoords='offset points',
        xytext=(-55, -35),
        fontsize=9,
    )

    configure_axis(
        ax,
        (-0.5, 5.0),
        (-0.5, 4.0),
        'World Frame  (p_W = R p_B + t_W)',
    )
    ax.legend(loc='upper left')


# ==================================================
# 実行系
# ==================================================

# アニメーションの各フレームを更新する
def update(frame_index, axes, p_body, t_world, theta_values):
    ax = axes[1]
    ax.clear()

    theta = theta_values[frame_index]
    theta_deg = np.rad2deg(theta)
    rotation = rotation_matrix_2d(theta)

    p_rotated, p_world = transform_point(
        p_body,
        rotation,
        t_world,
    )

    draw_world_frame(
        ax,
        p_rotated,
        p_world,
        t_world,
        rotation,
        theta_deg,
    )


# 座標変換アニメーションを作成してGIFとして保存する
def create_animation():
    setup_font()

    p_body = np.array([1.0, 0.5])
    t_world = np.array([2.0, 1.0])
    theta_values = np.linspace(0.0, 2.0 * np.pi, 37)

    fig, axes = plt.subplots(
        1,
        2,
        figsize=(12, 6),
    )
    fig.suptitle(
        'Body Frame から World Frame への座標変換',
        fontsize=14,
    )
    fig.subplots_adjust(
        left=0.06,
        right=0.98,
        bottom=0.10,
        top=0.88,
        wspace=0.25,
    )

    # Body Frame側は固定して一度だけ描画する
    draw_body_frame(axes[0], p_body)

    # アニメーションを作成する
    animation = FuncAnimation(
        fig,
        update,
        frames=len(theta_values),
        fargs=(axes, p_body, t_world, theta_values),
        interval=100,
        repeat=True,
    )

    # GIFとして保存する
    gif_path = 'coordinate_transform_rotation.gif'
    animation.save(
        gif_path,
        writer=PillowWriter(fps=10),
        dpi=90,
    )

    plt.close(fig)
    print(f'作成完了: {gif_path}')


# プログラムを実行する
if __name__ == '__main__':
    create_animation()