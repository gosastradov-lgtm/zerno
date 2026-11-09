"""
Zerno Coffee - Application Server Runner.
Launches the full-stack web application with C# .NET engine, SQLite, and 1C export.
"""

import os
import sys
import subprocess

# Ensure project root is available in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

try:
    import uvicorn
except (ImportError, ModuleNotFoundError):
    print("[INIT] Installing required runtime package 'uvicorn'...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "uvicorn>=0.29.0"])
    import uvicorn

def check_and_build_csharp():
    exe_path = os.path.join(BASE_DIR, "csharp_engine", "FiscalEngine.exe")
    cs_path = os.path.join(BASE_DIR, "csharp_engine", "FiscalEngine.cs")
    csc_path = r"C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe"

    if not os.path.exists(exe_path) and os.path.exists(csc_path) and os.path.exists(cs_path):
        print("[INIT] Compiling C# FiscalEngine.exe via Windows .NET Framework...")
        cmd = [csc_path, "/nologo", "/optimize+", "/r:System.Web.Extensions.dll", f"/out:{exe_path}", cs_path]
        res = subprocess.run(cmd)
        if res.returncode == 0:
            print("[SUCCESS] C# FiscalEngine.exe ready!")

def main():
    # 1. Initialize SQLite database & migrations
    from backend.database import init_db
    init_db()

    # 2. Check C# Engine binary
    check_and_build_csharp()

    print("=" * 64)
    print(" ☕ ZERNO — СЕТЬ РЕСТОРАНОВ И КОФЕЕН SPECIALTY")
    print("=" * 64)
    print(" Сервер запущен по адресу: http://127.0.0.1:8000")
    print(" Swagger API Документация: http://127.0.0.1:8000/docs")
    print(" Демо-аккаунты для входа в 1 клик:")
    print("   • Администратор: admin@zerno.coffee / admin123")
    print("   • Гость кофейни: alex@zerno.coffee / guest123")
    print("=" * 64)

    # 3. Start Uvicorn
    uvicorn.run("backend.app:app", host="127.0.0.1", port=8000, reload=False)

if __name__ == "__main__":
    main()

