# UUMit Finance Data API — 一键部署+上架
# 用法: .\deploy-and-register.ps1
# 前置: ngrok 已安装并配置好 authtoken

$ErrorActionPreference = "Stop"
$ROOT = Split-Path -Parent $MyInvocation.MyCommand.Path
$SRV_DIR = Join-Path $ROOT "finance-data-service"
$PORT = 8800

Write-Host "=== UUMit 金融数据API 一键部署 ===" -ForegroundColor Cyan

# 1. 启动 FastAPI 服务
Write-Host "[1/4] 启动 API 服务器..." -ForegroundColor Yellow
$proc = Start-Process -FilePath "python" `
    -ArgumentList "-m","uvicorn","src.server:app","--host","0.0.0.0","--port","$PORT","--log-level","warning" `
    -WorkingDirectory $SRV_DIR `
    -NoNewWindow `
    -PassThru
Start-Sleep -Seconds 3

# 验证服务
try {
    $r = Invoke-WebRequest -Uri "http://localhost:$PORT/" -TimeoutSec 5 -UseBasicParsing
    Write-Host "  Server OK: $($r.Content)" -ForegroundColor Green
} catch {
    Write-Host "  Server FAILED to start" -ForegroundColor Red
    exit 1
}

# 2. 启动 ngrok
Write-Host "[2/4] 启动 ngrok 隧道..." -ForegroundColor Yellow
$ngrok = Start-Process -FilePath "ngrok" `
    -ArgumentList "http","$PORT","--log=stdout" `
    -NoNewWindow `
    -PassThru
Start-Sleep -Seconds 3

# 获取 ngrok 公网 URL
try {
    $ngrokApi = Invoke-WebRequest -Uri "http://127.0.0.1:4040/api/tunnels" -TimeoutSec 5 -UseBasicParsing
    $tunnels = $ngrokApi.Content | ConvertFrom-Json
    $publicUrl = $tunnels.tunnels[0].public_url
    Write-Host "  Ngrok URL: $publicUrl" -ForegroundColor Green
} catch {
    Write-Host "  Ngrok FAILED — 检查 ngrok 是否已安装并登录" -ForegroundColor Red
    Stop-Process -Id $proc.Id -Force
    exit 1
}

# 3. 更新 skills.json 的 base_url
Write-Host "[3/4] 更新 skills.json..." -ForegroundColor Yellow
$skillsPath = Join-Path $SRV_DIR "uumit\skills.json"
$skills = Get-Content $skillsPath -Raw -Encoding UTF8 | ConvertFrom-Json
$skills.base_url = $publicUrl
$skills | ConvertTo-Json -Depth 10 | Out-File $skillsPath -Encoding UTF8
Write-Host "  base_url -> $publicUrl" -ForegroundColor Green

# 4. 上架 API 到 UUMit 数据广场
Write-Host "[4/4] 上架 API 到 UUMit 数据广场..." -ForegroundColor Yellow
Push-Location $SRV_DIR
try {
    python uumit/register.py 2>&1 | ForEach-Object { Write-Host "  $_" }
} finally {
    Pop-Location
}

Write-Host ""
Write-Host "=== 部署完成 ===" -ForegroundColor Cyan
Write-Host "  服务地址: $publicUrl" -ForegroundColor Green
Write-Host "  API 文档: $publicUrl/docs" -ForegroundColor Green
Write-Host "  进程 ID:  server=$($proc.Id)  ngrok=$($ngrok.Id)" -ForegroundColor Gray
Write-Host ""
Write-Host "  停止服务: Stop-Process -Id $($proc.Id),$($ngrok.Id)" -ForegroundColor Gray
