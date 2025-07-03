from fastapi import APIRouter, Depends, HTTPException
from ....models.collection_point import (
    CollectionPointResponse,
    CollectionPointsListResponse,
    CollectionPointsStatisticsResponse,
    CollectionPointFilters,
    CollectionPointCreate,
    CollectionPointUpdate,
)
from ....services.collection_points_service import collection_points_service
from ....data.mock_collection_points import AVAILABLE_MATERIALS, AVAILABLE_NEIGHBORHOODS

router = APIRouter()


@router.get("/", response_model=CollectionPointsListResponse)
async def get_collection_points(filters: CollectionPointFilters = Depends()):
    data = collection_points_service.get_all_collection_points(filters=filters)
    return CollectionPointsListResponse(
        success=True,
        data=data,
        total=len(data),
        message=f"Found {len(data)} collection points",
    )


@router.get("/{point_id}", response_model=CollectionPointResponse)
async def get_collection_point(point_id: str):
    point = collection_points_service.get_collection_point_by_id(point_id)
    if not point:
        raise HTTPException(status_code=404, detail="Collection point not found")
    return CollectionPointResponse(
        success=True, data=point, message="Collection point retrieved successfully"
    )


@router.get("/statistics/", response_model=CollectionPointsStatisticsResponse)
async def get_collection_points_statistics():
    stats = collection_points_service.get_collection_points_statistics()
    return CollectionPointsStatisticsResponse(
        success=True, data=stats, message="Statistics retrieved successfully"
    )


@router.get("/materials/")
async def get_available_materials():
    return {
        "success": True,
        "data": AVAILABLE_MATERIALS,
        "total": len(AVAILABLE_MATERIALS),
        "message": "Available materials retrieved successfully",
    }


@router.get("/neighborhoods/")
async def get_available_neighborhoods():
    return {
        "success": True,
        "data": AVAILABLE_NEIGHBORHOODS,
        "total": len(AVAILABLE_NEIGHBORHOODS),
        "message": "Available neighborhoods retrieved successfully",
    }


@router.post("/", response_model=CollectionPointResponse)
async def create_collection_point(collection_point: CollectionPointCreate):
    new_collection_point = collection_points_service.create_collection_point(
        collection_point
    )
    return CollectionPointResponse(
        success=True,
        data=new_collection_point,
        message="Collection point created successfully",
    )


@router.put("/{point_id}", response_model=CollectionPointResponse)
async def update_collection_point(
    point_id: str, collection_point: CollectionPointUpdate
):
    updated_point = collection_points_service.update_collection_point(
        point_id, collection_point
    )
    if not updated_point:
        raise HTTPException(status_code=404, detail="Collection point not found")
    return CollectionPointResponse(
        success=True,
        data=updated_point,
        message="Collection point updated successfully",
    )


@router.delete("/{point_id}", response_model=CollectionPointResponse)
async def delete_collection_point(point_id: str):
    deleted_point = collection_points_service.delete_collection_point(point_id)
    if not deleted_point:
        raise HTTPException(status_code=404, detail="Collection point not found")
    return CollectionPointResponse(
        success=True,
        data=deleted_point,
        message="Collection point deleted successfully",
    )
