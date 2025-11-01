#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
极简时钟 - 树莓派专用
功能：显示时间，支持自然照片轮播
"""

import pygame
import sys
import os
import platform
import time
from datetime import datetime
from pathlib import Path

# 初始化 Pygame
pygame.init()

def get_chinese_font():
    """获取支持中文的系统字体"""
    system = platform.system()
    
    # Windows 字体路径
    if system == "Windows":
        windows_fonts = [
            "C:/Windows/Fonts/msyh.ttc",  # 微软雅黑
            "C:/Windows/Fonts/simsun.ttc",  # 宋体
            "C:/Windows/Fonts/simhei.ttf",  # 黑体
            "C:/Windows/Fonts/simkai.ttf",  # 楷体
            "C:/Windows/Fonts/msyhbd.ttc",  # 微软雅黑 Bold
        ]
        for font_path in windows_fonts:
            if os.path.exists(font_path):
                return font_path
    
    # Linux/树莓派字体路径
    elif system == "Linux":
        linux_fonts = [
            "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",  # 文泉驿微米黑
            "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",  # 文泉驿正黑
            "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",  # Noto Sans CJK
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # DejaVu Sans
        ]
        for font_path in linux_fonts:
            if os.path.exists(font_path):
                return font_path
    
    # macOS 字体路径
    elif system == "Darwin":
        mac_fonts = [
            "/System/Library/Fonts/PingFang.ttc",
            "/System/Library/Fonts/STHeiti Light.ttc",
            "/Library/Fonts/Microsoft/Microsoft YaHei.ttf",
        ]
        for font_path in mac_fonts:
            if os.path.exists(font_path):
                return font_path
    
    # 如果没有找到中文字体，返回None
    return None

class SimpleClock:
    def __init__(self, width=1920, height=1080, fullscreen=True):
        """初始化时钟应用"""
        self.width = width
        self.height = height
        self.fullscreen = fullscreen
        
        # 设置显示模式
        if self.fullscreen:
            self.screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((width, height))
        
        pygame.display.set_caption("极简时钟")
        
        # 颜色配置
        self.bg_color = (30, 30, 30)  # 深灰色背景
        self.text_color = (255, 255, 255)  # 白色文字
        
        # 字体配置
        self.clock_font_size = int(self.height * 0.15)  # 时钟字体大小
        self.date_font_size = int(self.height * 0.05)   # 日期字体大小
        
        # 加载支持中文的字体
        chinese_font_path = get_chinese_font()
        self.has_chinese_font = False
        
        if chinese_font_path:
            try:
                print(f"使用字体: {chinese_font_path}")
                self.clock_font = pygame.font.Font(chinese_font_path, self.clock_font_size)
                self.date_font = pygame.font.Font(chinese_font_path, self.date_font_size)
                self.has_chinese_font = True
            except Exception as e:
                print(f"警告: 无法加载字体 {chinese_font_path}: {e}")
                # 降级到默认字体
                self.clock_font = pygame.font.Font(None, self.clock_font_size)
                self.date_font = pygame.font.Font(None, self.date_font_size)
                self.has_chinese_font = False
        else:
            print("警告: 未找到支持中文的字体，日期显示可能不正确")
            # 使用默认字体（可能不支持中文）
            self.clock_font = pygame.font.Font(None, self.clock_font_size)
            self.date_font = pygame.font.Font(None, self.date_font_size)
            self.has_chinese_font = False
        
        # 照片配置
        self.photos_dir = "photos"  # 照片目录
        self.photos = []
        self.current_photo_index = 0
        self.photo_scale_mode = "cover"  # cover: 覆盖整个屏幕，fit: 适应屏幕
        self.photo_display_time = 10  # 每张照片显示时间（秒）
        self.last_photo_change = time.time()
        self.use_background_photos = True  # 是否使用背景照片
        self.auto_switch_photos = False  # 是否自动切换照片（默认关闭，手动切换）
        
        # 加载照片
        self.load_photos()
        
        # 时钟位置
        self.clock_x = self.width // 2
        self.clock_y = self.height // 2 - 50
        
        self.date_x = self.width // 2
        self.date_y = self.height // 2 + 100
        
        # 触摸配置
        # 使用鼠标事件来模拟触摸（兼容性更好）
        pygame.mouse.set_visible(False)  # 隐藏鼠标指针（在触屏上更美观）
        
        # 触摸手势检测
        self.touch_start_pos = None
        self.touch_start_time = None
        self.swipe_threshold = 50  # 滑动阈值（像素）
        self.swipe_time_threshold = 0.5  # 滑动时间阈值（秒）
        
        # 左右箭头提示
        self.show_navigation_hints = True
        self.hint_arrow_size = int(self.height * 0.03)  # 箭头大小
        self.hint_arrow_color = (255, 255, 255, 150)  # 半透明白色
        self.hint_fade_time = 5  # 提示显示时间（秒）
        self.hint_start_time = time.time()
        
        # 计时器配置
        self.timer_set_time = 0  # 设置的计时时间（秒）
        self.timer_remaining = 0  # 剩余时间（秒）
        self.timer_running = False  # 计时器是否运行
        self.timer_paused = False  # 计时器是否暂停
        self.timer_start_time = None  # 计时器开始时间
        self.timer_font_size = int(self.height * 0.04)  # 计时器字体大小
        self.timer_font = None  # 计时器字体（稍后加载）
        self.timer_x = self.width - 100  # 计时器位置（右下角）
        self.timer_y = self.height - 60
        self.timer_alert_shown = False  # 是否已显示提示
        self.timer_alert_start_time = None  # 提示显示开始时间
        self.timer_alert_duration = 10  # 提示显示持续时间（秒）
        
        # 加载计时器字体
        chinese_font_path = get_chinese_font()
        if chinese_font_path:
            try:
                self.timer_font = pygame.font.Font(chinese_font_path, self.timer_font_size)
            except:
                self.timer_font = pygame.font.Font(None, self.timer_font_size)
        else:
            self.timer_font = pygame.font.Font(None, self.timer_font_size)
        
    def load_photos(self):
        """加载照片目录中的所有图片"""
        photos_path = Path(self.photos_dir)
        if not photos_path.exists():
            print(f"警告: 照片目录 '{self.photos_dir}' 不存在，将只显示时钟")
            self.use_background_photos = False
            return
        
        # 支持的图片格式
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif'}
        
        for file in photos_path.iterdir():
            if file.suffix.lower() in image_extensions:
                try:
                    img = pygame.image.load(str(file))
                    self.photos.append(img)
                    print(f"加载照片: {file.name}")
                except Exception as e:
                    print(f"无法加载照片 {file.name}: {e}")
        
        if len(self.photos) == 0:
            print(f"警告: 照片目录中没有找到有效图片，将只显示时钟")
            self.use_background_photos = False
        else:
            print(f"成功加载 {len(self.photos)} 张照片")
    
    def next_photo(self):
        """切换到下一张照片"""
        if len(self.photos) > 0:
            self.current_photo_index = (self.current_photo_index + 1) % len(self.photos)
            self.last_photo_change = time.time()
            self.hint_start_time = time.time()  # 重置提示显示时间
            print(f"切换到照片: {self.current_photo_index + 1}/{len(self.photos)}")
    
    def prev_photo(self):
        """切换到上一张照片"""
        if len(self.photos) > 0:
            self.current_photo_index = (self.current_photo_index - 1) % len(self.photos)
            self.last_photo_change = time.time()
            self.hint_start_time = time.time()  # 重置提示显示时间
            print(f"切换到照片: {self.current_photo_index + 1}/{len(self.photos)}")
    
    def get_background_surface(self):
        """获取背景（照片或纯色）"""
        if self.use_background_photos and len(self.photos) > 0:
            # 只有在启用自动切换时才自动切换照片
            if self.auto_switch_photos:
                current_time = time.time()
                if current_time - self.last_photo_change >= self.photo_display_time:
                    self.next_photo()
            
            # 获取当前照片
            photo = self.photos[self.current_photo_index]
            photo_width, photo_height = photo.get_size()
            
            # 创建背景表面
            background = pygame.Surface((self.width, self.height))
            
            if self.photo_scale_mode == "cover":
                # 覆盖模式：缩放照片以填满整个屏幕
                scale_x = self.width / photo_width
                scale_y = self.height / photo_height
                scale = max(scale_x, scale_y)  # 选择较大的缩放比例以确保覆盖
                
                scaled_width = int(photo_width * scale)
                scaled_height = int(photo_height * scale)
                scaled_photo = pygame.transform.scale(photo, (scaled_width, scaled_height))
                
                # 居中显示
                x_offset = (self.width - scaled_width) // 2
                y_offset = (self.height - scaled_height) // 2
                background.blit(scaled_photo, (x_offset, y_offset))
            else:
                # 适应模式：保持宽高比适应屏幕
                scale_x = self.width / photo_width
                scale_y = self.height / photo_height
                scale = min(scale_x, scale_y)  # 选择较小的缩放比例以确保适应
                
                scaled_width = int(photo_width * scale)
                scaled_height = int(photo_height * scale)
                scaled_photo = pygame.transform.scale(photo, (scaled_width, scaled_height))
                
                # 居中显示
                x_offset = (self.width - scaled_width) // 2
                y_offset = (self.height - scaled_height) // 2
                background.fill(self.bg_color)  # 填充背景色
                background.blit(scaled_photo, (x_offset, y_offset))
            
            # 添加半透明遮罩使文字更清晰
            overlay = pygame.Surface((self.width, self.height))
            overlay.set_alpha(100)  # 半透明
            overlay.fill((0, 0, 0))
            background.blit(overlay, (0, 0))
            
            return background
        else:
            # 纯色背景
            background = pygame.Surface((self.width, self.height))
            background.fill(self.bg_color)
            return background
    
    def get_time_string(self):
        """获取格式化的时间字符串"""
        now = datetime.now()
        time_str = now.strftime("%H:%M:%S")
        return time_str
    
    def get_date_string(self):
        """获取格式化的日期字符串"""
        now = datetime.now()
        # 中文格式：2024年1月1日 星期一
        weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
        date_str = f"{now.year}年{now.month}月{now.day}日 {weekdays[now.weekday()]}"
        return date_str
    
    def get_date_string_en(self):
        """获取英文格式的日期字符串（备用）"""
        now = datetime.now()
        weekdays_en = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        date_str = f"{now.year}-{now.month:02d}-{now.day:02d} {weekdays_en[now.weekday()]}"
        return date_str
    
    def render_text(self, text, font, color):
        """渲染文字"""
        return font.render(text, True, color)
    
    def format_timer(self, seconds):
        """格式化计时器显示（MM:SS）"""
        if seconds < 0:
            seconds = 0
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"
    
    def set_timer(self, minutes):
        """设置计时器（分钟）"""
        self.timer_set_time = minutes * 60
        self.timer_remaining = self.timer_set_time
        self.timer_running = False
        self.timer_paused = False
        self.timer_alert_shown = False
        print(f"计时器设置为: {minutes}分钟")
    
    def start_timer(self):
        """启动计时器"""
        if self.timer_set_time > 0:
            if self.timer_paused:
                # 从暂停状态恢复
                self.timer_start_time = time.time() - (self.timer_set_time - self.timer_remaining)
                self.timer_paused = False
            else:
                # 新启动
                self.timer_start_time = time.time()
                self.timer_remaining = self.timer_set_time
            self.timer_running = True
            self.timer_alert_shown = False
            print("计时器已启动")
    
    def pause_timer(self):
        """暂停计时器"""
        if self.timer_running and not self.timer_paused:
            self.timer_paused = True
            self.timer_running = False
            print("计时器已暂停")
    
    def reset_timer(self):
        """重置计时器"""
        self.timer_running = False
        self.timer_paused = False
        self.timer_remaining = self.timer_set_time if self.timer_set_time > 0 else 0
        self.timer_alert_shown = False
        print("计时器已重置")
    
    def update_timer(self):
        """更新计时器状态"""
        if self.timer_running and not self.timer_paused:
            elapsed = time.time() - self.timer_start_time
            self.timer_remaining = max(0, self.timer_set_time - elapsed)
            
            # 检查是否到时间
            if self.timer_remaining <= 0 and not self.timer_alert_shown:
                self.timer_running = False
                self.timer_alert_shown = True
                self.timer_alert_start_time = time.time()
                print("计时器到时间了！")
    
    def draw_timer(self, surface):
        """在右下角绘制计时器"""
        if self.timer_set_time <= 0 and not self.timer_alert_shown:
            return  # 如果没有设置计时器且没有提示，不显示
        
        # 更新计时器
        self.update_timer()
        
        # 如果正在显示提示
        if self.timer_alert_shown:
            current_time = time.time()
            elapsed = current_time - self.timer_alert_start_time
            
            if elapsed < self.timer_alert_duration:
                # 显示提示（闪烁效果）
                flash_interval = 0.5  # 闪烁间隔（秒）
                visible = (int(elapsed / flash_interval) % 2) == 0
                
                if visible:
                    # 绘制提示文字（居中显示）
                    alert_text = "时间到！"
                    if not self.has_chinese_font:
                        alert_text = "Time Up!"
                    
                    alert_font_size = int(self.height * 0.1)
                    try:
                        chinese_font_path = get_chinese_font()
                        if chinese_font_path:
                            alert_font = pygame.font.Font(chinese_font_path, alert_font_size)
                        else:
                            alert_font = pygame.font.Font(None, alert_font_size)
                    except:
                        alert_font = pygame.font.Font(None, alert_font_size)
                    
                    alert_surface = alert_font.render(alert_text, True, (255, 0, 0))  # 红色
                    alert_rect = alert_surface.get_rect(center=(self.width // 2, self.height // 2))
                    
                    # 绘制半透明背景
                    overlay = pygame.Surface((self.width, self.height))
                    overlay.set_alpha(200)
                    overlay.fill((0, 0, 0))
                    surface.blit(overlay, (0, 0))
                    
                    # 绘制提示文字
                    surface.blit(alert_surface, alert_rect)
            else:
                # 提示显示时间结束，自动关闭
                self.timer_alert_shown = False
            
            # 在右下角也显示计时器状态
            timer_text = "00:00"
            timer_color = (255, 0, 0)  # 红色表示到时间
        else:
            # 显示剩余时间
            timer_text = self.format_timer(self.timer_remaining)
            if self.timer_running:
                timer_color = (255, 255, 255)  # 白色表示运行中
            elif self.timer_paused:
                timer_color = (255, 255, 0)  # 黄色表示暂停
            else:
                timer_color = (150, 150, 150)  # 灰色表示未启动
        
        # 渲染计时器文字
        timer_surface = self.timer_font.render(timer_text, True, timer_color)
        timer_rect = timer_surface.get_rect()
        timer_rect.right = self.width - 20  # 距离右边缘20像素
        timer_rect.bottom = self.height - 20  # 距离下边缘20像素
        
        # 绘制半透明背景（可选，使文字更清晰）
        bg_rect = timer_rect.inflate(10, 5)
        bg_surface = pygame.Surface((bg_rect.width, bg_rect.height))
        bg_surface.set_alpha(100)
        bg_surface.fill((0, 0, 0))
        surface.blit(bg_surface, bg_rect)
        
        # 绘制计时器文字
        surface.blit(timer_surface, timer_rect)
    
    def draw_navigation_hints(self, surface):
        """绘制左右箭头提示"""
        if not self.show_navigation_hints or not self.use_background_photos or len(self.photos) <= 1:
            return
        
        # 检查提示显示时间
        current_time = time.time()
        if current_time - self.hint_start_time > self.hint_fade_time:
            return
        
        # 计算透明度（渐变淡出）
        fade_progress = (current_time - self.hint_start_time) / self.hint_fade_time
        alpha = int(150 * (1 - fade_progress))
        if alpha <= 0:
            return
        
        arrow_color = (255, 255, 255, alpha)
        
        # 左箭头（上一张）
        left_x = self.width // 8
        left_y = self.height // 2
        
        # 绘制左箭头
        arrow_points_left = [
            (left_x, left_y),
            (left_x + self.hint_arrow_size, left_y - self.hint_arrow_size // 2),
            (left_x + self.hint_arrow_size, left_y + self.hint_arrow_size // 2),
        ]
        pygame.draw.polygon(surface, arrow_color[:3], arrow_points_left)
        
        # 右箭头（下一张）
        right_x = self.width - self.width // 8
        right_y = self.height // 2
        
        # 绘制右箭头
        arrow_points_right = [
            (right_x, right_y),
            (right_x - self.hint_arrow_size, right_y - self.hint_arrow_size // 2),
            (right_x - self.hint_arrow_size, right_y + self.hint_arrow_size // 2),
        ]
        pygame.draw.polygon(surface, arrow_color[:3], arrow_points_right)
    
    def run(self):
        """运行主循环"""
        clock = pygame.time.Clock()
        running = True
        
        while running:
            # 处理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_f:
                        # 切换全屏模式
                        self.fullscreen = not self.fullscreen
                        if self.fullscreen:
                            self.screen = pygame.display.set_mode(
                                (self.width, self.height), pygame.FULLSCREEN
                            )
                        else:
                            self.screen = pygame.display.set_mode((self.width, self.height))
                    elif event.key == pygame.K_b:
                        # 切换背景模式（纯色/照片）
                        self.use_background_photos = not self.use_background_photos
                    elif event.key == pygame.K_s:
                        # 切换照片缩放模式
                        self.photo_scale_mode = "cover" if self.photo_scale_mode == "fit" else "fit"
                        print(f"照片模式: {self.photo_scale_mode}")
                    elif event.key == pygame.K_a:
                        # 切换自动/手动切换模式
                        self.auto_switch_photos = not self.auto_switch_photos
                        mode = "自动切换" if self.auto_switch_photos else "手动切换"
                        print(f"照片切换模式: {mode}")
                    elif event.key == pygame.K_LEFT:
                        # 上一张照片
                        if self.use_background_photos and len(self.photos) > 0:
                            self.prev_photo()
                    elif event.key == pygame.K_RIGHT:
                        # 下一张照片
                        if self.use_background_photos and len(self.photos) > 0:
                            self.next_photo()
                    elif event.key == pygame.K_t:
                        # 计时器控制
                        if self.timer_set_time <= 0:
                            # 如果没有设置，默认设置为25分钟（番茄钟）
                            self.set_timer(25)
                            self.start_timer()
                        elif self.timer_running:
                            self.pause_timer()
                        elif self.timer_paused:
                            self.start_timer()
                        else:
                            self.start_timer()
                    elif event.key == pygame.K_r:
                        # 重置计时器（同时关闭提示）
                        if self.timer_alert_shown:
                            self.timer_alert_shown = False
                        self.reset_timer()
                    elif event.key >= pygame.K_1 and event.key <= pygame.K_9:
                        # 数字键设置计时器（1-9对应10-90分钟）
                        minutes = (event.key - pygame.K_0) * 10
                        self.set_timer(minutes)
                        self.start_timer()
                    elif event.key >= pygame.K_KP1 and event.key <= pygame.K_KP9:
                        # 小键盘数字键
                        minutes = (event.key - pygame.K_KP0) * 10
                        self.set_timer(minutes)
                        self.start_timer()
                # 触摸事件处理
                elif event.type == pygame.FINGERDOWN:
                    # 手指按下
                    self.touch_start_pos = (event.x * self.width, event.y * self.height)
                    self.touch_start_time = time.time()
                    self.hint_start_time = time.time()  # 重置提示
                elif event.type == pygame.FINGERUP:
                    # 手指抬起，检测是否是点击或滑动
                    if self.touch_start_pos:
                        touch_end_pos = (event.x * self.width, event.y * self.height)
                        touch_duration = time.time() - self.touch_start_time
                        
                        dx = touch_end_pos[0] - self.touch_start_pos[0]
                        dy = touch_end_pos[1] - self.touch_start_pos[1]
                        
                        # 检测滑动
                        if abs(dx) > self.swipe_threshold and touch_duration < self.swipe_time_threshold:
                            # 水平滑动
                            if dx > 0:
                                # 向右滑动 - 上一张
                                if self.use_background_photos and len(self.photos) > 0:
                                    self.prev_photo()
                            else:
                                # 向左滑动 - 下一张
                                if self.use_background_photos and len(self.photos) > 0:
                                    self.next_photo()
                        elif abs(dx) < 30 and abs(dy) < 30 and touch_duration < 0.3:
                            # 点击（短距离，短时间）
                            click_x = self.touch_start_pos[0]
                            click_y = self.touch_start_pos[1]
                            
                            # 检查是否点击右下角（计时器区域）或提示区域
                            timer_area_width = 150
                            timer_area_height = 80
                            # 检查是否点击计时器区域或屏幕中心（关闭提示）
                            if (click_x > self.width - timer_area_width and 
                                click_y > self.height - timer_area_height):
                                # 点击计时器区域
                                if self.timer_alert_shown:
                                    # 如果正在显示提示，关闭提示
                                    self.timer_alert_shown = False
                                elif self.timer_set_time <= 0:
                                    # 如果没有设置，默认设置25分钟
                                    self.set_timer(25)
                                    self.start_timer()
                                elif self.timer_running:
                                    self.pause_timer()
                                elif self.timer_paused:
                                    self.start_timer()
                                else:
                                    self.start_timer()
                            elif self.timer_alert_shown:
                                # 如果正在显示提示，点击任意位置关闭
                                self.timer_alert_shown = False
                            else:
                                # 点击其他区域 - 切换照片
                                if click_x < self.width / 2:
                                    # 点击左侧 - 上一张
                                    if self.use_background_photos and len(self.photos) > 0:
                                        self.prev_photo()
                                else:
                                    # 点击右侧 - 下一张
                                    if self.use_background_photos and len(self.photos) > 0:
                                        self.next_photo()
                        
                        self.touch_start_pos = None
                        self.touch_start_time = None
                # 鼠标事件（用于非触摸屏设备，鼠标点击也可以切换）
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # 左键
                        mouse_pos = pygame.mouse.get_pos()
                        self.touch_start_pos = mouse_pos
                        self.touch_start_time = time.time()
                        self.hint_start_time = time.time()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1 and self.touch_start_pos:  # 左键
                        mouse_pos = pygame.mouse.get_pos()
                        touch_duration = time.time() - self.touch_start_time
                        
                        dx = mouse_pos[0] - self.touch_start_pos[0]
                        dy = mouse_pos[1] - self.touch_start_pos[1]
                        
                        # 检测滑动
                        if abs(dx) > self.swipe_threshold and touch_duration < self.swipe_time_threshold:
                            if dx > 0:
                                if self.use_background_photos and len(self.photos) > 0:
                                    self.prev_photo()
                            else:
                                if self.use_background_photos and len(self.photos) > 0:
                                    self.next_photo()
                        elif abs(dx) < 30 and abs(dy) < 30 and touch_duration < 0.3:
                            # 点击
                            click_x = self.touch_start_pos[0]
                            click_y = self.touch_start_pos[1]
                            
                            # 检查是否点击右下角（计时器区域）或提示区域
                            timer_area_width = 150
                            timer_area_height = 80
                            # 检查是否点击计时器区域或屏幕中心（关闭提示）
                            if (click_x > self.width - timer_area_width and 
                                click_y > self.height - timer_area_height):
                                # 点击计时器区域
                                if self.timer_alert_shown:
                                    # 如果正在显示提示，关闭提示
                                    self.timer_alert_shown = False
                                elif self.timer_set_time <= 0:
                                    self.set_timer(25)
                                    self.start_timer()
                                elif self.timer_running:
                                    self.pause_timer()
                                elif self.timer_paused:
                                    self.start_timer()
                                else:
                                    self.start_timer()
                            elif self.timer_alert_shown:
                                # 如果正在显示提示，点击任意位置关闭
                                self.timer_alert_shown = False
                            else:
                                # 点击其他区域 - 切换照片
                                if click_x < self.width / 2:
                                    if self.use_background_photos and len(self.photos) > 0:
                                        self.prev_photo()
                                else:
                                    if self.use_background_photos and len(self.photos) > 0:
                                        self.next_photo()
                        
                        self.touch_start_pos = None
                        self.touch_start_time = None
            
            # 获取背景
            background = self.get_background_surface()
            self.screen.blit(background, (0, 0))
            
            # 获取时间并渲染
            time_str = self.get_time_string()
            
            # 根据是否加载了中文字体来决定使用中文还是英文格式
            if self.has_chinese_font:
                date_str = self.get_date_string()
            else:
                date_str = self.get_date_string_en()
            
            time_text = self.render_text(time_str, self.clock_font, self.text_color)
            date_text = self.render_text(date_str, self.date_font, self.text_color)
            
            # 获取文字位置（居中）
            time_rect = time_text.get_rect(center=(self.clock_x, self.clock_y))
            date_rect = date_text.get_rect(center=(self.date_x, self.date_y))
            
            # 绘制文字
            self.screen.blit(time_text, time_rect)
            self.screen.blit(date_text, date_rect)
            
            # 绘制导航提示（左右箭头）
            self.draw_navigation_hints(self.screen)
            
            # 绘制计时器（右下角）
            self.draw_timer(self.screen)
            
            # 更新显示
            pygame.display.flip()
            clock.tick(30)  # 30 FPS
        
        pygame.quit()
        sys.exit()

def main():
    """主函数"""
    # 尝试获取实际屏幕尺寸
    try:
        info = pygame.display.Info()
        width = info.current_w
        height = info.current_h
    except:
        # 默认尺寸（树莓派常见分辨率）
        width = 1920
        height = 1080
    
    print(f"屏幕分辨率: {width}x{height}")
    print("按键说明:")
    print("  ESC - 退出程序")
    print("  F - 切换全屏/窗口模式")
    print("  B - 切换背景（纯色/照片）")
    print("  S - 切换照片缩放模式（覆盖/适应）")
    print("  A - 切换自动/手动切换照片模式")
    print("  左/右箭头键 - 切换照片")
    print("")
    print("计时器控制:")
    print("  T - 启动/暂停计时器")
    print("  R - 重置计时器")
    print("  1-9 - 设置10-90分钟计时器并启动")
    print("  触摸右下角计时器区域 - 启动/暂停计时器")
    print("")
    print("触摸操作:")
    print("  点击屏幕左侧 - 上一张照片")
    print("  点击屏幕右侧 - 下一张照片")
    print("  点击右下角 - 启动/暂停计时器")
    print("  向左滑动 - 下一张照片")
    print("  向右滑动 - 上一张照片")
    
    clock_app = SimpleClock(width=width, height=height, fullscreen=True)
    clock_app.run()

if __name__ == "__main__":
    main()

