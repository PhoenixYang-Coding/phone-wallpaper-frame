"""
配置管理模块

负责应用配置的读取、保存和管理
"""

import json
import os
from pathlib import Path


class ConfigManager:
    """配置管理器类"""
    
    def __init__(self):
        """初始化配置管理器"""
        self.config_file = self._get_config_file_path()
        self.config = self._load_default_config()
        self.load_config()
    
    def _get_config_file_path(self):
        """
        获取配置文件路径
        
        配置文件存储在用户主目录下
        
        @return: 配置文件的完整路径
        """
        home_dir = Path.home()
        config_file = home_dir / ".phone_wallpaper_config.json"
        return str(config_file)
    
    def _load_default_config(self):
        """
        加载默认配置
        
        @return: 包含默认配置的字典
        """
        default_config = {
            "source_image_folder": str(Path.home() / "Pictures"),
            "output_image_folder": str(Path.home() / "Pictures"),
            "silent_save": False,
            "filename_pattern": "timestamp",
            "save_format": "PNG",
            "save_quality": 95,
            "canvas_background_color": "#000000"
        }
        return default_config
    
    def load_config(self):
        """从文件加载配置"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    self.config.update(loaded_config)
            except Exception as e:
                print(f"加载配置文件失败: {e}")
        else:
            self.save_config()
    
    def save_config(self):
        """保存配置到文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"保存配置文件失败: {e}")
    
    def get(self, key, default=None):
        """
        获取配置项的值
        
        @param key: 配置项键名
        @param default: 默认值
        @return: 配置项的值
        """
        return self.config.get(key, default)
    
    def set(self, key, value):
        """
        设置配置项的值
        
        @param key: 配置项键名
        @param value: 配置项的值
        """
        self.config[key] = value
    
    def reset_to_default(self):
        """重置为默认配置"""
        self.config = self._load_default_config()
        self.save_config()
    
    def get_all(self):
        """
        获取所有配置
        
        @return: 配置字典
        """
        return self.config.copy()

