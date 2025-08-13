from __future__ import annotations

import re
from typing import Optional


def _to_float(num_str: str) -> Optional[float]:
    try:
        return float(num_str.replace(",", "."))
    except Exception:
        return None


def parse_height_m(text: str) -> Optional[float]:
    text_l = text.lower()
    # Примеры: 1.5 м, 1,8м, высота 2 м
    m = re.search(r"(высота\s*)?(\d+[\.,]?\d*)\s*(м(етр[аоы])?)", text_l)
    if m:
        return _to_float(m.group(2))
    # Частые варианты без единиц: 12x1.8, 1.8 высота
    m2 = re.search(r"(\d+[\.,]?\d*)\s*(высота)", text_l)
    if m2:
        return _to_float(m2.group(1))
    return None


def parse_length_m(text: str) -> Optional[float]:
    text_l = text.lower()
    # Примеры: 100 м, длина 80м, периметр 120м, 100 п.м.
    m = re.search(r"(длина|периметр|п[\s\.]?м\.|погоны[йх]\s*метр[аоы]?)*\s*(\d+[\.,]?\d*)\s*(п[\s\.]?м\.|м(етр[аоы])?)", text_l)
    if m and m.group(2):
        return _to_float(m.group(2))
    # В формате 100м без слова
    m2 = re.search(r"(\d+[\.,]?\d*)\s*м(етр[аоы])?", text_l)
    if m2:
        return _to_float(m2.group(1))
    return None


def parse_cell_mm(text: str) -> Optional[int]:
    text_l = text.lower().replace("мм", " mm ")
    # Примеры: ячейка 50, 50 мм, 50mm
    m = re.search(r"(ячейк[аы]\s*)?(\d{2})\s*(mm|мм)?", text_l)
    if m:
        try:
            val = int(m.group(2))
            if val in {40, 50, 60}:
                return val
            # Допустим любой разумный двухзначный
            if 20 <= val <= 80:
                return val
        except Exception:
            return None
    return None


def parse_wire_mm(text: str) -> Optional[float]:
    text_l = text.lower().replace("мм", " mm ")
    # Примеры: проволока 2.5, диаметр 3 мм, 3.0mm
    m = re.search(r"(проволок[аы]|диаметр)?\s*(\d+[\.,]?\d*)\s*(mm|мм)?", text_l)
    if m and m.group(2):
        return _to_float(m.group(2))
    return None


def parse_coating(text: str) -> Optional[str]:
    text_l = text.lower()
    if "горяч" in text_l:
        return "hot_dip"
    if "электро" in text_l:
        return "electro"
    if "оцинк" in text_l:
        # по умолчанию предположим горячее
        return "hot_dip"
    return None


def parse_distance_km(text: str) -> Optional[float]:
    text_l = text.lower().replace("км.", " км ")
    m = re.search(r"(\d+[\.,]?\d*)\s*км", text_l)
    if m:
        return _to_float(m.group(1))
    return None


def parse_phone(text: str) -> Optional[str]:
    # Очень простой парсер телефона
    m = re.search(r"(\+?\d[\d\s\-\(\)]{7,}\d)", text)
    if m:
        return re.sub(r"[^\d\+]", "", m.group(1))
    return None


def parse_name(text: str) -> Optional[str]:
    text_stripped = text.strip()
    if 2 <= len(text_stripped) <= 64 and not any(ch.isdigit() for ch in text_stripped):
        return text_stripped
    return None