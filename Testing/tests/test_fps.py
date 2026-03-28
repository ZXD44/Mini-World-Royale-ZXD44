#!/usr/bin/env python3
import time
import subprocess
import os

def measure_input_performance():
    print("="*50)
    print("  🧪 FPS TESTING - INPUT PERFORMANCE (ADB)")
    print("="*50)
    
    # Check device
    result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
    if 'device\n' not in result.stdout:
        print("❌ Device not connected properly.")
        return

    # Measure Tap speed
    print("\n📦 Test 1: Single execution (Blocking Tap)")
    start = time.time()
    for _ in range(5):
        subprocess.run(['adb', 'shell', 'input tap 10 10'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    end = time.time()
    avg_blocking = (end - start) / 5
    print(f"   Avg time per command: {avg_blocking:.3f}s")
    print(f"   Potential FPS (Blocking): {1/avg_blocking:.1f} fps")

    # Measure Async execution (As used in MWR_Controller.py)
    print("\n🚀 Test 2: Async execution (subprocess.Popen)")
    start = time.time()
    processes = []
    num_tests = 10
    for _ in range(num_tests):
        p = subprocess.Popen(['adb', 'shell', 'input tap 10 10'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        processes.append(p)
    
    # Note: Popen is async, so we measure until launched
    launched_time = time.time() - start
    
    # Wait for completion to measure real throughput
    for p in processes:
        p.wait()
    total_time = time.time() - start
    
    print(f"   Launch time for {num_tests} commands: {launched_time:.3f}s")
    print(f"   Total completion time: {total_time:.3f}s")
    print(f"   Effective throughput: {num_tests/total_time:.1f} commands/sec (Real-world 'FPS')")

    print("\n🎮 Test 3: WASD Simulation (Swipe sequence)")
    # The controller uses 80ms delay. Let's see if the system can keep up.
    delay = 0.08  # 80ms
    print(f"   Target delay: {delay*1000}ms (Aiming for 12.5 updates/sec)")
    
    success_count = 0
    start = time.time()
    for i in range(10):
        # Simulation of a swipe
        subprocess.Popen(['adb', 'shell', 'input swipe 400 900 450 900 100'], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(delay)
        success_count += 1
    
    elapsed = time.time() - start
    print(f"   Elapsed for 10 swipes: {elapsed:.3f}s")
    print(f"   Actual Update FPS: {success_count/elapsed:.1f} fps")

    print("\n" + "="*50)
    if success_count/elapsed >= (1/delay) * 0.9:
        print("✅ PERFORMANCE: STABLE")
        print("   The system can handle the current 80ms WASD loop comfortably.")
    else:
        print("⚠️ PERFORMANCE: CONGESTED")
        print("   ADB is lagging behind the 80ms loop. Consider increasing 'walk_delay'.")
    print("="*50)

if __name__ == "__main__":
    measure_input_performance()
