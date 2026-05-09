---
name: skill-merger
description: "融合技能：将功能重叠或互补的技能合并生成新技能。四阶段流程：扫描分析 → 适合性评估 → 规模决策 → 确认执行。融合后自动标识来源技能。"
metadata:
  copaw:
    emoji: "🔀"
  skill_version: "2.6.0-copaw"
  author: "CoPaw adapted"
  merged_from: []  # 融合来源标记（执行时自动填充）
---

# 技能融合器

将功能重叠或互补的技能融合，智能选择融合策略。

---

## ⚡ 检查点 (Checkpoint)

| CP | 检查项 | 验证方法 | 失败处理 |
|----|--------|----------|----------|
| **CP1** | 技能存在 | 读取SKILL.md成功 | 提示文件路径错误 |
| **CP2** | 适合性评估通过 | 用户确认融合方案 | 跳过融合，终止 |
| **CP3** | 融合后完整性 | 完整性≥80% | 回滚融合 |

---

## 🎯 杀手用法

| 场景 | 指令 | 效果 |
|------|------|------|
| 精准融合 | "融合A和B" | 直接评估这两个技能 |
| 批量整理 | "整理技能" | 全局扫描，找出候选组 |
| 分层设计 | "融合A和B，分层设计" | 强制使用分层策略 |
| 版本跟踪 | "检查融合版本" | 查看所有融合技能的版本状态 |

---

## 🔄 生命周期管理

> 📡 **[来自: skill-manager]**

### 融合生命周期

```
扫描分析 → 适合性评估 → 规模决策 → 确认执行 → 版本跟踪 → 更新检测
```

### 版本跟踪

每个融合技能记录：
- `metadata.merged_from`: 被融合的技能名列表
- `metadata.merged_from_details`: 被融合技能的详细信息
- `metadata.merged_version`: 融合版本号
- `metadata.merged_date`: 融合日期

### 更新检测

当被融合的源技能更新时：
1. 检测源技能版本变化
2. 评估是否需要重新融合
3. 提示用户是否更新

---

## 触发词

"融合技能"、"合并技能"、"整理技能"、"融合XXX和XXX"、"清理重复"、"技能去重"、"技能太多了"、"检查融合版本"

## 四阶段流程

```
扫描分析 → 适合性评估 → 规模决策 → 确认执行
```

---

## 阶段一：扫描分析

### 扫描路径

- `/app/working/skill_pool/` — 全局技能池
- `/app/working/workspaces/default/skills/` — 工作区技能

### 提取信息

每个技能提取：
- `name`（技能名）
- `description`（描述）
- `metadata`（版本、触发词）
- 正文行数
- 目录结构（scripts/、references/、prompts/）

### 功能分类

| 类别 | 关键词 |
|------|--------|
| 文档处理 | Word、docx、pdf、xlsx、Excel、pptx、PPT |
| 搜索 | 搜索、联网、news、爬虫 |
| 系统 | cron、定时、环境变量、容器 |
| AI/设计 | 设计、UI、UX、brainstorm、创意 |
| 文件 | 上传、下载、整理、文件 |
| 邮件 | 邮件、smtp、发送 |
| 浏览器 | 浏览器、browser、抓取 |
| 其他 | 均不匹配 |

---

## 阶段二：适合性评估 ⚡

### 评估维度

| 维度 | 权重 | 评估标准 |
|------|------|----------|
| 功能重叠度 | 40% | description 关键词重叠 ≥ 30% |
| 触发词互补 | 30% | 触发词有明显差异，可互补 |
| 用户意图 | 30% | 用户明确指定的技能对 |

### 适合融合判定

**适合融合 ✅**（满足以下任一条件）：
- 同类技能描述重叠 ≥ 40%
- 用户明确指定要融合的两个技能
- 功能互补且总触发词 ≤ 3 个

**不适合融合 ❌**（满足以下任一条件）：
- 功能完全无关（分类不同，关键词重叠 < 20%）
- 技能已过于精简（正文 < 50 行），融合收益低
- 技能已过于复杂（正文 > 2000 行），融合风险高

### 输出评估结论

