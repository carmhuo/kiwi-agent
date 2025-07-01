import uuid
from abc import ABC, abstractmethod


class Cache(ABC):
    """
    Define the interface for a cache that can be used to store data in a Flask app.
    """

    @abstractmethod
    def generate_id(self, *args, **kwargs):
        """
        Generate a unique ID for the cache.
        """
        pass

    @abstractmethod
    def get(self, id, field):
        """
        Get a value from the cache.
        """
        pass

    @abstractmethod
    def get_all(self, field_list) -> list:
        """
        Get all values from the cache.
        """
        pass

    @abstractmethod
    def set(self, id, field, value):
        """
        Set a value in the cache.
        """
        pass

    @abstractmethod
    def delete(self, id):
        """
        Delete a value from the cache.
        """
        pass


class MemoryCache(Cache):
    def __init__(self):
        self.cache = {}

    def generate_id(self, *args, **kwargs):
        return str(uuid.uuid4())

    def set(self, id, field, value):
        if id not in self.cache:
            self.cache[id] = {}

        self.cache[id][field] = value

    def get(self, id, field):
        if id not in self.cache:
            return None

        if field not in self.cache[id]:
            return None

        return self.cache[id][field]

    def get_all(self, field_list) -> list:
        return [
            {"id": id, **{field: self.get(id=id, field=field) for field in field_list}}
            for id in self.cache
        ]

    def delete(self, id):
        if id in self.cache:
            del self.cache[id]


from fastapi import HTTPException, Request, status
from functools import wraps
from typing import List, Optional


class CacheManager:
    """
    Examples：
    cache_manager = CacheManager()
    @cache_manager.requires_cache(
        required_fields=["name", "email"],
        optional_fields=["avatar_url"])
    async def user_profile(
        request: Request,
        id: str,
        name: str,
        email: str,
        avatar_url: Optional[str] = None
    ):
        return {
            "id": id,
            "name": name,
            "email": email,
            "avatar": avatar_url
        }
    """

    def __init__(self, cache: Cache = None):
        if cache is None:
            self.cache = MemoryCache()
        self.cache = cache

    def requires_cache(
            self,
            required_fields: List[str],
            optional_fields: Optional[List[str]] = None
    ):
        optional_fields = optional_fields or []

        def decorator(f):
            @wraps(f)
            async def decorated(request: Request, *args, **kwargs):
                # 1. 获取 ID（支持查询参数和请求体）
                id = request.query_params.get("id")

                if not id:
                    try:
                        json_data = await request.json()
                        id = json_data.get("id")
                    except Exception as e:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid request body"
                        )

                if not id:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="ID is required"
                    )

                # 2. 检查必需字段
                missing_fields = []
                for field in required_fields:
                    if self.cache.get(id, field) is None:
                        missing_fields.append(field)

                if missing_fields:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Missing required fields: {', '.join(missing_fields)}"
                    )

                # 3. 收集字段值
                field_values = {"id": id}
                for field in required_fields + optional_fields:
                    field_values[field] = self.cache.get(id, field)

                # 4. 调用原始函数
                try:
                    # 保留原始参数结构
                    return await f(request, *args, **kwargs, **field_values)
                except TypeError:
                    # 如果函数不接受额外参数，尝试直接调用
                    return await f(request, *args, **kwargs)

            return decorated

        return decorator