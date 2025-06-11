from core.adb_controller import ADBController, ADBError

def main():
    try:
        print("Testing ADB connectivity...")
        adb = ADBController()
        
        print("\nConnected devices:")
        devices = adb.get_connected_devices()
        for i, (device_id, model) in enumerate(devices, 1):
            print(f"{i}. {model} ({device_id})")
        
        if not devices:
            print("No devices found!")
            return
            
        adb.device_id = devices[0][0]
        print(f"\nTesting basic command on {devices[0][1]}...")
        output = adb.execute_command("echo Hello Android")
        print(f"Command output: {output}")
        
        print("\nTesting root access...")
        try:
            root_output = adb.execute_command("id", use_su=True)
            print(f"Root access output: {root_output}")
        except ADBError as e:
            print(f"Root access failed (expected for non-rooted devices): {e}")
            
        print("\nADB connectivity test passed!")
        
    except ADBError as e:
        print(f"ADB test failed: {e}")

if __name__ == "__main__":
    main()