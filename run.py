#!/usr/bin/env python3
"""Kiro API Proxy 启动脚本"""
import sys

if __name__ == "__main__":
    # CLI 子命令模式
    if len(sys.argv) > 1 and sys.argv[1] in ("accounts", "login", "status", "serve"):
        from kiro_proxy.cli import main
        main()
    
    # --no-ui 模式：跳过 UI 直接启动
    elif len(sys.argv) > 1 and sys.argv[1] == "--no-ui":
        port = int(sys.argv[2]) if len(sys.argv) > 2 else 8080
        from kiro_proxy.main import run
        run(port)
    
    # 兼容旧的启动方式: python run.py [port] (数字参数)
    elif len(sys.argv) > 1 and sys.argv[1].isdigit():
        port = int(sys.argv[1])
        from kiro_proxy.main import run
        run(port)
    
    # 默认：显示端口配置 UI
    else:
        from kiro_proxy.launcher import launch_with_ui
        launch_with_ui()
