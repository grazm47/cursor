from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Dict, Any, Optional
import json
import math
import os


CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "pricing.json")


@lru_cache(maxsize=1)
def load_pricing() -> Dict[str, Any]:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@dataclass
class QuoteInput:
    height_m: float
    length_m: float
    wire_mm: float
    cell_mm: int
    coating: str  # "hot_dip" | "electro"
    shipping_distance_km: Optional[float] = None


def calculate_mesh_quote(params: QuoteInput) -> Dict[str, Any]:
    cfg = load_pricing()

    base_price_per_m2 = float(cfg["base_price_per_m2"])  # базовая цена для 2.5 мм, 50 мм
    wire_mult = float(cfg["wire_diameter_multipliers"].get(str(params.wire_mm), 1.0))
    cell_mult = float(cfg["cell_size_multipliers"].get(str(params.cell_mm), 1.0))
    coat_mult = float(cfg["coating_multipliers"].get(params.coating, 1.0))

    roll_length_m = float(cfg["roll_length_m"])

    num_rolls = math.ceil(params.length_m / roll_length_m)
    effective_length_m = num_rolls * roll_length_m

    area_m2 = params.height_m * effective_length_m
    price_per_m2 = base_price_per_m2 * wire_mult * cell_mult * coat_mult

    subtotal_mesh = round(area_m2 * price_per_m2, 2)

    result: Dict[str, Any] = {
        "currency": cfg.get("currency", "₽"),
        "inputs": {
            "height_m": params.height_m,
            "length_m": params.length_m,
            "effective_length_m": effective_length_m,
            "wire_mm": params.wire_mm,
            "cell_mm": params.cell_mm,
            "coating": params.coating,
            "num_rolls": num_rolls,
        },
        "pricing": {
            "base_price_per_m2": base_price_per_m2,
            "wire_multiplier": wire_mult,
            "cell_multiplier": cell_mult,
            "coating_multiplier": coat_mult,
            "final_price_per_m2": round(price_per_m2, 2),
        },
        "area_m2": round(area_m2, 2),
        "subtotal_mesh": subtotal_mesh,
    }

    # Shipping (optional)
    if params.shipping_distance_km is not None:
        shipping_info = calculate_shipping_cost(params.shipping_distance_km, subtotal_mesh)
        result.update(shipping_info)
        result["total"] = round(subtotal_mesh + shipping_info["shipping_cost"], 2)
    else:
        result["total"] = subtotal_mesh

    return result


def calculate_shipping_cost(distance_km: float, items_subtotal: float) -> Dict[str, Any]:
    cfg = load_pricing()
    shipping_cfg = cfg.get("shipping", {})
    rate = float(shipping_cfg.get("base_rate_per_km", 0))
    minimum = float(shipping_cfg.get("minimum_shipping_cost", 0))
    free_threshold = float(shipping_cfg.get("free_shipping_threshold", 0))

    if items_subtotal >= free_threshold > 0:
        return {
            "shipping_distance_km": distance_km,
            "shipping_cost": 0.0,
            "shipping_comment": "Бесплатная доставка по сумме заказа"
        }

    raw_cost = distance_km * rate
    shipping_cost = max(raw_cost, minimum)
    return {
        "shipping_distance_km": distance_km,
        "shipping_cost": round(shipping_cost, 2),
        "shipping_comment": f"Расчёт по {rate} за км, мин. {minimum}"
    }