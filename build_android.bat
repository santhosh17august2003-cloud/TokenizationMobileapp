@echo off
setlocal

echo Building Tokenization Demo Android APK...

set "BACKUP_REQUIREMENTS=%TEMP%\tokenization_requirements_%RANDOM%.txt"
copy /Y requirements.txt "%BACKUP_REQUIREMENTS%" >NUL
copy /Y mobile_requirements.txt requirements.txt >NUL

flet build apk
set "BUILD_EXIT_CODE=%ERRORLEVEL%"

copy /Y "%BACKUP_REQUIREMENTS%" requirements.txt >NUL
del /Q "%BACKUP_REQUIREMENTS%" >NUL 2>NUL

if not "%BUILD_EXIT_CODE%"=="0" (
    echo.
    echo APK build failed. Install Android Studio and ensure the Android SDK is configured.
    exit /b %BUILD_EXIT_CODE%
)

echo.
echo APK created under the build\apk folder.