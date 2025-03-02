@echo off
setlocal

REM Define variables
set "downloadUrl=https://ollama.com/download/OllamaSetup.exe"
set "installFolder=C:\Ollama"
set "installerPath=%installFolder%\OllamaSetup.exe"

REM Ensure the installation directory exists
if not exist "%installFolder%" (
    echo [INFO] Creating directory: %installFolder%
    mkdir "%installFolder%"
)

REM Download the installer if it doesn't exist
if not exist "%installerPath%" (
    echo [INFO] Downloading OllamaSetup.exe...
    curl -L -o "%installerPath%" "%downloadUrl%"
    if errorlevel 1 (
        echo [ERROR] Failed to download the installer.
        exit /b 1
    ) else (
        echo [INFO] Download complete.
    )
) else (
    echo [INFO] Installer already exists, skipping download.
)

REM Install Ollama silently
echo [INFO] Installing Ollama silently...
"%installerPath%" /silent
if errorlevel 1 (
    echo [ERROR] Installation failed with exit code %errorlevel%.
    exit /b 1
)
echo [INFO] Installation complete.

REM Verify installation by checking if the 'ollama' command is available
where ollama >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Ollama command not found. Installation might have failed.
    exit /b 1
)

REM Pull model: llama3.2 non-interactively
echo [INFO] Pulling model: llama3.2...
ollama pull llama3.2
if errorlevel 1 (
    echo [ERROR] Failed to pull model llama3.2. Exit code: %errorlevel%.
    exit /b 1
)
echo [INFO] Model llama3.2 pulled successfully.

REM Pull model: nomic-embed-text non-interactively
echo [INFO] Pulling model: nomic-embed-text...
ollama pull nomic-embed-text
if errorlevel 1 (
    echo [ERROR] Failed to pull model nomic-embed-text. Exit code: %errorlevel%.
    exit /b 1
)
echo [INFO] Model nomic-embed-text pulled successfully.

REM Clean up installer file only; retain the installation folder
echo [INFO] Cleaning up installer file...
if exist "%installerPath%" (
    del /f "%installerPath%"
    echo [INFO] Installer file removed.
)

echo [INFO] Ollama installation and model pulls finished successfully.
endlocal
