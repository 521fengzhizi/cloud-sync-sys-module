# 安装指南

## 前置要求

- Python 3.8+
- pip（Python 包管理器）

## 方法 1: 从源代码安装（推荐开发）

```bash
# 克隆仓库
git clone https://github.com/521fengzhizi/cloud-sync-sys-module.git
cd cloud-sync-sys-module

# 进入 python 目录
cd python

# 安装依赖
pip install -r requirements.txt

# 以开发模式安装
pip install -e .
```

## 方法 2: 从 PyPI 安装（简单方式）

```bash
pip install cloud-sync-sys-module
```

## 方法 3: Docker 方式

```bash
# 构建 Docker 镜像
docker build -t cloud-sync-sys-module .

# 运行容器
docker run -it cloud-sync-sys-module python examples/demo_complete.py
```

## 验证安装

运行演示来验证安装成功：

```bash
# 进入 examples 目录
cd examples

# 运行演示
python demo_complete.py
```

你应该看到类似以下输出：

```
======================================================================
  演示1: 基础数据同步
======================================================================

[1] 用户服务创建用户...
    ✓ 用户已创建

[2] 订单服务获取用户数据...
    ✓ 获取用户数据: {'id': '123', 'name': 'Alice', 'email': 'alice@example.com'}
```

## 故障排除

### 导入错误

如果出现 `ModuleNotFoundError: No module named 'cloud_sync_sys'`：

```bash
# 确保已安装
pip install -e .

# 或者设置 PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/python"
```

### 权限错误

如果出现权限错误，使用虚拟环境（推荐）：

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
source venv/bin/activate  # Linux/Mac
# 或
venv\\Scripts\\activate  # Windows

# 安装
pip install -e .
```

### 网络错误（如果使用 JSONBin）

确保：
1. 网络连接正常
2. JSONBin API 可访问
3. API Key 正确

## 下一步

1. ✅ 安装完成后，运行 `python examples/demo_complete.py`
2. 📖 查看 [快速开始指南](docs/quick-start.md)
3. 💡 浏览 [更多示例](examples/)
4. 🚀 准备 [部署到生产环境](docs/deployment.md)
