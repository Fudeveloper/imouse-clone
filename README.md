# iMouse Clone

iOS 免越狱群控方案 —— AirPlay 投屏 + CH9329 硬件键盘 + OpenCV/PaddleOCR 视觉识别。

> iPhone 端零安装，仅需开启 AirPlay 屏幕镜像。

## 架构

```
iPhone → AirPlay 投屏 → PC (UxPlay) → 截图 → OpenCV/PaddleOCR → CH9329 键鼠注入
```

| 层 | 技术 |
|---|------|
| 硬件 | CH9329 HID 芯片 (¥15/个), USB Hub, Lightning OTG |
| 投屏 | UxPlay (C++ AirPlay 接收器) |
| 截图 | mss / PIL |
| 找图 | OpenCV matchTemplate |
| 找色 | OpenCV inRange |
| OCR | PaddleOCR (百度飞桨) |
| API | FastAPI + WebSocket (port 9911) |

## 安装

```bash
# 1. 安装系统依赖
sudo apt install xvfb imagemagick  # Linux / WSL
# macOS: UxPlay 需要自行编译

# 2. 安装 Python 依赖
pip install -r requirements.txt

# 3. 安装 UxPlay (AirPlay 接收器)
# https://github.com/FDH2/UxPlay
git clone https://github.com/FDH2/UxPlay.git
cd UxPlay && cmake -B build && cmake --build build
sudo cp build/uxplay /usr/local/bin/

# 4. 检查依赖
python -m imouse.main --check
```

## 启动

```bash
python -m imouse.main --port 9911 --display :99
```

## API 参考

所有接口对标 iMouse 原始 API，响应格式：

```json
{
  "status": 200,
  "message": "成功",
  "data": { "code": 0, "..." }
}
```

### 设备管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/devices` | 设备列表 |
| POST | `/api/device/register` | 注册设备 |
| POST | `/api/device/bind` | 绑定 CH9329 硬件 |
| GET | `/api/hardware/scan` | 扫描可用硬件 |
| POST | `/api/device/airplay/start` | 启动 AirPlay |
| POST | `/api/device/capture/start` | 开始截图采集 |

### 键鼠操作

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/click` | 点击坐标 |
| POST | `/api/swipe` | 滑动 |
| POST | `/api/type` | 输入文字 |
| POST | `/api/key` | 单键 |
| POST | `/api/combo` | 组合键 |

### 图像识别

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/find_image` | 找图（模板匹配） |
| POST | `/api/find_color` | 找色 |
| POST | `/api/ocr` | OCR 文字识别 |
| POST | `/api/find_text` | 找文字 |
| POST | `/api/screenshot` | 截图（base64） |

### 典型调用流程

```python
import requests

BASE = "http://localhost:9911"

# 1. 注册设备
r = requests.post(f"{BASE}/api/device/register", json={"device_id": "dev_1"})

# 2. 绑定硬件
r = requests.post(f"{BASE}/api/device/bind", json={
    "device_id": "dev_1", "port": "/dev/ttyUSB0"
})

# 3. 启动 AirPlay → iPhone 扫码投屏
r = requests.post(f"{BASE}/api/device/airplay/start", json={"device_id": "dev_1"})

# 4. 开始采集
r = requests.post(f"{BASE}/api/device/capture/start", json={"device_id": "dev_1"})

# 5. 找图 → 点击
r = requests.post(f"{BASE}/api/find_image", json={
    "device_id": "dev_1",
    "template_path": "templates/buy_button.png",
    "threshold": 0.8
})
# → {"x": 320, "y": 640, "confidence": 0.95}

requests.post(f"{BASE}/api/click", json={
    "device_id": "dev_1", "x": 320, "y": 640
})
```

## WebSocket

```
ws://localhost:9911/ws
```

支持实时事件推送和设备状态订阅。

## 硬件接线

```
CH9329 模块:
  VCC → 5V (USB)
  GND → GND
  TX  → USB-TTL RX (CH340)
  RX  → USB-TTL TX (CH340)

CH9329 → Lightning OTG → iPhone
```

每台 iPhone 需要一个 CH9329 芯片 + 一条 Lightning OTG 线。多台通过 USB Hub 连接 PC。

## 项目结构

```
imouse/
├── main.py           # 入口，启动服务
├── server.py         # FastAPI + WebSocket API
├── hardware.py       # CH9329 串口控制
├── airplay.py        # UxPlay 子进程管理
├── capture.py        # 屏幕截图引擎
├── vision.py         # OpenCV + PaddleOCR
├── device_manager.py # 设备注册/绑定/状态
└── __init__.py
```
