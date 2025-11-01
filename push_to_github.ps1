# GitHub上传脚本 (PowerShell版本)

Write-Host "===================================" -ForegroundColor Cyan
Write-Host "极简时钟 - GitHub上传脚本" -ForegroundColor Cyan
Write-Host "===================================" -ForegroundColor Cyan
Write-Host ""

# 检查是否已配置Git用户信息
$userName = git config --global user.name 2>$null
$userEmail = git config --global user.email 2>$null

if (-not $userName -or -not $userEmail) {
    Write-Host "需要配置Git用户信息：" -ForegroundColor Yellow
    $inputName = Read-Host "请输入你的GitHub用户名"
    $inputEmail = Read-Host "请输入你的GitHub邮箱"
    git config --global user.name $inputName
    git config --global user.email $inputEmail
    Write-Host "Git用户信息已配置！" -ForegroundColor Green
    Write-Host ""
}

# 显示当前状态
Write-Host "当前仓库状态：" -ForegroundColor Cyan
git status
Write-Host ""

# 添加文件
Write-Host "添加文件到暂存区..." -ForegroundColor Cyan
git add clock.py README.md requirements.txt start.sh config_example.txt .gitignore
Write-Host "文件已添加！" -ForegroundColor Green
Write-Host ""

# 提交
Write-Host "提交更改..." -ForegroundColor Cyan
git commit -m "初始提交：极简时钟应用 - 支持时间显示、照片轮播和计时功能"
Write-Host "提交完成！" -ForegroundColor Green
Write-Host ""

# 询问是否要推送到GitHub
$pushChoice = Read-Host "是否要推送到GitHub？(y/n)"

if ($pushChoice -eq "y" -or $pushChoice -eq "Y") {
    Write-Host ""
    Write-Host "请先在GitHub上创建新仓库，然后提供以下信息：" -ForegroundColor Yellow
    $githubUsername = Read-Host "GitHub用户名"
    $repoName = Read-Host "仓库名称"
    
    # 添加远程仓库
    $remoteExists = git remote get-url origin 2>$null
    if ($remoteExists) {
        git remote set-url origin "https://github.com/${githubUsername}/${repoName}.git"
    } else {
        git remote add origin "https://github.com/${githubUsername}/${repoName}.git"
    }
    
    # 推送到GitHub
    Write-Host ""
    Write-Host "正在推送到GitHub..." -ForegroundColor Cyan
    git push -u origin master 2>$null
    if ($LASTEXITCODE -ne 0) {
        git push -u origin main
    }
    
    Write-Host ""
    Write-Host "完成！你的代码已上传到：" -ForegroundColor Green
    Write-Host "https://github.com/${githubUsername}/${repoName}" -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "你可以稍后运行以下命令推送到GitHub：" -ForegroundColor Yellow
    Write-Host "git remote add origin https://github.com/你的用户名/仓库名.git" -ForegroundColor White
    Write-Host "git push -u origin master" -ForegroundColor White
}

