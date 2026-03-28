# 🧪 Tests - สคริปต์ทดสอบ

โฟลเดอร์นี้เก็บสคริปต์สำหรับทดสอบการทำงาน

---

## ไฟล์ในนี้

| ไฟล์ | หน้าที่ |
|------|--------|
| **test_system.py** | 🧪 ทดสอบระบบทั้งหมด (ADB, Screen, Input, QtScrcpy) |
| **test_direct.sh** | 👆 ทดสอบส่งคำสั่ง ADB โดยตรง (swipe ที่จอย) |
| **test_movement.sh** | 🚶 ทดสอบการเดิน 4 ทิศทาง |

---

## วิธีใช้

### ทดสอบระบบทั้งหมด (แนะนำ)
```bash
python3 tests/test_system.py
```

จะตรวจสอบ:
- ✅ ADB Connection
- ✅ Screen Size Detection
- ✅ Input Commands
- ✅ Swipe Commands
- ✅ Keymap File
- ✅ QtScrcpy Installation

### ทดสอบการเดิน
```bash
./tests/test_direct.sh    # ทดสอบเดินผ่าน ADB
./tests/test_movement.sh  # ทดสอบเดิน 4 ทิศทาง
```

---

## หมายเหตุ

- ใช้สำหรับ **ทดสอบ** หรือ **แก้ปัญหา** เท่านั้น
- ไม่จำเป็นต้องใช้สำหรับการเล่นเกมปกติ
- ใช้ `MWR_Controller.py` สำหรับเล่นจริง
