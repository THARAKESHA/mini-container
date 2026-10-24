@echo off
title Mini-Container: OS Project Demonstration
color 0B

echo ========================================================================
echo        MINI-CONTAINER: OPERATING SYSTEMS PROJECT DEMONSTRATION         
echo        Team: Tharakesha M (24BCE2538) ^& Mathu Metha S (24BCE2805)       
echo ========================================================================
echo.
echo Launching Interactive Container Demonstration in WSL...
echo.

wsl -u root --cd /mnt/c/Users/thara/.gemini/antigravity/scratch/mini-container bash interactive_menu.sh

echo.
echo ========================================================================
echo Container session ended.
echo ========================================================================
pause
