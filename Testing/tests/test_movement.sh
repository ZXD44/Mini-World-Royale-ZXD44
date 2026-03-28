#!/bin/bash
# ============================================
# 🧪 Test Movement - ทดสอบการเดิน
# ============================================

echo "=================================================="
echo "  🧪 TEST MOVEMENT - ทดสอบการเดิน"
echo "=================================================="
echo ""

# ตรวจสอบมือถือ
if ! adb devices | grep -q "device$"; then
    echo "❌ ไม่พบมือถือ"
    exit 1
fi

# ดึงขนาดหน้าจอ
SCREEN_SIZE=$(adb shell wm size 2>/dev/null | grep "Physical size" | cut -d: -f2 | tr -d ' \r')
if [ -z "$SCREEN_SIZE" ]; then
    SCREEN_SIZE=$(adb shell wm size 2>/dev/null | head -1 | cut -d: -f2 | tr -d ' \r')
fi

WIDTH=$(echo $SCREEN_SIZE | cut -dx -f1)
HEIGHT=$(echo $SCREEN_SIZE | cut -dx -f2)

# ถ้าเป็นแนวตั้ง ให้สลับ
if [ "$WIDTH" -lt "$HEIGHT" ]; then
    TEMP=$WIDTH
    WIDTH=$HEIGHT
    HEIGHT=$TEMP
fi

echo "📱 หน้าจอ: ${WIDTH}x${HEIGHT}"
echo ""

# คำนวณพิกัดจอย (ซ้ายล่าง)
# จากรูป: จอยอยู่ประมาณ 15% จากซ้าย, 78% จากบน
JOY_X=$(echo "$WIDTH * 0.15" | bc | cut -d. -f1)
JOY_Y=$(echo "$HEIGHT * 0.78" | bc | cut -d. -f1)

echo "🎯 พิกัดจอย: ($JOY_X, $JOY_Y)"
echo ""

# ฟังก์ชั่นเดิน
test_walk() {
    local direction=$1
    local x1=$2
    local y1=$3
    local x2=$4
    local y2=$5
    
    echo "  ▶️  $direction: swipe from ($x1, $y1) to ($x2, $y2)"
    adb shell input swipe $x1 $y1 $x2 $y2 300 &
    sleep 0.5
}

echo "🎮 เริ่มทดสอบการเดิน..."
echo "   (ดูที่หน้าจอมือถือว่าตัวละครเดินหรือไม่)"
echo ""

# ทดสอบเดินหน้า (W) - ปัดขึ้น
echo "⬆️  ทดสอบเดินหน้า (W)..."
TEST_X=$JOY_X
TEST_Y=$JOY_Y
UP_X=$JOY_X
UP_Y=$(echo "$JOY_Y - 150" | bc | cut -d. -f1)
test_walk "เดินหน้า" $TEST_X $TEST_Y $UP_X $UP_Y
sleep 1

# ทดสอบถอยหลัง (S) - ปัดลง
echo "⬇️  ทดสอบถอยหลัง (S)..."
DOWN_Y=$(echo "$JOY_Y + 150" | bc | cut -d. -f1)
test_walk "ถอยหลัง" $TEST_X $TEST_Y $TEST_X $DOWN_Y
sleep 1

# ทดสอบเดินซ้าย (A) - ปัดซ้าย
echo "⬅️  ทดสอบเดินซ้าย (A)..."
LEFT_X=$(echo "$JOY_X - 150" | bc | cut -d. -f1)
test_walk "เดินซ้าย" $TEST_X $TEST_Y $LEFT_X $TEST_Y
sleep 1

# ทดสอบเดินขวา (D) - ปัดขวา
echo "➡️  ทดสอบเดินขวา (D)..."
RIGHT_X=$(echo "$JOY_X + 150" | bc | cut -d. -f1)
test_walk "เดินขวา" $TEST_X $TEST_Y $RIGHT_X $TEST_Y
sleep 1

echo ""
echo "✅ ทดสอบเสร็จสิ้น"
echo ""
echo "💡 ถ้าตัวละครไม่เดิน แสดงว่า:"
echo "   1. ยังไม่ได้เข้าเกมจริง (อยู่ในหน้าล็อบบี้)"
echo "   2. พิกัดจอยไม่ตรง"
echo "   3. เกมไม่รองรับการควบคุมแบบนี้"
echo ""
echo "📝 ลองปรับพิกัดจอยใน configs/MWR.json:"
echo "   ค่าปัจจุบัน: centerPos {x: 0.134, y: 0.754}"
echo "   ลองเปลี่ยนเป็น: {x: 0.16, y: 0.78}"
