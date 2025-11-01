# 极简时钟 - 树莓派版本

一个简洁美观的时钟应用，专为树莓派设计。支持时间显示和自然照片轮播。

## 功能特性

- ✅ 大字体显示当前时间（时:分:秒）
- ✅ 显示日期和星期
- ✅ 深灰色/黑色背景，极简设计
- ✅ 支持自然照片轮播（自动切换）
- ✅ 全屏显示，适合树莓派作为桌面时钟
- ✅ 半透明遮罩确保文字清晰可读

## 安装步骤

### 1. 安装依赖

```bash
pip3 install -r requirements.txt
```

或使用启动脚本（会自动检查并安装依赖）：
```bash
chmod +x start.sh
./start.sh
```

### 2. 准备照片（可选）

如果你想要照片轮播功能，需要：

1. 创建 `photos` 目录：
```bash
mkdir photos
```

2. 将自然照片放入 `photos` 目录：
   - 支持格式：JPG, JPEG, PNG, BMP, GIF
   - 照片会自动轮播，每张显示10秒
   - 建议使用高分辨率照片（1920x1080或更高）

### 3. 运行程序

**方法一：直接运行**
```bash
python3 clock.py
```

**方法二：使用启动脚本** 
```bash
chmod +x start.sh
./start.sh
```

## 按键控制

程序运行后可以使用以下按键：

- **ESC** - 退出程序
- **F** - 切换全屏/窗口模式
- **B** - 切换背景模式（纯色背景 / 照片轮播）
- **S** - 切换照片缩放模式（覆盖整个屏幕 / 适应屏幕保持宽高比）

## 配置说明

你可以在 `clock.py` 中修改以下配置：

```python
# 背景颜色（RGB值）
self.bg_color = (30, 30, 30)  # 深灰色，改为(0, 0, 0)是纯黑色

# 文字颜色
self.text_color = (255, 255, 255)  # 白色

# 照片目录
self.photos_dir = "photos"

# 每张照片显示时间（秒）
self.photo_display_time = 10

# 照片缩放模式：cover（覆盖）或 fit（适应）
self.photo_scale_mode = "cover"
```

## 自动启动（可选）

如果你想让时钟在树莓派启动时自动运行，可以设置开机自启：

### 方法一：使用 systemd（推荐）

创建服务文件 `/etc/systemd/system/clock.service`：

```ini
[Unit]
Description=极简时钟
After=graphical.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/极简时钟
ExecStart=/usr/bin/python3 /home/pi/极简时钟/clock.py
Restart=always
RestartSec=10

[Install]
WantedBy=graphical.target
```

然后启动服务：
```bash
sudo systemctl enable clock.service
sudo systemctl start clock.service
```

### 方法二：使用 autostart

创建文件 `~/.config/autostart/clock.desktop`：

```ini
[Desktop Entry]
Type=Application
Name=极简时钟
Exec=/usr/bin/python3 /home/pi/极简时钟/clock.py
```

## 系统要求

- Python 3.6+
- Pygame 2.5+
- 树莓派（推荐树莓派4或更新版本）
- 建议分辨率：1920x1080 或更高

## 注意事项

- 如果没有照片或照片目录不存在，程序会使用纯色背景正常运行
- 程序会在启动时自动检测屏幕分辨率
- 建议在全屏模式下使用以获得最佳体验
- 如果遇到字体显示问题，可能需要安装额外的字体包

## 常见问题

**Q: 照片不显示？**
A: 检查 photos 目录是否存在，照片格式是否正确，权限是否正确。

**Q: 字体显示异常？**
A: 程序会尝试使用系统默认字体，如果出现问题，可能需要安装字体包：
```bash
sudo apt-get install fonts-wqy-microhei  # 中文字体
```

**Q: 如何退出程序？**
A: 按 ESC 键即可退出。

## 许可证

本项目仅供个人使用。
