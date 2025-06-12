from core.adb_controller import ADBController
from core.proccess_analyzer import ProcessAnalyzer

def main():
    adb = ADBController(adb_path="./bin/adb")
    analyzer = ProcessAnalyzer(adb)

    print("Fetching all processes...")
    processes = analyzer.get_processes()

    print(f"Total Processes Found: {len(processes)}")

    tree = analyzer.build_process_tree(processes)

    print("\nProcess Tree:")
    analyzer.display_process_tree(tree)

if __name__ == "__main__":
    main()
