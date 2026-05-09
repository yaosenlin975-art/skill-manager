---
name: skill-finder
description: "查找/发现AI技能。触发词：'查找技能'、'找技能'、'搜索技能'、'发现技能'、'有什么技能'、'技能搜索'。支持从 SkillsBook / SkillHub / LobeHub / npx skills CLI 四个源搜索技能。"
metadata:
  copaw:
    emoji: "🔎"
    skill_version: "1.0.0"
    author: "CoPaw Community | 融合自 find-skills (jimliuxinghai)"
    source: "customized"
  trigger_words:
    - "查找技能"
    - "找技能"
    - "搜索技能"
    - "发现技能"
    - "有什么技能"
    - "技能搜索"
    - "帮我找个技能"
    - "我想找一个能"
    - "有没有做XX的技能"
  search_sources:
    - name: "SkillsBook"
      url: "https://skillsbook.fun/"
      type: "browser"
      desc: "中文AI技能弹药库，覆盖办公/编程/设计/金融/学术等多领域，支持精准搜索和AI自动生成技能"
    - name: "SkillHub"
      url: "https://skillhub.cn/"
      type: "browser"
      desc: "中国优化的AI技能社区，6.8万+技能"
    - name: "LobeHub"
      url: "https://lobehub.com/zh/skills"
      type: "browser"
      desc: "全球最大的Agent技能市场，29.6万+技能"
    - name: "npx-skills"
      url: "https://skills.sh/"
      type: "cli"
      desc: "开源Agent技能生态系统CLI"
---

# 🔎 Skill Finder — 跨源技能查找器

> **版本**: v1.1.0 | **融合自**: find-skills (jimliuxinghai) | **查找源**: SkillsBook + SkillHub + LobeHub + npx skills CLI

## 什么时候用

| 用户说... | 触发 |
|-----------|------|
| "帮我找个能做XX的技能" | 查找技能 |
| "有没有做React测试的技能" | 查找技能 |
| "搜索一下有什么好技能" | 发现技能 |
| "我想找一个能帮我写文档的技能" | 查找特定领域技能 |
| "有什么好用的开发工具技能" | 浏览发现 |
| "帮我搜搜有没有邮件相关的技能" | 关键词搜索 |
| "我想扩展一下能力" | 发现技能 |

---

## 四源查找策略

```
用户需求
    │
    ├─→ 源1: SkillsBook ─────── 浏览器搜索 (中文AI技能弹药库, 办公/编程/设计/金融/学术)
    │
    ├─→ 源2: SkillHub ──────── 浏览器搜索 (中国优化, 6.8万)
    │
    ├─→ 源3: LobeHub ───────── 浏览器搜索 (全球最大, 29.6万)
    │
    └─→ 源4: npx skills CLI ── 快速关键词搜索 (开源生态)
```

### 源选择规则

```
用户需求
    │
    ├─→ 源1: npx skills CLI ── 快速关键词搜索 (开源生态)
    │
    ├─→ 源2: SkillHub ──────── 浏览器搜索 (中国优化, 6.8万)
    │
    └─→ 源3: LobeHub ───────── 浏览器搜索 (全球最大, 29.6万)
```

### 源选择规则

| 场景 | 首选源 | 备选 |
|------|--------|------|
| 用户要中文技能/办公场景 | SkillsBook（中文AI技能弹药库） | SkillHub |
| 用户提具体关键词 | npx skills CLI（最快） | SkillHub |
| 用户想浏览发现 | SkillHub（中文友好） | SkillsBook |
| 用户需要大量选择 | LobeHub（最大市场） | SkillHub |
| npx skills 搜不到 | SkillHub | SkillsBook / LobeHub |
| 用户要国际化技能 | LobeHub | npx skills |

**默认策略**: 四源并行搜索，汇总结果给用户选。

---

## 搜索流程

### Step 1: 理解用户需求

提取关键词：
- 领域：web开发、测试、部署、设计、文档...
- 具体任务：写测试、审查PR、生成changelog...
- 使用场景：React项目、Python开发、CI/CD...

