import sys
import requests

def main():
    if len(sys.argv) != 4:
        print("Использование: python send_to_telegram.py message.txt <BOT_TOKEN> <CHAT_ID>")
        sys.exit(1)

    msg_file, token, chat_id = sys.argv[1], sys.argv[2], sys.argv[3]

    try:
        with open(msg_file, "r", encoding="utf-8") as f:
            text = f.read().strip()
    except Exception as e:
        print(f"Не удалось прочитать файл: {e}")
        sys.exit(1)

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "disable_web_page_preview": True}
    try:
        r = requests.post(url, json=payload, timeout=10)
        if r.status_code == 200 and r.json().get("ok"):
            print("Сообщение отправлено")
        else:
            print(f"Ошибка отправки: {r.status_code} {r.text}")
    except Exception as e:
        print(f"Сбой запроса: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()