"""
图片处理核心模块

提供图片等比例缩放、居中放置和模板合成功能
"""

from PIL import Image
import os


class ImageProcessor:
    """图片处理器类"""
    
    TEMPLATE_WIDTH = 471
    TEMPLATE_HEIGHT = 923
    TARGET_WIDTH = 393
    TARGET_HEIGHT = 852
    
    def __init__(self, template_path, background_color="#000000"):
        """
        初始化图片处理器
        
        @param template_path: 模板图片路径
        @param background_color: 画布背景颜色（十六进制格式，如 "#000000"）
        """
        self.template_path = template_path
        self.template_image = None
        self.background_color = background_color
        self.load_template()
    
    def load_template(self):
        """加载模板图片"""
        if os.path.exists(self.template_path):
            self.template_image = Image.open(self.template_path).convert("RGBA")
        else:
            raise FileNotFoundError(f"模板图片不存在: {self.template_path}")
    
    def resize_image_proportional(self, image, target_width, target_height):
        """
        等比例缩放图片
        
        保持原始宽高比，缩放图片使其能够完全覆盖目标尺寸
        
        @param image: PIL Image 对象
        @param target_width: 目标宽度
        @param target_height: 目标高度
        @return: 缩放后的 PIL Image 对象
        """
        original_width, original_height = image.size
        
        width_ratio = target_width / original_width
        height_ratio = target_height / original_height
        
        scale_ratio = max(width_ratio, height_ratio)
        
        new_width = int(original_width * scale_ratio)
        new_height = int(original_height * scale_ratio)
        
        resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        return resized_image
    
    def crop_to_size(self, image, target_width, target_height):
        """
        居中裁剪图片到指定尺寸
        
        @param image: PIL Image 对象
        @param target_width: 目标宽度
        @param target_height: 目标高度
        @return: 裁剪后的 PIL Image 对象
        """
        img_width, img_height = image.size
        
        left = (img_width - target_width) // 2
        top = (img_height - target_height) // 2
        right = left + target_width
        bottom = top + target_height
        
        return image.crop((left, top, right, bottom))
    
    def add_rounded_corners(self, image, radius):
        """
        为图片添加圆角效果
        
        @param image: PIL Image 对象
        @param radius: 圆角半径（像素）
        @return: 添加圆角后的 PIL Image 对象
        """
        from PIL import ImageDraw
        
        mask = Image.new('L', image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle([(0, 0), image.size], radius=radius, fill=255)
        
        result = Image.new('RGBA', image.size, (0, 0, 0, 0))
        result.paste(image, (0, 0))
        result.putalpha(mask)
        
        return result
    
    def process_wallpaper(self, wallpaper_path):
        """
        处理壁纸图片
        
        将用户上传的壁纸图片等比例缩放、裁剪到 393x852，然后居中放置到 471x923 画布上，最后与模板图片合成
        
        @param wallpaper_path: 壁纸图片路径
        @return: 处理后的 PIL Image 对象
        """
        if not os.path.exists(wallpaper_path):
            raise FileNotFoundError(f"壁纸图片不存在: {wallpaper_path}")
        
        wallpaper_image = Image.open(wallpaper_path).convert("RGBA")
        
        resized_wallpaper = self.resize_image_proportional(
            wallpaper_image,
            self.TARGET_WIDTH,
            self.TARGET_HEIGHT
        )
        
        cropped_wallpaper = self.crop_to_size(
            resized_wallpaper,
            self.TARGET_WIDTH,
            self.TARGET_HEIGHT
        )
        
        rounded_wallpaper = self.add_rounded_corners(cropped_wallpaper, 22)
        
        bg_color = self._hex_to_rgb(self.background_color)
        canvas = Image.new("RGBA", (self.TEMPLATE_WIDTH, self.TEMPLATE_HEIGHT), bg_color + (255,))
        
        x_offset = (self.TEMPLATE_WIDTH - self.TARGET_WIDTH) // 2
        y_offset = (self.TEMPLATE_HEIGHT - self.TARGET_HEIGHT) // 2
        
        canvas.paste(rounded_wallpaper, (x_offset, y_offset), rounded_wallpaper)
        
        if self.template_image is None:
            self.load_template()
        
        result = Image.alpha_composite(canvas, self.template_image)
        
        return result
    
    def _hex_to_rgb(self, hex_color):
        """
        将十六进制颜色转换为 RGB 元组
        
        @param hex_color: 十六进制颜色字符串（如 "#000000"）
        @return: RGB 元组 (r, g, b)
        """
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def create_grid_layout(self, processed_images, rows, cols):
        """
        创建多图网格拼接
        
        @param processed_images: 处理后的图片列表
        @param rows: 行数
        @param cols: 列数
        @return: 拼接后的 PIL Image 对象
        """
        canvas_width = cols * self.TEMPLATE_WIDTH
        canvas_height = rows * self.TEMPLATE_HEIGHT
        bg_color = self._hex_to_rgb(self.background_color)
        canvas = Image.new('RGB', (canvas_width, canvas_height), bg_color)
        
        for idx, img in enumerate(processed_images):
            row = idx // cols
            col = idx % cols
            x = col * self.TEMPLATE_WIDTH
            y = row * self.TEMPLATE_HEIGHT
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            canvas.paste(img, (x, y))
        
        return canvas
    
    def save_result(self, image, output_path, save_format="PNG", quality=95):
        """
        保存处理后的图片
        
        @param image: PIL Image 对象
        @param output_path: 输出文件路径
        @param save_format: 保存格式 (PNG 或 JPG)
        @param quality: 保存质量 (1-100)
        """
        if image.mode == "RGBA" and save_format == "JPG":
            image = image.convert("RGB")
        
        if save_format == "PNG":
            image.save(output_path, format="PNG", optimize=True)
        else:
            if image.mode == "RGBA":
                image = image.convert("RGB")
            image.save(output_path, format="JPEG", quality=quality)

