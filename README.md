# Cloud Sync System Module 🌐

一个高性能的实时数据同步系统，设计用于支持**N个系统项目**间的实时数据共享与协调。

## 🎯 核心特性

### 📡 实时同步
- ✅ WebSocket 实时推送（<100ms 延迟）
- ✅ 多系统间数据实时共享
- ✅ 事件驱动架构
- ✅ 自动故障转移和重连

### 🏗️ 系统架构
- ✅ 支持10+个系统同时在线
- ✅ 分布式节点部署
- ✅ 系统间独立数据隔离
- ✅ 跨系统权限管理

### 💾 数据存储
- ✅ 多后端支持（JSONBin、Supabase、Firebase）
- ✅ GitHub Pages 静态配置
- ✅ 内存缓存 + 磁盘持久化
- ✅ 数据版本控制

### 🔐 安全特性
- ✅ API Key 认证
- ✅ 系统级访问控制
- ✅ 数据加密传输
- ✅ 操作审计日志

### ⚡ 性能优化
- ✅ 本地缓存优先
- ✅ 智能批量同步
- ✅ 带宽压缩
- ✅ 连接池管理

---

## 🚀 快速开始

### 1. 初始化系统

```python
from cloud_sync_sys import CloudSyncSystem, System

# 创建同步系统
sync_system = CloudSyncSystem(
    backend="jsonbin",  # 或 supabase, firebase, github_pages
    jsonbin_id="YOUR_BIN_ID",
    api_key="YOUR_API_KEY",
    enable_websocket=True
)

# 注册系统
user_system = System(
    name="user-service",
    namespace="users",
    version="1.0.0"
)

auth_system = System(
    name="auth-service",
    namespace="auth",
    version="1.0.0"
)

sync_system.register(user_system)
sync_system.register(auth_system)
```

### 2. 跨系统数据共享

```python
# 在用户服务中设置数据
user_system.set("user:123:profile", {
    "name": "Alice",
    "email": "alice@example.com",
    "created_at": "2024-01-01"
})

# 在认证服务中实时获取用户数据
auth_system.subscribe("user:123:profile", 
    callback=lambda key, value: on_user_updated(value)
)

# 跨系统查询
user_data = auth_system.query("user:123:profile")
```

### 3. 系统间通信

```python
# 发送系统事件
user_system.publish("user:created", {
    "user_id": "123",
    "timestamp": time.time()
})

# 监听其他系统的事件
auth_system.on_event("user:created", 
    callback=lambda event: sync_user_auth(event)
)
```

---

## 📋 系统架构

```
┌─────────────────────────────────────────────────────┐
│         Cloud Sync System Manager                    │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────┐  │
│  │ User System  │  │ Auth System  │  │ Order    │  │
│  │ (users ns)   │  │ (auth ns)    │  │ System   │  │
│  └──────┬───────┘  └──────┬───────┘  └────┬─────┘  │
│         │                 │               │         │
│         └─────────────────┼───────────────┘         │
│                           │                         │
│  ┌────────────────────────┴────────────────────┐   │
│  │    Sync Engine (WebSocket/EventBus)         │   │
│  │  • Real-time push                           │   │
│  │  • Event pub/sub                            │   │
│  │  • Cache management                         │   │
│  └────────────┬─────────────────────────────────┘   │
│               │                                     │
│  ┌────────────┴──────────────────────────────┐    │
│  │   Storage Layer                            │    │
│  │  ├─ JSONBin                                │    │
│  │  ├─ Supabase                               │    │
│  │  ├─ Firebase                               │    │
│  │  └─ GitHub Pages                           │    │
│  └────────────────────────────────────────────┘    │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 💻 核心API

### 系统管理

```python
# 创建同步系统
system = CloudSyncSystem(backend="jsonbin", ...)

# 注册系统
system.register(System(name="service-1", namespace="ns1"))
system.register(System(name="service-2", namespace="ns2"))

# 启动/停止
system.start()
system.stop()

# 获取系统信息
info = system.get_info()
stats = system.get_stats()
```

### 数据操作

```python
# 设置数据
service.set("key", value)

