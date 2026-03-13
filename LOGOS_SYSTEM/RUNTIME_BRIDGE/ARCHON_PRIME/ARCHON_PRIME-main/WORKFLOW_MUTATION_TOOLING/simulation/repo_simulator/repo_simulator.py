from pathlib import Path


def simulate():
    files = list(Path(".").rglob("*.py"))
    print("Simulated modules:", len(files))


if __name__ == "__main__":
    simulate()
