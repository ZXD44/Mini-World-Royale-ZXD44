# 🎮 Mini World Royale - FPS PC Controller

เล่น Mini World Royale บน PC ด้วยคีย์บอร์ดและเมาส์! รองรับการควบคุมแบบ FPS (First Person Shooter) เต็มรูปแบบ

---

## ✨ ฟีเจอร์หลัก

- 🎮 **ควบคุมแบบ FPS** - WASD เดิน, เมาส์หมุนหันหน้า
- 🔫 **ยิง/เล็ง** - คลิกซ้ายยิง, คลิกขวาเล็ง
- 📱 **รองรับทุกหน้าจอ** - Auto-calibration ตามขนาดมือถือ
- 🚀 **ใช้งานง่าย** - รันไฟล์เดียวจบ!

---

## 🚀 วิธีใช้งาน

### 1. ติดตั้ง (ครั้งแรก)
```bash
sudo apt install android-tools-adb python3
```

### 2. รันโปรแกรม
```bash
cd ~/Downloads/Game
python3 MWR_Controller.py
```

### 3. ตั้งค่าใน QtScrcpy
1. กด **Refresh** ที่ช่อง Keymap
2. เลือก **MWR** จากรายการ
3. กด **Tab** เพื่อเข้าโหมด FPS (เมาส์จะหายไป)
4. คลิกที่หน้าต่าง **Controller**
5. ลองกด **WASD** เดิน!

---

## 🎮 ปุ่มควบคุม

| ปุ่ม | การทำงาน |
|------|---------|
| **W/A/S/D** | เดิน (กดค้างเดินต่อเนื่อง) |
| **W+D** | เดินเฉียงขวาบน |
| **คลิกซ้าย** | ยิง |
| **คลิกขวา** | เล็งสโคป |
| **Space** | กระโดด |
| **R** | รีโหลด |
| **C** | นั่ง/ยอง |
| **Ctrl** | นอน |
| **Tab** | สลับโหมด FPS |
| **Alt** | มองรอบๆ (Free Look) |

---

## 📂 โครงสร้างโปรเจค

```
Game/
├── 🎮 MWR_Controller.py   # โปรแกรมหลัก (ใช้ไฟล์นี้!)
├── 🚀 Start_Game.sh       # รัน QtScrcpy อย่างเดียว
├── 📂 configs/
│   └── MWR.json          # ตั้งค่าปุ่ม
├── 📂 QtScrcpy_Pro/       # โปรแกรมแสดงหน้าจอมือถือ
├── 📂 tests/              # สคริปต์ทดสอบ
│   ├── test_direct.sh
│   └── test_movement.sh
├── 📂 archive/            # ไฟล์เก่า (ไม่ใช้แล้ว)
│   └── CALIBRATION.md
├── 📂 legacy/             # โค้ดเก่า (สำรอง)
│   └── keymapper.py
└── 📄 README.md           # คู่มือนี้
```

---

## 🐛 แก้ปัญหา

### กด WASD ไม่เดิน?
1. ตรวจสอบว่าเลือก **Keymap: MWR** ใน QtScrcpy
2. กด **Tab** ให้เมาส์หายไป (เข้าโหมด FPS)
3. คลิกที่หน้าต่าง Controller ให้เป็นหน้าต่าง active

### ไม่พบมือถือ?
```bash
adb devices
```
- เสียบสาย USB ใหม่
- เปิด USB Debugging บนมือถือ
- กด Allow บนหน้าจอมือถือ

### QtScrcpy ไม่เปิด?
```bash
chmod +x QtScrcpy_Pro/AppRun
./QtScrcpy_Pro/AppRun
```

---

## ⚙️ ตั้งค่าขั้นสูง

แก้ไขพิกัดปุ่มได้ที่ `configs/MWR.json`:

```json
{
  "centerPos": {
    "x": 0.16,    # ตำแหน่งจอยเดิน X
    "y": 0.78     # ตำแหน่งจอยเดิน Y
  },
  "speedRatio": 6   # ความไวเมาส์
}
```

---

## 📱 รองรับมือถือ

| แบรนด์ | สถานะ |
|--------|--------|
| iQOO | ✅ ทดสอบแล้ว |
| Samsung | ✅ รองรับ |
| Xiaomi | ✅ รองรับ |
| OPPO/Vivo | ✅ รองรับ |
| Realme | ✅ รองรับ |

**หมายเหตุ:** ต้องเป็น Android 5.0+ และเปิด USB Debugging

---

## 📝 License

โปรเจกต์นี้สร้างขึ้นเพื่อการศึกษาและใช้งานส่วนตัว

---

## 👤 ผู้สร้าง

**Created by: ZirconX**

---

*Last Updated: March 2025*
