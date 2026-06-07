import os
import json
import asyncio
import edge_tts
from moviepy import VideoClip, AudioFileClip, concatenate_videoclips
from PIL import Image, ImageDraw, ImageFont
import numpy as np

OUTPUT_DIR = "lesson_output"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)


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


async def generate_audio_segment(text, audio_path):
    communicate = edge_tts.Communicate(text, "zh-CN-XiaoxiaoNeural")
    await communicate.save(audio_path)
    return audio_path


def generate_chapter_image(chapter_title, chapter_content, output_path, chapter_num, total_chapters):
    width, height = 1920, 1080
    img = Image.new('RGB', (width, height), color=(66, 126, 234))
    draw = ImageDraw.Draw(img)
    
    font_title = get_chinese_font(56)
    font_content = get_chinese_font(32)
    font_small = get_chinese_font(24)
    
    header_y = 80
    
    chapter_label = f"章节 {chapter_num}/{total_chapters}"
    label_width = draw.textlength(chapter_label, font_small)
    draw.text(((width - label_width) // 2, header_y), chapter_label, font=font_small, fill="#b0d0ff")
    
    title_lines = []
    current_line = ""
    for word in chapter_title:
        if draw.textlength(current_line + word, font=font_title) < width - 200:
            current_line += word
        else:
            title_lines.append(current_line)
            current_line = word
    if current_line:
        title_lines.append(current_line)
    
    title_y = header_y + 60
    for i, line in enumerate(title_lines):
        text_width = draw.textlength(line, font=font_title)
        x = (width - text_width) // 2
        y = title_y + i * 70
        draw.text((x, y), line, font=font_title, fill="white")
    
    content_y = title_y + len(title_lines) * 70 + 60
    content_box_width = width - 200
    content_box_height = height - content_y - 100
    
    content_lines = []
    current_line = ""
    for word in chapter_content:
        if draw.textlength(current_line + word, font=font_content) < content_box_width:
            current_line += word
        else:
            content_lines.append(current_line)
            current_line = word
    if current_line:
        content_lines.append(current_line)
    
    max_lines = int(content_box_height / 40)
    content_lines = content_lines[:max_lines]
    
    for i, line in enumerate(content_lines):
        x = (width - draw.textlength(line, font=font_content)) // 2
        y = content_y + i * 40
        draw.text((x, y), line, font=font_content, fill="#e8f0ff")
    
    arrow_x = width // 2
    arrow_y = height - 60
    arrow_size = 20
    draw.polygon([
        (arrow_x - arrow_size, arrow_y - arrow_size),
        (arrow_x + arrow_size, arrow_y - arrow_size),
        (arrow_x, arrow_y)
    ], fill="#ffffff")
    
    img.save(output_path)
    return output_path


def generate_cover_image(title, output_path):
    width, height = 1920, 1080
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


def generate_end_image(title, output_path):
    width, height = 1920, 1080
    img = Image.new('RGB', (width, height), color=(66, 126, 234))
    draw = ImageDraw.Draw(img)
    
    font_title = get_chinese_font(64)
    font_subtitle = get_chinese_font(32)
    
    end_text = "🎉 课程结束"
    text_width = draw.textlength(end_text, font=font_title)
    draw.text(((width - text_width) // 2, height // 2 - 80), end_text, font=font_title, fill="white")
    
    thanks_text = "感谢观看"
    thanks_width = draw.textlength(thanks_text, font_subtitle)
    draw.text(((width - thanks_width) // 2, height // 2 + 40), thanks_text, font=font_subtitle, fill="#e0e0e0")
    
    img.save(output_path)
    return output_path


def parse_lesson_script(script_text):
    try:
        script_text = script_text.strip()
        if script_text.startswith('```json'):
            script_text = script_text[7:]
        if script_text.endswith('```'):
            script_text = script_text[:-3]
        
        data = json.loads(script_text)
        if isinstance(data, list):
            return data
        elif isinstance(data, dict) and 'chapters' in data:
            return data['chapters']
        else:
            return []
    except json.JSONDecodeError:
        return []


def build_lesson_video(title, chapters):
    lesson_name = f"{title[:20].replace(' ', '_')}_{hash(title) % 100000}"
    video_path = os.path.join(OUTPUT_DIR, f"{lesson_name}.mp4")
    
    if os.path.exists(video_path):
        print(f"[LESSON] Video already exists: {video_path}")
        return video_path
    
    cover_path = os.path.join(OUTPUT_DIR, f"{lesson_name}_cover.png")
    end_path = os.path.join(OUTPUT_DIR, f"{lesson_name}_end.png")
    
    print("[LESSON] Generating cover image...")
    generate_cover_image(title, cover_path)
    
    print("[LESSON] Generating end image...")
    generate_end_image(title, end_path)
    
    chapter_images = []
    chapter_audios = []
    
    for i, chapter in enumerate(chapters):
        chapter_title = chapter.get("title", f"章节 {i+1}")
        chapter_content = chapter.get("content", "")
        
        print(f"[LESSON] Processing chapter {i+1}: {chapter_title}")
        
        img_path = os.path.join(OUTPUT_DIR, f"{lesson_name}_chapter_{i+1}.png")
        audio_path = os.path.join(OUTPUT_DIR, f"{lesson_name}_chapter_{i+1}.mp3")
        
        generate_chapter_image(chapter_title, chapter_content, img_path, i+1, len(chapters))
        chapter_images.append(img_path)
        
        asyncio.run(generate_audio_segment(chapter_content, audio_path))
        chapter_audios.append(audio_path)
    
    print("[LESSON] Assembling video...")
    
    video_clips = []
    
    cover_img = Image.open(cover_path)
    cover_np = np.array(cover_img)
    
    def cover_frame(t):
        return cover_np
    
    cover_clip = VideoClip(cover_frame, duration=3)
    video_clips.append(cover_clip)
    
    for i, (img_path, audio_path) in enumerate(zip(chapter_images, chapter_audios)):
        audio_clip = AudioFileClip(audio_path)
        duration = audio_clip.duration
        
        chapter_img = Image.open(img_path)
        chapter_np = np.array(chapter_img)
        
        def make_chapter_frame(t, np_img=chapter_np):
            return np_img
        
        chapter_clip = VideoClip(make_chapter_frame, duration=duration)
        chapter_clip.audio = audio_clip
        video_clips.append(chapter_clip)
    
    end_img = Image.open(end_path)
    end_np = np.array(end_img)
    
    def end_frame(t):
        return end_np
    
    end_clip = VideoClip(end_frame, duration=2)
    video_clips.append(end_clip)
    
    final_video = concatenate_videoclips(video_clips, method="compose")
    
    final_video.write_videofile(video_path, fps=30, codec="libx264", audio_codec="aac")
    
    for clip in video_clips:
        if hasattr(clip, 'close'):
            clip.close()
    final_video.close()
    
    for img_path in chapter_images:
        if os.path.exists(img_path):
            os.remove(img_path)
    for audio_path in chapter_audios:
        if os.path.exists(audio_path):
            os.remove(audio_path)
    if os.path.exists(cover_path):
        os.remove(cover_path)
    if os.path.exists(end_path):
        os.remove(end_path)
    
    print(f"[LESSON] Lesson video generated successfully: {video_path}")
    return video_path