from typing import List, Dict, Any, Optional, Union
from math import radians, cos, sin, asin, sqrt
from ..models.collection_point import CollectionPoint, CollectionPointFilters, CollectionPointWithDistance
from ..data.mock_collection_points import MOCK_COLLECTION_POINTS


class CollectionPointsService:
    
    def __init__(self):
        self.collection_points: List[CollectionPoint] = [CollectionPoint(**point) for point in MOCK_COLLECTION_POINTS]

    def get_all_collection_points(self, filters: CollectionPointFilters) -> List[Union[CollectionPoint, CollectionPointWithDistance]]:

        if filters.is_active is not None:
            results = [p for p in self.collection_points if p.is_active == filters.is_active]
        else:
            results = self.collection_points[:]

        if filters.city:
            results = [p for p in results if p.city.lower() == filters.city.lower()]
            
        if filters.neighborhood:
            results = [p for p in results if p.neighborhood.lower() == filters.neighborhood.lower()]

        if filters.material:
            results = [p for p in results if filters.material in p.materials]

        if filters.accepts_all_materials is not None:
            results = [p for p in results if p.accepts_all_materials == filters.accepts_all_materials]

        if filters.search:
            query = filters.search.lower()
            results = [p for p in results if 
                       query in p.name.lower() or 
                       query in p.neighborhood.lower() or 
                       query in p.street.lower()]

        if filters.lat is not None and filters.lng is not None:
            points_with_distance = []
            for point in results:
                distance = self._haversine_distance(filters.lat, filters.lng, point.lat, point.lng)
                if distance <= filters.radius_km:
                    point_with_dist = CollectionPointWithDistance(**point.model_dump(), distance_km=round(distance, 2))
                    points_with_distance.append(point_with_dist)
            
            points_with_distance.sort(key=lambda p: p.distance_km)
            return points_with_distance

        return results

    def get_collection_point_by_id(self, point_id: str) -> Optional[CollectionPoint]:
        for point in self.collection_points:
            if point.id == point_id:
                return point
        return None

    def get_collection_points_statistics(self) -> Dict[str, Any]:
        active_points = [p for p in self.collection_points if p.is_active]
        total_points = len(active_points)
        materials_count = {}
        neighborhoods_count = {}
        
        for point in active_points:
            for material in point.materials:
                materials_count[material] = materials_count.get(material, 0) + 1
            
            neighborhood = point.neighborhood
            neighborhoods_count[neighborhood] = neighborhoods_count.get(neighborhood, 0) + 1
            
        return {
            "total_points": total_points,
            "materials_distribution": materials_count,
            "neighborhoods_distribution": neighborhoods_count,
            "points_accepting_all_materials": len([p for p in active_points if p.accepts_all_materials])
        }

    def _haversine_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        r = 6371
        return c * r


collection_points_service = CollectionPointsService()