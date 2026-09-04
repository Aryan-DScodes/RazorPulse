@echo off
title RazorPulse Orchestrator
echo ===================================================
echo   🛡️ Starting RazorPulse Enterprise Architecture
echo ===================================================
echo.

echo [1/3] Booting FastAPI State Engine (T-0)...
start "RazorPulse Backend" cmd /k "uvicorn app.main:app --reload"
timeout /t 3 /nobreak >nul

echo [2/3] Booting Merchant Traffic Generator...
start "RazorPulse Traffic" cmd /k "python synthetic/generator.py"
timeout /t 2 /nobreak >nul

echo [3/3] Booting Observability Dashboard (UI)...
start "RazorPulse UI" cmd /k "streamlit run dashboard/app.py"

echo.
echo ✅ All microservices running. 
echo 📡 The dashboard will open in your browser shortly.
pause