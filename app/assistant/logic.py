from __future__ import annotations

from typing import Dict, Any, List, Optional

from .memory import memory_store
from .nlu import (
    parse_height_m,
    parse_length_m,
    parse_cell_mm,
    parse_wire_mm,
    parse_coating,
    parse_distance_km,
    parse_phone,
    parse_name,
)
from .pricing import calculate_mesh_quote, QuoteInput


GREET = (
    "Здравствуйте! Я помогу подобрать и рассчитать сетку‑рабицу из оцинкованной проволоки. "
    "Напишите параметры или отвечайте на вопросы. Для начала укажите длину ограждения и желаемую высоту."
)


def _build_suggestions(state: Dict[str, Any]) -> List[str]:
    data = state["data"]
    suggestions: List[str] = []

    if not data.get("height_m"):
        suggestions += ["Высота 1.5 м", "Высота 1.8 м", "Высота 2.0 м"]
    if not data.get("length_m"):
        suggestions += ["Длина 50 м", "Длина 100 м"]
    if not data.get("cell_mm"):
        suggestions += ["Ячейка 40 мм", "Ячейка 50 мм", "Ячейка 60 мм"]
    if not data.get("wire_mm"):
        suggestions += ["Проволока 2.5 мм", "Проволока 3.0 мм"]
    if not data.get("coating"):
        suggestions += ["Горячее цинкование", "Электрооцинкование"]

    # Доп. действия
    suggestions += ["Рассчитать доставку", "Сброс"]
    return suggestions[:8]


def _update_data_from_message(message: str, data: Dict[str, Any]) -> None:
    h = parse_height_m(message)
    if h:
        data["height_m"] = h
    l = parse_length_m(message)
    if l:
        data["length_m"] = l
    cell = parse_cell_mm(message)
    if cell:
        data["cell_mm"] = cell
    w = parse_wire_mm(message)
    if w:
        data["wire_mm"] = w
    coat = parse_coating(message)
    if coat:
        data["coating"] = coat
    dist = parse_distance_km(message)
    if dist is not None:
        data["shipping_distance_km"] = dist
    phone = parse_phone(message)
    if phone:
        data["contact_phone"] = phone
    name = parse_name(message)
    # Имя записываем только если это не служебное слово
    if name and name.lower() not in {"сброс", "reset"}:
        data["contact_name"] = name


def _have_core_specs(data: Dict[str, Any]) -> bool:
    return all([
        data.get("height_m"),
        data.get("length_m"),
        data.get("cell_mm"),
        data.get("wire_mm"),
    ])


def _compose_quote_text(quote: Dict[str, Any]) -> str:
    c = quote.get("currency", "₽")
    inp = quote["inputs"]
    parts = [
        f"Расчёт: высота {inp['height_m']} м, длина {inp['length_m']} м (к закупке {inp['effective_length_m']} м),",
        f"ячейка {inp['cell_mm']} мм, проволока {inp['wire_mm']} мм, покрытие: {'горячее' if inp['coating']=='hot_dip' else 'электро'}.",
        f"Площадь: {quote['area_m2']} м². Цена за м²: {quote['pricing']['final_price_per_m2']} {c}.",
        f"Рулонов: {inp['num_rolls']} шт. Стоимость сетки: {quote['subtotal_mesh']} {c}."
    ]
    if "shipping_cost" in quote:
        parts.append(
            f"Доставка: {quote['shipping_cost']} {c} ({quote.get('shipping_comment', '')})."
        )
    parts.append(f"Итого: {quote['total']} {c}.")
    parts.append("Хотите оформить заказ или уточнить параметры?")
    return "\n".join(parts)


def handle_message(session_id: str | None, message: str) -> Dict[str, Any]:
    sid = memory_store.get_or_create_session(session_id)
    state = memory_store.get_state(sid)
    data = state["data"]

    text = message.strip()

    # Служебные команды
    if text.lower() in {"сброс", "reset", "/start"}:
        memory_store.reset(sid)
        new_state = memory_store.get_state(sid)
        return {
            "session_id": sid,
            "reply": GREET,
            "suggestions": _build_suggestions(new_state),
            "state": new_state,
            "quote": None,
        }

    # Обновляем известные данные из сообщения
    _update_data_from_message(text, data)

    # Если клиент просит доставку, подскажем ввести расстояние
    if "достав" in text.lower() and data.get("shipping_distance_km") is None:
        reply = (
            "Могу рассчитать доставку. Укажите расстояние от нашего склада до объекта, например: 25 км."
        )
        return {
            "session_id": sid,
            "reply": reply,
            "suggestions": _build_suggestions(state),
            "state": state,
            "quote": None,
        }

    # Если есть все параметры для расчёта — считаем
    quote_obj: Optional[Dict[str, Any]] = None
    if _have_core_specs(data):
        # Значение покрытия по умолчанию — hot_dip
        coating = data.get("coating") or "hot_dip"
        qi = QuoteInput(
            height_m=float(data["height_m"]),
            length_m=float(data["length_m"]),
            wire_mm=float(data["wire_mm"]),
            cell_mm=int(data["cell_mm"]),
            coating=coating,
            shipping_distance_km=(
                float(data["shipping_distance_km"]) if data.get("shipping_distance_km") is not None else None
            ),
        )
        quote_obj = calculate_mesh_quote(qi)
        reply_text = _compose_quote_text(quote_obj)
    else:
        # Спрашиваем недостающие параметры
        missing: List[str] = []
        if not data.get("length_m"):
            missing.append("длину ограждения в метрах")
        if not data.get("height_m"):
            missing.append("высоту сетки в метрах")
        if not data.get("cell_mm"):
            missing.append("размер ячейки в мм (например, 50)")
        if not data.get("wire_mm"):
            missing.append("диаметр проволоки в мм (например, 2.5)")

        reply_text = (
            "Чтобы рассчитать стоимость, укажите: " + ", ".join(missing) + ". "
            "Пример: 'длина 100 м, высота 1.8 м, ячейка 50, проволока 2.5'."
        )

    # Если контактные данные пришли — подтвердим
    confirm_bits: List[str] = []
    if data.get("contact_name"):
        confirm_bits.append(f"Имя: {data['contact_name']}")
    if data.get("contact_phone"):
        confirm_bits.append(f"Телефон: {data['contact_phone']}")
    if confirm_bits:
        reply_text += "\n" + "; ".join(confirm_bits) + "."

    return {
        "session_id": sid,
        "reply": reply_text if text else GREET,
        "suggestions": _build_suggestions(state),
        "state": state,
        "quote": quote_obj,
    }