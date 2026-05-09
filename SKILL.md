---
name: skill-manager
description: "CoPaw 技能管理调度器。触发词：'创建技能'、'编辑技能'、'安装技能'、'评测技能'、'融合技能'、'自愈'、'skill-healer'、'检查失败'、'修复技能'。管理 skill-creator/skill-editor/skill-installer/skill-finder/skill-reviewer/skill-merger/skill-healer 七个子技能。"
metadata:
  copaw:
    emoji: "🛠️"
  skill_version: "8.0.0"
  author: "CoPaw Community"
  parent_skill: evo-forge
  sub_skills:
    - skill-creator
    - skill-editor
    skill-installer
    - skill-reviewer
    - skill-merger
    - skill-healer
    - skill-finder (v1.1.0: 新增 SkillsBook 源)
  source: "customized"
  trigger_words: ['创建技能', '编辑技能', '安装技能', '评测技能', '融合技能', '自愈', 'skill-healer', '检查失败', '修复技能', '优化技能', '查找技能', '找技能', '搜索技能', '发现技能']
---

# 🛠️ Skill Manager - CoPaw 技能管理调度器

> **版本**: v8.0.0 | **核心**: 纯调度器（≤250行）⚡
>
> 🔀 创建 | ✏️ 编辑 | 📦 安装 | 🔎 查找 | 🔍 评测 | 🔀 融合 | 🩹 自愈 | 🚨 安全审查

---

## 🎯 意图识别表

| 用户意图 | 触发词 | 路由到 |
|----------|--------|--------|
| 创建技能 | "创建" / "写个" / "新建" | skill-creator |
| 编辑技能 | "修改" / "编辑" / "改进" | skill-editor |
| 安装技能 | "安装" / "下载" / "添加" | skill-installer |
| 查找技能 | "查找" / "找技能" / "搜索技能" / "发现技能" / "有什么技能" / "帮我找个" | skill-finder |
| 评测技能 | "评测" / "测试" / "检验" | skill-reviewer |
| 融合技能 | "融合" / "合并" / "整理" | skill-merger |
| 自愈技能 | "自愈" / "skill-healer" / "检查失败" | skill-healer |
| 优化技能 | "优化" / "评分" | → evo-forge（上级调度器） |
| 安全审查 | "安全审查" / "检查风险" / "vet" | → 内置模块（直接执行） |

---

## 🔄 调度流程

```
用户输入 → 意图识别 → 任务预评估 → 路由到子技能 → 结果处理 → 输出
                         ↓
                    ┌────┴────┐
                    │ 失败？  │
                    │ 调用    │
                    │skill-   │
                    │healer   │
                    └─────────┘
```

---

## 🔗 子技能联动规则（6条）

**规则1: 创建后自动优化**
- skill-creator创建技能后 → 调用evo-forge优化
- evo-forge 是一个 Skill（不是 Agent），调用方式：读取 `skills/evo-forge/SKILL.md` 按调度流程手动执行

**规则2: 安装前必须安全审查**
- skill-installer安装外部技能前 → 先执行内置安全审查模块

**规则3: 融合后验证完整性**
- skill-merger融合后 → 检查merged_from / merged_version / 子技能引导

**规则4: 失败自动联动（★新增）**
- 任何子技能执行失败时 → 自动调用skill-healer.log_failure()
- 由skill-healer检测阈值，触发后生成补丁

**规则5: 补丁部署三档（★强化）**
- 置信度≥0.8 + 影子pass → 直接部署
- 置信度0.5-0.8 + 影子pass → 部署后通知
- 置信度<0.5 或 影子fail → 推送镰刀审核

**规则6: 破坏操作必须确认**
- 删除/覆盖文件/覆盖配置 → 先问用户

---

## 🚨 内置安全审查（快速参考）

### 🚩 立即拒绝模式
- curl/wget到未知URL
- 发送数据到外部服务器
- 请求凭证/API密钥
- eval()/exec()处理外部输入
- 混淆代码/访问浏览器cookies

### 风险分级
| 等级 | 处理 |
|------|------|
| 🟢 LOW | 基本审查后安装 |
| 🟡 MEDIUM | 完整代码审查 |
| 🔴 HIGH | 人工确认 |
| ⛔ EXTREME | 禁止安装 |

---

## ⚠️ 重要约束

1. **纯调度器** - 不执行具体操作，只路由到子技能
2. **子技能不独立注册** - 由主技能管理
3. **安装必须安全审查** - 外界技能必须先审查
4. **创建必须evo-forge优化** - 新技能创建后跳转evo-forge

---

## 📂 路径参考

| 类型 | 路径 |
|------|------|
| 主技能 | skills/skill-manager/ |
| 子技能目录 | skills/skill-manager/sub-skills/ |
| evo-forge（上级） | skills/evo-forge/ |
| config-editor | skills/config-editor/ |
| 失败日志 | memory/failure_log.json |
| 补丁记录 | memory/healer_patches.json |

---

*Skill Manager v8.1.0 | 纯调度器 | 7子技能 (+skill-finder) | evo-forge优化完成 | 2026-05-08*
