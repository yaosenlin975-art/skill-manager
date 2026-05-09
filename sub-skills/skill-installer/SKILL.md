---
name: skill-installer
description: "安装外界技能到 CoPaw。触发词：'安装技能'、'装个skill'、'下载技能'、'安装xx技能'、'添加技能'。"
metadata:
  copaw:
    emoji: "📦"
  skill_version: "2.0.0"
  author: "CoPaw Community"
---

# 📦 Skill Installer - 安装外界技能

## 什么时候用

- 用户说"安装技能"、"装个skill"
- 用户提供了 GitHub/ClawdHub 链接
- 用户说"下载技能"、"添加技能"

---

## 安装流程

```
Step 1: 安全审查 (skill-vetter) ← 必须先审查
Step 2: 下载技能
Step 3: CoPaw 架构适配
Step 4: EvoForge优化 ← 直接执行，不问
Step 5: 注册到 skill.json
```

---

## Step 1: 安全审查 (skill-vetter)

**必须先审查，再安装！** 参考 `skill-vetter` 技能。

### 审查清单

| 检查项 | 说明 |
|--------|------|
| 来源检查 | GitHub/ClawdHub/官方？作者知名？Star数？ |
| 代码审查 | 读取所有 .py/.sh/.js，检查危险信号 |
| 风险评级 | 🟢 LOW / 🟡 MEDIUM / 🔴 HIGH |

### 🚨 危险信号（发现则拒绝）

```
• curl/wget 到未知URL
• 数据外发到外部服务器
• 请求凭证/API密钥
• 读取 ~/.ssh, ~/.aws 等敏感目录
• eval()/exec() 动态执行
• 修改系统文件
• 安装未列出的包
• 混淆/压缩代码
```

### 风险处理

| 风险等级 | 处理方式 |
|----------|----------|
| 🟢 LOW | 直接进入 Step 2 |
| 🟡 MEDIUM | 详细审查后安装 |
| 🔴 HIGH | **必须用户确认**才能继续 |

### 审查报告模板

```markdown
## SKILL VETTING REPORT 🔒

**Skill**: [name]
**Source**: [GitHub/ClawdHub/other]
**Author**: [username]
─────────────────────────────────────
**RISK LEVEL**: [🟢 LOW / 🟡 MEDIUM / 🔴 HIGH]
**VERDICT**: [✅ SAFE / ⚠️ CAUTION / ❌ DO NOT INSTALL]
```

---

## Step 2: 下载技能

```bash
# 方式1: Git Clone
cd /app/working/workspaces/default/skills/
git clone <repository_url> <skill-name>

# 方式2: 手动下载
curl -sL <raw_file_url> -o <output_file>
```

### 验证清单

- [ ] SKILL.md 存在
- [ ] frontmatter 完整
- [ ] 目录结构合理

---

## Step 3: CoPaw 架构适配

### 3.1 识别技能类型

安装后**必须判断技能类型**，决定是否需要额外组件：

| 类型 | 判断依据 | 需要 check_deps.py？ |
|------|----------|----------------------|
| **CLI 封装** | 技能依赖外部 CLI 命令（yt-dlp/ffmpeg/gh 等）或 pip 包 | ✅ 强制 |
| **MCP 封装** | 技能通过 MCP 协议调用外部服务（graphify MCP 等） | ✅ 强制 |
| **其他类型** | 纯脚本 / Agent 编排 / 信息获取（不依赖外部工具） | ❌ 不需要 |

**判断方法**：快速阅读 SKILL.md 和代码
- 有没有 `subprocess.run()` / `os.system()` 调用外部命令？
- 有没有 `pip install` / `apt install` 之类的安装命令？
- 有没有 MCP Server 配置或 `mcp` 相关调用？
- 有没有大量第三方 pip 依赖（超过 2 个）？

以上任意回答"是" → CLI/MCP 封装技能 → 必须加 check_deps.py

