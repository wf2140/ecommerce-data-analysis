# Git 常用指令大全

> 按使用频率标注：⭐⭐⭐（必须掌握）、⭐⭐（常用）、⭐（了解）

---

## 📚 目录

1. [基础操作](#基础操作)
2. [日常开发流程](#日常开发流程)
3. [分支管理](#分支管理)
4. [撤销操作](#撤销操作)
5. [查看操作](#查看操作)
6. [远程操作](#远程操作)
7. [配置管理](#配置管理)
8. [高级操作](#高级操作)

---

## 🔰 基础操作

### 初始化仓库 ⭐⭐⭐
```bash
git init                    # 初始化本地仓库
git clone <url>             # 克隆远程仓库
```

### 配置用户信息 ⭐⭐⭐
```bash
# 局部配置（当前项目专用）
git config user.name "zz77"
git config user.email "2786018700@qq.com"

# 全局配置（所有项目默认）
git config --global user.name "你的名字"
git config --global user.email "你的邮箱@example.com"

# 查看配置
git config user.name
git config user.email
git config --list           # 查看所有配置
git config --list --show-origin  # 查看配置文件位置
```

### 查看状态 ⭐⭐⭐
```bash
git status                  # 查看工作区状态
git status -s               # 简洁格式
git status -b               # 显示分支信息
```

---

## 🚀 日常开发流程

### 提交流程 ⭐⭐⭐
```bash
# 1. 查看修改
git status

# 2. 查看具体修改内容
git diff                    # 工作区 vs 暂存区
git diff --staged           # 暂存区 vs 上次提交

# 3. 添加文件到暂存区
git add .                   # 添加所有文件
git add file.py             # 添加指定文件
git add folder/             # 添加文件夹
git add -u                  # 添加所有已跟踪文件的修改

# 4. 提交
git commit -m "描述"        # 提交并描述
git commit -am "描述"       # 添加并提交（已跟踪文件）
git commit --amend          # 修改最后一次提交

# 5. 查看提交历史
git log
git log --oneline           # 简洁格式
```

### 清除暂存区 ⭐⭐
```bash
git reset HEAD <file>       # 清除指定文件的暂存
git reset HEAD              # 清除所有文件的暂存
git restore --staged <file> # 更推荐的方式
```

---

## 🌿 分支管理

### 创建和切换 ⭐⭐⭐
```bash
git branch                  # 查看本地分支
git branch -r               # 查看远程分支
git branch -a               # 查看所有分支
git branch <name>           # 创建分支
git checkout <name>         # 切换分支
git checkout -b <name>      # 创建并切换分支
git switch <name>           # 切换分支（新命令）
git switch -c <name>        # 创建并切换分支（新命令）
```

### 删除分支 ⭐⭐
```bash
git branch -d <name>        # 删除已合并分支
git branch -D <name>        # 强制删除分支
git push origin --delete <name>  # 删除远程分支
```

### 合并分支 ⭐⭐⭐
```bash
git merge <name>            # 合并分支到当前分支
git merge --no-ff <name>    # 合并并保留分支历史
git rebase <name>           # 变基（将当前分支重放）
```

### 查看分支差异 ⭐
```bash
git diff branch1 branch2    # 比较两个分支
git log branch1..branch2    # 查看分支间的提交
```

---

## ↩️ 撤销操作

### 撤销工作区修改 ⭐⭐⭐
```bash
git restore <file>          # 撤销工作区修改
git checkout -- <file>      # 旧版命令
```

### 撤销暂存区修改 ⭐⭐⭐
```bash
git restore --staged <file> # 撤销暂存区修改
git reset HEAD <file>       # 旧版命令
```

### 撤销提交 ⭐⭐
```bash
git reset --soft HEAD~1     # 撤销提交，保留修改在暂存区
git reset --mixed HEAD~1    # 撤销提交，保留修改在工作区（默认）
git reset --hard HEAD~1     # 撤销提交，丢弃所有修改
git reset --hard <commit>   # 回退到指定提交
```

### 恢复已删除文件 ⭐
```bash
git checkout HEAD~1 -- <file>  # 从上一次提交恢复
git reflog                  # 查看所有操作记录
git reset --hard <commit>   # 恢复到指定提交
```

---

## 👁️ 查看操作

### 查看历史 ⭐⭐⭐
```bash
git log                     # 查看详细历史
git log --oneline           # 简洁格式
git log --graph             # 图形化显示
git log --all               # 查看所有分支历史
git log -3                  # 查看最近3次提交
git log --author="zz77"     # 按作者筛选
git log --grep="bug"        # 按提交信息筛选
```

### 查看提交详情 ⭐⭐
```bash
git show <commit>           # 查看提交详情
git show HEAD               # 查看最新提交
git show HEAD~1:file.py     # 查看某次提交的文件内容
```

### 查看差异 ⭐⭐⭐
```bash
git diff                    # 工作区 vs 暂存区
git diff --staged           # 暂存区 vs 上次提交
git diff HEAD               # 工作区 vs 上次提交
git diff <commit1> <commit2> # 比较两次提交
git diff branch1 branch2    # 比较两个分支
```

### 查看文件历史 ⭐
```bash
git log --follow file.py    # 查看文件完整历史（包括重命名）
git blame file.py           # 查看每行代码是谁写的
```

---

## 🌐 远程操作

### 关联远程仓库 ⭐⭐⭐
```bash
git remote                  # 查看远程仓库
git remote -v               # 查看远程仓库（带URL）
git remote add origin <url> # 添加远程仓库
git remote remove origin    # 删除远程仓库
git remote set-url origin <url>  # 修改远程仓库URL
```

### 推送和拉取 ⭐⭐⭐
```bash
git push origin main        # 推送到远程
git push -u origin main     # 推送并设置上游分支
git push origin --all       # 推送所有分支
git push origin --tags      # 推送所有标签

git pull origin main        # 拉取远程代码
git pull --rebase origin main  # 拉取并变基
git fetch origin            # 获取远程更新（不合并）
git fetch --all             # 获取所有远程更新
```

### 同步远程分支 ⭐⭐
```bash
git branch --set-upstream-to=origin/main main  # 关联远程分支
git branch -u origin/main    # 简写
```

---

## ⚙️ 配置管理

### 常用配置 ⭐⭐
```bash
# 设置默认分支名
git config --global init.defaultBranch main

# 设置默认编辑器
git config --global core.editor notepad

# 设置换行符处理（Windows推荐）
git config --global core.autocrlf true

# 开启颜色输出
git config --global color.ui true

# 设置别名
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
```

### 查看配置 ⭐⭐
```bash
git config --list           # 查看所有配置
git config --list --show-origin  # 查看配置文件位置
git config --global --list  # 查看全局配置
```

### 删除配置 ⭐
```bash
git config --unset user.name
git config --global --unset user.name
```

---

## 🎯 高级操作

### 暂存工作区 ⭐⭐
```bash
git stash                   # 暂存当前修改
git stash save "描述"       # 暂存并添加描述
git stash list              # 查看暂存列表
git stash apply             # 恢复暂存（不删除）
git stash pop               # 恢复暂存（删除）
git stash drop              # 删除暂存
git stash clear             # 清空所有暂存
```

### 标签管理 ⭐
```bash
git tag                     # 查看所有标签
git tag v1.0.0              # 创建标签
git tag -a v1.0.0 -m "描述" # 创建带注释的标签
git tag -d v1.0.0           # 删除本地标签
git push origin v1.0.0      # 推送标签到远程
git push origin --tags      # 推送所有标签
```

### 变基操作 ⭐
```bash
git rebase main             # 将当前分支变基到main
git rebase -i HEAD~3        # 交互式变基（修改最近3次提交）
git rebase --continue       # 继续变基
git rebase --abort          # 放弃变基
```

### 查找提交 ⭐
```bash
git log --grep="关键词"     # 按提交信息搜索
git log --author="作者"     # 按作者搜索
git log --since="2024-01-01"  # 按时间搜索
git log --until="2024-12-31"
git log --all --full-history -- file.py  # 查找文件的所有历史
```

### 清理操作 ⭐
```bash
git clean -f                # 删除未跟踪文件
git clean -fd               # 删除未跟踪文件和目录
git gc                      # 垃圾回收，优化仓库
git prune                   # 清理不可达对象
```

---

## 📊 提交信息规范

### Conventional Commits 格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type 类型

| 类型 | 说明 | 示例 |
|------|------|------|
| `feat` | 新功能 | `feat: 添加用户登录功能` |
| `fix` | 修复bug | `fix: 修复登录超时问题` |
| `refactor` | 重构代码 | `refactor: 优化数据库连接` |
| `docs` | 文档更新 | `docs: 更新API文档` |
| `style` | 代码格式 | `style: 统一代码缩进` |
| `test` | 测试相关 | `test: 添加单元测试` |
| `chore` | 构建/工具 | `chore: 更新依赖版本` |
| `perf` | 性能优化 | `perf: 优化查询性能` |

### 示例

```bash
git commit -m "feat: 添加数据验证功能

- 添加输入验证逻辑
- 优化错误提示信息
- 添加单元测试

Closes #123"
```

---

## 🔥 常见问题处理

### 解决合并冲突 ⭐⭐⭐
```bash
# 1. 拉取时发现冲突
git pull origin main

# 2. 手动解决冲突文件
# 编辑冲突文件，保留需要的代码

# 3. 标记冲突已解决
git add 冲突文件.py

# 4. 继续合并
git commit -m "merge: 解决合并冲突"
```

### 忘记忽略文件 ⭐⭐
```bash
# 1. 从暂存区移除（保留本地文件）
git rm --cached .env
git commit -m "chore: 移除.env文件"

# 2. 在.gitignore中添加
echo ".env" >> .gitignore
git add .gitignore
git commit -m "chore: 更新.gitignore"
```

### 修改提交信息 ⭐⭐
```bash
# 修改最后一次提交信息
git commit --amend -m "正确的提交信息"

# 注意：如果已经push到远程，不要使用此命令
```

### 回滚到指定提交 ⭐⭐
```bash
# 查看历史
git log --oneline

# 回滚（保留历史）
git revert <commit>

# 回滚（丢弃历史，危险！）
git reset --hard <commit>
```

---

## 📋 快速参考

### 日常工作流程 ⭐⭐⭐
```bash
# 开始工作
git checkout -b feature/新功能

# 开发中
git status
git add .
git commit -m "feat: 完成第一步"

# 继续开发
git status
git add .
git commit -m "feat: 完成第二步"

# 完成开发
git checkout main
git merge feature/新功能
git push origin main

# 删除分支
git branch -d feature/新功能
```

### 常用组合命令 ⭐⭐
```bash
# 查看简洁状态
git status -sb

# 查看图形化历史
git log --graph --oneline --all

# 查看文件差异
git diff --stat

# 查看最近5次提交
git log -5 --oneline

# 撤销所有修改
git restore .
git restore --staged .
```

---

## 💡 使用建议

1. **小而频繁的提交** - 每完成一个小功能就提交
2. **清晰的提交信息** - 让别人能看懂你做了什么
3. **提交前检查** - 确保没有垃圾文件
4. **及时同步** - 每天开始工作前先拉取最新代码
5. **分支开发** - 不要在主分支上直接开发
6. **使用.gitignore** - 忽略不需要追踪的文件

---

**最后更新**: 2026-03-04
**适用版本**: Git 2.51.0+