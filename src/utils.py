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
        # 获取原图片的文件后缀名
        original_suffix = Path(image_path).suffix
        # 保存锐化后的图片到临时文件
        out_path = str(Path(image_path).with_suffix('')) + '_sharpened_' + original_suffix
        cv2.imwrite(out_path, sharpened)
        print(f"INFO: Sharpened image saved to {out_path}")
        return out_path
    except Exception as e:
        print(f"[WARN] Image sharpening failed: {e}, fallback to original image.")
        return image_path


from pathlib import Path


def resize_image_keep_quality(image, max_size=1600):
    """
    将图像按最长边 max_size 缩小，保持宽高比例
    """
    h, w = image.shape[:2]
    scale = min(max_size / max(h, w), 1.0)  # 仅当图像较大时才缩放
    if scale < 1.0:
        new_w = int(w * scale)
        new_h = int(h * scale)
        resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
        return resized
    else:
        return image


def process_image_2(image_path, resize_max=1600):
    """
    自动锐化并可选压缩图像尺寸，返回处理后图像路径。
    """
    try:
        print(f"INFO: Processing image at {image_path} with auto_sharpen...")

        # 锐化
        sharpened = auto_sharpen(image_path, show_steps=False)

        # 尺寸压缩（可选）
        sharpened = resize_image_keep_quality(sharpened, max_size=resize_max)

        # 保存路径
        original_suffix = Path(image_path).suffix
        out_path = str(Path(image_path).with_suffix('')) + '_sharpened_' + original_suffix

        # 保存图像（高质量 JPG）
        if original_suffix.lower() in ['.jpg', '.jpeg']:
            cv2.imwrite(out_path, sharpened, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
        else:
            cv2.imwrite(out_path, sharpened)

        print(f"INFO: Sharpened and resized image saved to {out_path}")
        return out_path

    except Exception as e:
        print(f"[WARN] Image sharpening failed: {e}, fallback to original image.")
        return image_path


if __name__ == "__main__":
    process_image_2("../tests/442.jpg")
