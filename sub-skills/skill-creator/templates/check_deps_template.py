#!/usr/bin/env python3
"""
check_deps.py — 依赖自愈检查脚本（模板）
===========================================
使用方式：
  1. 复制本文件到你的技能 scripts/ 目录
  2. 修改下方的 DEPENDENCIES_CONFIG 配置
  3. 在 SKILL.md 中要求每次使用前先跑此脚本

Usage:
  python scripts/check_deps.py           完整检查 + 自动修复
  python scripts/check_deps.py --check   仅检查不安装
  python scripts/check_deps.py --fix     仅安装不检查
  python scripts/check_deps.py --json    JSON 格式输出
"""

import json
import os
import subprocess
import sys
import importlib.util
from pathlib import Path

# ====================================================================
# ★★★ 依赖配置 — 根据你的技能修改这里 ★★★
# ====================================================================

DEPENDENCIES_CONFIG = {
    # Python 包依赖
    "pip_packages": [
        {
            "name": "包名",              # pip 包名
            "import_name": "包名",        # import 时用的名字（通常同包名）
            "min_version": None,          # 最低版本要求，如 "1.0.0"，None 表示不限制
            "optional": False,           # True=可选依赖，缺失只警告
            "reason": "核心引擎，用于 XXX", # 用途说明
        },
        # 示例：
        # { "name": "requests", "import_name": "requests", "min_version": None,
        #   "optional": False, "reason": "HTTP 请求" },
    ],

    # CLI 工具依赖（通过 which/where 检查）
    "cli_tools": [
        {
            "name": "工具名",             # 显示名，如 "ffmpeg"
            "check_cmd": "ffmpeg",        # 检查命令
            "install_hint": "apt install ffmpeg 或 choco install ffmpeg",
            "optional": False,
        },
    ],

    # 环境变量配置检查
    "env_vars": [
        {
            "name": "API Key 名称",       # 显示名
            "env_var": "YOUR_API_KEY",    # 环境变量名
            "optional": True,            # True=缺失只警告
            "hint": "设置 YOUR_API_KEY=xxx",
        },
    ],
}

# ====================================================================
# 检查引擎
# ====================================================================

def check_pip_package(config):
    """检查单个 Python 包"""
    name = config["name"]
    import_name = config.get("import_name", name)
    min_ver = config.get("min_version")

    result = {
        "type": "pip",
        "name": name,
        "installed": False,
        "version": None,
        "min_version": min_ver,
        "satisfied": False,
        "optional": config.get("optional", False),
        "reason": config.get("reason", ""),
    }

    try:
        spec = importlib.util.find_spec(import_name)
        if spec is not None:
            result["installed"] = True
            try:
                mod = importlib.import_module(import_name)
                ver = getattr(mod, "__version__", None)
                result["version"] = ver
            except Exception:
                pass
    except Exception:
        pass

    if result["installed"]:
        if min_ver and result["version"]:
            result["satisfied"] = _compare_versions(result["version"], min_ver) >= 0
        else:
            result["satisfied"] = True

    return result


def check_cli_tool(config):
    """检查 CLI 工具是否可用"""
    name = config["name"]
    check_cmd = config["check_cmd"]
    result = {
        "type": "cli",
        "name": name,
        "available": False,
        "optional": config.get("optional", False),
        "install_hint": config.get("install_hint", ""),
    }

    try:
        if sys.platform == "win32":
            r = subprocess.run(
                ["where", check_cmd],
                capture_output=True, text=True, timeout=5
            )
        else:
            r = subprocess.run(
                ["which", check_cmd],
                capture_output=True, text=True, timeout=5
            )
        result["available"] = r.returncode == 0
    except Exception:
        pass

    result["satisfied"] = result["available"]
    return result


def check_env_var(config):
    """检查环境变量是否配置"""
    name = config["name"]
    env_var = config["env_var"]
    value = os.environ.get(env_var, "")
    result = {
        "type": "env",
        "name": name,
        "env_var": env_var,
        "configured": bool(value and value.strip()),
        "optional": config.get("optional", False),
        "hint": config.get("hint", ""),
    }
    result["satisfied"] = result["configured"] or result["optional"]
    return result


def _compare_versions(v1, v2):
    """比较版本号，返回 -1/0/1"""
    try:
        parts1 = [int(x) for x in v1.split(".")]
        parts2 = [int(x) for x in v2.split(".")]
        for a, b in zip(parts1, parts2):
            if a < b:
                return -1
            if a > b:
                return 1
        return len(parts1) - len(parts2)
    except Exception:
        return 0