```
📋 **融合适合性评估**

**技能对**：skill-A + skill-B
**功能分类**：同属 [文档处理类]
**功能重叠度**：XX%
**触发词重叠**：XX%（有互补）
**评估结论**：✅ 适合融合 / ❌ 不适合融合

**理由**：
- [具体理由1]
- [具体理由2]

📌 **融合后来源标识**：
- 融合后将在 metadata.merged_from 中记录：[skill-a, skill-b]
- 融合后将在 SKILL.md 正文标注 "融合自 skill-a + skill-b"
```

---

## 阶段三：规模决策 ⚡

### 规模评估标准

| 规模 | 条件 | 推荐策略 |
|------|------|----------|
| **小规模** | 总正文行数 ≤ 500 行 | **直接融合**：简单合并 |
| **中规模** | 总正文行数 500-1500 行 | **直接融合+结构优化** |
| **大规模** | 总正文行数 1500-3000 行 | **分层设计**：父技能+子技能 |
| **超大规模** | 总正文行数 > 3000 行 | **架构重组**：拆分为多个独立子技能 |

### 分层设计方案（大规模用）

**父技能** = 协调层
- 只做判断分发（检测意图 → 调用对应子技能）
- 包含公共 prompt（决策逻辑）
- 行数控制在 100-200 行

**子技能** = 执行层
- 每个子技能专注单一功能
- 保留原技能的完整实现
- 可独立使用或被父技能调用

### ⭐ 子技能使用引导模板（分层设计必须包含）

> **重要**：分层设计的父技能必须包含子技能使用引导，否则调度器无法正确调用子技能。

**父技能必须包含以下内容**：

```markdown
## 🔗 子技能调度规则

> ⚠️ **核心规则**：父技能是调度器，子技能是执行器。父技能负责识别意图+调度，子技能负责具体执行。

### 调度逻辑

```
用户输入 → 父技能识别意图 → 路由到子技能 → 子技能执行 → 返回结果
```

### 意图识别表

| 用户意图 | 触发词 | 路由到 | 说明 |
|----------|--------|--------|------|
| 功能A | "xxx" / "yyy" | child-skill-a | 功能A的执行 |
| 功能B | "zzz" / "www" | child-skill-b | 功能B的执行 |

### 子技能调用说明

| 子技能 | 职责 | 流程 |
|--------|------|------|
| child-skill-a | 功能A的执行 | Phase 0→1→2→3 |
| child-skill-b | 功能B的执行 | Phase 0→1→2→3 |

### 子技能联动规则

#### 规则1: 子技能优化时自动检查子技能

当child-skill-a优化一个技能时，自动检查该技能是否有子技能：
- 有 → 提示用户是否一起优化
- 无 → 正常优化

#### 规则2: 子技能共享网络调研

父技能的网络调研结果可以被子技能使用：
- 有调研结果 → 询问是否使用
- 无 → 子技能独立优化
```

**子技能使用引导检查清单**：

- [ ] 父技能包含 `## 🔗 子技能调度规则` 章节
- [ ] 包含调度逻辑流程图
- [ ] 包含意图识别表（用户意图→触发词→路由到→说明）
- [ ] 包含子技能调用说明（子技能→职责→流程）
- [ ] 包含子技能联动规则（如需要）

### 策略确认输出

```
📊 **规模评估**

**技能A**：XX 行
**技能B**：XX 行
**总计**：XX 行
**评估规模**：小/中/大/超大规模

🎯 **推荐策略**：直接融合 / 分层设计

📌 **融合后标识预览**：
- 新技能 `metadata.merged_from`: [skill-a, skill-b]
- SKILL.md 将标注 "融合自 skill-a + skill-b"

**融合后结构预览**：
[直接融合] 新技能 = [A内容] + [B独有内容]
[分层设计] 父技能 → 子技能A + 子技能B
```

---

## 阶段四：确认执行

### 🔄 融合验证循环（来自refactoring-patterns）

> 📡 **[来自: refactoring-patterns]**

**核心原则**：融合不是重写，是一系列小的、行为保持的转换。

**融合循环**：
```
验证源技能 → 执行融合 → 验证融合结果 → 确认/回滚
```

**验证检查点**：

