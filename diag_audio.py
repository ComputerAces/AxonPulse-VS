import pyaudio
try:
    p = pyaudio.PyAudio()
    count = p.get_device_count()
    print(f"TOTAL_DEVICES: {count}")
    for i in range(count):
        info = p.get_device_info_by_index(i)
        print(f"DEVICE_{i}: {info}")
    p.terminate()
except Exception as e:
    print(f"ERROR: {e}")
