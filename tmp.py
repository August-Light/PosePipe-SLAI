from PIL import Image, ImageOps

def change_transparent_metal_hue(image_path, output_path, target_rgb):
    """
    改变银色金属贴图颜色，并完美保留 PNG 透明背景
    :param target_rgb: 目标颜色的 RGB 元组，例如红铜色 (184, 115, 51)
    """
    # 1. 以 RGBA 模式打开图片
    img = Image.open(image_path).convert("RGBA")
    
    # 2. 分离通道，提取出灰度颜色和透明度遮罩 (Alpha)
    r, g, b, alpha = img.split()
    gray_img = Image.merge("RGB", (r, g, b)).convert("L")
    
    # 3. 将灰度图着色为目标金属色（保留明暗高光）
    colored_rgb = ImageOps.colorize(gray_img, black="black", white=target_rgb)
    
    # 4. 将原本的透明度遮罩 (Alpha) 重新缝合回去
    final_img = Image.new("RGBA", img.size)
    final_img.paste(colored_rgb, (0, 0))
    final_img.putalpha(alpha)
    
    # 5. 保存为 PNG
    final_img.save(output_path, "PNG")
    print(f"转换完成！已保存至: {output_path}")

# --- 使用示例 ---
# 常见金属 RGB 值参考：
# 金色 (Gold): (212, 175, 55)
# 红铜色 (Copper): (184, 115, 51)
# 青铜色 (Bronze): (205, 127, 50)

change_transparent_metal_hue("img/pipe.png", "img/gold_pipe.png", (212, 175, 55))
