from pathlib import Path

import cv2

from src.image_cv2 import auto_sharpen

PUNCTUATION = "！？。＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘'‛""„‟…‧﹏."


def parse_text_for_display(text):
    """
    Parses raw text to be properly displayed in the Gradio HTML output.
    Handles code blocks and special characters.
    """
    lines = text.split("\n")
    lines = [line for line in lines if line != ""]
    count = 0
    for i, line in enumerate(lines):
        if "```" in line:
            count += 1
            items = line.split("`")
            if count % 2 == 1:
                lines[i] = f'<pre><code class="language-{items[-1]}">'
            else:
                lines[i] = f"<br></code></pre>"
        else:
            if i > 0:
                if count % 2 == 1:
                    line = line.replace("`", r"\`")
                    line = line.replace("<", "<")
                    line = line.replace(">", ">")
                    line = line.replace(" ", " ")
                    line = line.replace("*", "*")
                    line = line.replace("_", "_")
                    line = line.replace("-", "-")
                    line = line.replace(".", ".")
                    line = line.replace("!", "!")
                    line = line.replace("(", "(")
                    line = line.replace(")", ")")
                    line = line.replace("$", "$")
                lines[i] = "<br>" + line
    text = "".join(lines)
    return text


def is_video_file(filename):
    """
    Checks if a given filename has a video file extension.
    """
    video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.mpeg']
    if not isinstance(filename, str):
        return False
    return any(filename.lower().endswith(ext) for ext in video_extensions)


def process_image(image_path):
    """
    对图片进行自动锐化处理，返回锐化后图片的路径。
    若处理失败，则返回原图路径。
    """
    try:
        print(f"INFO: Processing image at {image_path} with auto_sharpen...")
        sharpened = auto_sharpen(image_path, show_steps=False)
        # 保存锐化后的图片到临时文件
        out_path = str(Path(image_path).with_suffix('')) + '_sharpened.png'
        cv2.imwrite(out_path, sharpened)
        print(f"INFO: Sharpened image saved to {out_path}")
        return out_path
    except Exception as e:
        print(f"[WARN] Image sharpening failed: {e}, fallback to original image.")
        return image_path
