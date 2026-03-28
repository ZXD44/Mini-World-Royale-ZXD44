#!/bin/bash
# ============================================
# 🧪 Direct Test - ทดสอบโดยตรงด้วย ADB
# ============================================

echo "=================================================="
echo "  🧪 DIRECT TEST - ทดสอบการควบคุมโดยตรง"
echo "=================================================="
echo ""

# ตรวจสอบมือถือ
if ! adb devices | grep -q "device$"; then
    echo "❌ ไม่พบมือถือ"
    exit 1
fi

# ดึงขนาดหน้าจอ
SCREEN=$(adb shell wm size | grep -o '[0-9]*x[0-9]*' | head -1)
W=$(echo $SCREEN | cut -dx -f1)
H=$(echo $SCREEN | cut -dx -f2)

# ถ้าเป็นแนวตั้ง สลับ
if [ "$W" -lt "$H" ]; then
    TMP=$W; W=$H; H=$TMP
fi

echo "📱 หน้าจอ: ${W}x${H}"
echo ""

# พิกัดจาก MWR.json (ใช้ค่าเปอร์เซ็นต์คูณกับขนาดจริง)
JOY_X=$(echo "$W * 0.16" | bc | cut -d. -f1)
JOY_Y=$(echo "$H * 0.78" | bc | cut -d. -f1)

echo "🎯 พิกัดจอยจาก config:"
echo "   เปอร์เซ็นต์: (0.16, 0.78)"
echo "   พิกัดจริง: ($JOY_X, $JOY_Y)"
echo ""

# คำนวณระยะปัด (offset)
OFFSET=$(echo "$W * 0.08" | bc | cut -d. -f1)
echo "📏 ระยะปัด: $OFFSET pixels"
echo ""

echo "🎮 เริ่มทดสอบใน 3 วินาที..."
echo "   👀 ดูที่หน้าจอมือถือ!"
sleep 3

echo ""
echo "⬆️  ทดสอบ: ปัดขึ้น (เดินหน้า)..."
UP_Y=$(echo "$JOY_Y - $OFFSET" | bc | cut -d. -f1)
adb shell input swipe $JOY_X $JOY_Y $JOY_X $UP_Y 500
echo "    swipe $JOY_X $JOY_Y $JOY_X $UP_Y 500"
sleep 1

echo "⬇️  ทดสอบ: ปัดลง (ถอยหลัง)..."
DOWN_Y=$(echo "$JOY_Y + $OFFSET" | bc | cut -d. -f1)
adb shell input swipe $JOY_X $JOY_Y $JOY_X $DOWN_Y 500
echo "    swipe $JOY_X $JOY_Y $JOY_X $DOWN_Y 500"
sleep 1

echo "⬅️  ทดสอบ: ปัดซ้าย..."
LEFT_X=$(echo "$JOY_X - $OFFSET" | bc | cut -d. -f1)
adb shell input swipe $JOY_X $JOY_Y $LEFT_X $JOY_Y 500
echo "    swipe $JOY_X $JOY_Y $LEFT_X $JOY_Y 500"
sleep 1

echo "➡️  ทดสอบ: ปัดขวา..."
RIGHT_X=$(echo "$JOY_X + $OFFSET" | bc | cut -d. -f1)
adb shell input swipe $JOY_X $JOY_Y $RIGHT_X $JOY_Y 500
echo "    swipe $JOY_X $JOY_Y $RIGHT_X $JOY_Y 500"
sleep 1

echo ""
echo "✅ ทดสอบเสร็จสิ้น"
echo ""
echo "💡 ผลลัพธ์:"
echo "   - ถ้าตัวละครเดิน = พิกัดถูกต้อง ✅"
echo "   - ถ้าไม่เดิน = พิกัดผิด ต้องปรับใหม่ ❌"
echo ""
echo "🔧 ให้ปรับพิกัดใน configs/MWR.json"
echo "   แก้ตรง: centerPos -> x และ y"
