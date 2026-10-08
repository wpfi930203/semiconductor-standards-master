"""生成「半导体标准专家」skill 图标（v1）。

设计：芯片（JESD）
  深蓝渐变底   = 半导体 / 硅基
  铜金引脚+壳体 = 封装与互连金属（Cu / Au —— 本 skill 考核的正是键合与焊点）
  靛蓝裸片     = die
  青色 JESD    = JEDEC 标准编号前缀 —— 这是本 skill 的独占语义

为什么不是「通用芯片」：一颗没有编号的芯片只能表示"半导体"，
本机已有多个芯片类 skill（chip-fa-*、semiconductor-process-master）会撞图。
芯片身上压"JESD"三个字母，才把"半导体"收窄成"半导体制程标准"——
这正是本 skill 的定位（不是做芯片，是用标准做工程判定）。

20 根引脚 = 封装可考性；左上角 pin-1 圆点 = 让方形读成"芯片"而不是"色块"。

输出：
  icons/logo.png   200x200 PNG（对齐 lean-production-expert 规格）
  icons/logo.svg   矢量源文件（可再编辑，零版权风险）

纯 Pillow 手绘矢量形状，不调用任何图像生成 API。
"""
import pathlib

from PIL import Image, ImageDraw, ImageFont

OUT = pathlib.Path(__file__).resolve().parent.parent / "icons"
OUT.mkdir(parents=True, exist_ok=True)

S = 200          # 输出尺寸
SS = 4           # 超采样倍数
W = S * SS

# 配色：深硅蓝底 + 铜金封装 + 靛蓝裸片 + 青色 JESD
BG_TOP = (14, 32, 56)       # #0E2038
BG_BOT = (26, 58, 92)       # #1A3A5C
SHELL_TOP = (245, 185, 66)  # #F5B942
SHELL_BOT = (217, 138, 31)  # #D98A1F
DIE = (12, 28, 48)          # #0C1C30
DIE_EDGE = (58, 110, 150)   # #3A6E96
JESD = (111, 227, 214)      # #6FE3D6
PIN1 = (120, 78, 16)        # #784E10

FONT_BOLD = r"C:\Windows\Fonts\arialbd.ttf"


def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def vgrad(size, c0, c1):
    """垂直渐变图层。"""
    w, h = size
    g = Image.new("RGB", (1, h))
    px = g.load()
    for y in range(h):
        px[0, y] = lerp(c0, c1, y / max(1, h - 1))
    return g.resize((w, h), Image.NEAREST)


def rrect_mask(size, box, radius):
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).rounded_rectangle(box, radius=radius, fill=255)
    return m


# ---- 结构坐标（以 200px 画布为基准）----
PIN_CENTERS = (62, 86, 110, 134)
PIN_HALF = 3.5          # 引脚半宽
PIN_OUT = 22            # 引脚外端
SHELL_T = 40.0           # 壳体上/左边界
SHELL_B = 160.0          # 壳体下/右边界
SHELL_R = 14.0
DIE_T, DIE_B, DIE_R = 58.0, 142.0, 8.0
PIN1_C = (55.0, 55.0)
PIN1_R = 4.5


def draw() -> Image.Image:
    img = vgrad((W, W), BG_TOP, BG_BOT).convert("RGBA")

    # 背景圆角遮罩
    bg_mask = rrect_mask((W, W), (0, 0, W - 1, W - 1), 44 * SS)
    img.putalpha(bg_mask)
    d = ImageDraw.Draw(img)

    s = SS  # 坐标缩放快捷方式

    # ---- 20 根铜金引脚（4 边 × 5 根）----
    pin_col = lerp(SHELL_TOP, SHELL_BOT, 0.45) + (255,)
    for c in PIN_CENTERS:
        # 上
        d.rectangle([(c - PIN_HALF) * s, PIN_OUT * s,
                     (c + PIN_HALF) * s, SHELL_T * s], fill=pin_col)
        # 下
        d.rectangle([(c - PIN_HALF) * s, SHELL_B * s,
                     (c + PIN_HALF) * s, (200 - PIN_OUT) * s], fill=pin_col)
        # 左
        d.rectangle([PIN_OUT * s, (c - PIN_HALF) * s,
                     SHELL_T * s, (c + PIN_HALF) * s], fill=pin_col)
        # 右
        d.rectangle([SHELL_B * s, (c - PIN_HALF) * s,
                     (200 - PIN_OUT) * s, (c + PIN_HALF) * s], fill=pin_col)

    # ---- 铜金壳体（垂直渐变）----
    shell_box = (SHELL_T * s, SHELL_T * s, SHELL_B * s, SHELL_B * s)
    shell_mask = rrect_mask((W, W), shell_box, SHELL_R * s)
    img.paste(vgrad((W, W), SHELL_TOP, SHELL_BOT), (0, 0), shell_mask)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle(shell_box, radius=SHELL_R * s, outline=(150, 92, 12, 255), width=2 * s)

    # ---- pin-1 定位点 ----
    d.ellipse([(PIN1_C[0] - PIN1_R) * s, (PIN1_C[1] - PIN1_R) * s,
               (PIN1_C[0] + PIN1_R) * s, (PIN1_C[1] + PIN1_R) * s],
              fill=PIN1 + (255,))

    # ---- 靛蓝裸片 ----
    die_box = (DIE_T * s, DIE_T * s, DIE_B * s, DIE_B * s)
    d.rounded_rectangle(die_box, radius=DIE_R * s, fill=DIE + (255,),
                        outline=DIE_EDGE + (255,), width=2 * s)

    # ---- JESD 字样 ----
    fsize = 30 * s
    font = ImageFont.truetype(FONT_BOLD, fsize)
    d.text((100 * s, 96 * s), "JESD", font=font, fill=JESD + (255,), anchor="mm")

    # 字下方的"标准编号"下划条，强化"这是一条标准"的读法
    d.rectangle([76 * s, 116 * s, 124 * s, 120 * s], fill=JESD + (255,))

    return img.convert("RGB").resize((S, S), Image.LANCZOS)


if __name__ == "__main__":
    out = draw()
    png = OUT / "logo.png"
    out.save(png, "PNG")
    print(f"✓ {png}  {out.size[0]}x{out.size[1]}  {png.stat().st_size:,} bytes")
    print("  (矢量源 icons/logo.svg 需手工保持与本脚本一致)")
