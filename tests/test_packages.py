from core.adb_controller import ADBController
from core.package_analyzer import PackageAnalyzer
import pprint

def debug_package_analysis(package_name):
    adb = ADBController(adb_path="./bin/adb")
    analyzer = PackageAnalyzer(adb)

    print(f"\n=== Debugging package: {package_name} ===")


    print("\n[RAW OUTPUT]")
    raw_output = adb.execute_command(f"dumpsys package {package_name}")
    print(raw_output[:2000] + ("..." if len(raw_output) > 2000 else ""))


    info = analyzer.get_package_info(package_name)


    print("\n[PARSED INFORMATION]")
    print(f"Package: {info['package']}")

    print("\nActivities:")
    pprint.pprint(info['activities'], width=120, compact=True)

    print("\nServices:")
    pprint.pprint(info['services'], width=120, compact=True)

    print("\nReceivers:")
    pprint.pprint(info['receivers'], width=120, compact=True)

    print("\nPermissions:")
    print("Granted:")
    pprint.pprint(info['permissions']['granted'], width=120, compact=True)
    print("\nRequested:")
    pprint.pprint(info['permissions']['requested'], width=120, compact=True)

    return info

def main():
    test_packages = [
        'com.android.chrome',  
    ]

    all_results = {}
    for pkg in test_packages:
        try:
            all_results[pkg] = debug_package_analysis(pkg)
            print("\n" + "="*80 + "\n")
        except Exception as e:
            print(f"Error analyzing {pkg}: {str(e)}")
            continue

    print("\n=== Analysis Complete ===")
    print(f"Successfully analyzed {len(all_results)}/{len(test_packages)} packages")

if __name__ == "__main__":
    main()
