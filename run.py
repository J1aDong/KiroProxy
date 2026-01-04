#!/usr/bin/env python3
"""Kiro API Proxy 启动脚本"""
import sys

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    
    from kiro_proxy.main import run
    run(port)
