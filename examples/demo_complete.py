#!/usr/bin/env python3
"""
Cloud Sync System Module - 完整可运行演示

无需任何外部配置，直接运行即可看到效果！

Usage:
    python demo_complete.py
"""

import sys
import time
import logging
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent / "python"))

from cloud_sync_sys import CloudSyncSystem, System

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def print_section(title):
    """打印分隔符"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def demo_1_basic_sync():
    """演示1: 基础数据同步"""
    print_section("演示1: 基础数据同步")
    
    # 创建同步系统（使用模拟存储，无需配置）
    sync_system = CloudSyncSystem(
        backend="mock"
    )
    
    # 创建两个系统
    user_system = System(name="user-service", namespace="users")
    order_system = System(name="order-service", namespace="orders")
    
    # 注册系统
    sync_system.register(user_system)
    sync_system.register(order_system)
    
    # 启动
    sync_system.start()
    
    try:
        print("[1] 用户服务创建用户...")
        user_system.set("user:123", {
            "id": "123",
            "name": "Alice",
            "email": "alice@example.com"
        })
        print("    ✓ 用户已创建")
        
        print("\n[2] 订单服务获取用户数据...")
        user_data = order_system.get("users:user:123")
        print(f"    ✓ 获取用户数据: {user_data}")
        
        print("\n[3] 用户服务更新用户...")
        user_system.set("user:123", {
            "id": "123",
            "name": "Alice Johnson",
            "email": "alice.johnson@example.com"
        })
        print("    ✓ 用户已更新")
        
        print("\n[4] 订单服务再次获取用户数据...")
        user_data = order_system.get("users:user:123")
        print(f"    ✓ 更新后的用户数据: {user_data}")
        
    finally:
        sync_system.stop()


def demo_2_subscription():
    """演示2: 数据变化订阅"""
    print_section("演示2: 数据变化订阅")
    
    sync_system = CloudSyncSystem(backend="mock")
    
    user_system = System(name="user-service", namespace="users")
    notify_system = System(name="notification-service", namespace="notify")
    
    sync_system.register(user_system)
    sync_system.register(notify_system)
    sync_system.start()
    
    try:
        # 记录回调次数
        callback_count = {"count": 0}
        
        print("[1] 通知服务订阅用户数据变化...")
        def on_user_change(key, value):
            callback_count["count"] += 1
            print(f"    📬 收到通知 #{callback_count['count']}: {key} = {value['name']}")
        
        subscription = notify_system.subscribe("users:user:*", on_user_change)
        print("    ✓ 已订阅")
        
        print("\n[2] 用户服务创建第一个用户...")
        user_system.set("user:101", {"id": "101", "name": "Bob"})
        time.sleep(0.1)
        
        print("\n[3] 用户服务创建第二个用户...")
        user_system.set("user:102", {"id": "102", "name": "Charlie"})
        time.sleep(0.1)
        
        print("\n[4] 用户服务更新用户...")
        user_system.set("user:101", {"id": "101", "name": "Bob Smith"})
        time.sleep(0.1)
        
        print(f"\n    总共收到 {callback_count['count']} 个通知 ✓")
        
    finally:
        sync_system.stop()


def demo_3_event_driven():
    """演示3: 事件驱动架构"""
    print_section("演示3: 事件驱动架构")
    
    sync_system = CloudSyncSystem(backend="mock")
    
    user_system = System(name="user-service", namespace="users")
    email_system = System(name="email-service", namespace="email")
    payment_system = System(name="payment-service", namespace="payment")
    
    sync_system.register(user_system)
    sync_system.register(email_system)
    sync_system.register(payment_system)
    sync_system.start()
    
    try:
        print("[1] 邮件服务监听 'user:created' 事件...")
        def on_user_created(event):
            user_data = event
            print(f"    📧 邮件服务: 发送欢迎邮件到 {user_data['email']}")
        
        email_system.on_event("user:created", on_user_created)
        print("    ✓ 已监听")
        
        print("\n[2] 支付服务监听 'user:created' 事件...")
        def on_user_created_payment(event):
            user_data = event
            print(f"    💳 支付服务: 初始化 {user_data['name']} 的账户")
        
        payment_system.on_event("user:created", on_user_created_payment)
        print("    ✓ 已监听")
        
        print("\n[3] 用户服务发布 'user:created' 事件...")
        user_system.publish("user:created", {
            "user_id": "123",
            "name": "David",
            "email": "david@example.com"
        })
        time.sleep(0.2)
        print("    ✓ 事件已发布")
        
    finally:
        sync_system.stop()


def demo_4_query():
    """演示4: 数据查询和过滤"""
    print_section("演示4: 数据查询和过滤")
    
    sync_system = CloudSyncSystem(backend="mock")
    user_system = System(name="user-service", namespace="users")
    
    sync_system.register(user_system)
    sync_system.start()
    
    try:
        print("[1] 创建用户...")
        users = [
            ("user:101", {"id": "101", "name": "Alice", "status": "active"}),
            ("user:102", {"id": "102", "name": "Bob", "status": "inactive"}),
            ("user:103", {"id": "103", "name": "Charlie", "status": "active"}),
            ("user:104", {"id": "104", "name": "David", "status": "active"}),
        ]
        
        for key, data in users:
            user_system.set(key, data)
            print(f"    ✓ 创建 {data['name']}")
        
        print("\n[2] 查询所有用户...")
        all_users = user_system.query("user:*")
        print(f"    ✓ 找到 {len(all_users)} 个用户")
        for key, data in all_users.items():
            print(f"      - {data['name']} ({data['status']})")
        
        print("\n[3] 查询活跃用户 (status=active)...")
        active_users = user_system.query(
            "user:*",
            filter_fn=lambda v: v.get("status") == "active"
        )
        print(f"    ✓ 找到 {len(active_users)} 个活跃用户")
        for key, data in active_users.items():
            print(f"      - {data['name']}")
        
    finally:
        sync_system.stop()


def demo_5_version_control():
    """演示5: 版本控制"""
    print_section("演示5: 版本控制")
    
    sync_system = CloudSyncSystem(backend="mock")
    config_system = System(name="config-service", namespace="config")
    
    sync_system.register(config_system)
    sync_system.start()
    
    try:
        print("[1] 创建配置版本...")
        config_system.set("app:version", "1.0.0")
        print("    ✓ 版本 1.0.0")
        
        config_system.set("app:version", "1.0.1")
        print("    ✓ 版本 1.0.1")
        
        config_system.set("app:version", "1.0.2")
        print("    ✓ 版本 1.0.2")
        
        print("\n[2] 获取版本历史...")
        history = config_system.get_version_history("app:version")
        print(f"    ✓ 共 {len(history)} 个版本")
        for i, record in enumerate(history):
            print(f"      版本 {i}: {record.value} (时间戳: {record.timestamp:.2f})")
        
        print("\n[3] 获取当前版本...")
        current = config_system.get("app:version")
        print(f"    ✓ 当前版本: {current}")
        
        print("\n[4] 恢复到版本 1...")
        config_system.restore_version("app:version", 1)
        restored = config_system.get("app:version")
        print(f"    ✓ 恢复后的版本: {restored}")
        
    finally:
        sync_system.stop()


def demo_6_multi_system():
    """演示6: 多系统协调"""
    print_section("演示6: 多系统协调 (电商系统)")
    
    sync_system = CloudSyncSystem(backend="mock")
    
    # 创建5个系统
    user_svc = System(name="user-service", namespace="users")
    product_svc = System(name="product-service", namespace="products")
    order_svc = System(name="order-service", namespace="orders")
    payment_svc = System(name="payment-service", namespace="payments")
    inventory_svc = System(name="inventory-service", namespace="inventory")
    
    for svc in [user_svc, product_svc, order_svc, payment_svc, inventory_svc]:
        sync_system.register(svc)
    
    sync_system.start()
    
    try:
        print("[1] 产品服务添加商品...")
        product_svc.set("product:P001", {
            "id": "P001",
            "name": "笔记本电脑",
            "price": 5999.99,
            "stock": 100
        })
        print("    ✓ 已添加商品")
        
        print("\n[2] 库存服务监听产品库存变化...")
        def on_product_change(key, value):
            print(f"    📦 库存服务: 产品 {value['name']} 库存更新为 {value['stock']}")
        
        inventory_svc.subscribe("products:product:*", on_product_change)
        print("    ✓ 已监听")
        
        print("\n[3] 用户服务创建用户...")
        user_svc.set("user:U001", {
            "id": "U001",
            "name": "张三",
            "email": "zhangsan@example.com"
        })
        print("    ✓ 用户已创建")
        
        print("\n[4] 订单服务下单...")
        order_svc.set("order:O001", {
            "id": "O001",
            "user_id": "U001",
            "product_id": "P001",
            "quantity": 2,
            "status": "pending"
        })
        print("    ✓ 订单已创建")
        
        print("\n[5] 支付服务监听订单事件...")
        def on_order_created(event):
            print(f"    💳 支付服务: 处理订单 {event['id']} 的支付")
        
        payment_svc.on_event("order:created", on_order_created)
        print("    ✓ 已监听")
        
        print("\n[6] 订单服务发布订单创建事件...")
        order_svc.publish("order:created", {
            "id": "O001",
            "user_id": "U001",
            "total": 11999.98
        })
        time.sleep(0.1)
        print("    ✓ 事件已发布")
        
        print("\n[7] 检查系统状态...")
        info = sync_system.get_info()
        print(f"    ✓ 运行中的系统: {info['systems_count']} 个")
        for name, stats in info['systems'].items():
            print(f"      - {name}: {stats['data_count']} 条数据")
        
    finally:
        sync_system.stop()


def main():
    """主程序"""
    print("\n" + "#" * 70)
    print("#" + " " * 68 + "#")
    print("#  Cloud Sync System Module - 完整可运行演示" + " " * 24 + "#")
    print("#" + " " * 68 + "#")
    print("#" * 70)
    
    try:
        # 运行所有演示
        demo_1_basic_sync()
        demo_2_subscription()
        demo_3_event_driven()
        demo_4_query()
        demo_5_version_control()
        demo_6_multi_system()
        
        # 总结
        print_section("✅ 演示完成！")
        print("""
完成的演示包括：

  1️⃣  基础数据同步 - 跨系统数据共享
  2️⃣  数据变化订阅 - 实时通知机制
  3️⃣  事件驱动架构 - 系统间通信
  4️⃣  数据查询和过滤 - 灵活的数据查询
  5️⃣  版本控制 - 数据版本管理
  6️⃣  多系统协调 - 完整的电商系统演示

下一步：

  📖 查看完整文档: docs/
  💡 查看更多示例: examples/
  🚀 部署到生产环境: docs/deployment.md

""")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  演示被中断")
    except Exception as e:
        logger.error(f"演示失败: {e}", exc_info=True)
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
