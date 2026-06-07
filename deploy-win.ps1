# UUMit 金融数据服务 - Windows 一键部署脚本
# 复制整段，粘贴到云服务器 PowerShell 回车即可

$ErrorActionPreference = "Stop"

Write-Host "=== UUMit 金融数据服务部署 ===" -ForegroundColor Cyan

# 1. 安装 Python
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "正在安装 Python 3.12..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.12.8/python-3.12.8-amd64.exe" -OutFile "$env:TEMP\python-installer.exe"
    Start-Process -Wait -FilePath "$env:TEMP\python-installer.exe" -ArgumentList "/quiet","InstallAllUsers=1","PrependPath=1"
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
}
Write-Host "Python: $(python --version 2>&1)" -ForegroundColor Green

# 2. 安装 Git
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "正在安装 Git..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri "https://github.com/git-for-windows/git/releases/download/v2.47.1.windows.1/Git-2.47.1-64-bit.exe" -OutFile "$env:TEMP\git-installer.exe"
    Start-Process -Wait -FilePath "$env:TEMP\git-installer.exe" -ArgumentList "/VERYSILENT","/NORESTART"
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
}
Write-Host "Git: $(git --version 2>&1)" -ForegroundColor Green

# 3. 克隆项目
if (Test-Path "C:\uumit-finance") { Remove-Item -Recurse -Force "C:\uumit-finance" }
Write-Host "正在克隆项目..." -ForegroundColor Yellow
git clone https://github.com/sssshangggg/uumit-finance-api.git C:\uumit-finance
Set-Location C:\uumit-finance\finance-data-service

# 4. 安装依赖
Write-Host "正在安装 Python 依赖..." -ForegroundColor Yellow
python -m pip install -r requirements.txt

# 5. 配置 .env（需要你的 Tushare Token）
Write-Host "请粘贴你的 Tushare Token：" -ForegroundColor Magenta
$token = Read-Host
@"
TUSHARE_TOKEN=$token
SERVER_HOST=0.0.0.0
SERVER_PORT=8800
CACHE_TTL_SECONDS=300
UUMIT_API_BASE=https://api.uumit.com
UUMIT_API_KEY=tmHkMAh5LN1ygSdx05tYVz4qt_grFGuTIn6e3AEBjAtwxwdBQvGHsPjKgMamW9NP
UUMIT_USER_ID=71e2c0fd-f489-476b-b79b-005de54b6ed7
"@ | Out-File -FilePath .env -Encoding utf8

# 6. 启动服务
Write-Host "正在启动服务..." -ForegroundColor Yellow
Start-Process -NoNewWindow -FilePath python -ArgumentList "-m","uvicorn","src.server:app","--host","0.0.0.0","--port","8800"

Start-Sleep -Seconds 3

# 7. 验证
$result = Invoke-RestMethod -Uri "http://localhost:8800/" -TimeoutSec 5
Write-Host "===================================" -ForegroundColor Cyan
Write-Host "部署成功！服务运行中：$($result.status) v$($result.version)" -ForegroundColor Green
Write-Host "本地测试: curl http://localhost:8800/" -ForegroundColor White
Write-Host "外网地址: http://47.98.96.250:8800/" -ForegroundColor Yellow
Write-Host "===================================" -ForegroundColor Cyan
