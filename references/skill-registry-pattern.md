# js-eyes Skill-Registry 协议模式

> 来源: https://github.com/imjszhang/js-eyes/tree/main/packages/protocol/skill-registry.js
> 分析日期: 2026-04-20
> 适用场景: CoPaw Skill 暴露工具 schema 的规范化设计

---

## 核心价值

js-eyes 的 Skill-Registry 实现了一套**工具级 dispatcher 间接层**，用于：

1. **热加载** - skill 更新时不需要重启 agent
2. **Schema 透传** - 让 LLM/OpenClaw 看到正确的参数约束
3. **工具绑定** - 动态映射 tool name → 实现

这套模式可以借鉴到 CoPaw 的 skill 系统中，让 skill 更容易被其他 agent 调用。

---

## 协议架构

### 核心概念

| 概念 | 说明 |
|------|------|
| **Skill** | 一个独立的 skill 单元，包含代码和 contract 定义 |
| **Contract** | skill 的元数据：触发词、工具列表、参数 schema |
| **Dispatcher** | 工具暴露对象：name + label + description + parameters + execute() |
| **Tool Binding** | tool name → dispatcher 实例的映射表 |
| **Hot Reload** | 更新 toolBindings 映射而不触碰宿主注册表 |

### 工具暴露结构

js-eyes 的每个工具都有标准 schema：

```javascript
{
  name: "browser_automation_open",        // 工具唯一名
  label: "打开网页",                     // 显示名
  description: "在浏览器中打开指定URL",  // LLM说明
  parameters: {                          // JSON Schema
    type: "object",
    required: ["url"],
    properties: {
      url: {
        type: "string",
        description: "目标URL地址",
      },
      wait: {
        type: "number",
        description: "等待秒数",
        default: 3000,
      }
    }
  },
  execute: async (toolCallId, params) => {  // 执行函数
    const { url, wait } = params;
    await browser.open(url);
    return { success: true, url };
  }
}
```

### 关键设计：Dispatcher 间接层

```javascript
// 每个工具名只注册一次，稳定的闭包
api.registerTool(name, dispatcher);

// 热加载时：只改 toolBindings 映射
toolBindings.set(name, newDispatcher);

// 宿主注册表不动，但 dispatcher 对象是引用类型
// 所以 LLM 看到的 schema 也会更新
```

**优势**：
- ✅ 首次注册后，后续热更新不需要重新注册
- ✅ Schema 变更通过引用 mutate 传播
- ✅ 不需要了解宿主注册表实现细节

---

## CoPaw 适配建议

### 当前 CoPaw Skill 的工具暴露方式

CoPaw skill 通过 SKILL.md 的 `triggers` 和 `tools` 字段暴露工具：

```yaml
name: web-scout
description: "网页搜索"
triggers:
  - "搜索网页"
  - "网上搜"
tools:
  - name: resource_searcher
    type: python_module
    command: "python -m scripts.resource_searcher"
```

### 改进方案：引入 JSON Schema

借鉴 js-eyes 模式，为 CoPaw skill 引入标准化的 tool schema：

```yaml
name: web-scout
description: "网页搜索"
version: "4.0.0"

# 新增：标准化工具暴露
tools:
  - name: resource_search
    label: "资源搜索"
    description: "在28个资源站点中搜索电子书/影视/音乐/游戏/软件"
    schema:
      type: "object"
      required: ["query"]
      properties:
        query:
          type: "string"
          description: "搜索关键词"
          example: "Python机器学习"
        category:
          type: "string"
          description: "资源类别"
          enum: ["ebook", "movie", "tv", "music", "anime", "game", "software", "telegram"]
          default: "ebook"
        limit:
          type: "integer"
          description: "返回结果数量"
          default: 10
          minimum: 1
          maximum: 50
        download:
          type: "boolean"
          description: "是否下载资源"
          default: false
    executor: python_module
    command: "python -m scripts.resource_searcher {args}"
    cacheable: true
    cache_ttl: 1800
```

### 工具发现协议

js-eyes 的 skill-registry 支持动态发现：

```javascript
// Agent 可以查询当前注册的所有工具
registry.listTools()
// 返回: [{name, label, description, schema}, ...]

// 按名称查询
registry.getTool(name)
// 返回: {name, label, description, schema, execute}

// 健康检查
registry.healthCheck()
// 返回: {status, loaded_count, enabled_skills}
```

### CoPaw 适配示例

```yaml
# skill-manager/references/tool-discovery.md

## 工具发现接口 (CoPaw Agent 可调用)

### 查询所有可用工具
```
GET /tools
Response: {tools: [{name, skill, label, description, schema_url}]}
```

### 查询特定工具
```
GET /tools/{name}
Response: {name, skill, label, description, schema, executor, reliability}
```

### 健康检查
```
GET /health
Response: {status, loaded_skills, total_tools, last_reload}
```

### 工具发现 Schema

```json
{
  "tools": [
    {
      "name": "resource_search",
      "skill": "web-scout",
      "label": "资源搜索",
      "description": "多源资源搜索和下载",
      "schema_url": "/skills/web-scout/schema/resource_search.json",
      "reliability": 0.85,
      "last_updated": "2026-04-20"
    }
  ]
}
```

---

## 热加载实现（参考）

js-eyes 的热加载核心逻辑：

```javascript
function createSkillRegistry(options) {
  const { api } = options;

  // toolName → dispatcher 映射
  const toolBindings = new Map();
  // 已注册的 dispatcher 引用（用于 schema mutate）
  const dispatchers = new Map();

  function registerTool(name, dispatcher) {
    // 首次注册
    if (!dispatchers.has(name)) {
      api.registerTool(name, dispatcher);
      dispatchers.set(name, dispatcher);
    }
    // 热更新：只改映射
    toolBindings.set(name, dispatcher);
  }

  function executeTool(name, toolCallId, params) {
    const dispatcher = toolBindings.get(name);
    if (!dispatcher) {
      throw new Error(`Tool "${name}" not found`);
    }
    return dispatcher.execute(toolCallId, params);
  }

  return { registerTool, executeTool, listTools, healthCheck };
}
```

---

## 与 CoPaw 现有机制的对比

| 维度 | js-eyes 模式 | CoPaw 当前 | 改进建议 |
|------|-------------|------------|---------|
| 工具定义 | JSON Schema + execute() | SKILL.md triggers | 引入 schema 字段 |
| 热加载 | dispatcher 引用映射 | 重载 agent | 可借鉴 dispatcher 层 |
| 工具发现 | registry.listTools() | 无 | 增加发现接口 |
| Schema 透传 | 引用 mutate | 需重启 | dispatcher 引用设计 |
| 安全策略 | policy/egress 分层 | 无 | 考虑引入 |

---

## 行动建议

| 优先级 | 动作 | 理由 |
|--------|------|------|
| **P2** | 为 web-scout 等核心 skill 补充 schema 字段 | 让 LLM 知道参数约束 |
| **P2** | 在 skill-manager 增加工具发现接口 | 便于 agent 间协作 |
| **P3** | 引入 dispatcher 热加载模式 | 避免 skill 更新需重启 |

---

## 参考链接

- js-eyes skill-registry: https://github.com/imjszhang/js-eyes/tree/main/packages/protocol/skill-registry.js
- js-eyes client-sdk: https://github.com/imjszhang/js-eyes/tree/main/packages/client-sdk
- js-eyes skill-recording: https://github.com/imjszhang/js-eyes/tree/main/packages/skill-recording
