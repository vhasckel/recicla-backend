from typing import List, Dict, Any, Optional, Union
from math import radians, cos, sin, asin, sqrt
import uuid
from datetime import datetime, timezone
from collections import Counter
from ..models.collection_point import (
    CollectionPoint,
    CollectionPointFilters,
    CollectionPointWithDistance,
    CollectionPointCreate,
    CollectionPointUpdate,
)
from ..data.mock_collection_points import MOCK_COLLECTION_POINTS


class CollectionPointsService:

    def __init__(self):
        self.collection_points: Dict[str, CollectionPoint] = {
            point["id"]: CollectionPoint(**point) for point in MOCK_COLLECTION_POINTS
        }

    def get_collection_point_by_id(self, point_id: str) -> Optional[CollectionPoint]:
        return self.collection_points.get(point_id)

    def get_all_collection_points(
        self, filters: CollectionPointFilters
    ) -> List[Union[CollectionPoint, CollectionPointWithDistance]]:
        all_points = list(self.collection_points.values())

        if filters.is_active is not None:
            results = [p for p in all_points if p.is_active == filters.is_active]
        else:
            results = all_points[:]

        if filters.city:
            results = [p for p in results if p.city.lower() == filters.city.lower()]

        if filters.neighborhood:
            results = [
                p
                for p in results
                if p.neighborhood.lower() == filters.neighborhood.lower()
            ]

        if filters.material:
            results = [p for p in results if filters.material in p.materials]

        if filters.accepts_all_materials is not None:
            results = [
                p
                for p in results
                if p.accepts_all_materials == filters.accepts_all_materials
            ]

        if filters.search:
            query = filters.search.lower()
            results = [
                p
                for p in results
                if query in p.name.lower()
                or query in p.neighborhood.lower()
                or query in p.street.lower()
            ]

        if filters.lat is not None and filters.lng is not None:
            points_with_distance = []
            for point in results:
                distance = self._haversine_distance(
                    filters.lat, filters.lng, point.lat, point.lng
                )
                if distance <= filters.radius_km:
                    point_with_dist = CollectionPointWithDistance(
                        **point.model_dump(), distance_km=round(distance, 2)
                    )
                    points_with_distance.append(point_with_dist)

            points_with_distance.sort(key=lambda p: p.distance_km)
            return points_with_distance

        return results

    def get_collection_points_statistics(self) -> Dict[str, Any]:
        active_points = [p for p in self.collection_points.values() if p.is_active]

        if not active_points:
            return {
                "total_points": 0,
                "materials_distribution": {},
                "neighborhoods_distribution": {},
                "points_accepting_all_materials": 0,
            }

        materials_dist = Counter(
            material for point in active_points for material in point.materials
        )
        neighborhoods_dist = Counter(point.neighborhood for point in active_points)

        return {
            "total_points": len(active_points),
            "materials_distribution": dict(materials_dist),
            "neighborhoods_distribution": dict(neighborhoods_dist),
            "points_accepting_all_materials": sum(
                1 for p in active_points if p.accepts_all_materials
            ),
        }

    def _haversine_distance(
        self, lat1: float, lon1: float, lat2: float, lon2: float
    ) -> float:
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        r = 6371
        return c * r

    def create_collection_point(
        self, collection_point_data: CollectionPointCreate
    ) -> CollectionPoint:
        new_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc)

        new_point_data = collection_point_data.model_dump()
        new_point = CollectionPoint(
            **new_point_data, id=new_id, created_at=now, updated_at=now, is_active=True
        )
        self.collection_points[new_point.id] = new_point
        return new_point

    def update_collection_point(
        self, point_id: str, collection_point_data: CollectionPointUpdate
    ) -> Optional[CollectionPoint]:
        point_to_update = self.get_collection_point_by_id(point_id)
        if not point_to_update:
            return None

        update_data = collection_point_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(point_to_update, field, value)

        point_to_update.updated_at = datetime.now(timezone.utc)
        self.collection_points[point_id] = point_to_update
        return point_to_update

    def delete_collection_point(self, point_id: str) -> Optional[CollectionPoint]:
        point = self.collection_points.get(point_id)
        if point:
            del self.collection_points[point_id]
            return point
        return None


collection_points_service = CollectionPointsService()
