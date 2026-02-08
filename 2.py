#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Текстовый квест «Тайна заброшенного особняка».

Версия: 1.1 (добавлена очистка консоли)
"""

import sys
import os
import textwrap

# ----------------------------------------------------------------------
# ── Утилиты ─────────────────────────────────────────────────────────────
# ----------------------------------------------------------------------
def clear():
    """Очистить окно терминала (кроссплатформенно)."""
    os.system('cls' if os.name == 'nt' else 'clear')


def wrap(text):
    """Обернуть текст под ширину терминала (80 символов)."""
    return textwrap.fill(text, width=80)


# ----------------------------------------------------------------------
# ── Данные игры ────────────────────────────────────────────────────────
# ----------------------------------------------------------------------
rooms = {
    "outside": {
        "title": "Улица перед особняком",
        "desc": """Вы стоите перед старым, покрытым мхом особняком. Дверь приоткрыта,
                словно приглашая войти. Вокруг ночная тишина, только луна светит сквозь
                облака.""",
        "exits": {"in": "foyer"},
        "items": [],
    },

    "foyer": {
        "title": "Холл",
        "desc": """Пыльный холл освещён единственной свечой, трепещущей на столе.
                Перед вами лестница, ведущая наверх, и дорога в подвал.""",
        "exits": {"out": "outside", "up": "upper_hall", "down": "basement"},
        "items": ["candle"],
    },

    "upper_hall": {
        "title": "Верхний зал",
        "desc": """Высокий зал с большим портретом женщины в золотой раме.
                На стене висит замок с ключом‑отмычкой.""",
        "exits": {"down": "foyer", "north": "library"},
        "items": [],
        "locked": True,          # дверь в библиотеку заперта
    },

    "library": {
        "title": "Библиотека",
        "desc": """Пыльные книги выстроены в высоту. В центре стола лежит
                старый дневник, открытый на странице с загадочным рисунком.""",
        "exits": {"south": "upper_hall"},
        "items": ["diary"],
        "secret": False,
    },

    "basement": {
        "title": "Подвал",
        "desc": """Темно и влажно. На полу влага, а в углу стоит огромный сундук.
                На крышке странный замок в виде цифр.""",
        "exits": {"up": "foyer"},
        "items": ["keypad_code"],
        "locked": True,          # сундук закрыт
    },

    "secret_room": {
        "title": "Секретная комната",
        "desc": """Здесь скрыт древний артефакт — золотой медальон. Тишина здесь
                почти осязаема, будто сама история задержала дыхание.""",
        "exits": {"south": "library"},
        "items": ["medallion"],
    },
}

inventory = []

flags = {
    "has_candle": False,
    "has_key": False,
    "code_entered": False,
    "diary_read": False,
}


# ----------------------------------------------------------------------
# ── Функции взаимодействия ─────────────────────────────────────────────
# ----------------------------------------------------------------------
def print_room(name):
    """Вывести описание текущей локации."""
    room = rooms[name]
    print("\n" + "=" * 40)
    print(f"{room['title']}".center(40))
    print("-" * 40)
    print(wrap(room["desc"]))

    if room.get("items"):
        print("\nВы видите: " + ", ".join(room["items"]))

    exits = ", ".join(room["exits"].keys())
    print("\nВозможные пути:", exits)


def get_command():
    return input("\n> ").strip().lower()


def move(current, direction):
    room = rooms[current]
    if direction not in room["exits"]:
        print("Туда нельзя пройти.")
        return current

    nxt = room["exits"][direction]

    # проверка запертой двери/сундука
    if rooms.get(nxt, {}).get("locked", False):
        if nxt == "upper_hall" and not flags["has_key"]:
            print("Дверь в верхний зал заперта. Нужно найти ключ.")
            return current
        if nxt == "library" and rooms["upper_hall"]["locked"]:
            print("Дверь в библиотеку заперта.")
            return current
        if nxt == "basement" and not flags["code_entered"]:
            print("Сундук в подвале закрыт кодовым замком.")
            return current
    return nxt


def take(item, location):
    room = rooms[location]
    if item not in room.get("items", []):
        print("Здесь нет такого предмета.")
        return

    inventory.append(item)
    room["items"].remove(item)
    print(f"Вы взяли {item}.")

    if item == "candle":
        flags["has_candle"] = True
    elif item == "keypad_code":
        print("На замке написано: 3‑1‑4‑2.")


def use(item, location):
    if item not in inventory:
        print("У вас этого нет.")
        return

    if item == "candle" and location == "basement":
        print("Свет свечи отгоняет мрак, но ничего особенного не происходит.")
    elif item == "diary" and location == "library":
        print("Вы читаете дневник. В нём говорится о тайном проходе за портретом.")
        flags["diary_read"] = True
        rooms["upper_hall"]["locked"] = False
        print("Дверь в библиотеку теперь открыта!")
    elif item == "keypad_code" and location == "basement":
        code = input("Введите 4‑значный код: ").strip()
        if code == "3142":
            print("Код верный! Сундук открылся.")
            rooms["basement"]["locked"] = False
            flags["code_entered"] = True
            rooms["basement"]["items"].append("key")
        else:
            print("Неправильный код.")
    elif item == "key" and location == "foyer":
        print("Вы используете найденный ключ, чтобы открыть дверь в верхний зал.")
        flags["has_key"] = True
    else:
        print("Нечего делать с этим предметом здесь.")


def show_inventory():
    if inventory:
        print("Инвентарь: " + ", ".join(inventory))
    else:
        print("Инвентарь пуст.")


def check_win():
    if "medallion" in inventory:
        clear()
        print("\n" + "=" * 40)
        print("Поздравляем! Вы нашли золотой медальон и раскрыли тайну особняка!".center(40))
        print("=" * 40)
        sys.exit(0)


# ----------------------------------------------------------------------
# ── Главный цикл игры ───────────────────────────────────────────────────
# ----------------------------------------------------------------------
def main():
    clear()
    print("\n" + "=" * 40)
    print("      ТАЙНА ЗАБРОШЕННОГО ОСОБНЯКА".center(40))
    print("=" * 40)

    current_room = "outside"

    while True:
        print_room(current_room)
        cmd = get_command()

        if cmd in ("выход", "quit", "exit"):
            print("Спасибо за игру!")
            break

        elif cmd.startswith(("идти ", "go ")):
            _, direction = cmd.split(maxsplit=1)
            current_room = move(current_room, direction)

        elif cmd.startswith("взять "):
            _, item = cmd.split(maxsplit=1)
            take(item, current_room)

        elif cmd.startswith("использовать "):
            _, item = cmd.split(maxsplit=1)
            use(item, current_room)

        elif cmd in ("инвентарь", "inventory"):
            show_inventory()

        elif cmd == "осмотреть":
            pass      # просто перерисуем комнату

        else:
            print("Неизвестная команда. Доступные: идти <направление>, "
                  "взять <предмет>, использовать <предмет>, инвентарь, осмотреть, выход.")

        check_win()
        # После ответа очищаем консоль, чтобы показать «чистый» следующий экран
        clear()


if __name__ == "__main__":
    main()
