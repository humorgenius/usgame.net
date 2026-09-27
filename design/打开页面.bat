@echo off
title usgame.net 本地预览 - 关闭此窗口即停止
cd /d "%~dp0.."
set PORT=8642
set PY=python
where python >nul 2>nul || set PY=py

echo ==============================================================
echo   usgame.net  本地预览服务
echo.
echo   服务目录 : %CD%
echo   服务地址 : http://127.0.0.1:%PORT%/
echo.
echo   【重要】必须用这种方式预览网页。
echo   直接双击 HTML 文件打开（file://）时，YouTube 会报
echo   "视频播放器配置错误 错误153"，那是 YouTube 的门禁，
echo   与网页代码无关，换成 http 打开就正常。
echo.
echo   关闭本窗口 = 停止服务
echo ==============================================================
echo.
echo 正在启动服务并打开页面...
start "" /b cmd /c "timeout /t 2 /nobreak >nul & start http://127.0.0.1:%PORT%/design/A-neon-vice/index.html"
start "" /b cmd /c "timeout /t 4 /nobreak >nul & start http://127.0.0.1:%PORT%/design/A-content-page/index.html"

echo.
echo 其他页面地址（可复制到浏览器打开）：
echo   B 新闻编辑部  http://127.0.0.1:%PORT%/design/B-newsroom-editorial/index.html
echo   C 抢劫档案    http://127.0.0.1:%PORT%/design/C-heist-dossier/index.html
echo   D 海报杂志    http://127.0.0.1:%PORT%/design/D-poster-magazine/index.html
echo   E Bento门户   http://127.0.0.1:%PORT%/design/E-bento-portal/index.html
echo.

%PY% -m http.server %PORT% --bind 127.0.0.1
