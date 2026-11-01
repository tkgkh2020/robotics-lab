# Quadruped Free Resources

> 2026-11-01 作成。[[Robotics｜ロボティクス]]（`docs/quadruped_roadmap.md`）の各 Stage で使う、無料で手に入る教材の一覧。
> Deep Research の調査結果から、無料で使えるものを残し、有料のものには無料の代替を付けた。

## 方針

- 本は、無料で公開されている Web 教科書・講義資料を使う
- 論文は、arXiv 版か Open Access 版を読む。トップ誌の論文でも、多くは arXiv に同じ内容がある
- 有料の本・セミナーは「今は不要」か「無料の代替あり」のどちらかに分類した
- GPU が必要なものは自宅では動かさず、4月以降の業務環境に回す

## 1. 教科書・講義（無料）

| 教材 | 無料で手に入る形 | 使う Stage | 使う範囲 |
|---|---|---|---|
| Modern Robotics（Lynch & Park） | 著者サイトのプレプリントPDF・講義動画・Python ライブラリ（https://hades.mech.northwestern.edu/index.php/Modern_Robotics ）、Coursera は聴講無料 | 1〜3 | Ch3〜6, 8.1〜8.2, 11, 12.2 |
| Underactuated Robotics（Tedrake, MIT） | Web 教科書（https://underactuated.mit.edu/ ）、講義動画 | 2〜3 | Ch4「Simple Models of Walking and Running」、Ch5「Highly-articulated Legged Robots」、「Planning and Control through Contact」の章 |
| ETH Zurich Robot Dynamics（Hutter ほか） | 講義ページ（https://rsl.ethz.ch/education-students/lectures/robotdynamics.html ）。2017年版の講義ノート（RD_HS2017script.pdf）と脚ロボット回のスライドが ETH のサイトで公開されていた | 2 | 浮遊ベースの運動学・動力学、接触拘束、タスク空間制御 |
| Featherstone の講義資料（Spatial Vector Algebra） | 著者サイトの講義スライド・ノート（https://royfeatherstone.org/teaching/ ） | 2（任意） | 6次元ベクトルによる剛体動力学。本（RBDA）の代わり |
| CMU 16-745 Optimal Control and RL（Manchester） | YouTube の講義動画（2025年第1回：https://www.youtube.com/watch?v=SvAYJC7jug8 ） | 3 | LQR、MPC、凸MPC、接触を伴う軌道最適化 |
| A micro Lie theory for state estimation in robotics（Solà ほか） | arXiv（https://arxiv.org/abs/1812.01537 ） | 2（任意） | SO(3) / SE(3) の微分を、状態推定で使う形で整理したもの |

## 2. サーベイ（無料）

| 論文 | 無料で手に入る形 | 使う Stage | 読み方 |
|---|---|---|---|
| Ha ら "Learning-based legged locomotion: State of the art and future perspectives"（IJRR 2025） | Open Access、arXiv（https://arxiv.org/abs/2406.01152 ） | 1.5, 4 | 1.5で§1〜2、4で MDP 設計と sim-to-real の節 |
| Wensing ら "Optimization-Based Control for Dynamic Legged Robots"（T-RO 2024） | arXiv（https://arxiv.org/abs/2211.11644 ） | 1.5, 3 | 1.5で§I〜II、3で簡略モデル・MPC・WBC の節 |
| Frey ら "Advances, challenges, and opportunities for legged robots"（Science Robotics） | arXiv（https://arxiv.org/abs/2607.28952 ） | 2 | 全体像。制御階層の周期の出典 |
| Katayama, Murooka, Tazaki "Model predictive control of legged and humanoid robots: models and algorithms"（Advanced Robotics 2023） | Open Access（https://doi.org/10.1080/01691864.2023.2168134 ） | 3 | MPC で使うモデル（LIPM〜全身）と解法の整理 |

## 3. マイルストーン論文（無料）