def install_pip_package(config):
    """安装 Python 包"""
    name = config["name"]
    print(f"[check-deps] 正在安装 {name}...", flush=True)

    try:
        cmd = [sys.executable, "-m", "pip", "install", name]
        if config.get("min_version"):
            cmd.append(f">={config['min_version']}")

        r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

        if r.returncode == 0:
            print(f"[check-deps] ✅ {name} 安装成功", flush=True)
            return True, ""
        else:
            err = r.stderr[-200:] if r.stderr else ""
            print(f"[check-deps] ❌ {name} 安装失败: {err}", flush=True)
            return False, err

    except subprocess.TimeoutExpired:
        print(f"[check-deps] ❌ {name} 安装超时", flush=True)
        return False, "timeout"
    except Exception as e:
        print(f"[check-deps] ❌ {name} 安装异常: {e}", flush=True)
        return False, str(e)


# ====================================================================
# 报告生成
# ====================================================================

def generate_report(all_results, auto_fixed=False):
    """生成检查报告"""
    pkgs = [r for r in all_results if r.get("type") == "pip"]
    clis = [r for r in all_results if r.get("type") == "cli"]
    envs = [r for r in all_results if r.get("type") == "env"]

    critical_missing = [
        r for r in all_results
        if not r["satisfied"] and not r.get("optional", False)
    ]
    all_satisfied = len(critical_missing) == 0

    lines = []
    lines.append("=" * 60)
    lines.append("  依赖自愈检查报告")
    lines.append("=" * 60)

    lines.append("\n【Python 包】")
    for r in pkgs:
        if r["satisfied"]:
            ver = f"v{r['version']}" if r["version"] else "已安装"
            lines.append(f"  [OK] {r['name']} ({ver})")
        elif r.get("optional"):
            lines.append(f"  [..] {r['name']} (可选, {r['reason']})")
        else:
            lines.append(f"  [!!] {r['name']} (必选, {r['reason']})")

    lines.append("\n【CLI 工具】")
    for r in clis:
        if r["satisfied"]:
            lines.append(f"  [OK] {r['name']}")
        else:
            lines.append(f"  [..] {r['name']} (安装: {r.get('install_hint', 'N/A')})")

    lines.append("\n【环境变量】")
    for r in envs:
        if r["satisfied"]:
            lines.append(f"  [OK] {r['name']}")
        else:
            lines.append(f"  [..] {r['name']} (设置: {r.get('hint', 'N/A')})")

    lines.append("\n【结论】")
    if auto_fixed:
        lines.append("  依赖已自动修复")
    elif all_satisfied:
        lines.append("  全部通过，可以正常使用")
    else:
        lines.append(f"  缺少 {len(critical_missing)} 个必要项，需修复")
        for r in critical_missing:
            lines.append(f"    - {r['name']}")

    return "\n".join(lines)


# ====================================================================
# 主流程
# ====================================================================

def full_check(fix=True):
    """完整检查，可选自动修复"""
    results = []
    auto_fixed = False

    # 检查 pip 包
    for cfg in DEPENDENCIES_CONFIG.get("pip_packages", []):
        r = check_pip_package(cfg)
        results.append(r)

        if fix and not r["satisfied"] and not r.get("optional", False):
            success, _ = install_pip_package(cfg)
            if success:
                auto_fixed = True
                new_r = check_pip_package(cfg)
                r.update(new_r)

    # 检查 CLI 工具
    for cfg in DEPENDENCIES_CONFIG.get("cli_tools", []):
        r = check_cli_tool(cfg)
        results.append(r)

    # 检查环境变量
    for cfg in DEPENDENCIES_CONFIG.get("env_vars", []):
        r = check_env_var(cfg)
        results.append(r)

    return results, auto_fixed


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="依赖自愈检查工具（模板）",
    )
    parser.add_argument("--check", action="store_true", help="仅检查不安装")
    parser.add_argument("--fix", action="store_true", help="仅安装不检查")
    parser.add_argument("--json", action="store_true", help="JSON 格式输出")

    args = parser.parse_args()

    if args.fix:
        # 仅修复
        for cfg in DEPENDENCIES_CONFIG.get("pip_packages", []):
            r = check_pip_package(cfg)
            if not r["satisfied"] and not r.get("optional", False):
                install_pip_package(cfg)
        return

    results, auto_fixed = full_check(fix=not args.check)

    if args.json:
        clean = []
        for r in results:
            clean.append({k: v for k, v in r.items()
                          if k not in ("type",)})
        print(json.dumps(clean, ensure_ascii=False, indent=2))
    else:
        print(generate_report(results, auto_fixed))

    # 退出码
    critical_missing = [
        r for r in results
        if not r["satisfied"] and not r.get("optional", False)
    ]
    sys.exit(2 if critical_missing else 0)


if __name__ == "__main__":
    # Windows GBK 兼容
    if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    main()
