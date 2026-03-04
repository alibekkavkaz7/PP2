import re
import json

def parse_receipt(file):
    text = open(file, encoding="utf-8").read()

    products = re.findall(r"\d+\.\s*\n(.+)", text)

    prices = re.findall(r"x\s*([\d\s]+,\d{2})", text)
    for i in range(len(prices)):
        prices[i] = float(prices[i].replace(" ", "").replace(",", "."))

    total = re.search(r"ИТОГО:\s*\n?([\d\s]+,\d{2})", text)
    if total:
        total = float(total.group(1).replace(" ", "").replace(",", "."))
    else:
        total = None

    payment = re.search(r"(Банковская карта|Наличные)", text)
    if payment:
        payment = payment.group(1)
    else:
        payment = None

    date = re.search(r"\d{2}\.\d{2}\.\d{4}\s+\d{2}:\d{2}:\d{2}", text)
    if date:
        date = date.group()
    else:
        date = None

    return {
        "products": products,
        "unit_prices": prices,
        "total": total,
        "payment_method": payment,
        "date_time": date
    }


data = parse_receipt("raw.txt")
print(json.dumps(data, indent=4, ensure_ascii=False))