# 快速开始

## 前置要求

- Python 3.8+
- JSONBin 账户（或其他云存储服务）

## 安��

### 方法1: 从源代码安装

```bash
cd python
pip install -r requirements.txt
pip install -e .
```

### 方法2: 从 PyPI 安装（后续支持）

```bash
pip install cloud-sync-sys-module
```

## 5 分钟快速开始

### 1. 获取 JSONBin 凭证

访问 [JSONBin.io](https://jsonbin.io)，创建账户并获取：
- `Bin ID`
- `Master Key`

### 2. 创建你的第一个同步系统

```python
from cloud_sync_sys import CloudSyncSystem, System

# 创建同步系统
sync_system = CloudSyncSystem(
    backend="jsonbin",
    jsonbin_id="YOUR_BIN_ID",
    api_key="YOUR_MASTER_KEY"
)

# 注册用户服务
user_service = System(name="user-service", namespace="users")
sync_system.register(user_service)

# 注册订单服务
order_service = System(name="order-service", namespace="orders")
sync_system.register(order_service)

# 启动系统
sync_system.start()

# 在用户服务中创建用户
user_service.set("user:123", {
    "id": "123",
    "name": "Alice",
    "email": "alice@example.com"
})

# 在订单服务中获取用户数据
user_data = order_service.get("users:user:123")
print(user_data)

# 停止系统
sync_system.stop()
```

## 核心概念

### System（系统）

每个 System 代表一个微服务或子系统：

```python
# 创建系统
user_system = System(
    name="user-service",      # 系统唯一标识
    namespace="users",         # 数据命名空间
    version="1.0.0"           # 版本号
)
```

### 数据操作

```python
# 设置数据
system.set("user:123", {"name": "Alice"})

# 获取数据
user = system.get("user:123")

# 删除数据
system.delete("user:123")

# 批量查询
all_users = system.query("user:*")

# 条件查询
active_users = system.query(
    "user:*",
    filter_fn=lambda v: v.get("status") == "active"
)
```

### 订阅（实时同步）

```python
# 订阅单个键
subscription = system.subscribe("user:123", 
    callback=lambda key, value: print(f"{key} changed to {value}")
)

# 订阅模式（通配符）
system.subscribe("user:*",
    callback=lambda key, value: on_any_user_change(key, value)
)

# 取消订阅
system.unsubscribe(subscription)
```

### 事件驱动

```python
# 发布事件
user_system.publish("user:created", {
    "user_id": "123",
    "timestamp": time.time()
})

# 监听事件
order_system.on_event("user:created",
    callback=lambda event: on_new_user(event)
)
```

### 版本控制

```python
# 获取版本历史
history = system.get_version_history("config:app")
for i, record in enumerate(history):
    print(f"Version {i}: {record.value}")

# 恢复到特定版本
system.restore_version("config:app", version=1)
```

## 常见使用场景

### 场景 1: 电商系统

```python
sync_system = CloudSyncSystem(
    backend="jsonbin",
    jsonbin_id="YOUR_BIN_ID",
    api_key="YOUR_API_KEY"
)

# 各个微服务
user_svc = System(name="user", namespace="users")
product_svc = System(name="product", namespace="products")
order_svc = System(name="order", namespace="orders")
payment_svc = System(name="payment", namespace="payments")

sync_system.register(user_svc)
sync_system.register(product_svc)
sync_system.register(order_svc)
sync_system.register(payment_svc)

sync_system.start()

# 用户创建订单时，订单服务发布事件
order_svc.publish("order:created", {"order_id": "001", "user_id": "123"})

# 支付服务监听订单事件
payment_svc.on_event("order:created", 
    callback=lambda event: process_payment(event)
)
```

### 场景 2: CRM 系统

```python
# 销售系统保存交易
sales_svc.set("customer:123:deals", [
    {"deal_id": "D001", "value": 10000},
    {"deal_id": "D002", "value": 5000}
])

# 营销系统自动获取客户信息
marketing_svc.subscribe("customer:*:deals",
    callback=lambda key, deals: send_campaign(key, deals)
)
```

### 场景 3: 实时通知

```python
# 系统 A 更新状态
system_a.set("status:processing", {"job_id": "123", "progress": 50})

# 系统 B 实时监听
system_b.subscribe("status:*",
    callback=lambda key, value: update_ui(key, value)
)
```

## 配置选项

```python
sync_system = CloudSyncSystem(
    backend="jsonbin",
    jsonbin_id="YOUR_BIN_ID",
    api_key="YOUR_API_KEY",
    
    # 同步配置
    sync_interval=30,        # 同步间隔（秒）
    
    # WebSocket 配置（后续支持）
    enable_websocket=False,
    websocket_url="wss://sync.example.com",
    
    # 缓存配置（后续支持）
    cache_enabled=True,
    cache_ttl=3600,
    
    # 监控配置（后续支持）
    enable_metrics=False,
)
```

## 获取帮助

- 📚 查看 [完整 API 文档](../docs/api-reference.md)
- 💡 查看 [更多示例](../examples/)
- 🐛 [提交 Issue](https://github.com/521fengzhizi/cloud-sync-sys-module/issues)

## 下一步

1. ✅ 完成了基础设置？→ 查看 [高级用法](./advanced.md)
2. 🔌 想要集成到 Flask/FastAPI？ → 查看 [框架集成指南](./framework-integration.md)
3. 📊 需要监控和统计？ → 查看 [监控指南](./monitoring.md)
4. 🚀 准备生产部署？ → 查看 [部署指南](./deployment.md)
