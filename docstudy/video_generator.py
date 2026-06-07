import os
import asyncio
import edge_tts
from moviepy import VideoClip, AudioFileClip, CompositeVideoClip
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import time


VIDEO_OUTPUT_DIR = "video_output"

if not os.path.exists(VIDEO_OUTPUT_DIR):
    os.makedirs(VIDEO_OUTPUT_DIR)


async def generate_audio_with_retry(text, audio_path, max_retries=3):
    for attempt in range(max_retries):
        try:
            communicate = edge_tts.Communicate(text, "zh-CN-XiaoxiaoNeural")
            await communicate.save(audio_path)
            print(f"[VIDEO] Audio generated successfully (attempt {attempt + 1})")
            return audio_path
        except Exception as e:
            print(f"[VIDEO] Audio generation failed (attempt {attempt + 1}/{max_retries}): {str(e)}")
            if attempt < max_retries - 1:
                print(f"[VIDEO] Retrying in {2 ** attempt} seconds...")
                await asyncio.sleep(2 ** attempt)
    
    raise Exception(f"Audio generation failed after {max_retries} attempts")


def get_chinese_font(font_size):
    font_paths = [
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/simfang.ttf",
        "C:/Windows/Fonts/simsun.ttc",
        "C:/Windows/Fonts/msyhbd.ttc",
    ]
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                return ImageFont.truetype(font_path, font_size)
            except:
                continue
    
    try:
        return ImageFont.truetype("arial.ttf", font_size)
    except:
        return ImageFont.load_default()


def generate_cover_image(title, output_path, width=1920, height=1080):
    img = Image.new('RGB', (width, height), color=(66, 126, 234))
    draw = ImageDraw.Draw(img)
    
    font_title = get_chinese_font(64)
    font_subtitle = get_chinese_font(32)
    
    title_lines = []
    current_line = ""
    for word in title:
        if draw.textlength(current_line + word, font=font_title) < width - 100:
            current_line += word
        else:
            title_lines.append(current_line)
            current_line = word
    if current_line:
        title_lines.append(current_line)
    
    y_offset = height // 2 - len(title_lines) * 40
    
    for i, line in enumerate(title_lines):
        text_width = draw.textlength(line, font=font_title)
        x = (width - text_width) // 2
        y = y_offset + i * 80
        draw.text((x, y), line, font=font_title, fill="white")
    
    subtitle = "DocStudy - AI学习助手"
    subtitle_width = draw.textlength(subtitle, font=font_subtitle)
    draw.text(((width - subtitle_width) // 2, height - 100), subtitle, font=font_subtitle, fill="#e0e0e0")
    
    img.save(output_path)
    return output_path


def generate_video(audio_path, cover_image_path, video_path):
    audio_clip = AudioFileClip(audio_path)
    duration = audio_clip.duration
    
    cover_img = Image.open(cover_image_path)
    cover_np = np.array(cover_img)
    
    def make_frame(t):
        return cover_np
    
    video_clip = VideoClip(make_frame, duration=duration)
    video_clip.audio = audio_clip
    
    video_clip.write_videofile(video_path, fps=30, codec="libx264", audio_codec="aac")
    
    audio_clip.close()
    video_clip.close()
    
    return video_path


def create_teaching_video(title, script):
    video_name = f"{title[:20].replace(' ', '_')}_{hash(title + script) % 100000}.mp4"
    video_path = os.path.join(VIDEO_OUTPUT_DIR, video_name)
    
    if os.path.exists(video_path):
        print(f"[VIDEO] Video already exists: {video_path}")
        return video_path
    
    audio_path = os.path.join(VIDEO_OUTPUT_DIR, f"audio_{hash(script) % 100000}.mp3")
    cover_path = os.path.join(VIDEO_OUTPUT_DIR, f"cover_{hash(title) % 100000}.png")
    
    print("[VIDEO] Generating cover image...")
    generate_cover_image(title, cover_path)
    
    print("[VIDEO] Generating audio...")
    asyncio.run(generate_audio_with_retry(script, audio_path))
    
    print("[VIDEO] Generating video...")
    generate_video(audio_path, cover_path, video_path)
    
    if os.path.exists(audio_path):
        os.remove(audio_path)
    if os.path.exists(cover_path):
        os.remove(cover_path)
    
    print(f"[VIDEO] Video generated successfully: {video_path}")
    return video_path