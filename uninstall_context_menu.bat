@echo off
chcp 65001 >nul
title Uninstall PDF to Markdown Context Menu

echo ===================================================
echo   Removing PDF to Markdown Right-Click Menu
echo ===================================================
echo.

python "%~dp0setup_context_menu.py" --uninstall

echo.
echo ===================================================
pause
