import cv2


def estimate_blur_score(gray_image):
    laplacian = cv2.Laplacian(gray_image, cv2.CV_64F)
    return laplacian.var()


def auto_sharpen(image_path, save_path=None, show_steps=True):
    # 读取图像
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"无法读取图像: {image_path}")

    # 转灰度
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 估算清晰度（方差越高越清晰）
    blur_score = estimate_blur_score(gray)

    # 决定锐化强度
    if blur_score < 50:
        # 非常模糊：强烈锐化
        alpha, beta, sigma = 1.8, 0.8, 3.0
        sharpen_level = "Strong"
    elif blur_score < 150:
        # 普通模糊：中等锐化
        alpha, beta, sigma = 1.5, 0.5, 2.0
        sharpen_level = "Medium"
    elif blur_score < 300:
        # 轻度模糊：轻柔锐化
        alpha, beta, sigma = 1.3, 0.3, 1.5
        sharpen_level = "Light"
    else:
        # 足够清晰：跳过锐化
        sharpened = gray
        sharpen_level = "None"

    if sharpen_level != "None":
        blurred = cv2.GaussianBlur(gray, (7, 7), sigma)
        sharpened = cv2.addWeighted(gray, alpha, blurred, -beta, 0)


    return sharpened
