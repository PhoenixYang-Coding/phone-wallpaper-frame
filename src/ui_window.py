"""
GUI 界面模块

使用 PyQt5 创建科技风格的桌面应用界面
"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QMessageBox,
    QFrame, QRadioButton, QButtonGroup, QListWidget,
    QListWidgetItem, QScrollArea, QSpinBox, QStackedWidget
)
from PyQt5.QtCore import Qt, QSize, QPoint
from PyQt5.QtGui import QPixmap, QFont, QDragEnterEvent, QDropEvent, QIcon
import os
from image_processor import ImageProcessor


class MainWindow(QMainWindow):
    """主窗口类"""
    
    def __init__(self, template_path):
        """
        初始化主窗口
        
        @param template_path: 模板图片路径
        """
        super().__init__()
        self.template_path = template_path
        self.processor = None
        self.current_wallpaper_path = None
        self.processed_image = None
        self.uploaded_images = []
        self.current_layout = (1, 1)
        self.drag_position = QPoint()
        self.is_maximized = False
        self.init_ui()
        self.init_processor()
    
    def init_processor(self):
        """初始化图片处理器"""
        try:
            self.processor = ImageProcessor(self.template_path)
        except FileNotFoundError as e:
            QMessageBox.critical(self, "错误", f"无法加载模板图片:\n{str(e)}")
    
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle("手机壁纸边框工具")
        self.setGeometry(100, 100, 900, 700)
        
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        central_widget.setLayout(main_layout)
        
        self.apply_dark_theme()
        
        title_bar = self.create_title_bar()
        main_layout.addWidget(title_bar)
        
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        sidebar = self.create_sidebar()
        content_layout.addWidget(sidebar)
        
        self.content_stack = self.create_main_content_area()
        content_layout.addWidget(self.content_stack, 1)
        
        content_widget = QWidget()
        content_widget.setLayout(content_layout)
        main_layout.addWidget(content_widget, 1)
        
        self.setAcceptDrops(True)
    
    def create_title_bar(self):
        """创建自定义标题栏"""
        title_bar = QWidget()
        title_bar.setFixedHeight(40)
        title_bar.setStyleSheet("background-color: #2b2d30;")
        
        layout = QHBoxLayout()
        layout.setContentsMargins(15, 0, 10, 0)
        layout.setSpacing(5)
        title_bar.setLayout(layout)
        
        icon_label = QLabel()
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        icon_path = os.path.join(project_root, "assets", "icons", "logo.png")
        if os.path.exists(icon_path):
            pixmap = QPixmap(icon_path)
            scaled_pixmap = pixmap.scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            icon_label.setPixmap(scaled_pixmap)
        else:
            icon_label.setText("📱")
            icon_label.setFont(QFont("Microsoft YaHei", 13))
        icon_label.setStyleSheet("background-color: transparent;")
        layout.addWidget(icon_label)
        
        # title_label = QLabel("手机壁纸边框工具")
        # title_label.setFont(QFont("Microsoft YaHei", 11, QFont.Bold))
        # title_label.setStyleSheet("color: #F3FCF4;")
        # layout.addWidget(title_label)
        
        layout.addStretch()
        
        button_style = """
            QPushButton {
                background-color: transparent;
                color: #c3d0cb;
                border: none;
                padding: 5px 15px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #3e4042;
            }
            QPushButton:pressed {
                background-color: #2b2d30;
            }
        """
        
        close_button_style = """
            QPushButton {
                background-color: transparent;
                color: #c3d0cb;
                border: none;
                padding: 5px 15px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #e81123;
                color: white;
            }
            QPushButton:pressed {
                background-color: #c01018;
            }
        """
        
        min_btn = QPushButton("—")
        min_btn.setStyleSheet(button_style)
        min_btn.setFixedSize(45, 40)
        min_btn.clicked.connect(self.minimize_window)
        layout.addWidget(min_btn)
        
        max_btn = QPushButton("□")
        max_btn.setStyleSheet(button_style)
        max_btn.setFixedSize(45, 40)
        max_btn.clicked.connect(self.maximize_restore_window)
        layout.addWidget(max_btn)
        self.max_btn = max_btn
        
        close_btn = QPushButton("✕")
        close_btn.setStyleSheet(close_button_style)
        close_btn.setFixedSize(45, 40)
        close_btn.clicked.connect(self.close_window)
        layout.addWidget(close_btn)
        
        self.title_bar_widget = title_bar
        return title_bar
    
    def create_sidebar(self):
        """创建左侧侧边栏"""
        sidebar = QWidget()
        sidebar.setFixedWidth(50)
        sidebar.setStyleSheet("background-color: #2b2d30;")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 10, 0, 10)
        layout.setSpacing(5)
        sidebar.setLayout(layout)
        
        sidebar_button_base_style = """
            QPushButton {
                background-color: transparent;
                color: #c3d0cb;
                border: none;
                border-left: 2px solid transparent;
                padding: 10px;
                font-size: 24px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #3e4042;
            }
        """
        
        sidebar_button_active_style = """
            QPushButton {
                background-color: #37373d;
                color: #ffffff;
                border: none;
                border-left: 2px solid #00D9FF;
                padding: 10px;
                font-size: 24px;
                text-align: center;
            }
        """
        
        main_btn = QPushButton()
        main_btn.setFixedHeight(50)
        main_btn.setToolTip("生成图片")
        main_btn.setStyleSheet(sidebar_button_active_style)
        main_btn.clicked.connect(self.switch_to_main_page)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        image_icon_path = os.path.join(project_root, "assets", "icons", "image.png")
        if os.path.exists(image_icon_path):
            main_btn.setIcon(QIcon(image_icon_path))
            main_btn.setIconSize(QSize(32, 32))
        else:
            main_btn.setText("📷")
        layout.addWidget(main_btn)
        self.main_btn = main_btn
        
        settings_btn = QPushButton()
        settings_btn.setFixedHeight(50)
        settings_btn.setToolTip("设置")
        settings_btn.setStyleSheet(sidebar_button_base_style)
        settings_btn.clicked.connect(self.switch_to_settings_page)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        settings_icon_path = os.path.join(project_root, "assets", "icons", "settings.png")
        if os.path.exists(settings_icon_path):
            settings_btn.setIcon(QIcon(settings_icon_path))
            settings_btn.setIconSize(QSize(32, 32))
        else:
            settings_btn.setText("⚙")
        layout.addWidget(settings_btn)
        self.settings_btn = settings_btn
        
        layout.addStretch()
        
        self.sidebar_button_base_style = sidebar_button_base_style
        self.sidebar_button_active_style = sidebar_button_active_style
        
        return sidebar
    
    def create_main_content_area(self):
        """创建主内容区"""
        stack = QStackedWidget()
        stack.setStyleSheet("background-color: #1e1f22;")
        
        main_page = self.create_main_page()
        stack.addWidget(main_page)
        
        settings_page = self.create_settings_page()
        stack.addWidget(settings_page)
        
        return stack
    
    def create_main_page(self):
        """创建生成图片主页面"""
        page = QWidget()
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        page.setLayout(main_layout)
        
        title_label = QLabel("手机壁纸边框工具")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Microsoft YaHei", 16, QFont.Bold))
        title_label.setStyleSheet("color: #c3d0cb; padding: 10px;")
        main_layout.addWidget(title_label)
        
        layout_selector_layout = QHBoxLayout()
        layout_selector_layout.addStretch()
        
        layout_label = QLabel("选择布局:")
        layout_label.setStyleSheet("color: #c3d0cb; font-size: 14px;")
        layout_selector_layout.addWidget(layout_label)
        
        self.layout_button_group = QButtonGroup()
        
        radio_style = "color: #00D9FF; font-size: 14px;"
        
        self.radio_1x1 = QRadioButton("1x1 (1张)")
        self.radio_1x1.setStyleSheet(radio_style)
        self.radio_1x1.setChecked(True)
        self.radio_1x1.toggled.connect(lambda checked: self.on_preset_layout_changed(1, 1, checked))
        self.layout_button_group.addButton(self.radio_1x1)
        layout_selector_layout.addWidget(self.radio_1x1)
        
        self.radio_2x3 = QRadioButton("2x3 (6张)")
        self.radio_2x3.setStyleSheet(radio_style)
        self.radio_2x3.toggled.connect(lambda checked: self.on_preset_layout_changed(2, 3, checked))
        self.layout_button_group.addButton(self.radio_2x3)
        layout_selector_layout.addWidget(self.radio_2x3)
        
        self.radio_2x4 = QRadioButton("2x4 (8张)")
        self.radio_2x4.setStyleSheet(radio_style)
        self.radio_2x4.toggled.connect(lambda checked: self.on_preset_layout_changed(2, 4, checked))
        self.layout_button_group.addButton(self.radio_2x4)
        layout_selector_layout.addWidget(self.radio_2x4)
        
        self.radio_custom = QRadioButton("自定义")
        self.radio_custom.setStyleSheet(radio_style)
        self.radio_custom.toggled.connect(self.on_custom_layout_toggled)
        self.layout_button_group.addButton(self.radio_custom)
        layout_selector_layout.addWidget(self.radio_custom)
        
        spinbox_style = """
            QSpinBox {
                background-color: #2b2d30;
                color: #00D9FF;
                border: 1px solid #555555;
                border-radius: 3px;
                padding: 3px;
                min-width: 60px;
            }
            QSpinBox:disabled {
                background-color: #1e1f22;
                color: #666666;
                border-color: #333333;
            }
        """
        
        self.row_input = QSpinBox()
        self.row_input.setMinimum(1)
        self.row_input.setMaximum(10)
        self.row_input.setValue(2)
        self.row_input.setPrefix("行: ")
        self.row_input.setEnabled(False)
        self.row_input.setStyleSheet(spinbox_style)
        self.row_input.valueChanged.connect(self.on_custom_layout_changed)
        layout_selector_layout.addWidget(self.row_input)
        
        self.col_input = QSpinBox()
        self.col_input.setMinimum(1)
        self.col_input.setMaximum(10)
        self.col_input.setValue(2)
        self.col_input.setPrefix("列: ")
        self.col_input.setEnabled(False)
        self.col_input.setStyleSheet(spinbox_style)
        self.col_input.valueChanged.connect(self.on_custom_layout_changed)
        layout_selector_layout.addWidget(self.col_input)
        
        layout_selector_layout.addStretch()
        main_layout.addLayout(layout_selector_layout)
        
        button_layout = QHBoxLayout()
        
        button_style = """
            QPushButton {
                background-color: #2b2d30;
                color: #00D9FF;
                border: 1px solid #00D9FF;
                border-radius: 4px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #3e4042;
                border-color: #00FFFF;
            }
            QPushButton:pressed {
                background-color: #1e1f22;
            }
            QPushButton:disabled {
                background-color: #1e1f22;
                color: #666666;
                border-color: #333333;
            }
        """
        
        self.upload_btn = QPushButton("批量上传")
        self.upload_btn.setMinimumHeight(45)
        self.upload_btn.setFont(QFont("Microsoft YaHei", 10))
        self.upload_btn.setStyleSheet(button_style)
        self.upload_btn.clicked.connect(self.upload_images_batch)
        button_layout.addWidget(self.upload_btn)
        
        self.add_single_btn = QPushButton("逐个添加")
        self.add_single_btn.setMinimumHeight(45)
        self.add_single_btn.setFont(QFont("Microsoft YaHei", 10))
        self.add_single_btn.setStyleSheet(button_style)
        self.add_single_btn.clicked.connect(self.add_single_image)
        button_layout.addWidget(self.add_single_btn)
        
        self.clear_btn = QPushButton("清空列表")
        self.clear_btn.setMinimumHeight(45)
        self.clear_btn.setFont(QFont("Microsoft YaHei", 10))
        self.clear_btn.setStyleSheet(button_style)
        self.clear_btn.clicked.connect(self.clear_images)
        button_layout.addWidget(self.clear_btn)
        
        self.process_btn = QPushButton("处理图片")
        self.process_btn.setMinimumHeight(45)
        self.process_btn.setFont(QFont("Microsoft YaHei", 10))
        self.process_btn.setStyleSheet(button_style)
        self.process_btn.clicked.connect(self.process_images)
        self.process_btn.setEnabled(False)
        button_layout.addWidget(self.process_btn)
        
        self.save_btn = QPushButton("保存图片")
        self.save_btn.setMinimumHeight(45)
        self.save_btn.setFont(QFont("Microsoft YaHei", 10))
        self.save_btn.setStyleSheet(button_style)
        self.save_btn.clicked.connect(self.save_image)
        self.save_btn.setEnabled(False)
        button_layout.addWidget(self.save_btn)
        
        main_layout.addLayout(button_layout)
        
        self.image_count_label = QLabel("已上传: 0 张 | 需要: 1 张")
        self.image_count_label.setAlignment(Qt.AlignCenter)
        self.image_count_label.setStyleSheet("color: #00D9FF; padding: 10px; font-size: 14px;")
        main_layout.addWidget(self.image_count_label)
        
        self.image_list = QListWidget()
        self.image_list.setStyleSheet("""
            QListWidget {
                background-color: #2b2d30;
                border: 1px solid #555555;
                border-radius: 4px;
                color: #c3d0cb;
                padding: 5px;
            }
            QListWidget::item {
                padding: 5px;
                border-bottom: 1px solid #3e4042;
            }
            QListWidget::item:selected {
                background-color: #37373d;
                color: #00D9FF;
            }
        """)
        self.image_list.setMaximumHeight(120)
        self.image_list.itemDoubleClicked.connect(self.remove_image_from_list)
        main_layout.addWidget(self.image_list)
        
        preview_layout = QHBoxLayout()
        
        self.original_label = QLabel("原始图片")
        self.original_label.setAlignment(Qt.AlignCenter)
        self.original_label.setStyleSheet("""
            QLabel {
                background-color: #2b2d30;
                border: 2px dashed #555555;
                border-radius: 4px;
                color: #888888;
                min-height: 300px;
            }
        """)
        self.original_label.setMinimumWidth(350)
        preview_layout.addWidget(self.original_label)
        
        self.preview_label = QLabel("处理后预览")
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setStyleSheet("""
            QLabel {
                background-color: #2b2d30;
                border: 2px dashed #555555;
                border-radius: 4px;
                color: #888888;
                min-height: 300px;
            }
        """)
        self.preview_label.setMinimumWidth(350)
        preview_layout.addWidget(self.preview_label)
        
        main_layout.addLayout(preview_layout)
        
        self.status_label = QLabel("请上传壁纸图片")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #c3d0cb; padding: 10px;")
        main_layout.addWidget(self.status_label)
        
        return page
    
    def create_settings_page(self):
        """创建设置页面"""
        page = QWidget()
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        page.setLayout(layout)
        
        icon_label = QLabel()
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        settings_icon_path = os.path.join(project_root, "assets", "icons", "settings.png")
        if os.path.exists(settings_icon_path):
            pixmap = QPixmap(settings_icon_path)
            scaled_pixmap = pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            icon_label.setPixmap(scaled_pixmap)
            icon_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(icon_label)
        
        label = QLabel("设置功能")
        label.setFont(QFont("Microsoft YaHei", 18))
        label.setStyleSheet("color: #c3d0cb; margin-top: 20px;")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        
        desc_label = QLabel("设置功能待开发")
        desc_label.setFont(QFont("Microsoft YaHei", 12))
        desc_label.setStyleSheet("color: #888888; margin-top: 20px;")
        desc_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(desc_label)
        
        return page
    
    def apply_dark_theme(self):
        """应用VSCode风格主题"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1f22;
            }
            QWidget {
                background-color: #1e1f22;
                color: #c3d0cb;
            }
            QRadioButton {
                spacing: 5px;
            }
            QRadioButton::indicator {
                width: 16px;
                height: 16px;
            }
            QRadioButton::indicator:unchecked {
                border: 2px solid #555555;
                background-color: #2b2d30;
                border-radius: 8px;
            }
            QRadioButton::indicator:checked {
                border: 2px solid #00D9FF;
                background-color: #00D9FF;
                border-radius: 8px;
            }
        """)
    
    def switch_to_main_page(self):
        """切换到主页面"""
        self.content_stack.setCurrentIndex(0)
        self.main_btn.setStyleSheet(self.sidebar_button_active_style)
        self.settings_btn.setStyleSheet(self.sidebar_button_base_style)
    
    def switch_to_settings_page(self):
        """切换到设置页面"""
        self.content_stack.setCurrentIndex(1)
        self.settings_btn.setStyleSheet(self.sidebar_button_active_style)
        self.main_btn.setStyleSheet(self.sidebar_button_base_style)
    
    def minimize_window(self):
        """最小化窗口"""
        self.showMinimized()
    
    def maximize_restore_window(self):
        """最大化/还原窗口"""
        if self.isMaximized():
            self.showNormal()
            self.max_btn.setText("□")
        else:
            self.showMaximized()
            self.max_btn.setText("❐")
    
    def close_window(self):
        """关闭窗口"""
        self.close()
    
    def mousePressEvent(self, event):
        """鼠标按下事件"""
        if event.button() == Qt.LeftButton:
            if event.y() <= 40:
                self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
                event.accept()
    
    def mouseMoveEvent(self, event):
        """鼠标移动事件"""
        if event.buttons() == Qt.LeftButton and self.drag_position is not None:
            if event.y() <= 40 and not self.isMaximized():
                self.move(event.globalPos() - self.drag_position)
                event.accept()
    
    def mouseDoubleClickEvent(self, event):
        """鼠标双击事件"""
        if event.button() == Qt.LeftButton and event.y() <= 40:
            self.maximize_restore_window()
            event.accept()
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        """拖拽进入事件"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def dropEvent(self, event: QDropEvent):
        """拖拽放下事件"""
        files = [url.toLocalFile() for url in event.mimeData().urls()]
        valid_files = [f for f in files if self.is_valid_image_file(f)]
        if valid_files:
            self.add_images_to_list(valid_files)
        else:
            QMessageBox.warning(self, "警告", "请上传 JPG 或 PNG 格式的图片")
    
    def is_valid_image_file(self, file_path):
        """检查文件是否为有效的图片格式"""
        valid_extensions = ['.jpg', '.jpeg', '.png']
        file_ext = os.path.splitext(file_path)[1].lower()
        return file_ext in valid_extensions
    
    def on_layout_changed(self, rows, cols):
        """布局选择改变"""
        self.current_layout = (rows, cols)
        required_count = rows * cols
        self.update_image_count()
        self.status_label.setText(f"已切换到 {rows}x{cols} 布局，需要 {required_count} 张图片")
    
    def on_preset_layout_changed(self, rows, cols, checked):
        """预设布局改变"""
        if checked:
            self.on_layout_changed(rows, cols)
    
    def on_custom_layout_toggled(self, checked):
        """自定义布局切换"""
        self.row_input.setEnabled(checked)
        self.col_input.setEnabled(checked)
        if checked:
            self.on_custom_layout_changed()
    
    def on_custom_layout_changed(self):
        """自定义布局数值改变"""
        if self.radio_custom.isChecked():
            rows = self.row_input.value()
            cols = self.col_input.value()
            self.on_layout_changed(rows, cols)
    
    def upload_images_batch(self):
        """批量上传图片"""
        file_paths, _ = QFileDialog.getOpenFileNames(
            self,
            "批量选择壁纸图片",
            "",
            "图片文件 (*.jpg *.jpeg *.png);;所有文件 (*.*)"
        )
        
        if file_paths:
            self.add_images_to_list(file_paths)
    
    def add_single_image(self):
        """逐个添加图片"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择壁纸图片",
            "",
            "图片文件 (*.jpg *.jpeg *.png);;所有文件 (*.*)"
        )
        
        if file_path:
            self.add_images_to_list([file_path])
    
    def add_images_to_list(self, file_paths):
        """将图片添加到列表"""
        added_count = 0
        for file_path in file_paths:
            if file_path not in self.uploaded_images:
                try:
                    pixmap = QPixmap(file_path)
                    if not pixmap.isNull():
                        self.uploaded_images.append(file_path)
                        filename = os.path.basename(file_path)
                        item_text = f"{len(self.uploaded_images)}. {filename}"
                        self.image_list.addItem(item_text)
                        added_count += 1
                except Exception as e:
                    QMessageBox.warning(self, "警告", f"无法加载图片 {file_path}:\n{str(e)}")
        
        if added_count > 0:
            self.update_image_count()
            self.update_preview_grid()
            self.status_label.setText(f"成功添加 {added_count} 张图片")
    
    def clear_images(self):
        """清空图片列表"""
        self.uploaded_images.clear()
        self.image_list.clear()
        self.update_image_count()
        self.original_label.clear()
        self.original_label.setText("原始图片")
        self.preview_label.clear()
        self.preview_label.setText("处理后预览")
        self.processed_image = None
        self.save_btn.setEnabled(False)
        self.process_btn.setEnabled(False)
        self.status_label.setText("已清空图片列表")
    
    def remove_image_from_list(self, item):
        """从列表中删除图片（双击删除）"""
        row = self.image_list.row(item)
        if 0 <= row < len(self.uploaded_images):
            removed_file = self.uploaded_images.pop(row)
            self.image_list.takeItem(row)
            
            for i in range(self.image_list.count()):
                item = self.image_list.item(i)
                file_path = self.uploaded_images[i]
                filename = os.path.basename(file_path)
                item.setText(f"{i + 1}. {filename}")
            
            self.update_image_count()
            self.update_preview_grid()
            self.status_label.setText(f"已删除: {os.path.basename(removed_file)}")
    
    def update_image_count(self):
        """更新图片数量显示"""
        rows, cols = self.current_layout
        required_count = rows * cols
        current_count = len(self.uploaded_images)
        
        self.image_count_label.setText(f"已上传: {current_count} 张 | 需要: {required_count} 张")
        
        if current_count == required_count:
            self.process_btn.setEnabled(True)
            self.image_count_label.setStyleSheet("color: #00FF00; padding: 10px; font-size: 14px;")
        elif current_count > 0:
            self.process_btn.setEnabled(False)
            self.image_count_label.setStyleSheet("color: #FFA500; padding: 10px; font-size: 14px;")
        else:
            self.process_btn.setEnabled(False)
            self.image_count_label.setStyleSheet("color: #00D9FF; padding: 10px; font-size: 14px;")
    
    def update_preview_grid(self):
        """更新原始图片网格预览"""
        if not self.uploaded_images:
            self.original_label.clear()
            self.original_label.setText("原始图片")
            return
        
        rows, cols = self.current_layout
        cell_width = 150
        cell_height = 300
        
        grid_width = cols * cell_width
        grid_height = rows * cell_height
        
        from PIL import Image
        grid_image = Image.new('RGB', (grid_width, grid_height), (26, 26, 26))
        
        for idx, img_path in enumerate(self.uploaded_images):
            if idx >= rows * cols:
                break
            try:
                img = Image.open(img_path)
                img.thumbnail((cell_width - 4, cell_height - 4), Image.Resampling.LANCZOS)
                
                row = idx // cols
                col = idx % cols
                x = col * cell_width + (cell_width - img.width) // 2
                y = row * cell_height + (cell_height - img.height) // 2
                
                grid_image.paste(img, (x, y))
            except Exception:
                pass
        
        temp_path = "temp_grid_preview.png"
        grid_image.save(temp_path)
        
        pixmap = QPixmap(temp_path)
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(
                400, 400,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.original_label.setPixmap(scaled_pixmap)
            self.original_label.setText("")
        
        if os.path.exists(temp_path):
            os.remove(temp_path)
    
    def process_images(self):
        """处理多图片"""
        rows, cols = self.current_layout
        required_count = rows * cols
        
        if len(self.uploaded_images) != required_count:
            QMessageBox.warning(self, "警告", f"请上传 {required_count} 张图片\n当前已上传 {len(self.uploaded_images)} 张")
            return
        
        if not self.processor:
            QMessageBox.warning(self, "警告", "图片处理器未初始化")
            return
        
        try:
            self.status_label.setText("正在处理图片...")
            self.process_btn.setEnabled(False)
            
            processed_images = []
            for idx, img_path in enumerate(self.uploaded_images):
                self.status_label.setText(f"正在处理第 {idx + 1}/{required_count} 张图片...")
                processed_img = self.processor.process_wallpaper(img_path)
                processed_images.append(processed_img)
            
            if rows == 1 and cols == 1:
                self.processed_image = processed_images[0]
            else:
                self.status_label.setText("正在拼接图片...")
                self.processed_image = self.processor.create_grid_layout(processed_images, rows, cols)
            
            temp_path = "temp_preview.png"
            self.processor.save_result(self.processed_image, temp_path)
            
            pixmap = QPixmap(temp_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(
                    400, 400,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.preview_label.setPixmap(scaled_pixmap)
                self.preview_label.setText("")
            
            if os.path.exists(temp_path):
                os.remove(temp_path)
            
            self.save_btn.setEnabled(True)
            self.process_btn.setEnabled(True)
            self.status_label.setText("处理完成！可以保存图片了")
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"处理图片失败:\n{str(e)}")
            self.process_btn.setEnabled(True)
            self.status_label.setText("处理失败")
    
    def save_image(self):
        """保存图片"""
        if not self.processed_image:
            QMessageBox.warning(self, "警告", "没有可保存的图片")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "保存图片",
            "",
            "PNG 图片 (*.png);;JPG 图片 (*.jpg);;所有文件 (*.*)"
        )
        
        if file_path:
            try:
                self.processor.save_result(self.processed_image, file_path)
                QMessageBox.information(self, "成功", f"图片已保存到:\n{file_path}")
                self.status_label.setText(f"已保存: {os.path.basename(file_path)}")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"保存图片失败:\n{str(e)}")

