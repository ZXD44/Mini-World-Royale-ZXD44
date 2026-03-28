import os
import shutil
import time
from pathlib import Path

# --- ตั้งค่าหมวดหมู่แบบเรียบง่าย (Clean & Beautiful) ---
CATEGORIES = {
    "Docs": [".md", ".pdf", ".txt", ".docx", ".xlsx", ".pptx"],
    "Tests": ["test_", ".spec", ".test"],
    "Trash_ขยะ": ["old", "temp", "backup", "archive", "legacy"]
}

# ไฟล์โค้ดสำคัญ (จะไม่ถูกย้ายไป Trash แม้จะไม่ได้แก้ไขนาน)
KEEP_EXTENSIONS = [".py", ".sh", ".json", ".js", ".html", ".css"]

def clean_and_simplify(project_dir="."):
    base = Path(project_dir).resolve()
    print(f"✨ กำลังสร้างโครงสร้างที่เรียบง่ายสวยงามให้กับ: {base.name}")
    print("-" * 50)
    
    # สร้างโฟลเดอร์หลักเพียง 4 หมวดเดียว
    for folder in ["Docs", "Tests", "Others", "Trash_ขยะ"]:
        (base / folder).mkdir(exist_ok=True)

    counts = {}
    
    # ดึงไฟล์ที่อยู่นอกโฟลเดอร์หลักออกมาจัดระเบียบใหม่
    for item in list(base.iterdir()):
        # ข้ามโฟลเดอร์หลักที่เราสร้าง และโฟลเดอร์ระบบ
        if item.name in ["Docs", "Tests", "Others", "Trash_ขยะ"] or item.name.startswith(".") or item.suffix == ".py":
            continue

        target = "Others"
        name_lower = item.name.lower()
        
        # 1. เช็คขยะ (ถ้าไม่ใช่ไฟล์โค้ดสำคัญ)
        is_trash_name = any(word in name_lower for word in CATEGORIES["Trash_ขยะ"])
        is_old = (time.time() - item.stat().st_mtime) > (180 * 24 * 60 * 60) # 6 เดือน
        is_code = item.suffix.lower() in KEEP_EXTENSIONS

        if (is_trash_name or is_old) and not is_code:
            target = "Trash_ขยะ"
        
        # 2. เช็ค Tests
        elif any(word in name_lower for word in CATEGORIES["Tests"]):
            target = "Tests"
            
        # 3. เช็ค Docs
        elif item.suffix.lower() in CATEGORIES["Docs"]:
            target = "Docs"

        # ย้ายไฟล์/โฟลเดอร์
        try:
            dest = base / target / item.name
            
            # ป้องกันชื่อซ้ำ
            if dest.exists():
                timestamp = int(time.time())
                dest = base / target / f"{item.stem if item.is_file() else item.name}_{timestamp}{item.suffix if item.is_file() else ''}"
            
            shutil.move(str(item), str(dest))
            counts[target] = counts.get(target, 0) + 1
            print(f"✅ ย้าย {item.name} -> 📁 {target}")
        except Exception as e:
            print(f"❌ ย้ายไม่ได้ {item.name}: {e}")

    # แสดงผลลัพธ์
    print("-" * 50)
    if not counts:
        print("🌟 ทุกอย่างเรียบร้อยและสวยงามอยู่แล้วครับ!")
    else:
        print("📊 สรุปผลการจัดระเบียบใหม่:")
        for folder, count in sorted(counts.items()):
            icon = "🗑️" if "Trash" in folder else "📁"
            print(f"  {icon} {folder}: {count} รายการ")
    print("-" * 50)
    print("✨ เรียบง่าย สวยงาม และลงตัวที่สุด!")

if __name__ == "__main__":
    clean_and_simplify()