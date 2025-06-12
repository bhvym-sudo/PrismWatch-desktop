from core.adb_controller import ADBController
from core.uid_mapper import UIDMapper

def main():
    adb = ADBController(adb_path="./bin/adb")
    uid_mapper = UIDMapper(adb)

    test_packages = [
        'com.android.chrome',
        'com.google.android.gms',
        'com.android.settings'
    ]

    for package in test_packages:
        try:
            uid = uid_mapper.get_uid_for_package(package)
            print(f"Package: {package} --> UID: {uid}")
        except Exception as e:
            print(f"Error processing {package}: {str(e)}")

if __name__ == "__main__":
    main()