| # | 检查项 | 验证方法 | 失败处理 |
|---|--------|----------|----------|
| 1 | 源技能完整性 | 读取所有源技能SKILL.md | 终止融合 |
| 2 | 融合后结构 | 检查目录结构是否正确 | 回滚融合 |
| 3 | 触发词冲突 | 检查触发词是否重复 | 调整触发词 |
| 4 | 功能覆盖 | 检查所有功能是否保留 | 补充功能 |
| 5 | 来源标识 | 检查metadata.merged_from | 补充标识 |

### 📌 融合来源标识（核心功能）

**必须记录融合来源**，包括：

#### 1. metadata 中标记
```yaml
metadata:
  copaw:
    emoji: "🔀"
  merged_from:
    - skill_name_a  # 被融合的技能名
    - skill_name_b
  merged_from_details:
    - name: skill_name_a
      description: "原技能描述摘要"
      version: "x.x.x"
    - name: skill_name_b
      description: "原技能描述摘要"
      version: "x.x.x"
```

#### 2. SKILL.md 正文开头标识
在融合后技能的开头添加：

```markdown
---
name: new-merged-skill
description: "新技能描述..."
metadata:
  merged_from: [skill_a, skill_b]  # ⭐ 必须标识融合来源
---

# 🔀 新技能名

> **融合自**：[skill-a](#skill-a-来源) + [skill-b](#skill-b-来源)
> **融合时间**：[YYYY-MM-DD]
> **版本**：1.0.0

## 📜 融合来源详情

### skill-a 来源
- **原名**：skill-a
- **功能**：xxx
- **触发词**：xxx
- **版本**：x.x.x

### skill-b 来源
- **原名**：skill-b
- **功能**：xxx
- **触发词**：xxx
- **版本**：x.x.x

---
```

### 直接融合规则

- `name`：总分最高技能的 name + 后缀（_merged 或取融合含义名）
- `description`：触发词并集 + "融合自 A、B"
- `metadata.merged_from`：**必须填写**被融合的技能名列表
- `metadata.merged_from_details`：**必须填写**被融合技能的详细信息
- `body`：
  1. 主技能结构为主框架
  2. 副技能独有流程作为补充章节
  3. 触发词合并去重
  4. **开头必须包含融合来源标识章节**

### 分层设计规则

> ⭐ **重要**：分层设计不仅是逻辑分发，**必须有对应的物理目录结构**。子技能必须放在父技能的 `sub-skills/` 目录下。

**正确结构（必须遵循）**：
```
parent-skill/                    ← 父技能 = 协调层
├── SKILL.md                     ← 父技能：协调分发逻辑（100-200行）
├── scripts/                     ← （可选）公共脚本
└── sub-skills/                 ← ⭐ 核心：子技能物理目录
    ├── child-skill-a/
    │   └── SKILL.md            ← 含 metadata.parent + metadata.merged_from
    ├── child-skill-b/
    │   └── SKILL.md            ← 含 metadata.parent + metadata.merged_from
    └── child-skill-c/
        └── SKILL.md            ← 含 metadata.parent + metadata.merged_from
```

**错误结构（常见 bug）**：
```
skills/
├── parent-skill/                ← ❌ 只有 SKILL.md，没有 sub-skills/
├── child-skill-a → symlink     ← ❌ 子技能独立顶层，未嵌套
├── child-skill-b → symlink     ← ❌ 子技能独立顶层，未嵌套
└── child-skill-c               ← ❌ 子技能独立顶层，未嵌套
```

**父技能结构**：
```markdown
---
name: new-merged-skill
metadata:
  merged_from: [skill_a, skill_b]  # ⭐ 必须标识
---

# 🔀 融合技能名

> **融合自**：[skill-a](#skill-a-来源) + [skill-b](#skill-b-来源)

## 概述
融合自 A 和 B，协调分发任务。

## 📜 融合来源

### skill-a 来源
- **原名**：skill-a
- **功能**：xxx
- **触发词**：xxx

### skill-b 来源
- **原名**：skill-b
- **功能**：xxx
- **触发词**：xxx

## 决策逻辑
- 检测到 [关键词X] → 调用 skill-A
- 检测到 [关键词Y] → 调用 skill-B

## 公共说明
[共同规则、边界条件]
```

