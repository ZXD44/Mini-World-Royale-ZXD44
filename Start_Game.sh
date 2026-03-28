#!/bin/bash

# ============================================
# 🎮 Mini World Royale - PC FPS Mode v6.3
# Auto-Calibration Edition
# ============================================

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

ENGINE_DIR="$DIR/SystemCore/QtScrcpy_Pro"
# If not found, check parent directory (for Others/ folder)
if [ ! -d "$ENGINE_DIR" ]; then 
    DIR="$(cd "$DIR/.." && pwd)"
    ENGINE_DIR="$DIR/SystemCore/QtScrcpy_Pro"
fi
# If not found, check Root for compatibility
if [ ! -d "$ENGINE_DIR" ]; then 
    ENGINE_DIR="$DIR/QtScrcpy_Pro"
fi

if [ ! -d "$ENGINE_DIR" ]; then
    echo "❌ ไม่พบตัวโปรแกรม QtScrcpy"
    exit 1
fi

echo "=================================================="
echo "  🚀 MINI WORLD ROYALE - PC FPS MODE v6.3"
echo "=================================================="

# ตรวจสอบ ADB
if ! command -v adb &> /dev/null; then
    echo "❌ ไม่พบ ADB"
    echo "   ติดตั้ง: sudo apt install android-tools-adb"
    exit 1
fi

# ตรวจสอบมือถือ
echo ""
echo "📱 กำลังตรวจสอบมือถือ..."
adb_devices_output=$(adb devices 2>/dev/null)
if ! echo "$adb_devices_output" | grep -q "device$"; then
    echo "❌ ไม่พบมือถือ!"
    echo "   1. เสียบสาย USB"
    echo "   2. เปิด USB Debugging"
    echo "   3. กด Allow บนมือถือ"
    echo ""
    adb devices
    exit 1
fi

# ===== AUTO CALIBRATE =====
echo ""
echo "🎯 กำลังปรับพิกัดอัตโนมัติ..."
if [ -f "$DIR/auto_calibrate.sh" ]; then
    bash "$DIR/auto_calibrate.sh" > /tmp/calibrate.log 2>&1
    if [ $? -eq 0 ]; then
        echo "   ✅ ปรับพิกัดเสร็จสิ้น"
        tail -n 5 /tmp/calibrate.log | grep -E "(พิกัด|จอย|ยิง|เล็ง)" | sed 's/^/   /'
    else
        echo "   ⚠️  ปรับพิกัดไม่สำเร็จ ใช้ค่าเดิม"
    fi
else
    echo "   ⚠️  ไม่พบ auto_calibrate.sh"
fi

# ดึงข้อมูลมือถือ
DEVICE_MODEL=$(adb shell getprop ro.product.model 2>/dev/null | tr -d '\r')
SCREEN_SIZE=$(adb shell wm size 2>/dev/null | grep "Physical size" | cut -d: -f2 | tr -d ' \r')
if [ -z "$SCREEN_SIZE" ]; then
    SCREEN_SIZE=$(adb shell wm size 2>/dev/null | head -1 | cut -d: -f2 | tr -d ' \r')
fi

echo ""
echo "   ✅ เชื่อมต่อ: $DEVICE_MODEL"
echo "   📐 หน้าจอ: $SCREEN_SIZE"

# ตรวจสอบ Keymap
CONFIG_FILE="$DIR/SystemCore/configs/MWR.json"
if [ ! -f "$CONFIG_FILE" ]; then
    CONFIG_FILE="$DIR/configs/MWR.json"
fi

if [ ! -f "$CONFIG_FILE" ]; then
    echo "❌ ไม่พบ MWR.json"
    exit 1
fi

if ! python3 -c "import json; json.load(open('$CONFIG_FILE'))" 2>/dev/null; then
    echo "❌ MWR.json ผิดพลาด"
    exit 1
fi

echo "   ✅ Keymap ถูกต้อง กำลังคัดลอก..."
cp "$CONFIG_FILE" "$ENGINE_DIR/usr/share/keymap/MWR.json" 2>/dev/null
cp "$CONFIG_FILE" "$ENGINE_DIR/keymap/MWR.json" 2>/dev/null
mkdir -p ~/.config/QtScrcpy/keymap
cp "$CONFIG_FILE" ~/.config/QtScrcpy/keymap/MWR.json 2>/dev/null

# แสดงวิธีใช้
echo ""
echo "=================================================="
echo "  🎮 วิธีใช้งาน:"
echo "=================================================="
echo "  1. รอ QtScrcpy เปิด"
echo "  2. กด [Refresh] ที่ช่อง Keymap"
echo "  3. เลือก 'MWR'"
echo "  4. กด [Tab] เพื่อเข้าโหมด FPS"
echo ""
echo "  ⌨️  ปุ่มควบคุม:"
echo "     WASD      = เดิน"
echo "     คลิกซ้าย  = ยิง"
echo "     คลิกขวา   = เล็ง"
echo "     Space     = กระโดด"
echo "     R         = รีโหลด"
echo "     C         = นั่ง"
echo "     Ctrl      = นอน"
echo "     Alt       = มองรอบๆ"
echo "     Tab       = สลับโหมด FPS"
echo "=================================================="
echo ""

# รันโปรแกรม
echo "🚀 กำลังเปิด QtScrcpy..."
export QT_QPA_PLATFORM=xcb
export QT_QPA_PLATFORM_PLUGIN_PATH="$ENGINE_DIR/usr/plugins"
export LD_LIBRARY_PATH="$ENGINE_DIR/usr/lib:$LD_LIBRARY_PATH"

"$ENGINE_DIR/AppRun"
