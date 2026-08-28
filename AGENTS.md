
# Apps 项目工作约定（自动提交 + 推送）

## 提交与推送
每次修改 / 新增 / 删除文件后，**自动执行**：
1. `git add -A`
2. `git commit`（提交信息用中文，简明概括改动）
3. `git push origin main`（GitHub 备份）
4. `git push server main`（触发服务器自动部署：拉取→构建→上线）
