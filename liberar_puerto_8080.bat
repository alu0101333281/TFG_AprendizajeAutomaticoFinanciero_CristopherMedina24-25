@echo off
echo Buscando procesos en el puerto 8080...

for /f "tokens=5" %%a in ('netstat -aon ^| find ":8080" ^| find "LISTENING"') do (
    echo Terminando proceso con PID %%a...
    taskkill /PID %%a /F
)

echo Puerto 8080 liberado (si había algo usándolo).
pause
