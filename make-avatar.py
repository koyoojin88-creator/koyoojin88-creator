#!/usr/bin/env python3
"""GitHub 프로필 사진 후보를 만든다.

아바타는 프로필에서 260px, 목록에서 40px, 댓글 옆에서 20px 까지 줄어든다.
그래서 500px 로 그려 놓고 끝내면 안 되고, 실제로 쓰이는 크기로 줄여서 봐야
한다 — contact.png 가 네 크기를 나란히 붙여 준다.

GitHub 은 대부분의 자리에서 아바타를 원으로 잘라 보여준다. 모서리에 뭘 두면
잘려 나가므로 가운데에서 멀리 두지 않는다.

    python3 make-avatar.py

avatar-a.png / avatar-b.png / avatar-c.png 와 contact.png 를 만든다.
"""
from PIL import Image, ImageDraw, ImageFont

BG = (251, 250, 249)      # --bg
ACCENT = (194, 96, 60)    # --accent
TEXT = (28, 26, 24)       # --text
WHITE = (255, 255, 255)

S = 1000   # 프로필은 260px CSS · 레티나 2배 = 520px 이라 500 으로는 살짝 무르다
TTC = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
BOLD = 6


def new():
    img = Image.new("RGB", (S, S), BG)
    return img, ImageDraw.Draw(img)


def circle(d, cx, cy, r, fill=None, outline=None, width=1):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill, outline=outline, width=width)


def a_dot():
    """사이트 파비콘 그대로. 헤더의 점과 같은 비율(반지름 = 변의 0.375)."""
    img, d = new()
    circle(d, S / 2, S / 2, S * 0.375, fill=ACCENT)
    return img


def b_initial():
    """강조색 원 위에 흰 「고」. 원으로 잘려도 그대로다."""
    img, d = new()
    circle(d, S / 2, S / 2, S / 2, fill=ACCENT)
    f = ImageFont.truetype(TTC, int(S * 0.52), index=BOLD)
    box = d.textbbox((0, 0), "고", font=f)
    d.text(((S - (box[2] - box[0])) / 2 - box[0],
            (S - (box[3] - box[1])) / 2 - box[1]), "고", font=f, fill=WHITE)
    return img


def c_one_and_many():
    """한 사람 하나, 페르소나 여럿.

    처음엔 빈 원 여섯으로 둘렀는데 40px 아래에서 얼룩이 됐다 — 선 두께가
    1px 미만으로 줄어 회색 점으로 뭉갠다. 개수를 셋으로 줄이고 속을 채워
    큰 덩어리 넷이 남게 했다. 20px 에서도 '여럿' 이 보인다."""
    import math
    img, d = new()
    cx = cy = S / 2
    ring = S * 0.30
    for i in range(3):
        ang = -math.pi / 2 + i * (2 * math.pi / 3)
        x, y = cx + ring * math.cos(ang), cy + ring * math.sin(ang)
        circle(d, x, y, S * 0.105, fill=ACCENT)
    circle(d, cx, cy, S * 0.165, fill=ACCENT)
    return img


def contact(imgs):
    """실제로 쓰이는 크기로 줄여 나란히 붙인다. 260 / 64 / 40 / 20."""
    sizes = [260, 64, 40, 20]
    pad, gap, label = 24, 22, 26   # label = 이름표가 차지하는 높이
    w = pad * 2 + sum(sizes) + gap * (len(sizes) - 1)
    row = 260 + label
    sheet = Image.new("RGB", (w, pad * 2 + label + row * len(imgs) + gap * (len(imgs) - 1)), (255, 255, 255))
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype(TTC, 15, index=BOLD)
    y = pad + label
    for name, im in imgs:
        x = pad
        for s in sizes:
            small = im.resize((s, s), Image.LANCZOS)
            # GitHub 은 원으로 자른다. 자른 모습으로 봐야 한다.
            mask = Image.new("L", (s * 4, s * 4), 0)
            ImageDraw.Draw(mask).ellipse([0, 0, s * 4 - 1, s * 4 - 1], fill=255)
            mask = mask.resize((s, s), Image.LANCZOS)
            sheet.paste(small, (x, y + (260 - s) // 2), mask)
            d.text((x, y + 264), "%dpx" % s, font=f, fill=(150, 150, 150))
            x += s + gap
        d.text((pad, y - 4), name, font=f, fill=(28, 26, 24))
        y += row + gap
    return sheet


def main():
    made = [("A 점", a_dot()), ("B 고", b_initial()), ("C 하나와 여럿", c_one_and_many())]
    for key, (_, img) in zip("abc", made):
        img.save("avatar-%s.png" % key)
    contact(made).save("contact.png")
    print("avatar-a.png / avatar-b.png / avatar-c.png · contact.png (%dx%d)" % (S, S))


if __name__ == "__main__":
    main()
