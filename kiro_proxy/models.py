"""数据模型"""
from dataclasses import dataclass, field
from typing import Optional, List, Dict
from collections import deque
from pathlib import Path
import time
import json

from .config import TOKEN_PATH


@dataclass
class Account:
    """账号信息"""
    id: str
    name: str
    token_path: str
    enabled: bool = True
    rate_limited_until: Optional[float] = None
    request_count: int = 0
    error_count: int = 0
    last_used: Optional[float] = None
    
    def is_available(self) -> bool:
        if not self.enabled:
            return False
        if self.rate_limited_until and time.time() < self.rate_limited_until:
            return False
        return True
    
    def get_token(self) -> str:
        try:
            with open(self.token_path) as f:
                return json.load(f).get("accessToken", "")
        except:
            return ""


@dataclass
class RequestLog:
    """请求日志"""
    id: str
    timestamp: float
    method: str
    path: str
    model: str
    account_id: Optional[str]
    status: int
    duration_ms: float
    tokens_in: int = 0
    tokens_out: int = 0
    error: Optional[str] = None


class ProxyState:
    """全局状态管理"""
    def __init__(self):
        self.accounts: List[Account] = []
        self.request_logs: deque = deque(maxlen=1000)
        self.total_requests: int = 0
        self.total_errors: int = 0
        self.session_locks: Dict[str, str] = {}
        self.session_timestamps: Dict[str, float] = {}
        self.start_time: float = time.time()
        self._init_default_account()
    
    def _init_default_account(self):
        if TOKEN_PATH.exists():
            self.accounts.append(Account(
                id="default",
                name="默认账号",
                token_path=str(TOKEN_PATH)
            ))
    
    def get_available_account(self, session_id: Optional[str] = None) -> Optional[Account]:
        """获取可用账号（支持会话粘性）"""
        if session_id and session_id in self.session_locks:
            account_id = self.session_locks[session_id]
            ts = self.session_timestamps.get(session_id, 0)
            if time.time() - ts < 60:
                for acc in self.accounts:
                    if acc.id == account_id and acc.is_available():
                        self.session_timestamps[session_id] = time.time()
                        return acc
        
        available = [a for a in self.accounts if a.is_available()]
        if not available:
            return None
        
        account = min(available, key=lambda a: a.request_count)
        
        if session_id:
            self.session_locks[session_id] = account.id
            self.session_timestamps[session_id] = time.time()
        
        return account
    
    def mark_rate_limited(self, account_id: str, duration_seconds: int = 60):
        """标记账号限流"""
        for acc in self.accounts:
            if acc.id == account_id:
                acc.rate_limited_until = time.time() + duration_seconds
                acc.error_count += 1
                break
    
    def add_log(self, log: RequestLog):
        self.request_logs.append(log)
        self.total_requests += 1
        if log.error:
            self.total_errors += 1
    
    def get_stats(self) -> dict:
        uptime = time.time() - self.start_time
        return {
            "uptime_seconds": int(uptime),
            "total_requests": self.total_requests,
            "total_errors": self.total_errors,
            "error_rate": f"{(self.total_errors / max(1, self.total_requests) * 100):.1f}%",
            "accounts_total": len(self.accounts),
            "accounts_available": len([a for a in self.accounts if a.is_available()]),
            "recent_logs": len(self.request_logs)
        }


# 全局状态实例
state = ProxyState()