| 論文 | 無料で手に入る形 | Stage | 一言で |
|---|---|---|---|
| Di Carlo ら 2018 "Dynamic Locomotion in the MIT Cheetah 3 Through Convex MPC"（IROS） | MIT DSpace（https://dspace.mit.edu/bitstream/handle/1721.1/138000/convex_mpc_2fix.pdf ） | 3 | 単剛体モデルを線形化して QP にする凸MPC。P3 の実装元 |
| Kim ら 2019 "Highly dynamic quadruped locomotion via whole-body impulse control and MPC" | arXiv（https://arxiv.org/abs/1909.06586 ） | 3 | MPC＋WBC（Mini Cheetah） |
| Bloesch ら 2012 "State Estimation for Legged Robots – Consistent Fusion of Leg Kinematics and IMU"（RSS） | RSS の論文集（無料公開） | 3（任意） | 脚オドメトリ＋IMU の融合 |
| Hartley ら 2018 "Contact-Aided Invariant Extended Kalman Filtering for Legged Robot State Estimation"（RSS） | arXiv（https://arxiv.org/abs/1805.10410 ）、実装（https://github.com/UMich-BipedLab/Contact-Aided-Invariant-EKF ） | 5 | リー群上の EKF による脚ロボットの状態推定 |
| Hwangbo ら 2019 "Learning agile and dynamic motor skills for legged robots" | arXiv（https://arxiv.org/abs/1901.08652 ） | 4 | アクチュエータネットワークで RL 方策を実機へ転移 |
| Rudin ら 2021 "Learning to walk in minutes using massively parallel deep RL" | arXiv（https://arxiv.org/abs/2109.11978 ） | 4 | GPU 並列学習（legged_gym） |
| Lee ら 2020 "Learning quadrupedal locomotion over challenging terrain" | arXiv（https://arxiv.org/abs/2010.11251 ） | 4 | 教師－生徒学習＋カリキュラム |
| Kumar ら 2021 "RMA: Rapid Motor Adaptation for Legged Robots" | arXiv（https://arxiv.org/abs/2107.04034 ） | 4 | 履歴から環境パラメータを推定してオンライン適応 |
| Miki ら 2022 "Learning robust perceptive locomotion for quadrupedal robots in the wild" | arXiv（https://arxiv.org/abs/2201.08117 ） | 4→5 | エレベーションマップと固有受容感覚の融合 |
| Grandia ら 2023 "Perceptive Locomotion through Nonlinear MPC"（T-RO） | arXiv（https://arxiv.org/abs/2208.08373 ） | 5 | 地形の平面セグメンテーションを制約にした NMPC |

DTC（Jenelten 2024）、ANYmal Parkour（Hoeller 2024）なども、arXiv 版を探してから読む。

## 4. コード・シミュレータ（無料・CPUで動く）

| ツール | URL | Stage | 用途 |
|---|---|---|---|
| MuJoCo | https://mujoco.readthedocs.io/ （`pip install mujoco`） | 1.5〜4 | 物理シミュレータ。macOS でも動く |
| MuJoCo Menagerie | https://github.com/google-deepmind/mujoco_menagerie | 1.5〜4 | Unitree Go2 のモデル（`unitree_go2/scene.xml`）。Go1、A1、ANYmal なども入っている |
| cvxpy / OSQP | https://www.cvxpy.org/ 、https://osqp.org/ | 2〜3 | 接触力配分QP、凸MPC |
| Quadruped-PyMPC（iit-DLSLab） | https://github.com/iit-DLSLab/Quadruped-PyMPC | 3 | Python＋MuJoCo の単剛体モデルMPC。詰まったときの参照実装（acados のビルドが必要） |
| MIT Cheetah-Software | https://github.com/mit-biomimetics/Cheetah-Software | 3 | 凸MPC・WBC の C++ 実装。読む用 |
| Pinocchio | https://github.com/stack-of-tasks/pinocchio （`pip install pin`） | 2（任意） | 剛体動力学ライブラリ。MuJoCo の値との比較用 |
| Gymnasium（MuJoCo Ant） | https://gymnasium.farama.org/environments/mujoco/ant/ | 4 | CPU で学習できる4脚の RL 環境 |
| Stable-Baselines3 | https://stable-baselines3.readthedocs.io/ | 4 | PPO の実装 |

## 5. RL入門（無料）

