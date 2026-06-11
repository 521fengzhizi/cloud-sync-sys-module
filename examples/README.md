# 示例代码

## 快速开始

### 1. 直接运行完整演示（无需任何配置！）

```bash
cd examples
python demo_complete.py
```

这个演示包括：
- ✅ 基础数据同步
- ✅ 数据变化订阅
- ✅ 事件驱动架构
- ✅ 数据查询
- ✅ 版本控制
- ✅ 多系统协调

### 2. 运行实际的 JSONBin 集成示例

首先获取 JSONBin 凭证：

1. 访问 https://jsonbin.io
2. 注册账户
3. 创建新 Bin
4. 复制 Bin ID 和 Master Key

然后修改 `demo_jsonbin.py` 中的配置：

```python
sync_system = CloudSyncSystem(
    backend="jsonbin",
    jsonbin_id="YOUR_BIN_ID",        # 替换为你的 Bin ID
    api_key="YOUR_MASTER_KEY"        # 替换为你的 Master Key
)
```

运行：

```bash
python demo_jsonbin.py
```

## 代码结构

```
examples/
├── demo_complete.py          # 完整演示（模拟存储，无需配置）
├── demo_jsonbin.py           # JSONBin 后端演示
├── ecommerce_system.py       # 电商系统示例
├── crm_system.py             # CRM 系统示例
├── microservice_architecture.py  # 微服务架构示例
└── README.md
```

## 推荐学习顺序

1. **demo_complete.py** - 了解核心概念
2. **demo_jsonbin.py** - 实际集成外部存储
3. **ecommerce_system.py** - 学习真实应用
4. **microservice_architecture.py** - 深入了解架构
5. **crm_system.py** - 学习高级特性

## 常见问题

### 如何在我的项目中使用？

```python
from cloud_sync_sys import CloudSyncSystem, System

# 初始化
sync_system = CloudSyncSystem(backend="mock")  # 或 "jsonbin"
system = System(name="my-service", namespace="my-ns")
sync_system.register(system)
sync_system.start()

# 使用
system.set("key", value)
data = system.get("key")
```

### 如何与 Flask 集成？

查看 `ecommerce_system.py` 中的 Flask 示例。

### 如何处理错误？

```python
try:
    system.set("key", value)
except Exception as e:
    logger.error(f"操作失败: {e}")
```

## 更多信息

- 📖 [完整文档](../docs/)
- 🚀 [部署指南](../docs/deployment.md)
- 💡 [API 参考](../docs/api-reference.md)
