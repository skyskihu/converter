@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

npx wrangler deploy

pause