# 系统架构设计

## 高级架构

```
┌──────────────────────────────────────────────────────────────┐
│              Cloud Sync System Manager                        │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐           │
│  │  System 1   │  │  System 2   │  │  System N   │           │
│  │  (Service A)│  │  (Service B)│  │  (Service C)│           │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘           │
│         │                 │               │                   │
│         └─────────────────┼───────────────┘                   │
│                           │                                   │
│  ┌────────────────────────┴────────────────────────┐         │
│  │           Sync Engine                          │         │
│  │  ┌──────────────────────────────────────────┐  │         │
│  │  │ Event Bus (pub/sub)                      │  │         │
│  │  └──────────────────────────────────────────┘  │         │
│  │  ┌──────────────────────────────────────────┐  │         │
│  │  │ Data Sync Layer (Queue + Workers)        │  │         │
│  │  └──────────────────────────────────────────┘  │         │
│  │  ┌──────────────────────────────────────────┐  │         │
│  │  │ Cache Manager (Memory + Disk)            │  │         │
│  │  └──────────────────────────────────────────┘  │         │
│  │  ┌──────────────────────────────────────────┐  │         │
│  │  │ Version Control + History                │  │         │
│  │  └──────────────────────────────────────────┘  │         │
│  └────────────────────────────────────────────────┘         │
│                           │                                   │
│  ┌────────────────────────┴────────────────────────┐         │
│  │    Storage Layer                               │         │
│  │  ┌──────────────────────────────────────────┐  │         │
│  │  │ JSONBin / Supabase / Firebase / GitHub  │  │         │
│  │  └──────────────────────────────────────────┘  │         │
│  └─────────────────────────────────────────────────┘         │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

## 数据流

### 写入流程

```
Application → System.set(key, value)
    ↓
Local Memory Cache Update
    ↓
Sync Queue
    ↓
SyncEngine Worker Thread
    ↓
Remote Storage (JSONBin)
    ↓
Notify Subscribers (in same system)
    ↓
Broadcast to Other Systems
```

### 读取流程

```
Application → System.get(key)
    ↓
Check Local Cache
    ├─ Hit → Return Value ✓
    │
    └─ Miss → Query Remote Storage
        ↓
        Fetch from Storage
        ↓
        Update Local Cache
        ↓
        Return Value
```

### 订阅流程

```
System A → System.subscribe(pattern, callback)
    ↓
Register in Subscriptions Map
    ↓
Wait for updates
    ↓
When System B calls set(key, value)
    ↓
Pattern Match Check
    ├─ Match → Call Callback
    │
    └─ No Match → Skip
```

## 核心组件

### 1. System

代表一个微服务单位：
- 命名空间隔离
- 独立数据存储
- 订阅和发布能力
- 版本控制

### 2. CloudSyncSystem

系统协调器：
- 管理多个 System
- 启动/停止生命周期
- 事件分发
- 统计信息收集

### 3. SyncEngine

同步引擎：
- 异步数据同步
- 批量处理
- 缓存管理
- 故障恢复

### 4. EventBus

事件总线：
- Pub/Sub 模式
- 系统间通信
- 事件排队和分发

### 5. StorageProvider

存储抽象：
- 支持多种后端
- 统一接口
- 连接池管理

## 特性详解

### 命名空间隔离

```python
# 不同系统的数据隔离
user_system = System(name="user-svc", namespace="users")
order_system = System(name="order-svc", namespace="orders")

# 即使 key 相同，也在不同的命名空间中
user_system.set("service:config", {"version": "1.0"})
order_system.set("service:config", {"version": "2.0"})
```

### 模式匹配订阅

```python
# 精确匹配
system.subscribe("user:123", callback)

# 通配符匹配
system.subscribe("user:*", callback)          # 所有用户
system.subscribe("*/status", callback)        # 所有状态
system.subscribe("*", callback)               # 所有数据
```

### 版本控制

```python
# 自动保存版本历史（最近 20 个）
system.set("key", "value_v1")
system.set("key", "value_v2")
system.set("key", "value_v3")

# 获取历史
history = system.get_version_history("key")
# [Record(v1), Record(v2), Record(v3)]

# 时间旅行
system.restore_version("key", version=0)
# key 值恢复为 value_v1
```

### 事务支持（后续）

```python
# 原子性操作
with system.transaction():
    system.set("account:123:balance", 1000)
    system.set("account:456:balance", 900)
    # 同时提交或全部回滚
```

## 性能考虑

### 延迟指标

| 操作 | 延迟 |
|------|------|
| 本地写入 | < 1ms |
| 本地读取（缓存命中） | < 1ms |
| 远程写入 | ~100ms |
| 远程读取 | ~100ms |
| 事件分发 | ~10ms |

### 吞吐量

- 单系统: 10,000+ ops/sec
- 多系统: 5,000+ ops/sec per system
- 事件: 100,000+ events/sec

### 可扩展性

- **垂直扩展**: 增加 System 数量（测试过 100+ systems）
- **水平扩展**: 多实例（后续 WebSocket 支持）
- **存储扩展**: 支持多种后端和自定义 Provider

## 容错机制

### 重连策略

```
首次连接失败
    ↓
指数退避重试（1s, 2s, 4s, ...）
    ↓
最大重试 3 次
    ↓
使用本地缓存降级
```

### 数据一致性

- 单点写入一致性
- 最终一致性保证
- 版本号追踪

### 故障恢复

```
检测到连接丢失
    ↓
停止新操作
    ↓
缓存维持本地功能
    ↓
恢复连接后同步
    ↓
合并冲突（最新版本优先）
```

## 安全设计

### 数据隔离

- 命名空间级别隔离
- 系统间权限管理（后续）
- 字段级别加密（后续）

### 传输安全

- HTTPS/TLS 加密（所有存储提供商都支持）
- API Key 认证
- Token 刷新机制

### 审计日志

- 所有操作记录
- 用户追踪
- 变更历史

## 监控和调试

### 系统指标

```python
info = sync_system.get_info()
# {
#   "backend": "jsonbin",
#   "systems_count": 3,
#   "systems": { ... }
# }

stats = sync_system.get_stats()
# {
#   "total_syncs": 1234,
#   "total_events": 5678,
#   "uptime": 3600,
#   ...
# }
```

### 日志输出

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("cloud_sync_sys")
# 启用详细日志
```

## 最佳实践

1. **使用命名空间**: 为每个系统设置明确的命名空间
2. **监听模式**: 使用通配符订阅相关数据
3. **错误处理**: 订阅回调中添加 try-catch
4. **资源清理**: 不再使用时取消订阅
5. **批量操作**: 使用事务或批量 API
6. **缓存策略**: 启用本地缓存以提高性能
7. **版本管理**: 定期检查和清理版本历史
8. **监控告警**: 设置关键指标告警

