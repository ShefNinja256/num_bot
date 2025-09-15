def reduce_number(n: int) -> int:
    while n > 9 and n not in (11, 22, 33):
        n = sum(int(ch) for ch in str(n))
    return n

def calc_numbers(birthdate: str):
    day, month, year = map(int, birthdate.split("."))

    digits = [int(ch) for ch in birthdate if ch.isdigit()]
    destiny = reduce_number(sum(digits))
    soul = reduce_number(day)
    personality = reduce_number(day + month)
    maturity = reduce_number(destiny + soul)

    return {
        "судьбы": destiny,
        "души": soul,
        "личности": personality,
        "зрелости": maturity
    }

def calc_compatibility(date1: str, date2: str) -> dict:
    n1 = calc_numbers(date1)
    n2 = calc_numbers(date2)

    # простая логика совместимости:
    # считаем разницу по каждому числу
    diff = {k: abs(n1[k] - n2[k]) for k in n1}

    return {"person1": n1, "person2": n2, "разница": diff}
