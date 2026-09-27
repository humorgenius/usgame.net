@echo off
chcp 65001 >nul
rem ==== 打开 usgame.net 的 5 个首页设计方案 ====
rem 双击本文件即可在默认浏览器里打开全部 5 个方案（每个一个标签页）

set DIR=%~dp0

start "" "%DIR%A-neon-vice\index.html"
start "" "%DIR%B-newsroom-editorial\index.html"
start "" "%DIR%C-heist-dossier\index.html"
start "" "%DIR%D-poster-magazine\index.html"
start "" "%DIR%E-bento-portal\index.html"

echo.
echo 已打开 5 个方案：
echo   1. A-neon-vice           霓虹罪恶城
echo   2. B-newsroom-editorial  新闻编辑部
echo   3. C-heist-dossier       行动档案 / 终端
echo   4. D-poster-magazine     杂志封面
echo   5. E-bento-portal        Bento 工具门户
echo.
echo 提示：页面右上角可以切换 中文 / EN，点导航里的筛选标签可以试筛选。
echo.
pause
