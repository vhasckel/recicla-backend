"""
Collection Points API Endpoints - REVISED
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from ....models.collection_point import (
    CollectionPoint,
    CollectionPointResponse,
    CollectionPointsListResponse,
    CollectionPointsStatisticsResponse,
    CollectionPointFilters 
)
from ....services.collection_points_service import collection_points_service
from ....data.mock_collection_points import AVAILABLE_MATERIALS, AVAILABLE_NEIGHBORHOODS

router = APIRouter()


@router.get("/", response_model=CollectionPointsListResponse)
async def get_collection_points(
    filters: CollectionPointFilters = Depends() 
):
    """
    Get collection points with combined optional filters.
    Can filter by material, neighborhood, city, search query, coordinates, etc.
    """
    try:
        data = collection_points_service.get_all_collection_points(filters=filters)
        
        return CollectionPointsListResponse(
            success=True,
            data=data,
            total=len(data),
            message=f"Found {len(data)} collection points"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving collection points: {str(e)}")


@router.get("/{point_id}", response_model=CollectionPointResponse)
async def get_collection_point(point_id: str):
    """
    Get a specific collection point by ID
    """
    try:
        point = collection_points_service.get_collection_point_by_id(point_id)
        
        if not point:
            raise HTTPException(status_code=404, detail="Collection point not found")
        
        return CollectionPointResponse(
            success=True,
            data=point,
            message="Collection point retrieved successfully"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving collection point: {str(e)}")


@router.get("/statistics/", response_model=CollectionPointsStatisticsResponse)
async def get_collection_points_statistics():
    """
    Get statistics about collection points
    """
    try:
        stats = collection_points_service.get_collection_points_statistics()
        return CollectionPointsStatisticsResponse(
            success=True,
            data=stats,
            message="Statistics retrieved successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving statistics: {str(e)}")


@router.get("/materials/")
async def get_available_materials():
    """
    Get list of available materials
    """
    return {
        "success": True,
        "data": AVAILABLE_MATERIALS,
        "total": len(AVAILABLE_MATERIALS),
        "message": "Available materials retrieved successfully"
    }


@router.get("/neighborhoods/")
async def get_available_neighborhoods():
    """
    Get list of available neighborhoods
    """
    return {
        "success": True,
        "data": AVAILABLE_NEIGHBORHOODS,
        "total": len(AVAILABLE_NEIGHBORHOODS),
        "message": "Available neighborhoods retrieved successfully"
    }