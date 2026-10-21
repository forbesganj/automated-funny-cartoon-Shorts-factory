import argparse, json, math, os, tempfile
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

W, H, FPS, DURATION = 720, 1280, 12, 30
BG = (239, 229, 208)
INK = (28, 27, 25)
MUTED = (170, 155, 130)
WHITE = (250, 248, 241)
RED = (190, 75, 58)

def font(size, bold=False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/Library/Fonts/Arial.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def centered(draw, xy, text, fnt, fill):
    box = draw.textbbox((0,0), text, font=fnt)
    draw.text((xy[0]-(box[2]-box[0])/2, xy[1]), text, font=fnt, fill=fill)

def draw_person(draw, cx, cy, t, action, muscular=False, helper=False):
    # Cy is the approximate head centre. Deterministic, simple vector cartoon.
    bob = int(3*math.sin(t*5))
    cx, cy = int(cx), int(cy+bob)
    head_r = 42 if not muscular else 46
    # body and clothes
    draw.ellipse((cx-head_r,cy-head_r,cx+head_r,cy+head_r), fill=WHITE, outline=INK, width=5)
    # eyes
    eye_y = cy-5
    draw.ellipse((cx-17,eye_y-4,cx-9,eye_y+4), fill=INK)
    draw.ellipse((cx+9,eye_y-4,cx+17,eye_y+4), fill=INK)
    # expression
    if action in ("shake","help") and not muscular:
        draw.arc((cx-17,cy+8,cx+17,cy+30), 15, 165, fill=INK, width=4)
        draw.ellipse((cx+27,cy-29,cx+36,cy-17), outline=(80,150,190), width=3)
    elif action == "pose":
        draw.arc((cx-18,cy+5,cx+18,cy+25), 190, 345, fill=INK, width=4)
    else:
        draw.line((cx-13,cy+17,cx+13,cy+17), fill=INK, width=4)
    # torso
    shoulder = 58 if muscular else 39
    torso_bottom = cy+150
    draw.rounded_rectangle((cx-shoulder,cy+head_r-2,cx+shoulder,torso_bottom), radius=18, fill=WHITE, outline=INK, width=5)
    # arms vary by action
    if action == "pose":
        draw.line((cx-shoulder+3,cy+head_r+18,cx-shoulder-35,cy+head_r-15,cx-shoulder-13,cy+head_r-42), fill=INK, width=12, joint="curve")
        draw.line((cx+shoulder-3,cy+head_r+18,cx+shoulder+35,cy+head_r-15,cx+shoulder+13,cy+head_r-42), fill=INK, width=12, joint="curve")
    elif action == "lift":
        draw.line((cx-shoulder+2,cy+head_r+18,cx-shoulder-30,cy+head_r+65), fill=INK, width=12)
        draw.line((cx+shoulder-2,cy+head_r+18,cx+shoulder+30,cy+head_r+65), fill=INK, width=12)
        # dumbbell
        dx = cx+shoulder+40
        dy = cy+head_r+65-int(12*abs(math.sin(t*3)))
        draw.line((dx-22,dy,dx+22,dy), fill=INK, width=7)
        draw.rounded_rectangle((dx-30,dy-15,dx-20,dy+15), radius=3, fill=MUTED, outline=INK, width=3)
        draw.rounded_rectangle((dx+20,dy-15,dx+30,dy+15), radius=3, fill=MUTED, outline=INK, width=3)
    elif action == "squat":
        draw.line((cx-shoulder+2,cy+head_r+18,cx-shoulder-30,cy+head_r+60), fill=INK, width=12)
        draw.line((cx+shoulder-2,cy+head_r+18,cx+shoulder+30,cy+head_r+60), fill=INK, width=12)
    else:
        draw.line((cx-shoulder+2,cy+head_r+18,cx-shoulder-22,cy+head_r+80), fill=INK, width=12)
        draw.line((cx+shoulder-2,cy+head_r+18,cx+shoulder+22,cy+head_r+80), fill=INK, width=12)
    # legs
    if action == "squat":
        draw.line((cx-22,torso_bottom,cx-48,torso_bottom+35,cx-20,torso_bottom+65), fill=INK, width=14, joint="curve")
        draw.line((cx+22,torso_bottom,cx+48,torso_bottom+35,cx+20,torso_bottom+65), fill=INK, width=14, joint="curve")
    else:
        draw.line((cx-22,torso_bottom,cx-28,torso_bottom+88), fill=INK, width=14)
        draw.line((cx+22,torso_bottom,cx+28,torso_bottom+88), fill=INK, width=14)
    # shoes
    draw.line((cx-28,torso_bottom+88,cx-50,torso_bottom+88), fill=INK, width=12)
    draw.line((cx+28,torso_bottom+88,cx+50,torso_bottom+88), fill=INK, width=12)

def render(script_path, output_path, preview=False):
    with open(script_path, encoding="utf-8") as f:
        story = json.load(f)
    writer = imageio_ffmpeg.write_frames(
        output_path, (W,H), fps=FPS, codec="libx264", quality=8,
        pix_fmt_in="rgb24", pix_fmt_out="yuv420p",
        output_params=["-movflags","+faststart","-an"]
    )
    writer.send(None)
    total = FPS * DURATION
    for frame in range(total):
        t = frame / FPS
        scene = next((s for s in story["scenes"] if s["start"] <= t < s["end"]), story["scenes"][-1])
        action = scene.get("action", "enter")
        im = Image.new("RGB", (W,H), BG)
        d = ImageDraw.Draw(im)
        # background gym details
        d.rectangle((0, 930, W, H), fill=(225,211,185))
        d.line((0,930,W,930), fill=MUTED, width=3)
        # wall lines / floor tiles
        for x in range(40, W, 120):
            d.line((x,140,x,900), fill=(226,215,195), width=2)
            d.line((x,930,x-30,H), fill=(212,197,172), width=2)
        # rack
        d.line((70,520,70,920), fill=INK, width=9)
        d.line((650,520,650,920), fill=INK, width=9)
        d.line((70,570,650,570), fill=INK, width=8)
        # scene heading
        centered(d,(W/2,65),story["title"].upper(),font(26,True),INK)
        # character motion
        shake = 7*math.sin(t*16) if action == "shake" else 0
        main_x = 300 + shake
        draw_person(d, main_x, 480, t, action)
        if action in ("help","pose"):
            draw_person(d, 500, 485, t+1, "pose", muscular=True, helper=True)
        # caption card
        caption = scene.get("caption","")
        d.rounded_rectangle((38,1050,W-38,1178), radius=22, fill=WHITE, outline=INK, width=3)
        words = caption.split()
        lines, current = [], ""
        for word in words:
            test = (current+" "+word).strip()
            if d.textbbox((0,0),test,font=font(31,True))[2] > W-100:
                lines.append(current); current=word
            else: current=test
        if current: lines.append(current)
        for i,line in enumerate(lines[:2]):
            centered(d,(W/2,1070+i*42),line,font(31,True),INK)
        # tiny brand mark
        d.text((35,1220),"GYM SKETCHES",font=font(17,True),fill=(95,86,72))
        # dialogue bubble at relevant moments
        dialogue = next((x for x in story.get("dialogue",[]) if abs(x["time"]-t)<(0.5/FPS)),None)
        if dialogue:
            txt = dialogue["text"][:38]
            d.rounded_rectangle((95,210,625,285),radius=20,fill=WHITE,outline=INK,width=3)
            centered(d,(W/2,230),txt,font(22,True),INK)
        writer.send(im.tobytes())
    writer.close()
    print(f"Rendered {output_path} ({W}x{H}, {DURATION}s, {FPS}fps)")

if __name__ == "__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--script",default="script.json")
    p.add_argument("--output",default="preview.mp4")
    p.add_argument("--preview",action="store_true")
    a=p.parse_args()
    render(a.script,a.output,a.preview)
