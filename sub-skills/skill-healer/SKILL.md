---
name: skill-healer
description: "技能自愈系统。触发词：'自愈'、'skill-healer'、'检查失败'、'修复技能'、'自我修复'。失败日志 -> 阈值检测 -> 补丁生成 -> 影子验证 -> 自动部署。已实现完整 Python CLI。"
metadata:
  copaw:
    emoji: "🩹"
  skill_version: "2.0.0"
  author: "CoPaw Community"
  parent: skill-manager
  source: "customized"
  trigger_words:
    - 自愈
    - skill-healer
    - 检查失败
    - 修复技能
    - 自我修复
    - healer
---

# 🩹 Skill Healer — 技能自愈系统

> **版本**: v2.0.0 | **状态**: 已实现 ✅
>
> 被动触发式自愈：失败日志 → 阈值检测 → 补丁生成 → 影子验证 → 部署决策

---

## 这是什么

Skill Healer 是一个被动触发（失败后触发）的自愈系统。当技能/工具执行失败时，记录失败日志，达到阈值后自动生成补丁、验证并部署修复。

**不是主动扫描器** — 它只会在失败发生后被动响应。

---

## 架构

```
失败发生 → log_failure() → 写入 failure_log.json
                              ↓
                          check_threshold() → 未触发 → 结束
                              ↓ 触发
                          generate_patch() → 写入 healer_patches.json
                              ↓
                          shadow_execute() → 影子验证
                              ↓
                          deploy_patch() → 部署/推送审核
```

---

## 文件路径

| 文件 | 路径 |
|------|------|
| 可执行脚本 | `skills/skill-manager/sub-skills/skill-healer/healer.py` |
| 失败日志数据 | `memory/failure_log.json` |
| 补丁记录数据 | `memory/healer_patches.json` |

---

## CLI 命令参考

所有命令通过 `healer.py` 执行，工作目录为项目根目录。

### 记录失败

```bash
python skills/skill-manager/sub-skills/skill-healer/healer.py log-failure \
    --skill <技能名> \
    --error-type <错误类型> \
    --error-msg "<错误消息>" \
    --root-cause <根因分类> \
    --context "<发生场景>" \
    [--confidence 0.7]
```

**参数说明**:

| 参数 | 必填 | 说明 |
|------|------|------|
| `--skill` | ✅ | 技能名称，如 graphify / wechat-draft |
| `--error-type` | ✅ | 错误类型: tool_failure / dependency_missing / api_error / timeout / permission |
| `--error-msg` | ✅ | 错误描述，最多 200 字 |
| `--root-cause` | ✅ | 根因分类（见下方） |
| `--context` | ✅ | 发生上下文，便于溯源 |
| `--confidence` | ❌ | 置信度 0-1，默认 0.7 |

**根因分类参考**:

| 根因 | 适用场景 |
|------|----------|
| `api_timeout` | API 请求超时 |
| `dep_not_installed` | 依赖包未安装 |
| `token_expired` | Token 过期 |
| `path_not_found` | 路径不存在 |
| `permission_denied` | 权限拒绝 |
| `connection_refused` | 连接被拒绝 |
| `memory_miss` | 记忆遗漏 |
| `wrong_skill` | 技能误触发 |
| `api_incompatible` | API 不兼容 |
| `config_missing` | 配置缺失 |

### 检查阈值

```bash
python skills/skill-manager/sub-skills/skill-healer/healer.py check
```

触发条件（方案C）:

| 条件 | 阈值 |
|------|------|
| 同技能同错误类型 | >= 2 次 |
| 同根因错误 | >= 3 次 |

### 一键自愈

```bash
python skills/skill-manager/sub-skills/skill-healer/healer.py auto-heal
```

执行完整流程：检查阈值 → 生成补丁 → 影子验证 → 部署决策。

### 生成报告

```bash
python skills/skill-manager/sub-skills/skill-healer/healer.py report
```

输出：总览统计、根因分布、技能分布、最近补丁。

### 查看记录

```bash
# 列出最近失败记录
python skills/skill-manager/sub-skills/skill-healer/healer.py list-failures

# 列出补丁记录
python skills/skill-manager/sub-skills/skill-healer/healer.py list-patches
```

### 高级操作

```bash
# 为指定触发项生成补丁
python skills/skill-manager/sub-skills/skill-healer/healer.py generate-patch \
    --key "graphify::dependency_missing" --type skill_error

# 影子验证补丁
python skills/skill-manager/sub-skills/skill-healer/healer.py shadow-execute \
    --patch-id <uuid>

# 部署补丁
python skills/skill-manager/sub-skills/skill-healer/healer.py deploy-patch \
    --patch-id <uuid>

# 强制部署（跳过规则检查）
python skills/skill-manager/sub-skills/skill-healer/healer.py deploy-patch \
    --patch-id <uuid> --force
```

---

## Python API 参考

healer.py 的所有核心函数也可作为 Python 模块导入使用：

```python
import sys
sys.path.insert(0, "skills/skill-manager/sub-skills/skill-healer")
from healer import log_failure, check_threshold, auto_heal, generate_report

# 记录失败
entry = log_failure(
    skill="graphify",
    error_type="dependency_missing",
    error_msg="graphifyy not installed",
    root_cause="dep_not_installed",
    context="extract phase",
    confidence=0.8
)

# 检查阈值
triggered = check_threshold()

# 一键自愈
result = auto_heal()

# 生成报告
print(generate_report())
```

---

## 部署决策策略

| 置信度 | 影子验证 | 动作 |
|--------|----------|------|
| >= 0.8 | pass | 直接部署 (`deployed`) |
| 0.5 - 0.8 | pass | 部署并通知 (`deployed_notified`) |
| < 0.5 或 fail | 任意 | 推送用户审核 (`pending_review`) |

---

## 使用场景

### 场景1：工具调用失败后记录

当某个工具调用失败时，Agent 应主动调用 log_failure 记录：

```python
# 在 except 块中
healer.log_failure(
    skill="graphify",
    error_type="tool_failure",
    error_msg=str(e),
    root_cause="dep_not_installed",
    context="graphify extract"
)
```

### 场景2：手动触发自愈

当用户说"检查一下最近的失败"或"自愈检查"时：

```bash
cd {workspace}
python skills/skill-manager/sub-skills/skill-healer/healer.py auto-heal
```

### 场景3：查看自愈历史

```bash
python skills/skill-manager/sub-skills/skill-healer/healer.py report
```

---

## 与 graphify 依赖自愈的联动

graphify 使用 **主动依赖自愈**（运行前检查），skill-healer 使用 **被动故障自愈**（失败后修复）。两者互补：

```
主动（graphify check_deps.py）: 运行前检查 → 缺啥装啥 → 预防失败
被动（skill-healer）: 失败后记录 → 阈值触发 → 修复 → 防止再犯
```

当 graphify 的 check_deps.py 修复失败时，会通过 `log_failure()` 将失败记录给 skill-healer。

---

## 注意事项

1. **不主动扫描** — skill-healer 只在失败写入后被动检测
2. **补丁建议是文本修复方向** — 实际代码修改需要 Agent 或用户执行
3. **数据文件自动创建** — `memory/failure_log.json` 和 `memory/healer_patches.json` 在首次使用时自动初始化
4. **GBK 兼容** — Windows 环境下自动切换 stdout 编码为 UTF-8
5. **补丁可追溯** — 每次补丁有唯一 ID，可查询、可回滚

---

*Skill Healer v2.0.0 | 🩹 已实现 | CLI + Python API | 联动 graphify 依赖自愈 | 2026-05-08*