### 3.2 添加 check_deps.py（CLI/MCP 封装技能）

**如果技能类型为 CLI 封装 或 MCP 封装，必须添加依赖自愈脚本**：

```bash
# 复制通用模板到技能目录
cp skills/skill-manager/sub-skills/skill-creator/templates/check_deps_template.py \
   skills/<skill-name>/scripts/check_deps.py
```

**修改 check_deps.py 顶部的 DEPENDENCIES_CONFIG**，根据技能的实际情况配置：

```python
DEPENDENCIES_CONFIG = {
    "pip_packages": [
        {
            "name": "包名",
            "import_name": "包名",
            "min_version": None,
            "optional": False,
            "reason": "用途说明",
        },
    ],
    "cli_tools": [
        {
            "name": "工具名",
            "check_cmd": "命令名",
            "install_hint": "安装方式说明",
            "optional": False,
        },
    ],
    "env_vars": [
        {
            "name": "API Key 名称",
            "env_var": "XXX_API_KEY",
            "optional": True,
            "hint": "设置方式说明",
        },
    ],
}
```

**验证 check_deps.py 能正常工作**：

```bash
python skills/<skill-name>/scripts/check_deps.py --check
python skills/<skill-name>/scripts/check_deps.py --json
```

### 3.3 更新 SKILL.md（CLI/MCP 封装技能）

在 SKILL.md 的"前置条件"或"快速开始"部分加入依赖自愈步骤：

```markdown
## 前置条件

运行前先执行依赖检查：
```bash
python scripts/check_deps.py
```
```

### 3.4 必须添加的 Metadata

```yaml
---
name: <skill-name>
description: "触发词：'中文触发'、'english trigger'。用途：xxx。不做：xxx。"
metadata:
  copaw:
    emoji: "🎯"                    # 必填
    skill_version: "1.0.0"        # 必填
    author: "原作者 | CoPaw适配"   # 必填
  tags: []                        # 推荐
  related_skills: []              # 推荐
---
```

### 适配后验证

- [ ] metadata 字段完整
- [ ] 触发词包含中英文
- [ ] related_skills 已关联
- [ ] （如 CLI/MCP 封装）scripts/check_deps.py 已添加并配置
- [ ] （如 CLI/MCP 封装）SKILL.md 已添加依赖自愈步骤

---

## Step 4: EvoForge优化 ⚡直接执行

**直接调用EvoForge优化，不问用户！**

### 执行方式

1. 读取 `evo-forge/sub-skills/evo-skill-optimizer/SKILL.md`
2. 对刚安装的技能执行优化流程
3. **直接执行，不询问用户**
4. 除非有**多个不同优化方向**需要选择，才暂停问用户

### 什么情况需要问用户？

- 优化方案有多个方向选择时
- 用户明确说了偏好（如"要简洁"、"要详细"）

### 什么情况不问？

- 默认优化流程
- 常规适配改进

---

## Step 5: 注册技能

```bash
# 复制到全局技能池
cp -r /app/working/workspaces/default/skills/<skill-name>/ /app/working/skill_pool/

# 更新 skill.json
```

### 多智能体同步

如果其他智能体有同名技能，**强制覆盖**。

---

## 快速检查清单

```
□ Step 1: 安全审查通过
□ Step 2: 技能下载成功
□ Step 3: CoPaw 架构适配完成
□ Step 4: EvoForge优化完成 ⚡
□ Step 5: 注册到 skill.json
```

---

## 📂 路径参考

| 类型 | 路径 |
|------|------|
| 工作区技能 | `/app/working/workspaces/default/skills/` |
| 全局技能池 | `/app/working/skill_pool/` |
| 达尔文优化器 | `/app/working/workspaces/default/skills/darwin-skill/sub-skills/darwin-skill-optimizer/`

---

## 🔗 相关技能

- `skill-vetter` - 安全审查
- `evo-forge` - EvoForge优化（自动调用）
- `skill-editor` - 调度器
