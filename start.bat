@echo off
chcp 65001 >nul
echo ========================================
echo Запуск Cobalt
echo ========================================
echo.

REM Проверка установки Node.js
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo [ОШИБКА] Node.js не установлен!
    echo Скачайте с https://nodejs.org/
    pause
    exit /b 1
)

REM Проверка установки pnpm
where pnpm >nul 2>nul
if %errorlevel% neq 0 (
    echo [ОШИБКА] pnpm не установлен!
    echo Установите командой: npm install -g pnpm
    pause
    exit /b 1
)

echo [1/3] Установка зависимостей...
call pnpm install
if %errorlevel% neq 0 (
    echo [ОШИБКА] Не удалось установить зависимости
    pause
    exit /b 1
)

echo.
echo [2/3] Запуск API сервера...
start "Cobalt API" cmd /k "cd api && pnpm start"

timeout /t 3 /nobreak >nul

echo.
echo [3/3] Запуск веб-сервера...
start "Cobalt Web" cmd /k "cd web && pnpm dev"

echo.
echo ========================================
echo Cobalt запущен!
echo ========================================
echo API: http://localhost:9000
echo Web: http://localhost:5173
echo.
echo Для остановки закройте окна серверов
echo ========================================
pause