# 获取数据（带缓存优先）
data = service.get("key")

# 删除数据
service.delete("key")

# 批量操作
service.set_batch({
    "key1": value1,
    "key2": value2
})

# 条件查询
results = service.query("user:*", filter={"status": "active"})
```

### 订阅与通知

```python
# 订阅数据变化
subscription = service.subscribe("key", callback)

# 订阅模式匹配
service.subscribe("user:*", on_user_change)

# 取消订阅
service.unsubscribe(subscription)

# 发布事件
service.publish("event:name", {
    "data": "value",
    "timestamp": time.time()
})

# 监听事件
service.on_event("event:name", callback)
```

### 事务与同步

```python
# 事务操作
with service.transaction():
    service.set("key1", value1)
    service.set("key2", value2)
    # 原子性提交

# 手动同步
service.sync()

# 版本控制
service.get_version("key")
service.restore_version("key", version_id)
```

---

## 🔌 集成示例

### Flask 应用集成

```python
from flask import Flask, jsonify
from cloud_sync_sys import CloudSyncSystem, System

app = Flask(__name__)

# 初始化同步系统
sync_system = CloudSyncSystem(backend="jsonbin", ...)
api_system = System(name="api-service", namespace="api")
sync_system.register(api_system)

@app.route("/api/users/<user_id>")
def get_user(user_id):
    # 从同步系统获取数据
    user = api_system.get(f"user:{user_id}")
    return jsonify(user)

