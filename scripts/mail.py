import sys
import re
from typing import Tuple
try:
    import dns.resolver
except ImportError:
    print("Не найден dnspython. Установите: pip install dnspython")
    sys.exit(1)

EMAIL_RE = re.compile(r"^[^@\s]+@([^@\s]+\.[^@\s]+)$")

def parse_domain(email: str) -> Tuple[str, str]:
    email = email.strip()
    m = EMAIL_RE.match(email)
    if not m:
        return email, ""
    return email, m.group(1)

def check_domain(domain: str) -> Tuple[bool, str]:
    try:
        dns.resolver.resolve(domain, "A")
        a_exists = True
    except Exception:
        try:
            dns.resolver.resolve(domain, "AAAA")
            a_exists = True
        except Exception:
            a_exists = False

    mx_ok = False
    if a_exists:
        try:
            answers = dns.resolver.resolve(domain, "MX")
            mx_ok = len(answers) > 0
        except Exception:
            mx_ok = False

    if not a_exists:
        return False, "домен отсутствует"
    if not mx_ok:
        return True, "MX-записи отсутствуют или некорректны"
    return True, "домен валиден"

def main():
    if len(sys.argv) != 2:
        print("Использование: python check_mx.py emails.txt")
        sys.exit(1)
    path = sys.argv[1]
    try:
        with open(path, "r", encoding="utf-8") as f:
            emails = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"Не удалось открыть файл: {e}")
        sys.exit(1)

    for email in emails:
        email_norm, domain = parse_domain(email)
        if not domain:
            print(f"{email_norm} -> MX-записи отсутствуют или некорректны (неверный формат email)")
            continue
        exists, status = check_domain(domain)
        print(f"{email_norm} -> {status}")

if __name__ == "__main__":
    main()