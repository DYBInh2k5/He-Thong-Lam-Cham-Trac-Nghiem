@echo off
echo ========================================
echo    UPDATE HE THONG - TU DONG DEPLOY
echo ========================================
echo.

echo [1/4] Kiem tra thay doi...
git status
echo.

echo [2/4] Add files da thay doi...
git add .
echo OK - Da add files

echo.
echo [3/4] Commit thay doi...
set /p message="Nhap mo ta thay doi (Enter de dung mac dinh): "
if "%message%"=="" set message=Update: Cap nhat he thong

git commit -m "%message%"
echo OK - Da commit

echo.
echo [4/4] Push len GitHub...
git push origin main
echo OK - Da push

echo.
echo ========================================
echo    UPDATE THANH CONG!
echo ========================================
echo.
echo Render.com se TU DONG deploy lai sau 1-2 phut
echo.
echo Kiem tra tien trinh deploy tai:
echo https://dashboard.render.com
echo.
pause
