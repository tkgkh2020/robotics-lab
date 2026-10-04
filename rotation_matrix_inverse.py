import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import FancyArrowPatch


# ==================================================
# 計算系の関数
# ==================================================

# 2次元の回転行列を計算する
def rotation_matrix(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([
        [c, -s],
        [s,  c],
    ])


# 回転行列を転置する
def transpose_rotation(rotation):
    return rotation.T


# 回転行列を使って点を回転させる
def rotate_point(point, rotation):
    return rotation @ point


# 回転行列が逆変換になっていることを検証する
def verify_inverse(rotation):
    rotation_transpose = rotation.T
    identity = rotation_transpose @ rotation
    return identity


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
            '',
            xy=endpoint,
            xytext=origin,
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
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title(title)


# 元の点とベクトルを描画する
def draw_original(ax, point):
    identity = np.eye(2)
    origin = np.zeros(2)

    draw_frame(
        ax,
        origin,
        identity,
        1.4,
        'W',
    )

    ax.plot(
        *origin,
        'ks',
        markersize=8,
        label='原点',
    )

    ax.plot(
        *point,
        'o',
        color='tab:orange',
        markersize=10,
        label='元の点 p',
    )

    ax.plot(
        [0, point[0]],
        [0, point[1]],
        '--',
        color='tab:orange',
        lw=1.5,
    )

    ax.annotate(
        rf'$p = ({point[0]:.2f}, {point[1]:.2f})$',
        point,
        textcoords='offset points',
        xytext=(8, 8),
        fontsize=10,
    )

    configure_axis(
        ax,
        (-1.5, 2.0),
        (-1.5, 2.0),
        '元の座標',
    )

    ax.legend(loc='upper left')


# 回転後の点と回転の向きを描画する
def draw_forward_rotation(
    ax,
    point,
    rotated_point,
    rotation,
    theta_deg,
):
    identity = np.eye(2)
    origin = np.zeros(2)

    draw_frame(
        ax,
        origin,
        identity,
        1.4,
        'W',
    )

    ax.plot(
        *origin,
        'ks',
        markersize=8,
        label='原点',
    )

    ax.plot(
        *point,
        'o',
        color='tab:orange',
        markersize=10,
        label='元の点 p',
    )

    ax.plot(
        *rotated_point,
        'o',
        color='tab:blue',
        markersize=10,
        label=r'回転後 $Rp$',
    )

    ax.plot(
        [0, point[0]],
        [0, point[1]],
        '--',
        color='tab:orange',
        lw=1.5,
    )

    ax.plot(
        [0, rotated_point[0]],
        [0, rotated_point[1]],
        '--',
        color='tab:blue',
        lw=1.5,
    )

    ax.add_patch(
        FancyArrowPatch(
            point,
            rotated_point,
            arrowstyle='->',
            mutation_scale=12,
            color='tab:purple',
            lw=1.5,
            linestyle='--',
        )
    )

    midpoint = 0.5 * (point + rotated_point)

    ax.text(
        *(midpoint + np.array([0.05, 0.15])),
        rf'$R$：+{theta_deg:.0f}°回転',
        color='tab:purple',
        fontsize=9,
    )

    ax.annotate(
        rf'$p = ({point[0]:.2f}, {point[1]:.2f})$',
        point,
        textcoords='offset points',
        xytext=(8, 8),
        fontsize=10,
    )

    ax.annotate(
        rf'$Rp = ({rotated_point[0]:.2f}, '
        rf'{rotated_point[1]:.2f})$',
        rotated_point,
        textcoords='offset points',
        xytext=(8, 8),
        fontsize=10,
    )

    configure_axis(
        ax,
        (-2.0, 2.0),
        (-2.0, 2.0),
        rf'順変換  ($R$：+{theta_deg:.0f}°)',
    )

    ax.legend(loc='upper left')


# 逆回転によって元に戻る過程を描画する
def draw_inverse_rotation(
    ax,
    rotated_point,
    restored_point,
    rotation_transpose,
    theta_deg,
):
    identity = np.eye(2)
    origin = np.zeros(2)

    draw_frame(
        ax,
        origin,
        identity,
        1.4,
        'W',
    )

    ax.plot(
        *origin,
        'ks',
        markersize=8,
        label='原点',
    )

    ax.plot(
        *rotated_point,
        'o',
        color='tab:blue',
        markersize=10,
        label=r'回転後 $Rp$',
    )

    ax.plot(
        *restored_point,
        'o',
        color='tab:orange',
        markersize=10,
        label=r'元に戻った点 $R^TRp$',
    )

    ax.plot(
        [0, rotated_point[0]],
        [0, rotated_point[1]],
        '--',
        color='tab:blue',
        lw=1.5,
    )

    ax.plot(
        [0, restored_point[0]],
        [0, restored_point[1]],
        '--',
        color='tab:orange',
        lw=1.5,
    )

    ax.add_patch(
        FancyArrowPatch(
            rotated_point,
            restored_point,
            arrowstyle='->',
            mutation_scale=12,
            color='tab:purple',
            lw=1.5,
            linestyle='--',
        )
    )

    midpoint = 0.5 * (rotated_point + restored_point)

    ax.text(
        *(midpoint + np.array([0.05, 0.15])),
        rf'$R^T$：-{theta_deg:.0f}°回転',
        color='tab:purple',
        fontsize=9,
    )

    ax.annotate(
        rf'$Rp = ({rotated_point[0]:.2f}, '
        rf'{rotated_point[1]:.2f})$',
        rotated_point,
        textcoords='offset points',
        xytext=(8, 8),
        fontsize=10,
    )

    ax.annotate(
        rf'$R^TRp = ({restored_point[0]:.2f}, '
        rf'{restored_point[1]:.2f})$',
        restored_point,
        textcoords='offset points',
        xytext=(8, 8),
        fontsize=10,
    )

    configure_axis(
        ax,
        (-2.0, 2.0),
        (-2.0, 2.0),
        rf'逆変換  ($R^T$：-{theta_deg:.0f}°)',
    )

    ax.legend(loc='upper left')


# ==================================================
# 実行系の関数
# ==================================================

# 計算結果をコンソールに出力する
def print_results(
    point,
    theta_deg,
    rotation,
    rotation_transpose,
    rotated_point,
    restored_point,
    identity,
):
    print('=== 回転行列の逆変換と転置 ===')

    print(f'元の点 p                = {point}')
    print(f'回転角 theta             = {theta_deg:.1f} deg')

    print('\n回転行列 R =')
    print(rotation)

    print('\n転置行列 R^T =')
    print(rotation_transpose)

    print(f'\n回転後の点 R p           = {rotated_point}')
    print(f'逆回転後の点 R^T R p     = {restored_point}')

    print('\nR^T R = I')
    print(identity)

    print('\nR^T R = I を確認')
    print(np.allclose(identity, np.eye(2)))

    print('\nR^-1 = R^T を確認')
    print(
        np.allclose(
            np.linalg.inv(rotation),
            rotation_transpose,
        )
    )


# 回転・逆回転の計算・検証・出力・描画を実行する
def main():
    setup_font()

    point = np.array([1.0, 0.5])
    theta_deg = 60.0
    theta = np.deg2rad(theta_deg)

    # +thetaの回転行列を計算する
    rotation = rotation_matrix(theta)

    # 回転行列の転置を計算する
    rotation_transpose = transpose_rotation(rotation)

    # Rによって点を回転させる
    rotated_point = rotate_point(
        point,
        rotation,
    )

    # R^Tによって逆回転させる
    restored_point = rotate_point(
        rotated_point,
        rotation_transpose,
    )

    # R^T R = I を計算する
    identity = verify_inverse(rotation)

    # 逆変換によって元の点に戻ることを検証する
    assert np.allclose(
        restored_point,
        point,
    )

    # R^-1 = R^T であることを検証する
    assert np.allclose(
        np.linalg.inv(rotation),
        rotation_transpose,
    )

    print_results(
        point,
        theta_deg,
        rotation,
        rotation_transpose,
        rotated_point,
        restored_point,
        identity,
    )

    # 元の点・順変換・逆変換を描画する
    fig, axes = plt.subplots(
        1,
        3,
        figsize=(16, 5),
    )

    draw_original(
        axes[0],
        point,
    )

    draw_forward_rotation(
        axes[1],
        point,
        rotated_point,
        rotation,
        theta_deg,
    )

    draw_inverse_rotation(
        axes[2],
        rotated_point,
        restored_point,
        rotation_transpose,
        theta_deg,
    )

    fig.suptitle(
        r'回転行列の逆変換：$R^{-1} = R^T$',
        fontsize=14,
    )

    fig.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()