---
name: skill-editor
description: "编辑/修改 CoPaw 技能。触发词：'修改技能'、'编辑技能'、'改进技能'、'更新技能'、'调整技能'。"
metadata:
  copaw:
    emoji: "✏️"
  skill_version: "2.0.0"
  author: "CoPaw Community"
---

# ✏️ Skill Editor - 编辑/修改 CoPaw 技能

## 五阶段流程（含EvoForge优化）

```
定位技能 → 修改评估 → 确认策略 → 执行修改 → EvoForge 优化
```

---

## 阶段一：定位技能

### 确定目标

| 用户输入 | 目标 |
|----------|------|
| "修改 xxx 技能" | 指定技能 |
| "编辑 skill-name" | 指定技能 |
| "改进触发词" | 当前/指定技能 |

### 定位路径

```bash
# 检查工作区
ls /app/working/workspaces/default/skills/<skill>/

# 检查全局池
ls /app/working/skill_pool/<skill>/

# 读取内容
read_file("/app/working/workspaces/default/skills/<skill>/SKILL.md")
```

---

## 阶段二：修改评估 ⚡

### 评估维度

| 维度 | 权重 | 评估标准 |
|------|------|----------|
| **修改类型** | 40% | 触发词/描述/流程/结构 |
| **修改范围** | 30% | 小改/中改/大改 |
| **风险等级** | 30% | 影响其他功能？ |

### 修改类型分类

| 类型 | 描述 | 风险 |
|------|------|------|
| **触发词调整** | 修改 description 中的触发词 | 低 |
| **描述优化** | 优化 description 内容 | 低 |
| **流程微调** | 修改个别步骤 | 中 |
| **结构重构** | 调整目录/文件结构 | 高 |
| **功能增删** | 添加/删除核心功能 | 高 |

### 修改范围评估

| 范围 | 行数变化 | 执行策略 |
|------|----------|----------|
| **小改** | ±10% 以内 | 直接修改 |
| **中改** | ±10-50% | 备份后修改 |
| **大改** | ±50% 以上 | 分步修改 + 确认 |

### 评估输出

```
📋 **修改评估**

**目标技能**：skill-name
**当前规模**：XX 行

**修改类型**：触发词 / 描述 / 流程 / 结构
**修改范围**：小 / 中 / 大（±XX%）
**风险等级**：🟢 LOW / 🟡 MEDIUM / 🔴 HIGH

**评估结论**：✅ 可修改 / ❌ 建议重构

**修改建议**：
- [具体建议]
```

---

## 阶段三：确认策略

### 低风险修改（小改）

直接执行，修改后汇报。

### 中风险修改（中改）

```
⚠️ **确认修改**

修改内容：
- [修改点1]
- [修改点2]

将备份原文件到：`/tmp/skill_backup/<skill>/`

确认请回复：确认 / 取消
```

### 高风险修改（大改/结构）

```
⚠️ **重大修改确认**

⚠️ 这是一次较大修改，建议：
1. 先评测当前技能质量
2. 考虑是否更适合"融合"或"重构"

当前状态：
- 现有行数：XXX 行
- 预估修改后：XXX 行

建议选项：
1. [继续修改] - 分步执行
2. [评测后优化] - 先走 skill-reviewer
3. [重构创建] - 删除重建

确认请回复：1 / 2 / 3 / 取消
```

---

## 阶段四：执行修改

### 修改前备份

```bash
# 备份原技能
mkdir -p /tmp/skill_backup/<skill>/
cp -r /app/working/workspaces/default/skills/<skill>/ /tmp/skill_backup/<skill>/
```

### 执行修改

使用 `edit_file` 进行精准修改：

```python
# 修改指定内容
edit_file(
    file_path="skills/<skill>/SKILL.md",
    old_text="旧内容",
    new_text="新内容"
)
```

### 修改后验证

```
✅ **修改完成**

**技能**：skill-name
**修改类型**：触发词优化
**备份位置**：`/tmp/skill_backup/<skill>/`

**验证**：
- [x] 文件可读
- [x] 格式正确
- [x] 内容符合预期
```

---

## 阶段五：EvoForge优化（必须）

> ⚠️ 修改完成后必须调用 EvoForge 优化

```bash
chat_with_agent(to_agent="evo-forge", text="优化 skills/<skill>")
```

### 优化内容

| 维度 | 检查点 |
|------|--------|
| **代码质量** | 冗余、重复、结构 |
| **触发词** | 覆盖度、精确度 |
| **流程** | 逻辑、完整性 |
| **格式** | YAML、Markdown 规范 |

### 优化输出

```
🧬 **Darwin 优化完成**

**优化项**：
- [x] 冗余代码清理
- [x] 触发词增强
- [x] 流程结构优化
- [x] 格式规范化

**优化建议**：如需人工介入，列出待确认项
```

---

## 常见修改场景

### 1. 修改触发词

```python
# 找到 description
old = '触发词："创建技能"、"写个skill"'
new = '触发词："创建技能"、"写个skill"、"做个新技能"'

edit_file(old_text=old, new_text=new)
```

### 2. 修改描述

```python
# 优化 description
old = '用途：xxx。'
new = '用途：xxx。不做：xxx。'
```

### 3. 调整流程

```python
# 修改步骤
old = '## 步骤一：xxx\n## 步骤二：yyy'
new = '## 阶段一：xxx\n## 阶段二：yyy\n## 阶段三：zzz'
```

---

## 安全约束

1. **备份优先**：所有修改前先备份
2. **精准修改**：使用 `edit_file`，避免全文件覆盖
3. **格式校验**：修改后检查 YAML frontmatter 完整性
4. **功能验证**：修改后确认原有功能不受影响

---

## 📂 路径参考

| 类型 | 路径 |
|------|------|
| 工作区技能 | `/app/working/workspaces/default/skills/` |
| 全局技能池 | `/app/working/skill_pool/` |
| 备份目录 | `/tmp/skill_backup/` |

---

## 🔗 相关技能

| 技能 | 用途 |
|------|------|
| `skill-creator` | 创建新技能 |
| `skill-reviewer` | 评测技能 |
| `skill-merger` | 融合技能 |
| `evo-forge` | EvoForge优化 |
