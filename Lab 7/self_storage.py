def parse_rental(text):
    if not isinstance(text, str):
        return None, 0.0
    text = text.strip()
    if ':' not in text:
        return None, 0.0
    parts = text.split(':')
    if len(parts) != 2:
        return None, 0.0
    unit, months_str = parts
    try:
        months = float(months_str.strip())
    except (ValueError, TypeError):
        return None, 0.0
    return unit.strip().title(), months


def duration_average(months_csv):
    if not isinstance(months_csv, str):
        return 0
    clean_csv = months_csv.strip()
    if not clean_csv:
        return 0
    parts = clean_csv.split(',')
    values = []
    for item in parts:
        item = item.strip()
        if not item:
            continue
        try:
            values.append(int(item))
        except (ValueError, TypeError):
            continue
    if not values:
        return 0
    return sum(values) // len(values)


def payable_rent(text):
    if not isinstance(text, str):
        return 0.0
    text = text.strip()
    if '|' not in text:
        return 0.0
    parts = text.split('|')
    if len(parts) != 2:
        return 0.0
    rent_str, discount_str = parts
    try:
        rent = float(rent_str.strip())
        discount = float(discount_str.strip())
    except (ValueError, TypeError):
        return 0.0
    total = rent * 1.18 - discount
    return max(total, 0.0)


def main():
    print("==== Running parse_rental ====")
    user_input = input("Enter unit:months (e.g. medium:6): ")
    result = parse_rental(user_input)
    print("Unit and Months:", result)

    print("\n==== Running duration_average ====")
    user_input = input("Enter rental months as CSV (e.g. 3,6,12): ")
    result = duration_average(user_input)
    print("Average Duration:", result)

    print("\n==== Running payable_rent ====")
    user_input = input("Enter rent|discount (e.g. 2400|200): ")
    result = payable_rent(user_input)
    print("Payable Rent:", result)


if __name__ == "__main__":
    main()