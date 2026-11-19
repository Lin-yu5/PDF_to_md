@echo off
chcp 65001 >nul
title Install PDF to Markdown Context Menu

echo ===================================================
echo   Installing PDF to Markdown Right-Click Menu
echo ===================================================
echo.

python "%~dp0setup_context_menu.py" --install

echo.
echo ===================================================
pause
