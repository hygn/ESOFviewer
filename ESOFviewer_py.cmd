git clone https://gitlab.com/Hygn/esofviewer.git
cd esofviewer
pip install pycurl
pip install wget
pip install browser_cookie3
pip install youtube_dl
@echo off
cls
python ESOFviewer.py
echo.
echo Press any key to close this script
pause >nul
exit
