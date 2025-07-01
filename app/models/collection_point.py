"""
Collection Point Models - Data models for collection points
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class CollectionPointBase(BaseModel):
    """Base model for collection point data"""
    name: str = Field(..., description="Name of the collection point")
    cep: str = Field(..., description="CEP (postal code)")
    city: str = Field(..., description="City name")
    neighborhood: str = Field(..., description="Neighborhood name")
    street: str = Field(..., description="Street name")
    number: str = Field(..., description="Street number")
    lat: float = Field(..., description="Latitude coordinate")
    lng: float = Field(..., description="Longitude coordinate")
    materials: List[str] = Field(..., description="List of accepted materials")
    description: str = Field("", description="Description of the collection point")
    phone: str = Field("", description="Contact phone number")
    email: str = Field("", description="Contact email")
    operating_hours: str = Field("Segunda a Sexta: 8h às 18h", description="Operating hours")
    accepts_all_materials: bool = Field(False, description="Whether accepts all materials")


class CollectionPointCreate(CollectionPointBase):
    """Model for creating a new collection point"""
    pass


class CollectionPointUpdate(BaseModel):
    """Model for updating a collection point"""
    name: Optional[str] = None
    cep: Optional[str] = None
    city: Optional[str] = None
    neighborhood: Optional[str] = None
    street: Optional[str] = None
    number: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    materials: Optional[List[str]] = None
    description: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    operating_hours: Optional[str] = None
    accepts_all_materials: Optional[bool] = None
    is_active: Optional[bool] = None


class CollectionPoint(CollectionPointBase):
    """Complete collection point model with all fields"""
    id: str = Field(..., description="Unique identifier")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    is_active: bool = Field(True, description="Whether the collection point is active")
    
    class Config:
        from_attributes = True


class CollectionPointWithDistance(CollectionPoint):
    """Collection point model with distance information"""
    distance_km: Optional[float] = Field(None, description="Distance in kilometers")


class CollectionPointResponse(BaseModel):
    """Response model for collection point operations"""
    success: bool = Field(..., description="Operation success status")
    data: Optional[CollectionPoint] = Field(None, description="Collection point data")
    message: str = Field("", description="Response message")


class CollectionPointsListResponse(BaseModel):
    """Response model for collection points list operations"""
    success: bool = Field(..., description="Operation success status")
    data: List[CollectionPoint] = Field(..., description="List of collection points")
    total: int = Field(..., description="Total number of collection points")
    message: str = Field("", description="Response message")


class CollectionPointsSearchResponse(BaseModel):
    """Response model for collection points search operations"""
    success: bool = Field(..., description="Operation success status")
    data: List[CollectionPoint] = Field(..., description="List of collection points")
    total: int = Field(..., description="Total number of results")
    query: str = Field(..., description="Search query used")
    message: str = Field("", description="Response message")


class CollectionPointsStatisticsResponse(BaseModel):
    """Response model for collection points statistics"""
    success: bool = Field(..., description="Operation success status")
    data: dict = Field(..., description="Statistics data")
    message: str = Field("", description="Response message")


# Filter models
class CollectionPointFilters(BaseModel):
    """Model for collection point filters"""
    material: Optional[str] = Field(None, description="Filter by material")
    neighborhood: Optional[str] = Field(None, description="Filter by neighborhood")
    city: Optional[str] = Field(None, description="Filter by city")
    search: Optional[str] = Field(None, description="Search query")
    lat: Optional[float] = Field(None, description="Latitude for proximity search")
    lng: Optional[float] = Field(None, description="Longitude for proximity search")
    radius_km: Optional[float] = Field(5.0, description="Radius for proximity search in kilometers")
    accepts_all_materials: Optional[bool] = Field(None, description="Filter by accepts all materials")
    is_active: Optional[bool] = Field(True, description="Filter by active status") 