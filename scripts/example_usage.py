"""
Example usage of the collection points structure
"""

from app.services.collection_points_service import collection_points_service
from app.data.mock_collection_points import AVAILABLE_MATERIALS, AVAILABLE_NEIGHBORHOODS


def example_usage():
    """Example of how to use the collection points service"""
    
    print("=== Collection Points Service Examples ===\n")
    
    # 1. Get all collection points
    print("1. All collection points:")
    all_points = collection_points_service.get_all_collection_points()
    print(f"   Total: {len(all_points)} points\n")
    
    # 2. Get points by material
    print("2. Points that accept 'Vidro':")
    glass_points = collection_points_service.get_collection_points_by_material("Vidro")
    print(f"   Found: {len(glass_points)} points")
    for point in glass_points[:3]:  # Show first 3
        print(f"   - {point['name']} ({point['neighborhood']})")
    print()
    
    # 3. Search by neighborhood
    print("3. Points in 'Centro':")
    centro_points = collection_points_service.get_collection_points_by_neighborhood("Centro")
    print(f"   Found: {len(centro_points)} points")
    for point in centro_points:
        print(f"   - {point['name']} ({point['street']})")
    print()
    
    # 4. Search by query
    print("4. Search for 'lagoa':")
    lagoa_points = collection_points_service.search_collection_points("lagoa")
    print(f"   Found: {len(lagoa_points)} points")
    for point in lagoa_points:
        print(f"   - {point['name']} ({point['neighborhood']})")
    print()
    
    # 5. Get nearby points
    print("5. Points near Centro (lat: -27.5969, lng: -48.5495):")
    nearby_points = collection_points_service.get_collection_points_by_coordinates(
        lat=-27.5969, 
        lng=-48.5495, 
        radius_km=2.0
    )
    print(f"   Found: {len(nearby_points)} points within 2km")
    for point in nearby_points[:3]:  # Show first 3
        print(f"   - {point['name']} ({point['distance_km']}km)")
    print()
    
    # 6. Get statistics
    print("6. Statistics:")
    stats = collection_points_service.get_collection_points_statistics()
    print(f"   Total points: {stats['total_points']}")
    print(f"   Materials distribution: {stats['materials_distribution']}")
    print(f"   Points accepting all materials: {stats['points_accepting_all_materials']}")
    print()
    
    # 7. Available materials and neighborhoods
    print("7. Available options:")
    print(f"   Materials: {AVAILABLE_MATERIALS}")
    print(f"   Neighborhoods: {AVAILABLE_NEIGHBORHOODS}")


if __name__ == "__main__":
    example_usage() 