@app.route("/api/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.json
    # 更新会自动同步到所有订阅系统
    api_system.set(f"user:{user_id}", data)
    return jsonify({"success": True})
```

### FastAPI 实时更新

```python
from fastapi import FastAPI, WebSocket
from cloud_sync_sys import CloudSyncSystem, System

app = FastAPI()
sync_system = CloudSyncSystem(backend="jsonbin", ...)
web_system = System(name="web-service", namespace="web")
sync_system.register(web_system)

@app.websocket("/ws/sync/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    
    def on_data_change(key, value):
        # 实时推送给前端
        await websocket.send_json({
            "type": "data_update",
            "key": key,
            "value": value
        })
    
    # 订阅所有变化
    web_system.subscribe("*", on_data_change)
    
    while True:
        data = await websocket.receive_json()
        # 处理前端数据
        web_system.set(data["key"], data["value"])
```

### React 前端集成

```javascript
import { useCloudSync } from 'cloud-sync-react';

function UserProfile({ userId }) {
  // Hook 自动处理实时同步
  const { data, set, error, loading } = useCloudSync({
    key: `user:${userId}`,
    provider: 'jsonbin'
  });

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      <h1>{data.name}</h1>
      <input 
        value={data.email}
        onChange={(e) => set({ ...data, email: e.target.value })}
      />
    </div>
  );
}
```

---

## 🎨 使用场景

### 场景1：电商系统架构

```
┌─────────────────────────────────────┐
│    Cloud Sync System               │
├─────────────────────────────────────┤
│                                     │
├─ User Service (用户系统)            │
│  └─ users:* → 用户数据             │
│                                     │
├─ Order Service (订单系统)           │
│  └─ orders:* → 订单数据            │
│  └─ 实时监听 users:* 变化          │
│                                     │
├─ Payment Service (支付系统)         │
│  └─ payments:* → 支付数据          │
│  └─ 监听 orders:* 变化             │
│                                     │
├─ Inventory Service (库存系统)       │
│  └─ inventory:* → 库存数据         │
│  └─ 监听 orders:* 变化             │
│                                     │
└─────────────────────────────────────┘
```

### 场景2：CRM 系统

```python
# 销售系统
sales_system.set("customer:123:deals", [
    {"deal_id": "D001", "value": 10000},
    {"deal_id": "D002", "value": 5000}
])

# 营销系统自动获取
marketing_system.subscribe("customer:*:deals", 
    on_customer_deals_change
)

# 财务系统实时同步
finance_system.on_event("deal:closed", 
    lambda event: record_revenue(event)
)
```

### 场景3：微服务协调

```python
# 服务发现
service_registry.set("service:user-api:health", {
    "status": "healthy",
    "instances": 3,
    "load": 45.2
})

# 其他服务实时获取负载信息
async_service.subscribe("service:*:health", 
    on_service_health_change
)
```

---

## 📊 性能指标

| 指标 | 目标值 | 说明 |
|------|--------|------|
| **消息延迟** | < 100ms | WebSocket 实时推送 |
| **吞吐量** | 10k+ msg/s | 每秒消息数 |
| **系统连接数** | 100+ | 同时在线系统数 |
| **缓存命中率** | > 85% | 本地缓存效率 |
| **可用性** | 99.9% | 系统稳定性 |

---

## 🔧 配置选项

```python
sync_system = CloudSyncSystem(
    # 后端存储
    backend="jsonbin",
    jsonbin_id="YOUR_BIN_ID",
    api_key="YOUR_API_KEY",
    
    # 连接配置
    enable_websocket=True,
    websocket_url="wss://sync.example.com",
    
    # 缓存配置
    cache_enabled=True,
    cache_ttl=3600,
    cache_persist=True,
    
    # 同步配置
    sync_interval=30,
    batch_size=100,
    retry_count=3,
    
    # 监控配置
    enable_metrics=True,
    metrics_port=8000,
    
    # 安全配置
    encryption_enabled=True,
    api_rate_limit=1000  # 每秒请求数
)
```

---

## 📦 项目结构

```
cloud-sync-sys-module/
├── python/
│   ├── cloud_sync_sys/
│   │   ├── __init__.py
│   │   ├── core/
│   │   │   ├── system.py          # 系统核心类
│   │   │   ├── sync_engine.py     # 同步引擎
│   │   │   ├── event_bus.py       # 事件总线
│   │   │   └── cache.py           # 缓存管理
│   │   ├── storage/
│   │   │   ├── base.py
│   │   │   ├── jsonbin.py
│   │   │   ├── supabase.py
│   │   │   └── firebase.py
│   │   ├── network/
│   │   │   ├── websocket.py       # WebSocket 支持
│   │   │   ├── client.py
│   │   │   └── protocol.py
│   │   ├── utils/
│   │   │   ├── encryption.py
│   │   │   ├── compression.py
│   │   │   └── monitoring.py
│   │   └── exceptions.py
│   ├── examples/
│   │   ├── basic_sync.py
│   │   ├── ecommerce_system.py
│   │   ├── crm_system.py
│   │   └── microservice_arch.py
│   ├── tests/
│   ├── setup.py
│   └── requirements.txt
│
├── javascript/
│   ├── src/
│   │   ├── CloudSyncClient.js
│   │   ├── System.js
│   │   ├── SyncEngine.js
│   │   └── hooks/
│   │       └── useCloudSync.js
│   ├── examples/
│   │   ├── react-app/
│   │   └── vue-app/
│   └── package.json
│
├── docs/
│   ├── architecture.md
│   ├── api-reference.md
│   ├── deployment.md
│   ├── cloud-providers.md
│   └── examples.md
│
├── github-pages/
│   ├── index.html              # 系统监控面板
│   ├── dashboard/
│   └── config.json             # GitHub Pages 配置
│
└── README.md
```

---

## 🚀 部署方案

### 方案1：JSONBin + GitHub Pages

```bash
# 最简单、完全免费
# 适合中小型项目（< 100万请求/月）
```

### 方案2：Supabase + GitHub Actions

```bash
# 功能完整、自动部署
# 适合需要实时数据库的项目
```

### 方案3：Docker + Kubernetes

```bash
# 生产级别、高可用
# 适合大型企业应用
```

---

## 📞 获取帮助

- 📖 [完整文档](./docs/)
- 💡 [使用示例](./examples/)
- 🐛 [提交Issue](https://github.com/521fengzhizi/cloud-sync-sys-module/issues)
- 💬 [讨论](https://github.com/521fengzhizi/cloud-sync-sys-module/discussions)

---

**开始构建你的系统协调平台吧！** 🚀
