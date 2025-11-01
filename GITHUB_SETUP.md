# 上传到GitHub指南

## 步骤1：配置Git用户信息（如果还没有配置）

```bash
git config --global user.name "你的GitHub用户名"
git config --global user.email "你的GitHub邮箱"
```

## 步骤2：在GitHub上创建新仓库

1. 登录 GitHub
2. 点击右上角的 "+" 号，选择 "New repository"
3. 输入仓库名称（例如：`simple-clock` 或 `极简时钟`）
4. 选择 Public 或 Private
5. **不要**初始化 README、.gitignore 或 license（因为我们已经有了）
6. 点击 "Create repository"

## 步骤3：连接到GitHub仓库并推送

在项目目录下运行以下命令（将 `你的用户名` 和 `仓库名` 替换为实际值）：

```bash
# 添加远程仓库
git remote add origin https://github.com/你的用户名/仓库名.git

# 推送代码
git push -u origin master
```

或者如果使用 main 分支：

```bash
git branch -M main
git push -u origin main
```

## 快速命令集合

```bash
# 1. 配置Git（只需运行一次）
git config --global user.name "你的用户名"
git config --global user.email "你的邮箱"

# 2. 初始化仓库（已完成）
git init

# 3. 添加文件（已完成）
git add clock.py README.md requirements.txt start.sh config_example.txt .gitignore

# 4. 提交
git commit -m "初始提交：极简时钟应用"

# 5. 添加远程仓库并推送
git remote add origin https://github.com/你的用户名/仓库名.git
git push -u origin master
```

## 注意事项

- 照片目录（`photos/`）已被 `.gitignore` 忽略，不会被上传
- 如果你还没有GitHub账户，请先到 [github.com](https://github.com) 注册
- 如果提示需要身份验证，可以使用 Personal Access Token 或 SSH 密钥

