"""
手机壁纸边框工具 - 主程序入口

跨平台桌面应用，用于给壁纸图片添加手机边框
"""

import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from ui_window import MainWindow


def resource_path(relative_path):
    """
    获取资源文件的绝对路径
    
    支持开发环境和打包后的环境
    
    @param relative_path: 相对于项目根目录的资源文件路径
    @return: 资源文件的绝对路径
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def get_template_path():
    """
    获取模板图片路径
    
    支持跨平台路径处理和打包后环境
    
    @return: 模板图片的绝对路径
    """
    template_path = resource_path(os.path.join("assets", "templates", "phone-holder.png"))
    return template_path


def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    app.setFont(QFont("Microsoft YaHei", 10))
    
    template_path = get_template_path()
    
    if not os.path.exists(template_path):
        from PyQt5.QtWidgets import QMessageBox
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("错误")
        msg.setText(f"模板图片不存在:\n{template_path}")
        msg.exec_()
        sys.exit(1)
    
    window = MainWindow(template_path)
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

