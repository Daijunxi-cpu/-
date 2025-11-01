#!/bin/bash
# GitHub上传脚本

echo "==================================="
echo "极简时钟 - GitHub上传脚本"
echo "==================================="
echo ""

# 检查是否已配置Git用户信息
if ! git config --global user.name > /dev/null 2>&1; then
    echo "需要配置Git用户信息："
    read -p "请输入你的GitHub用户名: " username
    read -p "请输入你的GitHub邮箱: " email
    git config --global user.name "$username"
    git config --global user.email "$email"
    echo "Git用户信息已配置！"
    echo ""
fi

# 显示当前状态
echo "当前仓库状态："
git status
echo ""

# 添加文件
echo "添加文件到暂存区..."
git add clock.py README.md requirements.txt start.sh config_example.txt .gitignore
echo "文件已添加！"
echo ""

# 提交
echo "提交更改..."
git commit -m "初始提交：极简时钟应用 - 支持时间显示、照片轮播和计时功能"
echo "提交完成！"
echo ""

# 询问是否要推送到GitHub
read -p "是否要推送到GitHub？(y/n): " push_choice

if [ "$push_choice" = "y" ] || [ "$push_choice" = "Y" ]; then
    echo ""
    echo "请先在GitHub上创建新仓库，然后提供以下信息："
    read -p "GitHub用户名: " github_username
    read -p "仓库名称: " repo_name
    
    # 添加远程仓库
    git remote add origin "https://github.com/${github_username}/${repo_name}.git" 2>/dev/null || \
    git remote set-url origin "https://github.com/${github_username}/${repo_name}.git"
    
    # 推送到GitHub
    echo ""
    echo "正在推送到GitHub..."
    git push -u origin master || git push -u origin main
    
    echo ""
    echo "完成！你的代码已上传到："
    echo "https://github.com/${github_username}/${repo_name}"
else
    echo ""
    echo "你可以稍后运行以下命令推送到GitHub："
    echo "git remote add origin https://github.com/你的用户名/仓库名.git"
    echo "git push -u origin master"
fi