| 教材 | URL | Stage | 使う範囲 |
|---|---|---|---|
| Sutton & Barto "Reinforcement Learning: An Introduction"（第2版） | 著者サイトで PDF 公開（http://incompleteideas.net/book/the-book-2nd.html ） | 4 | Ch3（MDP）、Ch13（方策勾配） |
| OpenAI Spinning Up | https://spinningup.openai.com/ | 4 | PPO の解説と擬似コード |
| Hugging Face Deep RL Course | https://huggingface.co/learn/deep-rl-course | 4（任意） | 手を動かす入門 |
| MuJoCo Playground | https://github.com/google-deepmind/mujoco_playground 、locomotion ノートブック（https://colab.research.google.com/github/google-deepmind/mujoco_playground/blob/main/learning/notebooks/locomotion.ipynb ） | 4 | Colab の GPU ランタイムで Go1 の速度追従を学習する |
| legged_gym | https://github.com/leggedrobotics/legged_gym | 4（読むだけ） | 報酬関数・ランダマイゼーションの実装例 |

## 6. Deep Research の有料教材と、無料の代替

| 有料の教材 | 判断 | 無料の代替 |
|---|---|---|
| Springer Handbook of Robotics 第48章（Wieber・Tedrake・Kuindersma） | 今は不要 | Underactuated Ch4〜5、Wensing らのサーベイ |
| 梶田『ヒューマノイドロボット（改訂2版）』 | 今は不要。4月以降、部門の共通テキストにするなら部門で購入を検討 | Underactuated Ch5（ZMP・重心）、Katayama らのサーベイ（LIPM） |
| Raibert "Legged Robots That Balance" | 今は不要 | Underactuated Ch4（Raibert ホッパー）、Di Carlo 2018（Raibert ヒューリスティックによる着地点） |
| Featherstone "Rigid Body Dynamics Algorithms" | 今は不要 | Featherstone 本人の講義スライド、MR Ch8、Pinocchio のドキュメント |
| 日本ロボット学会 ロボット工学セミナー | 自費では不要。業務の研修として検討 | Underactuated・CMU 16-745 の講義動画 |
| IEEE Robotics & Automation Magazine のレビュー（知覚付き歩行） | Stage 5 で必要になったら | arXiv 版や著者版を探す。会社の文献サービスを使う |

Modern Robotics は書籍版が有料だが、著者サイトのプレプリントPDFで足りる。

## 7. GPU が要るもの（自宅では動かせない）

| ツール | 必要な環境 | 自宅での代替 | 本格的に使う時期 |
|---|---|---|---|
| Isaac Lab / Isaac Sim | NVIDIA RTX GPU（Linux / Windows） | MuJoCo Playground（Colab） | 4月以降 |
| legged_gym / Isaac Gym | NVIDIA GPU（Linux） | コードを読むだけ | 4月以降 |
| unitree_rl_gym | NVIDIA GPU（Linux） | — | 4月以降（実機導入の手順書として） |
| MuJoCo Playground | GPU（Colab の GPU ランタイムで可） | Colab の無料枠 | 3月（P4） |

## 8. 日本語の無料資料

日本語の無料の体系書は、ほとんどない。英語の無料教材を主にし、日本語は実装例と国内の動向を知るために使う。

- RT Net / チームMA-KING「4足歩行ロボット MEVIUS 製作」シリーズ（Isaac Gym / Isaac Lab での学習）：https://rt-net.jp/mobility/archives/27731 、https://rt-net.jp/mobility/archives/28025
- 富士ソフト「Isaac Lab のインストール方法と四足歩行ロボットの強化学習の方法を解説」：https://www.fsi.co.jp/robot_simulator/cases/08.html
- J-STAGE の日本ロボット学会誌：解説記事の多くが無料で読める。「四脚」「歩行制御」「モデル予測制御」で検索する
- Katayama・Murooka・Tazaki のサーベイは英語だが、国内の研究者による整理

## 9. 会社のリソースで確認したいこと

- 文献サービス（IEEE Xplore、SpringerLink など）の契約。あれば Springer Handbook の章や IEEE の論文も読める
- 書籍購入・セミナー参加の費用を、来年度の業務として出せるか
- GPU ワークステーションと実機（Go2 クラスなど）を使える時期

## 確認状況

- このノートの作成時（2026-11-01）に Web で確認できたもの：Frey らのレビュー（arXiv:2607.28952）、Quadruped-PyMPC、MuJoCo Playground の locomotion ノートブック（GPU ランタイム必須、Go1 の速度追従は RTX 4090 で約7分）、Menagerie の Go2 モデル、Hartley の InEKF、Featherstone の講義資料
- MIT・ETH・Northwestern の各サイトは、作成時に接続して確認できなかった。リンク切れがあれば、タイトルで検索し直す
- 講演動画の URL は Deep Research の記載による（未確認）