**子技能改造**：
- 原技能内容完整保留（或适当精简）
- **必须**添加 `metadata.parent` 标记指向父技能
- **必须**添加 `metadata.merged_from` 标记（指向融合来源）
- 调整触发词避免与父技能冲突

**执行命令**：
```bash
# 1. 创建父技能 sub-skills 目录
mkdir -p /app/working/skill_pool/<父技能>/sub-skills/

# 2. 将子技能移入父技能 sub-skills/ 下
mv /app/working/skill_pool/<子技能A>/ /app/working/skill_pool/<父技能>/sub-skills/<子技能A>/
mv /app/working/skill_pool/<子技能B>/ /app/working/skill_pool/<父技能>/sub-skills/<子技能B>/

# 3. 为每个子技能添加 metadata.parent 标记
# 4. 更新父技能 SKILL.md 添加 metadata.sub_skills 声明
```

### ⭐ 分层设计校验检查清单（融合完成后必须验证）

每次分层融合完成后，**必须逐项验证**，如有遗漏立即修复：

**结构校验**：
- [ ] `父技能/SKILL.md` 存在 `metadata.sub_skills` 字段，列出所有子技能名
- [ ] `父技能/sub-skills/` 目录存在（非空）
- [ ] 每个子技能的 `SKILL.md` 包含 `metadata.parent` 字段，指向父技能名
- [ ] 每个子技能的 `SKILL.md` 包含 `metadata.merged_from` 字段，列出融合来源
- [ ] 子技能物理位置在 `父技能/sub-skills/<子技能名>/` 下（**非顶层独立目录**）
- [ ] 原顶层独立目录/symlink 已删除（避免残留）
- [ ] 父技能 `SKILL.md` 正文包含 `## 📜 融合来源` 章节

**⭐ 子技能使用引导校验**（新增）：
- [ ] 父技能包含 `## 🔗 子技能调度规则` 章节
- [ ] 包含调度逻辑流程图
- [ ] 包含意图识别表（用户意图→触发词→路由到→说明）
- [ ] 包含子技能调用说明（子技能→职责→流程）
- [ ] 包含子技能联动规则（如需要）

> ⚠️ **特别注意**：融合完成后，必须检查 `skills/` 和 `skill_pool/` 下是否还有被融合技能的残留。残留的顶层独立目录/symlink 必须删除，确保子技能只在父技能的 `sub-skills/` 下存在。

**父技能 metadata.sub_skills 示例**：
```yaml
metadata:
  sub_skills:
    - writing-plans
    - executing-plans
    - planning-with-files
```

**子技能 metadata 要求示例**：
```yaml
# writing-plans 的 metadata
metadata:
  parent: plans-master           # ⭐ 必须指向父技能
  merged_from: [writing-plans]   # ⭐ 列出融合来源
```

### 执行命令

```bash
# 1. 创建新技能目录
mkdir -p /app/working/skill_pool/<新技能>/
mkdir -p /app/working/skill_pool/<新技能>/scripts/
mkdir -p /app/working/skill_pool/<新技能>/prompts/

# 2. 写入融合后的 SKILL.md
cp SKILL.md /app/working/skill_pool/<新技能>/

# 3. 备份被融合技能（可选）
cp -r /app/working/skill_pool/<原技能>/ /tmp/skill_backup/

# 4. 删除被融合技能
rm -rf /app/working/skill_pool/<原技能>/

# 5. 更新 skill.json（移除被合并技能）
```

### 报告模板

```
✅ **融合完成**

**融合策略**：[直接融合 / 分层设计]

**📦 融合来源**（已标识）：
- 来源技能A：skill-a（版本 x.x.x）
- 来源技能B：skill-b（版本 x.x.x）

**生成**：
- 新技能：`skill_pool/new-skill/`
  - 父技能：new-skill (协调层)
  - 子技能：new-skill-A, new-skill-B (执行层)
  - ⭐ 已自动标记 `metadata.merged_from` 字段

**删除**：
- 原技能：old-skill-A, old-skill-B

**行数统计**：
- 融合前总计：XXX 行
- 融合后总计：XXX 行（精简 XX%）

**版本跟踪**：
- 融合版本：1.0.0
- 融合日期：YYYY-MM-DD
- 源技能版本：skill-a v1.0.0, skill-b v2.0.0

**后续追踪**：
- 可通过 `grep -r "merged_from" skill_pool/` 查询所有融合技能
- 融合来源信息位于每个技能的 metadata.merged_from 字段
- 可通过 "检查融合版本" 查看所有融合技能的版本状态
```

