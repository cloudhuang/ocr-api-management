from paddleocr import PaddleOCR

ocr = PaddleOCR(use_angle_cls=True,
                lang='ch')  # 中文检测模型（支持简繁）
result = ocr.predict('400.png')

print("Result:\n")

# 可视化结果并保存 json 结果
for res in result:
    res.print()
    res.save_to_img("output")
    res.save_to_json("output")
