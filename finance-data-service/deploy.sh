#!/bin/bash
# VPS 一键部署脚本
# 使用方法: bash deploy.sh

set -e

echo "=== UUMit 金融数据服务部署 ==="

# 检查 Docker
if ! command -v docker &> /dev/null; then
    echo "安装 Docker..."
    curl -fsSL https://get.docker.com | sh
fi

# 检查 .env
if [ ! -f .env ]; then
    echo "请先创建 .env 文件（参考 .env.example）"
    exit 1
fi

if grep -q "your_tushare_token_here" .env 2>/dev/null || grep -q "^TUSHARE_TOKEN=$" .env; then
    echo "错误: 请在 .env 中填入 Tushare Token"
    echo "注册获取: https://tushare.pro/register"
    exit 1
fi

# 构建并启动
docker compose up -d --build

# 等待服务启动
echo "等待服务启动..."
sleep 3

# 验证
if curl -s http://localhost:443/ | grep -q "ok"; then
    echo ""
    echo "部署成功！"
    echo "API 文档: http://$(curl -s ifconfig.me):443/docs"
    echo "健康检查: http://$(curl -s ifconfig.me):443/"
else
    echo "服务可能未正常启动，请检查日志: docker compose logs"
fi
