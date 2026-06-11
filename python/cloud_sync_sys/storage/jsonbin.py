"""
JSONBin 存储提供商
"""

import logging
import requests
import json
from typing import Any, Optional
from .base import StorageProvider

logger = logging.getLogger(__name__)


class JSONBinProvider(StorageProvider):
    """JSONBin 存储提供商"""
    
    def __init__(self, jsonbin_id: str, api_key: str, **kwargs):
        """
        初始化 JSONBin 提供商
        
        Args:
            jsonbin_id: JSONBin Bin ID
            api_key: JSONBin API Key
        """
        self.bin_id = jsonbin_id
        self.api_key = api_key
        self.base_url = "https://api.jsonbin.io/v3"
        self.headers = {
            "Content-Type": "application/json",
            "X-Master-Key": api_key
        }
    
    def get(self, key: str, timeout: int = 10) -> Optional[Any]:
        """获取数据"""
        try:
            url = f"{self.base_url}/b/{self.bin_id}/latest"
            response = requests.get(url, headers=self.headers, timeout=timeout)
            response.raise_for_status()
            
            data = response.json().get("record", {})
            value = self._get_nested(data, key)
            
            logger.debug(f"Retrieved key: {key}")
            return value
        
        except Exception as e:
            logger.error(f"Error getting key {key}: {e}")
            return None
    
    def set(self, key: str, value: Any, timeout: int = 10) -> bool:
        """设置数据"""
        try:
            # 获取完整数据
            url = f"{self.base_url}/b/{self.bin_id}/latest"
            response = requests.get(url, headers=self.headers, timeout=timeout)
            response.raise_for_status()
            
            data = response.json().get("record", {})
            self._set_nested(data, key, value)
            
            # 更新
            response = requests.put(
                url,
                headers=self.headers,
                json=data,
                timeout=timeout
            )
            response.raise_for_status()
            
            logger.debug(f"Set key: {key}")
            return True
        
        except Exception as e:
            logger.error(f"Error setting key {key}: {e}")
            return False
    
    def delete(self, key: str, timeout: int = 10) -> bool:
        """删除数据"""
        try:
            url = f"{self.base_url}/b/{self.bin_id}/latest"
            response = requests.get(url, headers=self.headers, timeout=timeout)
            response.raise_for_status()
            
            data = response.json().get("record", {})
            self._delete_nested(data, key)
            
            response = requests.put(
                url,
                headers=self.headers,
                json=data,
                timeout=timeout
            )
            response.raise_for_status()
            
            logger.debug(f"Deleted key: {key}")
            return True
        
        except Exception as e:
            logger.error(f"Error deleting key {key}: {e}")
            return False
    
    def sync(self, timeout: int = 10) -> bool:
        """同步数据"""
        try:
            url = f"{self.base_url}/b/{self.bin_id}/latest"
            response = requests.get(url, headers=self.headers, timeout=timeout)
            response.raise_for_status()
            
            logger.debug("Sync completed")
            return True
        
        except Exception as e:
            logger.error(f"Error syncing: {e}")
            return False
    
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
