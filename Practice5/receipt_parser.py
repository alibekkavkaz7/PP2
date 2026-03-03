import re
import json

def parse_receipt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    result = {}

    products = re.findall(r"\d+\.\s*\n(.+)", text)
    result["products"] = products

    raw_prices = re.findall(r"x\s*([\d\s]+,\d{2})", text)
    prices = []
    for p in raw_prices:
        p = p.replace(" ", "").replace(",", ".")
        prices.append(float(p))
    result["unit_prices"] = prices

    total_match = re.search(r"ИТОГО:\s*\n?([\d\s]+,\d{2})", text)
    if total_match:
        total = total_match.group(1).replace(" ", "").replace(",", ".")
        result["total"] = float(total)
    else:
        result["total"] = None

    payment = re.search(r"(Банковская карта|Наличные)", text)
    result["payment_method"] = payment.group(1) if payment else None

    date = re.search(r"Время:\s*(\d{2}\.\d{2}\.\d{4}\s+\d{2}:\d{2}:\d{2})", text)
    result["date_time"] = date.group(1) if date else None

    return result


if __name__ == "__main__":
    data = parse_receipt("raw.txt")
    print(json.dumps(data, indent=4, ensure_ascii=False))