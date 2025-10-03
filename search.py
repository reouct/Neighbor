from typing import List, Dict, Any, Tuple
from collections import OrderedDict
import os
import json

LISTINGS_PATH = os.environ.get(
    "LISTINGS_FILE",
    os.path.join(os.path.dirname(__file__), "listings.json"),
)


class Vehicle:
    def __init__(self, length: int):
        self.length = length


class Listing:
    __slots__ = ("id", "location_id", "length", "width", "price_in_cents")

    def __init__(
        self, id: str, location_id: str, length: int, width: int, price_in_cents: int
    ):
        self.id = id
        self.location_id = location_id
        self.length = length
        self.width = width
        self.price_in_cents = price_in_cents

    @property
    def capacity(self) -> int:
        return self.length

    def can_fit_any_vehicle(self) -> bool:
        return self.width >= 10


def load_listings() -> Dict[str, List[Listing]]:
    with open(LISTINGS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    by_location: Dict[str, List[Listing]] = {}
    for raw in data:
        listing = Listing(
            id=raw["id"],
            location_id=raw["location_id"],
            length=int(raw["length"]),
            width=int(raw["width"]),
            price_in_cents=int(raw["price_in_cents"]),
        )
        if listing.can_fit_any_vehicle():
            by_location.setdefault(listing.location_id, []).append(listing)
    for listings in by_location.values():
        listings.sort(key=lambda lst: lst.price_in_cents)
    return by_location


LISTINGS_BY_LOCATION = load_listings()


def validate_request(payload: Any) -> List[Vehicle]:
    if not isinstance(payload, list):
        raise ValueError("Root JSON must be an array of vehicle specs")
    vehicles: List[Vehicle] = []
    total_qty = 0
    for idx, item in enumerate(payload):
        if not isinstance(item, dict):
            raise ValueError(f"Item at index {idx} must be an object")
        if "length" not in item or "quantity" not in item:
            raise ValueError(f"Item at index {idx} missing 'length' or 'quantity'")
        length = item["length"]
        quantity = item["quantity"]
        if not (isinstance(length, int) and length > 0):
            raise ValueError(f"Item {idx} 'length' must be positive integer")
        if not (isinstance(quantity, int) and quantity > 0):
            raise ValueError(f"Item {idx} 'quantity' must be positive integer")
        total_qty += quantity
        if total_qty > 5:
            raise ValueError("Sum of all quantities must be <= 5")
        vehicles.extend(Vehicle(length=length) for _ in range(quantity))
    return vehicles


def cheapest_assignment_for_location(
    vehicles: List[Vehicle], listings: List[Listing]
) -> Tuple[int, List[str]] | None:
    if not listings:
        return None
    total_vehicle_length = sum(v.length for v in vehicles)
    if sum(lst.length for lst in listings) < total_vehicle_length:
        return None
    vehicles_sorted = sorted(vehicles, key=lambda v: v.length, reverse=True)
    n_listings = len(listings)
    best_cost = float("inf")
    best_selection: List[str] = []
    listing_lengths = [lst.capacity for lst in listings]
    listing_prices = [lst.price_in_cents for lst in listings]
    remaining = listing_lengths[:]
    used = [False] * n_listings

    def backtrack(vehicle_idx: int, current_cost: int):
        nonlocal best_cost, best_selection
        if current_cost >= best_cost:
            return
        if vehicle_idx == len(vehicles_sorted):
            if current_cost < best_cost:
                best_cost = current_cost
                best_selection = [listings[i].id for i in range(n_listings) if used[i]]
            return
        length_needed = vehicles_sorted[vehicle_idx].length
        for i in range(n_listings):
            if remaining[i] >= length_needed:
                newly_opened = not used[i]
                tentative_cost = current_cost + (
                    listing_prices[i] if newly_opened else 0
                )
                if tentative_cost >= best_cost:
                    continue
                remaining[i] -= length_needed
                was_used = used[i]
                used[i] = True
                backtrack(vehicle_idx + 1, tentative_cost)
                remaining[i] += length_needed
                used[i] = was_used

    backtrack(0, 0)
    if best_cost == float("inf"):
        return None
    return int(best_cost), best_selection


def compute_results(vehicles: List[Vehicle]) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    if not vehicles:
        return results
    for location_id, listings in LISTINGS_BY_LOCATION.items():
        outcome = cheapest_assignment_for_location(vehicles, listings)
        if outcome is None:
            continue
        cost, listing_ids = outcome
        results.append(
            OrderedDict(
                [
                    ("location_id", location_id),
                    ("listing_ids", listing_ids),
                    ("total_price_in_cents", cost),
                ]
            )
        )
    results.sort(key=lambda r: r["total_price_in_cents"])
    return results


def search_vehicles(payload: Any) -> List[Dict[str, Any]]:
    """Convenience wrapper: validate raw payload then compute results."""
    vehicles = validate_request(payload)
    return compute_results(vehicles)
