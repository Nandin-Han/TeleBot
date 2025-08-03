# execute_project_command 函数实现说明

## 功能概述
`execute_project_command` 函数现在已经实现了实际的项目部署命令执行逻辑，支持演示环境的完整部署流程。

## 实现的功能

### 1. 参数验证
- **Tag验证**: 确保tag不为空且格式正确（v主版本.次版本.修订版本）
- **环境验证**: 确保environment参数存在
- **完整性检查**: 所有必要参数都经过验证

### 2. 演示环境部署流程（environment == "pre"）

#### 步骤1: 脚本同步
```bash
cd /opt/infra-deploy/
rsync -av --delete ./scripts/ deployer@172.31.40.106:/home/deployer/scripts/
```
- **功能**: 将本地脚本同步到远程服务器
- **参数说明**:
  - `-av`: 归档模式，保持文件属性
  - `--delete`: 删除远程目录中本地不存在的文件
- **超时设置**: 60秒
- **错误处理**: 失败时记录错误并返回False

#### 步骤2: 远程部署执行
```bash
ssh deployer@172.31.40.106 "bash /home/deployer/scripts/pre/{project_name}.sh {action_type} {tag}"
```
- **功能**: 在远程服务器执行具体的部署脚本
- **参数传递**: 
  - `project_name`: 项目名称（如 pd-admin）
  - `action_type`: 操作类型（update 或 rollback）
  - `tag`: 版本标签（如 v1.1.23）
- **超时设置**: 5分钟（300秒）
- **输出记录**: 成功时记录stdout，失败时记录stderr

### 3. 生产环境处理（environment == "prod"）
- **当前状态**: 预留接口，暂未实现
- **返回值**: False
- **日志记录**: 警告信息提示功能未实现

### 4. 错误处理机制

#### 超时处理
- **rsync超时**: 60秒
- **ssh部署超时**: 5分钟
- **异常捕获**: `subprocess.TimeoutExpired`

#### 异常处理
- **格式验证失败**: tag格式不正确
- **命令执行失败**: subprocess返回非零退出码
- **未知环境**: 不支持的environment值
- **通用异常**: 其他未预期的错误

## 日志记录

### 信息级别日志
- 命令开始执行
- rsync命令详情
- ssh命令详情
- 成功执行的输出

### 错误级别日志
- 参数验证失败
- 命令执行失败
- 超时异常
- 未知错误

## 使用示例

### 成功的调用示例
```python
success = await execute_project_command(
    project_name="pd-admin",
    action_type="update", 
    tag="v1.2.3",
    environment="pre"
)
# 返回: True (成功)
```

### 实际执行的命令序列
1. `cd /opt/infra-deploy/ && rsync -av --delete ./scripts/ deployer@172.31.40.106:/home/deployer/scripts/`
2. `ssh deployer@172.31.40.106 "bash /home/deployer/scripts/pre/pd-admin.sh update v1.2.3"`

## 安全考虑

### 命令注入防护
- 使用subprocess.run而不是os.system
- tag参数经过格式验证
- 固定的命令模板，减少注入风险

### 网络安全
- SSH连接使用key-based认证（假设已配置）
- 超时设置防止长时间占用资源

## 扩展计划

### 生产环境实现
- 需要添加生产环境的具体命令逻辑
- 可能需要额外的安全检查和确认步骤
- 建议添加回滚机制

### 功能增强
- 支持更多的action_type（如restart、status）
- 添加命令执行进度回调
- 支持批量项目操作

## 错误码说明
- `True`: 执行成功
- `False`: 执行失败（具体原因见日志）

## 依赖要求
- 本地需要安装rsync
- 远程服务器SSH访问权限
- 远程服务器上存在相应的部署脚本

## 测试建议
1. 验证rsync命令是否正确同步文件
2. 确认SSH连接和权限配置
3. 测试各种tag格式的验证
4. 验证超时机制是否正常工作
5. 测试错误情况的处理
