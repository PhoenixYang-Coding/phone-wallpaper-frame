"""
手机壁纸边框工具 - 主程序入口

跨平台桌面应用，用于给壁纸图片添加手机边框
"""

import sys
import os
from PyQt5.QtWidgets import QApplication
from ui_window import MainWindow


def get_template_path():
    """
    获取模板图片路径
    
    支持跨平台路径处理
    
    @return: 模板图片的绝对路径
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    template_path = os.path.join(project_root, "assets", "templates", "phone-holder.png")
    return template_path


def main():
    """主函数"""
    app = QApplication(sys.argv)
    
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

