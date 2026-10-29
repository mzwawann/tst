import json
import csv

def baca_nasabah(filepath: str) -> list[dict]:
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def update_saldo(filepath: str, norekening: int, perubahan: float) -> bool:
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return False

    ditemukan = False

    for nasabah in data:
        if nasabah.get("norekening") == norekening:
            nasabah["saldo"] = float(nasabah["saldo"]) + float(perubahan)
            ditemukan = True
            break

    if not ditemukan:
        return False

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)

    return True


def ekspor_ke_csv(json_path: str, csv_path: str) -> int:
    try:
        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return 0

    fieldnames = ["norekening", "nama", "saldo", "matauang"]

    with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for nasabah in data:
            writer.writerow(nasabah)

    return len(data)
