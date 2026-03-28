#!/usr/bin/env python3
"""
🎮 Mini World Royale - FPS Controller
รวมทุกอย่าง: เปิด QtScrcpy + ควบคุมคีย์บอร์ด
Created by: ZirconX
"""

import subprocess
import threading
import time
import sys
import os
import signal
from tkinter import Tk, Label, Frame, Canvas

# ============================================
# ⚙️ การตั้งค่า
# ============================================

CONFIG = {
    'joystick': {'x': 0.134, 'y': 0.754, 'radius': 0.045},
    'buttons': {
        'fire':   (0.888, 0.744),
        'ads':    (0.951, 0.545),
        'jump':   (0.931, 0.644),
        'reload': (0.831, 0.684),
        'crouch': (0.941, 0.824),
        'prone':  (0.881, 0.864),
    },
    'walk_duration': 100,  # ms - เวลาปัด
    'walk_delay': 0.08,    # 80ms ระหว่างการเดิน
}

# ============================================
# 🔧 ADB Controller
# ============================================

class ADBController:
    def __init__(self):
        self.screen_w = 2800
        self.screen_h = 1260
        self.update_screen_size()
        print(f"📱 หน้าจอ: {self.screen_w}x{self.screen_h}")
        print(f"🎯 จอย: ({self.joy_x}, {self.joy_y})")
    
    def update_screen_size(self):
        """ดึงขนาดหน้าจอจากมือถือ"""
        try:
            result = subprocess.run(['adb', 'shell', 'wm', 'size'],
                capture_output=True, text=True, timeout=3)
            for line in result.stdout.split('\n'):
                if 'Physical size' in line:
                    size = line.split(':')[1].strip()
                    w, h = map(int, size.split('x'))
                    self.screen_w = max(w, h)
                    self.screen_h = min(w, h)
                    break
        except Exception as e:
            print(f"⚠️ ใช้ขนาด default: {e}")
        
        self.joy_x = int(self.screen_w * CONFIG['joystick']['x'])
        self.joy_y = int(self.screen_h * CONFIG['joystick']['y'])
        self.joy_radius = int(self.screen_w * CONFIG['joystick']['radius'])
    
    def tap(self, pos_name):
        """แตะที่ตำแหน่ง - ใช้ subprocess โดยตรง (ไวกว่า)"""
        if pos_name not in CONFIG['buttons']:
            return
        x_ratio, y_ratio = CONFIG['buttons'][pos_name]
        x = int(self.screen_w * x_ratio)
        y = int(self.screen_h * y_ratio)
        
        # ใช้ Popen แบบ non-blocking
        subprocess.Popen(['adb', 'shell', f'input tap {x} {y}'],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    def walk(self, dx, dy):
        """เดิน dx,dy = -1,0,1"""
        tx = self.joy_x + (dx * self.joy_radius)
        ty = self.joy_y + (dy * self.joy_radius)
        dur = CONFIG['walk_duration']
        
        subprocess.Popen(['adb', 'shell', 
            f'input swipe {self.joy_x} {self.joy_y} {tx} {ty} {dur}'],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# ============================================
# 🎮 Game Controller with UI
# ============================================

class GameController:
    def __init__(self):
        self.adb = ADBController()
        self.running = True
        self.keys = {'w': False, 'a': False, 's': False, 'd': False}
        self.lock = threading.Lock()
        
        # สร้าง UI
        self.root = Tk()
        self.root.title("🎮 MWR FPS Controller - ZirconX")
        self.root.geometry("350x450")
        self.root.configure(bg='#1a1a1a')
        self.root.attributes('-topmost', True)
        
        self.build_ui()
        self.bind_keys()
        
        # เริ่ม thread เดิน
        self.move_thread = threading.Thread(target=self.move_loop, daemon=True)
        self.move_thread.start()
    
    def build_ui(self):
        """สร้างหน้าต่าง UI"""
        # หัวข้อ
        Label(self.root, text="🎮 MWR Controller", 
              font=('Arial', 18, 'bold'), bg='#1a1a1a', fg='#00ff00').pack(pady=10)
        
        Label(self.root, text="by ZirconX", 
              font=('Arial', 10), bg='#1a1a1a', fg='#666666').pack()
        
        # สถานะ
        self.status = Label(self.root, text="⏸️ หยุด", 
                           font=('Arial', 14), bg='#1a1a1a', fg='#888888')
        self.status.pack(pady=10)
        
        # Canvas แสดงการกด
        self.canvas = Canvas(self.root, width=180, height=180, 
                            bg='#2a2a2a', highlightthickness=0)
        self.canvas.pack(pady=15)
        
        # วาดจุดกลางและปุ่ม WASD
        self.canvas.create_oval(80, 80, 100, 100, fill='#444444', outline='')
        self.vis = {
            'w': self.canvas.create_text(90, 35, text='W', font=('Arial', 20, 'bold'), fill='#666666'),
            's': self.canvas.create_text(90, 145, text='S', font=('Arial', 20, 'bold'), fill='#666666'),
            'a': self.canvas.create_text(35, 90, text='A', font=('Arial', 20, 'bold'), fill='#666666'),
            'd': self.canvas.create_text(145, 90, text='D', font=('Arial', 20, 'bold'), fill='#666666'),
        }
        
        # ข้อมูล
        info = "⌨️  WASD = เดิน | F = ยิง\n" + \
               "⬆️ Space = กระโดด | 🔄 R = รีโหลด\n" + \
               "⬇️ C = นั่ง | ❌ ESC = ออก"
        
        Label(self.root, text=info, font=('Arial', 11),
              bg='#1a1a1a', fg='#aaaaaa', justify='center').pack(pady=10)
              
        # ปุ่มแสดง Overlay
        from tkinter import Button
        Button(self.root, text="👀 แสดงคีย์บนจอ (Overlay Layout)", 
               command=self.toggle_overlay, bg='#333333', fg='white', 
               font=('Arial', 10, 'bold'), relief='flat', padx=10, pady=5).pack(pady=5)
               
    def toggle_overlay(self):
        """แสดง/ซ่อน หน้าต่างโปร่งใสสำหรับทาบบน QtScrcpy เพื่อดูปุ่ม"""
        if hasattr(self, 'overlay') and self.overlay.winfo_exists():
            self.overlay.destroy()
        else:
            from tkinter import Toplevel, Canvas
            self.overlay = Toplevel(self.root)
            self.overlay.title("🎮 MWR Keymap Overlay (ลากไปทับจอเกม)")
            self.overlay.geometry("800x400")
            self.overlay.attributes('-alpha', 0.6)  # โปร่งใส 60%
            self.overlay.attributes('-topmost', True)
            self.overlay.configure(bg='black')
            
            canvas = Canvas(self.overlay, bg='black', highlightthickness=0)
            canvas.pack(fill='both', expand=True)
            
            def draw_keys(event):
                canvas.delete('all')
                w, h = event.width, event.height
                
                # วาด Joystick
                jx, jy = CONFIG['joystick']['x'] * w, CONFIG['joystick']['y'] * h
                jr = max(CONFIG['joystick']['radius'] * w, 30)
                canvas.create_oval(jx-jr, jy-jr, jx+jr, jy+jr, outline='#00ff00', width=3, dash=(5,2))
                canvas.create_text(jx, jy, text='WASD', fill='#00ff00', font=('Arial', 14, 'bold'))
                
                # วาดปุ่มต่างๆ
                for name, (rx, ry) in CONFIG['buttons'].items():
                    bx, by = rx * w, ry * h
                    r = 25
                    canvas.create_oval(bx-r, by-r, bx+r, by+r, outline='#ffaa00', width=2)
                    canvas.create_text(bx, by, text=name.upper(), fill='white', font=('Arial', 11, 'bold'))
            
            canvas.bind('<Configure>', draw_keys)
    
    def bind_keys(self):
        """ผูกปุ่มคีย์บอร์ดแบบ Global (ทำงานแม้คลิกจออื่น)"""
        from pynput import keyboard
        
        self.root.protocol("WM_DELETE_WINDOW", self.quit)
        
        # ใช้ pynput เพื่อดักจับปุ่มทั่วทั้งระบบ!
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release)
        self.listener.start()
        
        # ไม่จำเป็นต้องบังคับ focus แล้ว แต่ให้หน้าต่างอยู่บนสุด
        self.root.attributes('-topmost', True)
    
    def on_press(self, key):
        """เมื่อกดปุ่ม (Global)"""
        try:
            # ดึงตัวอักษร
            if hasattr(key, 'char') and key.char:
                k = key.char.lower()
            else:
                k = key.name.lower()
        except:
            return
            
        if k in ['w', 'a', 's', 'd']:
            with self.lock:
                if not self.keys[k]:
                    self.keys[k] = True
                    # อัพเดต UI ใน thread หลัก
                    self.root.after(0, self.update_visual, k, True)
                    self.root.after(0, self.update_status)
        
        elif k == 'f':
            self.adb.tap('fire')
            self.root.after(0, self.set_temp_status, '🔫 ยิง!', '#ff4444')
        elif k == 'r':
            self.adb.tap('reload')
            self.root.after(0, self.set_temp_status, '🔄 รีโหลด!', '#ffaa00')
        elif k == 'c':
            self.adb.tap('crouch')
            self.root.after(0, self.set_temp_status, '⬇️ นั่ง!', '#00aa00')
        elif k == 'space':
            self.adb.tap('jump')
            self.root.after(0, self.set_temp_status, '⬆️ กระโดด!', '#4444ff')
        elif k == 'esc':
            self.root.after(0, self.quit)
    
    def on_release(self, key):
        """เมื่อปล่อยปุ่ม (Global)"""
        try:
            if hasattr(key, 'char') and key.char:
                k = key.char.lower()
            else:
                k = key.name.lower()
        except:
            return
            
        if k in ['w', 'a', 's', 'd']:
            with self.lock:
                self.keys[k] = False
                self.root.after(0, self.update_visual, k, False)
                self.root.after(0, self.update_status)
    
    def update_visual(self, key, active):
        """อัพเดตสีบน canvas"""
        color = '#00ff00' if active else '#666666'
        self.canvas.itemconfig(self.vis[key], fill=color)
    
    def update_status(self):
        """อัพเดตสถานะการเดิน"""
        with self.lock:
            any_pressed = any(self.keys.values())
        if any_pressed:
            self.status.config(text="▶️ เดิน", fg='#00ff00')
        else:
            self.status.config(text="⏸️ หยุด", fg='#888888')
    
    def set_temp_status(self, text, color):
        """ตั้งค่าสถานะชั่วคราว"""
        self.status.config(text=text, fg=color)
        self.root.after(200, self.update_status)
    
    def move_loop(self):
        """ลูปการเดิน - ทำงานตลอดเวลาที่กดค้าง"""
        while self.running:
            with self.lock:
                w, a, s, d = self.keys['w'], self.keys['a'], self.keys['s'], self.keys['d']
            
            dx = dy = 0
            if w: dy -= 1
            if s: dy += 1
            if a: dx -= 1
            if d: dx += 1
            
            if dx != 0 or dy != 0:
                self.adb.walk(dx, dy)
                time.sleep(CONFIG['walk_delay'])
            else:
                time.sleep(0.03)  # 30ms ถ้าไม่ได้กด
    
    def quit(self):
        """ออกจากโปรแกรม"""
        self.running = False
        if hasattr(self, 'listener'):
            self.listener.stop()
        self.root.destroy()
    
    def run(self):
        """เริ่มโปรแกรม"""
        self.root.mainloop()

# ============================================
# 🚀 QtScrcpy Launcher
# ============================================

def launch_qtscrcpy():
    """เปิด QtScrcpy"""
    # Find project root (check Root or SystemCore folder)
    game_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Check in SystemCore first (New Structure)
    if os.path.exists(os.path.join(game_dir, 'SystemCore', 'QtScrcpy_Pro')):
         qtscrcpy_dir = os.path.join(game_dir, 'SystemCore', 'QtScrcpy_Pro')
    else:
         qtscrcpy_dir = os.path.join(game_dir, 'QtScrcpy_Pro')
    
    apprun = os.path.join(qtscrcpy_dir, 'AppRun')
    
    if not os.path.exists(apprun):
        print(f"❌ ไม่พบ QtScrcpy ที่ {apprun}")
        return False
    
    print("🚀 กำลังเปิด QtScrcpy...")
    
    env = os.environ.copy()
    env['QT_QPA_PLATFORM'] = 'xcb'
    env['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(qtscrcpy_dir, 'usr/plugins')
    env['LD_LIBRARY_PATH'] = os.path.join(qtscrcpy_dir, 'usr/lib')
    
    try:
        subprocess.Popen([apprun], env=env, 
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(3)  # รอให้เปิด
        return True
    except Exception as e:
        print(f"❌ เปิด QtScrcpy ไม่ได้: {e}")
        return False

def check_adb():
    """ตรวจสอบ ADB และมือถือ"""
    try:
        result = subprocess.run(['adb', 'devices'], 
            capture_output=True, text=True, timeout=5)
        lines = [l for l in result.stdout.split('\n') if 'device' in l and 'List' not in l]
        if not lines:
            print("❌ ไม่พบมือถือ")
            print("   1. เสียบสาย USB")
            print("   2. เปิด USB Debugging")
            print("   3. กด Allow บนมือถือ")
            return False
        print("✅ เชื่อมต่อมือถือแล้ว")
        return True
    except Exception as e:
        print(f"❌ ADB error: {e}")
        return False

def copy_keymap():
    """คัดลอก keymap ไปทุกตำแหน่ง"""
    # Find project root
    game_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Check in SystemCore first
    if os.path.exists(os.path.join(game_dir, 'SystemCore', 'configs')):
        config_src = os.path.join(game_dir, 'SystemCore', 'configs', 'MWR.json')
    else:
        config_src = os.path.join(game_dir, 'configs', 'MWR.json')
    
    if not os.path.exists(config_src):
        print(f"⚠️ ไม่พบ {config_src}")
        return
    
    # Determine QtScrcpy path
    if os.path.exists(os.path.join(game_dir, 'SystemCore', 'QtScrcpy_Pro')):
         qtscrcpy_dir = os.path.join(game_dir, 'SystemCore', 'QtScrcpy_Pro')
    else:
         qtscrcpy_dir = os.path.join(game_dir, 'QtScrcpy_Pro')
    
    destinations = [
        os.path.join(qtscrcpy_dir, 'usr', 'share', 'keymap', 'MWR.json'),
        os.path.join(qtscrcpy_dir, 'keymap', 'MWR.json'),
        os.path.expanduser('~/.config/QtScrcpy/keymap/MWR.json'),
    ]
    
    try:
        import shutil
        for dest in destinations:
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.copy(config_src, dest)
        print("✅ Keymap ติดตั้งแล้ว")
    except Exception as e:
        print(f"⚠️ Keymap: {e}")

# ============================================
# 🎯 Main
# ============================================

def main():
    print("="*50)
    print("  🎮 Mini World Royale - FPS Controller")
    print("  Created by: ZirconX")
    print("="*50)
    
    # ตรวจสอบ ADB
    if not check_adb():
        input("\nกด Enter เพื่อออก...")
        return
    
    # คัดลอก keymap
    copy_keymap()
    
    # เปิด QtScrcpy
    if not launch_qtscrcpy():
        print("⚠️ ไม่สามารถเปิด QtScrcpy อัตโนมัติได้")
        response = input("   ต้องการเปิดเองหรือไม่? (y/n): ")
        if response.lower() != 'y':
            return
    
    print("\n" + "="*50)
    print("✅ QtScrcpy พร้อมใช้งาน!")
    print("="*50)
    print("📋 ขั้นตอนต่อไป:")
    print("   1. ใน QtScrcpy: กด Refresh → เลือก 'MWR'")
    print("   2. กด Tab เพื่อเข้าโหมด FPS")
    print("   3. คลิกที่หน้าต่าง Controller นี้")
    print("   4. ลองกด WASD เดิน!")
    print("="*50 + "\n")
    
    # เริ่ม Controller
    try:
        controller = GameController()
        controller.run()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        input("กด Enter เพื่อออก...")

if __name__ == '__main__':
    main()
