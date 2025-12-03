@echo off
echo ========================================
echo    DEPLOY HE THONG CHAM TRAC NGHIEM
echo ========================================
echo.

echo [1/5] Kiem tra Git...
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git chua duoc cai dat!
    echo Vui long tai Git tai: https://git-scm.com/download/win
    pause
    exit /b 1
)
echo OK - Git da san sang

echo.
echo [2/5] Khoi tao Git repository...
if not exist .git (
    git init
    echo OK - Da khoi tao Git
) else (
    echo OK - Git repository da ton tai
)

echo.
echo [3/5] Add files...
git add .
echo OK - Da add files

echo.
echo [4/5] Commit...
git commit -m "Deploy: He thong cham trac nghiem"
echo OK - Da commit

echo.
echo [5/5] Huong dan tiep theo:
echo.
echo 1. Tao repository tren GitHub:
echo    https://github.com/new
echo.
echo 2. Chay lenh sau (thay YOUR_USERNAME):
echo    git remote add origin https://github.com/YOUR_USERNAME/he-thong-cham-trac-nghiem.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo 3. Deploy tren Render.com:
echo    https://render.com
echo    - New + ^> Web Service
echo    - Connect repository
echo    - Deploy!
echo.
echo ========================================
echo    SAn SANG DEPLOY!
echo ========================================
pause
