# 🎮 Mini World Royale - PC FPS Controller

> [!WARNING]
> **Work In Progress (WIP):** โปรเจกต์นี้ยังอยู่ในการพัฒนาและอาจมีข้อผิดพลาด (Bugs) หรือฟีเจอร์ที่ยังไม่สมบูรณ์อยู่บ้าง กำลังทยอยปรับปรุงให้ดีขึ้นในอนาคตครับ!

---

โปรแกรมช่วยเล่นเกม **Mini World Royale** บน PC โดยใช้คีย์บอร์ดและเมาส์ (Keyboard & Mouse Mapping) ผ่าน **QtScrcpy** โดยเน้นความลื่นไหลในการเดินแบบ WASD และระบบควบคุม FPS แบบครบวงจร

---

## ✨ คุณสมบัติหลัก (Features)

*   **Global Key Hooks:** ใช้ระบบดักจับปุ่มกด (Global Keyboard Hook) ทำให้สามารถกดเดิน (WASD) ได้แม้ว่าหน้าต่างเกมจะถูกแย่ง Focus ไป (รองรับการเล่นโหมด FPS)
*   **Overlay Layout Visualizer:** มีหน้าต่างโปร่งใสแสดงตำแหน่งปุ่มที่คุณตั้งค่าไว้ (x, y) เพื่อให้สามารถลากไปทับจอเกมและปรับแต่งพิกัดปุ่มให้ตรงกับหน้าจอมือถือได้อย่างแม่นยำ
*   **Auto-Keymap Sync:** ทุกครั้งที่เริ่มเกมผ่านสคริปต์ ระบบจะคัดลอกไฟล์ `MWR.json` (Keymap) เข้าไปในระบบของ QtScrcpy ให้โดยอัตโนมัติ
*   **Native ADB Integration:** ใช้คำสั่ง ADB โดยตรงเพื่อให้การตอบสนองของการกดปุ่ม (Tap/Swipe) ทำได้ไวที่สุด

---

## 🛠️ โครงสร้างโปรเจกต์ (Project Structure)

```text
Mini-World-Royale-ZXD44/
├── MWR_Controller.py    # ตัวควบคุมหลัก (UI + Controller + Key Hook)
├── Start_Game.sh        # สคริปต์เริ่มต้นอัตโนมัติ (Check ADB + Sync Keymap + Launch Game)
├── SystemCore/
│   ├── QtScrcpy_Pro/    # ตัวโปรแกรม QtScrcpy (Linux version)
│   └── configs/         # ไฟล์ตั้งค่าปุ่ม (MWR.json)
├── Documentation/       # คู่มือและเอกสารประกอบ
└── Testing/             # สคริปต์และโค้ดสำหรับการทดสอบระบบ
```

---

## 🚀 วิธีเริ่มต้นใช้งาน (Getting Started)

### 1. การติดตั้ง (Prerequisites)
ก่อนใช้งานโปรแกรม ต้องแน่ใจว่าได้ติดตั้งคุณสมบัติต่อไปนี้ในเครื่อง Linux ของคุณ:
```bash
# ติดตั้ง ADB
sudo apt install android-tools-adb

# ติดตั้ง Library ที่จำเป็นสำหรับ Python
pip install pynput tkinter
```

### 2. การเปิดใช้งาน (Running the Game)
คุณสามารถเลือกใช้งานได้ 2 วิธี:

*   **วิธีที่ 1 (แนะนำ):** รันผ่านสคริปต์เริ่มต้นอัตโนมัติ
    ```bash
    chmod +x Start_Game.sh
    ./Start_Game.sh
    ```
*   **วิธีที่ 2:** รันผ่าน Python Controller โดยตรง
    ```bash
    python3 MWR_Controller.py
    ```

### 3. การควบคุม (Controls)
*   **WASD:** เดิน (Movement)
*   **Left Click:** ยิง (Fire)
*   **Right Click:** เล็ง (ADS)
*   **Space:** กระโดด (Jump)
*   **R:** รีโหลดกระสุน (Reload)
*   **C:** นั่ง/ยอง (Crouch)
*   **Ctrl:** นอน (Prone)
*   **Tab:** สลับโหมด FPS (เมาส์หาย)
*   **Esc:** ออกจากโปรแกรม

---

## 🧩 การปรับแต่งปุ่ม (Calibration)
หากตำแหน่งปุ่มบนหน้าจอมือถือไม่ตรงกับตำแหน่งในโปรแกรม:
1. เปิดโปรแกรม `MWR_Controller.py`
2. กดปุ่ม **"👀 แสดงคีย์บนจอ (Overlay Layout)"**
3. ลากหน้าต่างโปร่งใสที่ปรากฏขึ้นไปทับบนหน้าต่าง QtScrcpy ให้พอดีกับจอเกม
4. หากวงกลมสีส้มไม่ตรงกับปุ่มในเกม ให้แก้ไขพิกัด `x, y` ในไฟล์ `SystemCore/configs/MWR.json` หรือในตัวแปร `CONFIG` ภายในไฟล์ `MWR_Controller.py`

---

## 👨‍💻 ผู้พัฒนา (Credits)
*   **Created by:** ZirconX
*   **Engine:** Powered by QtScrcpy & ADB
*   **Repository:** [ZXD44/Mini-World-Royale-ZXD44](https://github.com/ZXD44/Mini-World-Royale-ZXD44)
