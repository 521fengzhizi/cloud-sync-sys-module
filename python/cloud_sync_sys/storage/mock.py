"""
模拟存储提供商 - 无需外部依赖，可直接运行
"""

import logging
import json
from typing import Any, Optional
from .base import StorageProvider

logger = logging.getLogger(__name__)


class MockStorageProvider(StorageProvider):
    """模拟存储提供商 - 用于演示和测试"""
    
    def __init__(self, **kwargs):
        """初始化模拟存储"""
        self.data = {}
        logger.info("MockStorageProvider initialized")
    
    def get(self, key: str, timeout: int = 10) -> Optional[Any]:
        """获取数据"""
        try:
            value = self._get_nested(self.data, key)
            logger.debug(f"Retrieved key: {key}")
            return value
        except Exception as e:
            logger.error(f"Error getting key {key}: {e}")
            return None
    
    def set(self, key: str, value: Any, timeout: int = 10) -> bool:
        """设置数据"""
        try:
            self._set_nested(self.data, key, value)
            logger.debug(f"Set key: {key}")
            return True
        except Exception as e:
            logger.error(f"Error setting key {key}: {e}")
            return False
    
    def delete(self, key: str, timeout: int = 10) -> bool:
        """删除数据"""
        try:
            self._delete_nested(self.data, key)
            logger.debug(f"Deleted key: {key}")
            return True
        except Exception as e:
            logger.error(f"Error deleting key {key}: {e}")
            return False
    
    def sync(self, timeout: int = 10) -> bool:
        """同步数据"""
        logger.debug("Sync completed")
        return True
    
    @staticmethod
    def _get_nested(data: dict, key: str) -> Optional[Any]:
        """获取嵌套数据"""
        keys = key.split(":")
        current = data
        
        for k in keys:
            if isinstance(current, dict):
                current = current.get(k)
            else:
                return None
        
        return current
    
    @staticmethod
    def _set_nested(data: dict, key: str, value: Any):
        """设置嵌套数据"""
        keys = key.split(":")
        current = data
        
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        
        current[keys[-1]] = value
    
    @staticmethod
    def _delete_nested(data: dict, key: str):
        """删除嵌套数据"""
        keys = key.split(":")
        current = data
        
        for k in keys[:-1]:
            if k in current:
                current = current[k]
            else:
                return
        
        if isinstance(current, dict) and keys[-1] in current:
            del current[keys[-1]]
    
    def get_all_data(self):
        """获取所有数据（仅用于调试）"""
        return json.dumps(self.data, indent=2, ensure_ascii=False)
