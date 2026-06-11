"""
Cloud Sync System Module - 安装配置
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="cloud-sync-sys-module",
    version="1.0.0",
    author="521fengzhizi",
    description="N个系统项目间的实时数据同步和协调模块",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/521fengzhizi/cloud-sync-sys-module",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8+",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.28.0"
    ],
)