### Step 2: 选择查找方式

根据源选择规则确定用哪个源（或并行）。

#### 方式A: SkillsBook 浏览器搜索

1. 打开 https://skillsbook.fun/
2. 在首页搜索框输入关键词（如 "unity"、"llm"、"websocket"）
3. 浏览搜索结果列表
4. 点击技能卡片查看详情，支持下载 ZIP 获取技能包

**适用**: 中文技能搜索、办公/编程/设计等通用场景

#### 方式B: npx skills CLI 搜索

```bash
# 搜索技能
npx skills find <关键词>

# 示例
npx skills find react testing
npx skills find pr review
npx skills find email
```

**适用**: 用户有具体关键词，快速定位

#### 方式C: SkillHub 浏览器搜索

1. 打开 https://skillhub.cn/
2. 在搜索框输入关键词
3. 浏览结果列表
4. 点击进入技能详情页获取信息

**适用**: 中文搜索、浏览发现

#### 方式D: LobeHub 浏览器搜索

1. 打开 https://lobehub.com/zh/skills
2. 按分类浏览或搜索
3. 查看技能详情

**适用**: 大量选择、分类浏览

---

### Step 3: 汇总结果呈现

```markdown
## 🔎 搜索结果: [关键词]

### 📗 SkillsBook
| 技能名 | 描述 | 链接 |
|--------|------|------|
| xxx | xxx | https://skillsbook.fun/skills/xxx |

### 📦 npx skills CLI 生态
| 技能名 | 描述 | 安装方式 |
|--------|------|----------|
| xxx | xxx | `npx skills add xxx` |

### 🏪 SkillHub
| 技能名 | 描述 | 链接 |
|--------|------|------|
| xxx | xxx | https://skillhub.cn/skills/xxx |

### 🌐 LobeHub
| 技能名 | 描述 | 分类 |
|--------|------|------|
| xxx | xxx | xxx |
```

### Step 4: 引导用户

- 用户选中的技能 → 路由到 **skill-installer** 安装
- 如果搜索结果为空 → 推荐用户自己创建技能（路由到 **skill-creator**）
- 用户不确定 → 推荐几个热门技能

---

## 热门技能推荐（兜底）

如果用户不知道想要什么，推荐以下热门类别：

| 类别 | 示例关键词 | 推荐源 |
|------|-----------|--------|
| Web开发 | react, nextjs, typescript, css, tailwind | npx skills / SkillHub |
| 测试 | testing, jest, playwright, e2e | npx skills |
| DevOps | deploy, docker, kubernetes, ci-cd | LobeHub |
| 文档 | docs, readme, changelog, api-docs | npx skills |
| 代码质量 | review, lint, refactor, best-practices | LobeHub |
| 设计 | ui, ux, design-system, accessibility | LobeHub |
| 生产力 | workflow, automation, git | SkillHub |
| AI/LLM | prompt, agent, rag, llm | LobeHub |

---

## 与 skill-installer 联动

1. **查找技能** → skill-finder 执行
2. **用户选中** → 路由到 skill-installer 安装
3. **安装完成** → skill-reviewer 评测（可选）

---

## 📂 路径参考

| 项 | 路径 |
|----|------|
| 子技能目录 | skills/skill-manager/sub-skills/skill-finder/ |
| 上级调度器 | skills/skill-manager/SKILL.md |
| 安装联动 | skills/skill-manager/sub-skills/skill-installer/SKILL.md |
| SkillsBook | https://skillsbook.fun/ |
| SkillHub | https://skillhub.cn/ |
| LobeHub | https://lobehub.com/zh/skills |
| npx skills | https://www.npmjs.com/package/@openagents/skills |

---

## 🔗 相关技能

| 技能 | 关系 |
|------|------|
| skill-installer | 搜索结果安装落地 |
| skill-creator | 找不到时创建新技能 |
| skill-reviewer | 安装后评测 |
| skill-manager | 上级调度器 |

---

*Skill Finder v1.1.0 | 四源查找 | 融合自 find-skills (jimliuxinghai)*
