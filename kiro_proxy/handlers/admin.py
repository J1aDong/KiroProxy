"""管理 API 处理"""
import json
import uuid
import time
import httpx
from pathlib import Path
from datetime import datetime
from dataclasses import asdict
from fastapi import Request, HTTPException, Query

from ..config import TOKEN_PATH, MODELS_URL, MACHINE_ID
from ..models import state, Account


async def get_status():
    """服务状态"""
    try:
        with open(TOKEN_PATH) as f:
            data = json.load(f)
        return {
            "ok": True,
            "expires": data.get("expiresAt"),
            "stats": state.get_stats()
        }
    except Exception as e:
        return {"ok": False, "error": str(e), "stats": state.get_stats()}


async def get_stats():
    """获取统计信息"""
    return state.get_stats()


async def get_logs(limit: int = Query(100, le=1000)):
    """获取请求日志"""
    logs = list(state.request_logs)[-limit:]
    return {
        "logs": [asdict(log) for log in reversed(logs)],
        "total": len(state.request_logs)
    }


async def get_accounts():
    """获取账号列表"""
    return {
        "accounts": [
            {
                "id": a.id,
                "name": a.name,
                "enabled": a.enabled,
                "available": a.is_available(),
                "request_count": a.request_count,
                "error_count": a.error_count,
                "rate_limited": a.rate_limited_until > time.time() if a.rate_limited_until else False,
                "rate_limited_until": a.rate_limited_until
            }
            for a in state.accounts
        ]
    }


async def add_account(request: Request):
    """添加账号"""
    body = await request.json()
    name = body.get("name", f"账号{len(state.accounts)+1}")
    token_path = body.get("token_path")
    
    if not token_path or not Path(token_path).exists():
        raise HTTPException(400, "Invalid token path")
    
    account = Account(
        id=uuid.uuid4().hex[:8],
        name=name,
        token_path=token_path
    )
    state.accounts.append(account)
    return {"ok": True, "account": asdict(account)}


async def delete_account(account_id: str):
    """删除账号"""
    state.accounts = [a for a in state.accounts if a.id != account_id]
    return {"ok": True}


async def toggle_account(account_id: str):
    """启用/禁用账号"""
    for acc in state.accounts:
        if acc.id == account_id:
            acc.enabled = not acc.enabled
            return {"ok": True, "enabled": acc.enabled}
    raise HTTPException(404, "Account not found")


async def speedtest():
    """测试 API 延迟"""
    account = state.get_available_account()
    if not account:
        return {"ok": False, "error": "No available account"}
    
    start = time.time()
    try:
        token = account.get_token()
        headers = {
            "content-type": "application/json",
            "x-amz-user-agent": f"aws-sdk-js/1.0.27 KiroIDE-0.8.0-{MACHINE_ID}",
            "Authorization": f"Bearer {token}",
        }
        async with httpx.AsyncClient(verify=False, timeout=10) as client:
            resp = await client.get(MODELS_URL, headers=headers, params={"origin": "AI_EDITOR"})
            latency = (time.time() - start) * 1000
            return {
                "ok": resp.status_code == 200,
                "latency_ms": round(latency, 2),
                "status": resp.status_code
            }
    except Exception as e:
        return {"ok": False, "error": str(e), "latency_ms": (time.time() - start) * 1000}


async def scan_tokens():
    """扫描系统中的 Kiro token 文件"""
    found = []
    sso_cache = Path.home() / ".aws/sso/cache"
    if sso_cache.exists():
        for f in sso_cache.glob("*.json"):
            try:
                with open(f) as fp:
                    data = json.load(fp)
                    if "accessToken" in data:
                        found.append({
                            "path": str(f),
                            "name": f.stem,
                            "expires": data.get("expiresAt"),
                            "provider": data.get("provider", "unknown"),
                            "region": data.get("region", "unknown")
                        })
            except:
                pass
    return {"tokens": found}


async def add_from_scan(request: Request):
    """从扫描结果添加账号"""
    body = await request.json()
    token_path = body.get("path")
    name = body.get("name", "扫描账号")
    
    if not token_path or not Path(token_path).exists():
        raise HTTPException(400, "Token 文件不存在")
    
    if any(a.token_path == token_path for a in state.accounts):
        raise HTTPException(400, "该账号已添加")
    
    try:
        with open(token_path) as f:
            data = json.load(f)
            if "accessToken" not in data:
                raise HTTPException(400, "无效的 token 文件")
    except json.JSONDecodeError:
        raise HTTPException(400, "无效的 JSON 文件")
    
    account = Account(
        id=uuid.uuid4().hex[:8],
        name=name,
        token_path=token_path
    )
    state.accounts.append(account)
    return {"ok": True, "account_id": account.id}


async def export_config():
    """导出配置"""
    return {
        "accounts": [
            {"name": a.name, "token_path": a.token_path, "enabled": a.enabled}
            for a in state.accounts
        ],
        "exported_at": datetime.now().isoformat()
    }


async def import_config(request: Request):
    """导入配置"""
    body = await request.json()
    accounts = body.get("accounts", [])
    imported = 0
    
    for acc_data in accounts:
        token_path = acc_data.get("token_path", "")
        if Path(token_path).exists():
            if not any(a.token_path == token_path for a in state.accounts):
                account = Account(
                    id=uuid.uuid4().hex[:8],
                    name=acc_data.get("name", "导入账号"),
                    token_path=token_path,
                    enabled=acc_data.get("enabled", True)
                )
                state.accounts.append(account)
                imported += 1
    
    return {"ok": True, "imported": imported}


async def refresh_token_check():
    """检查所有账号的 token 状态"""
    results = []
    for acc in state.accounts:
        try:
            with open(acc.token_path) as f:
                data = json.load(f)
                expires = data.get("expiresAt", "")
                if expires:
                    exp_time = datetime.fromisoformat(expires.replace("Z", "+00:00"))
                    now = datetime.now(exp_time.tzinfo)
                    is_valid = exp_time > now
                    remaining = (exp_time - now).total_seconds() if is_valid else 0
                else:
                    is_valid = False
                    remaining = 0
                
                results.append({
                    "id": acc.id,
                    "name": acc.name,
                    "valid": is_valid,
                    "expires": expires,
                    "remaining_seconds": int(remaining)
                })
        except Exception as e:
            results.append({
                "id": acc.id,
                "name": acc.name,
                "valid": False,
                "error": str(e)
            })
    
    return {"accounts": results}


async def get_kiro_login_url():
    """获取 Kiro 登录说明"""
    return {
        "message": "Kiro 使用 AWS Identity Center 认证，无法直接 OAuth",
        "instructions": [
            "1. 打开 Kiro IDE",
            "2. 点击登录按钮，使用 Google/GitHub 账号登录",
            "3. 登录成功后，token 会自动保存到 ~/.aws/sso/cache/",
            "4. 本代理会自动读取该 token"
        ],
        "token_path": str(TOKEN_PATH),
        "token_exists": TOKEN_PATH.exists()
    }
