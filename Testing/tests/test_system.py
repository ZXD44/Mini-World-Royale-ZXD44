#!/usr/bin/env python3
"""
🧪 System Test - ทดสอบระบบ
"""

import subprocess
import sys
import os

def test_adb():
    """ทดสอบ ADB"""
    print("\n📱 Test 1: ADB Connection")
    print("-" * 40)
    try:
        result = subprocess.run(['adb', 'devices'], 
            capture_output=True, text=True, timeout=5)
        print(result.stdout)
        # ตรวจสอบว่ามี device ต่ออยู่ (มีบรรทัดที่ลงท้ายด้วย 'device')
        has_device = any(line.strip().endswith('device') for line in result.stdout.split('\n'))
        if has_device:
            print("✅ ADB: OK")
            return True
        else:
            print("❌ ADB: No device found")
            return False
    except Exception as e:
        print(f"❌ ADB Error: {e}")
        return False

def test_screen_size():
    """ทดสอบดึงขนาดหน้าจอ"""
    print("\n📐 Test 2: Screen Size")
    print("-" * 40)
    try:
        result = subprocess.run(['adb', 'shell', 'wm', 'size'],
            capture_output=True, text=True, timeout=3)
        print(result.stdout)
        if 'Physical size' in result.stdout:
            print("✅ Screen: OK")
            return True
        else:
            print("⚠️ Screen: Using default")
            return True
    except Exception as e:
        print(f"❌ Screen Error: {e}")
        return False

def test_input_command():
    """ทดสอบคำสั่ง input"""
    print("\n🎮 Test 3: Input Command")
    print("-" * 40)
    try:
        # ทดสอบแตะที่มุมซ้ายบน (ไม่มีผลกับเกม)
        result = subprocess.run(['adb', 'shell', 'input tap 100 100'],
            capture_output=True, text=True, timeout=3)
        if result.returncode == 0:
            print("✅ Input: OK")
            return True
        else:
            print(f"⚠️ Input: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Input Error: {e}")
        return False

def test_swipe_command():
    """ทดสอบคำสั่ง swipe"""
    print("\n👆 Test 4: Swipe Command")
    print("-" * 40)
    try:
        # ทดสอบปัดสั้นๆ
        result = subprocess.run(['adb', 'shell', 'input swipe 400 900 500 900 200'],
            capture_output=True, text=True, timeout=3)
        if result.returncode == 0:
            print("✅ Swipe: OK")
            print("   (ดูที่หน้าจอมือถือว่ามีการปัดหรือไม่)")
            return True
        else:
            print(f"⚠️ Swipe: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Swipe Error: {e}")
        return False

def test_keymap_exists():
    """ทดสอบไฟล์ keymap"""
    print("\n📁 Test 5: Keymap File")
    print("-" * 40)
    keymap_path = './configs/MWR.json'
    if os.path.exists(keymap_path):
        print(f"✅ Keymap: {keymap_path}")
        return True
    else:
        print(f"❌ Keymap not found: {keymap_path}")
        return False

def test_qtscrcpy_exists():
    """ทดสอบ QtScrcpy"""
    print("\n🖥️  Test 6: QtScrcpy")
    print("-" * 40)
    apprun_path = './QtScrcpy_Pro/AppRun'
    if os.path.exists(apprun_path):
        print(f"✅ QtScrcpy: {apprun_path}")
        return True
    else:
        print(f"❌ QtScrcpy not found: {apprun_path}")
        return False

def main():
    print("="*50)
    print("  🧪 SYSTEM TEST - MWR FPS Controller")
    print("="*50)
    
    tests = [
        test_adb,
        test_screen_size,
        test_input_command,
        test_swipe_command,
        test_keymap_exists,
        test_qtscrcpy_exists,
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"❌ Test failed: {e}")
            results.append(False)
    
    print("\n" + "="*50)
    passed = sum(results)
    total = len(results)
    print(f"  ผลการทดสอบ: {passed}/{total} ผ่าน")
    print("="*50)
    
    if passed == total:
        print("\n✅ ระบบพร้อมใช้งาน!")
        print("   รัน: python3 MWR_Controller.py")
    else:
        print("\n⚠️  มีบางอย่างผิดพลาด ตรวจสอบด้านบน")
    
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
