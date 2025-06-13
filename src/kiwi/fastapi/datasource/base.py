from datetime import datetime

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uuid
import json
import os

router = APIRouter(
    prefix="/api/datasource",
    tags=["DataSource"]
)


# 数据源模型
class DataSource(BaseModel):
    id: str
    name: str
    type: str  # sqlite, duckdb, postgresql, etc.
    connection: str
    description: Optional[str] = None
    created_at: str


# 测试连接请求模型
class TestConnectionRequest(BaseModel):
    connection: str


# 数据源存储文件路径
DATA_SOURCES_FILE = "data_sources.json"


def load_data_sources():
    if not os.path.exists(DATA_SOURCES_FILE):
        return []

    try:
        with open(DATA_SOURCES_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_data_sources(data_sources):
    with open(DATA_SOURCES_FILE, "w") as f:
        json.dump(data_sources, f, indent=2)


@router.post("/test", response_model=dict)
async def test_connection(request: TestConnectionRequest):
    """
    测试数据库连接
    """
    # 在实际应用中，这里会使用SQLAlchemy测试连接
    # 为简单起见，这里仅做模拟
    try:
        # 模拟连接测试
        if "sqlite" in request.connection:
            return {"status": "success", "message": "Connection successful"}
        elif "postgresql" in request.connection:
            return {"status": "success", "message": "Connection successful"}
        elif "duckdb" in request.connection:
            return {"status": "success", "message": "Connection successful"}
        else:
            return {"status": "error", "message": "Unsupported database type"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=List[DataSource])
async def get_data_sources():
    """
    获取所有数据源
    """
    return load_data_sources()


@router.post("", response_model=DataSource)
async def create_data_source(data_source: DataSource):
    """
    创建新数据源
    """
    data_sources = load_data_sources()

    # 生成唯一ID
    data_source.id = str(uuid.uuid4())
    data_source.created_at = datetime.now().isoformat()

    data_sources.append(data_source.dict())
    save_data_sources(data_sources)

    return data_source


@router.put("/{data_source_id}", response_model=DataSource)
async def update_data_source(data_source_id: str, data_source: DataSource):
    """
    更新数据源
    """
    data_sources = load_data_sources()

    for idx, ds in enumerate(data_sources):
        if ds["id"] == data_source_id:
            data_sources[idx] = data_source.dict()
            save_data_sources(data_sources)
            return data_source

    raise HTTPException(status_code=404, detail="DataSource not found")


@router.delete("/{data_source_id}", response_model=dict)
async def delete_data_source(data_source_id: str):
    """
    删除数据源
    """
    data_sources = load_data_sources()
    new_data_sources = [ds for ds in data_sources if ds["id"] != data_source_id]

    if len(new_data_sources) == len(data_sources):
        raise HTTPException(status_code=404, detail="DataSource not found")

    save_data_sources(new_data_sources)
    return {"status": "success", "message": "DataSource deleted"}