---

## 边界条件

### 无重复技能
"扫描完毕，当前没有发现适合融合的技能组合。"

### 用户拒绝融合
"好的，已跳过。可随时重新触发。"

### 内置技能冲突
"检测到内置技能（source=builtin）涉及重叠，已自动跳过，不做修改。"

### 技能数量不足
"当前技能较少（<5个待融合），融合收益不明显，建议积累后再使用。"

### 超大规模警告
"检测到融合后规模超过 3000 行，建议拆分为多个独立技能而非强行融合。"

### ⭐ 融合来源标识遗漏警告
"⚠️ 融合来源标识遗漏：必须为 `metadata.merged_from` 字段赋值，格式：`merged_from: [skill_a, skill_b]`"

### ⭐ 版本跟踪边界条件
- 源技能不存在：跳过该源技能，继续融合其他技能
- 源技能版本未知：记录为"unknown"，继续融合
- 融合版本冲突：自动递增版本号

---

## 安全约束

1. **内置技能只读**：builtin 源不删不改
2. **先确认后删除**：删除必须用户明确同意
3. **规模预警**：超过 3000 行时建议拆分
4. **备份优先**：删除前自动备份到 `/tmp/skill_backup/`
5. **倾向保守**：无法判断时保留原技能
6. **⭐ 融合来源必须标识**：每次融合后必须在 `metadata.merged_from` 字段中记录来源技能，不可遗漏
7. **⭐ 来源信息永久保留**：即使被融合的源技能被删除，融合后的技能中仍需保留 `merged_from` 和 `merged_from_details` 记录
8. **⭐ 版本信息必须记录**：每次融合后必须在 `metadata.merged_version` 和 `metadata.merged_date` 字段中记录版本信息

---

## 快速参考

| 场景 | 操作 |
|------|------|
| 用户说"融合XX和XX" | 直接评估这两个技能 |
| 用户说"整理技能" | 全局扫描，找出候选组，逐个评估 |
| 规模 ≤ 1500 行 | 直接融合 |
| 规模 > 1500 行 | 分层设计 |
| 规模 > 3000 行 | 建议拆分，不强行融合 |
| 用户说"检查融合版本" | 列出所有融合技能的版本状态 |

---

## ⭐ 融合来源标识清单

每次融合必须完成以下标识：

**来源标识**：
- [ ] `metadata.merged_from`: 列出所有被融合的技能名（数组）
- [ ] `metadata.merged_from_details`: 列出详细信息（name、description、version）
- [ ] SKILL.md 正文开头添加 `> **融合自**：xxx + xxx` 引用
- [ ] SKILL.md 正文添加 `## 📜 融合来源详情` 章节

**分层设计标识**：
- [ ] 子技能需添加 `metadata.parent` 标记指向父技能
- [ ] **分层设计**：父技能需添加 `metadata.sub_skills` 声明子技能列表
- [ ] **分层设计**：子技能必须物理放置在 `父技能/sub-skills/<子技能名>/` 下
- [ ] **分层设计**：验证后删除原顶层残留目录/symlink

**⭐ 子技能使用引导标识**（新增）：
- [ ] 父技能包含 `## 🔗 子技能调度规则` 章节
- [ ] 包含调度逻辑流程图
- [ ] 包含意图识别表（用户意图→触发词→路由到→说明）
- [ ] 包含子技能调用说明（子技能→职责→流程）
- [ ] 包含子技能联动规则（如需要）

**⭐ 版本跟踪标识**（新增）：
- [ ] `metadata.merged_version`: 融合版本号（如1.0.0）
- [ ] `metadata.merged_date`: 融合日期（YYYY-MM-DD）
