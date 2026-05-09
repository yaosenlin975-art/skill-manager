---
name: skill-creator
description: "从零创建 CoPaw 技能。触发词：'创建技能'、'写个skill'、'做个新技能'、'新建技能'。"
metadata:
  copaw:
    emoji: "✨"
  skill_version: "2.0.0"
  author: "CoPaw Community"
---

# ✨ Skill Creator - 从零创建 CoPaw 技能

## 四阶段流程

```
需求理解 → 适合性评估 → 规模决策 → 创建执行
```

---

## 阶段一：需求理解

主动询问用户，确认以下信息：

| 问题 | 目的 |
|------|------|
| 技能要做什么？ | 明确核心功能 |
| 什么时候触发？ | 确定触发词 |
| 期望什么输出？ | 定义输出格式 |
| 需要什么依赖？ | 确定 requirements |

---

## 阶段二：适合性评估 ⚡

### 评估维度

| 维度 | 权重 | 评估标准 |
|------|------|----------|
| **功能独立性** | 30% | 能否独立于其他技能运行？ |
| **触发明确性** | 25% | 用户能否清楚知道何时使用？ |
| **复杂度适中** | 25% | 行数预估 ≤ 1000 行？ |
| **复用价值** | 20% | 是否有通用性？ |

### 技能类型识别（★重要）

评估时**必须识别技能类型**，这会决定创建时的目录结构和附加组件：

| 技能类型 | 特征 | 示例 |
|----------|------|------|
| **CLI 封装** | 封装外部 CLI 工具，依赖系统命令或 pip 包 | `yt-dlp` 封装、`ffmpeg` 封装、`himalaya` 封装 |
| **MCP 封装** | 封装 MCP Server，通过 MCP 协议调用外部服务 | `graphify` MCP、`sqlite` MCP、`filesystem` MCP |
| **纯脚本** | 独立 Python/Shell 逻辑，不依赖外部工具 | 文本处理、格式转换、数据计算 |
| **Agent 编排** | 编排多个 Agent/技能协作完成任务 | 招聘流程、研究报告生成 |
| **信息获取** | 从网络/API 获取信息 | 新闻聚合、天气查询、股价查询 |

**判断准则**：技能的核心功能是否依赖外部命令/Python 包/MCP 服务？
- 是 → CLI 封装 或 MCP 封装 ⚡
- 否 → 其他类型

### 适合创建 ✅

满足以下任一：
- 功能独立，使用频率高
- 用户明确说"做个技能固化流程"
- 涉及多步骤复杂操作

### 不适合创建 ❌

满足以下任一：
- 功能过于简单（1句话搞定）
- 与现有技能完全重叠
- 功能边界不清

### 评估输出

```
📋 **适合性评估**

**技能类型**：CLI封装 / MCP封装 / 纯脚本 / Agent编排 / 信息获取
**复杂度预估**：小 / 中 / 大（XX 行）
**复用价值**：高 / 中 / 低

**评估结论**：✅ 适合创建 / ❌ 不适合

**理由**：
- [理由1]
- [理由2]
```

---

## 阶段三：规模决策 ⚡

| 规模 | 行数 | 策略 |
|------|------|------|
| **简单技能** | ≤ 300 行 | 单文件 SKILL.md |
| **普通技能** | 300-800 行 | SKILL.md + scripts/ |
| **复杂技能** | > 800 行 | SKILL.md + scripts/ + prompts/ + 分层设计 |

---

## 阶段四：创建执行

### 目录结构（按规模）

**简单技能**：
```
skill-name/
└── SKILL.md          # 包含所有内容
```

**普通技能**：
```
skill-name/
├── SKILL.md
├── scripts/
│   └── main.py       # 核心逻辑
└── prompts/
    └── template.md   # 提示模板
```

**复杂技能**：
```
skill-name/
├── SKILL.md          # 主技能（协调层）
├── scripts/
│   └── main.py
├── prompts/
│   └── template.md
└── sub-skills/       # 执行层子技能
    ├── sub-1/
    └── sub-2/
```

### ★ CLI/MCP 封装技能的强制要求

**如果阶段二识别的技能类型为 CLI封装 或 MCP封装，必须满足以下要求：**

**目录结构必须包含**：
```
skill-name/
├── SKILL.md
└── scripts/
    ├── main.py              # 核心逻辑
    └── check_deps.py        # ★ 依赖自愈（强制）
```

**check_deps.py 必须实现**：
- 检查所有外部依赖（Python 包、CLI 工具、环境变量）
- 缺失时自动 pip install
- 输出检查报告
- CLI 入口支持 `--check` / `--fix` / `--json`

**快速集成方式**：复制模板后修改依赖配置

```bash
# 复制通用模板到新技能
cp skills/skill-manager/sub-skills/skill-creator/templates/check_deps_template.py \
   skills/<skill-name>/scripts/check_deps.py

# 修改 check_deps.py 顶部的 DEPENDENCIES_CONFIG 配置
```

**模板路径**：`skills/skill-manager/sub-skills/skill-creator/templates/check_deps_template.py`

### SKILL.md 模板

```yaml
---
name: <skill-name>              # 小写+横线
description: "触发词：'xxx'。用途：xxx。不做：xxx。"
metadata:
  copaw:
    emoji: "🎯"
    skill_version: "1.0.0"
    author: "作者"
  tags: []
  related_skills: []
---
```

---

## 执行命令

```bash
# 1. 创建目录
mkdir -p /app/working/workspaces/default/skills/<skill-name>/

# 2. 创建子目录（按规模）
mkdir -p /app/working/workspaces/default/skills/<skill-name>/scripts/
mkdir -p /app/working/workspaces/default/skills/<skill-name>/prompts/

# 3. 写入 SKILL.md
write_file("skills/<skill-name>/SKILL.md", content)

# 4. 注册到 skill.json（如需要）
```

---

## 完成报告

```
✅ **技能创建完成**

**技能名**：skill-name
**规模**：简单 / 普通 / 复杂
**路径**：`/app/working/workspaces/default/skills/skill-name/`

**下一步**：
- 说"测试技能"可评测质量
- 说"优化技能"可用EvoForge优化
```

---

## 安全约束

1. **同名检查**：创建前检查是否已存在同名技能
2. **字段完整**：metadata 必须包含 emoji、version、author
3. **触发词不冲突**：检查是否与其他技能触发词重叠

---

## 📂 路径参考

| 类型 | 路径 |
|------|------|
| 工作区技能 | `/app/working/workspaces/default/skills/` |
| 全局技能池 | `/app/working/skill_pool/` |
| skill.json | `/app/working/skill_pool/skill.json` |

---

## 🔗 相关技能

| 技能 | 用途 |
|------|------|
| `skill-reviewer` | 评测技能质量 |
| `skill-merger` | 融合技能 |
| `evo-forge` | EvoForge 优化 |
