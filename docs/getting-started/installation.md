# Installation Guide

This guide will help you set up Ollama PDF RAG on your system. It covers the standard installation, Docker and Poetry-based installations, and includes ready-to-use Windows scripts (BAT and PowerShell).

---

## Prerequisites

Before installing Ollama PDF RAG, ensure you have:

1. **Python 3.9 or higher** installed  
2. **pip** (Python package installer)  
3. **git** installed  
4. **Ollama** installed on your system  
5. *(Optional)* **Docker** installed (for containerized deployment)  
6. *(Optional)* **Poetry** installed (for dependency management)

---

## Installing Ollama

1. Visit [Ollama's website](https://ollama.ai) to download and install the application.
2. After installation, pull the required models:
   ```bash
   ollama pull llama3.2  # or your preferred model
   ollama pull nomic-embed-text
   ```

---

## Standard Installation of Ollama PDF RAG

1. **Clone the repository:**
   ```bash
   git clone https://github.com/tonykipkemboi/ollama_pdf_rag.git
   cd ollama_pdf_rag
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # On macOS/Linux:
   python -m venv venv
   source venv/bin/activate

   # On Windows:
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## Alternative Installations

### Docker Installation

Use Docker to containerize the application.

1. **Create a Dockerfile** (place this in your project root):

   ```dockerfile
   # Use an official Python runtime as a parent image
   FROM python:3.10-slim

   # Set the working directory
   WORKDIR /app

   # Install system dependencies required by Poetry and your project
   RUN apt-get update && apt-get install -y --no-install-recommends \
       build-essential \
       && rm -rf /var/lib/apt/lists/*

   # Install Poetry
   RUN pip install poetry

   # Copy only the Poetry files to leverage Docker cache
   COPY pyproject.toml poetry.lock* /app/

   # Configure Poetry to install dependencies in the container
   RUN poetry config virtualenvs.create false \
       && poetry install --no-dev --no-interaction --no-ansi

   # Copy the rest of your application code
   COPY . /app

   # Specify the command to run your application
   CMD ["python", "your_script.py"]
   ```

2. **Build and run the Docker image:**

   ```bash
   docker build -t ollama_pdf_rag .
   docker run -d -p 8501:8501 ollama_pdf_rag
   ```

3. **Access your application** at `http://localhost:8501`.

4. *(Optional)* Use the following `docker-compose.yml` for a multi-container setup:

   ```yaml
   version: '3.8'

   services:
     app:
       build: .
       ports:
         - "8000:8000"  # Adjust if your app needs to expose a different port
       volumes:
         - .:/app     # Mount the current directory for live code updates (optional)
       environment:
         - ENV=production  # Add additional environment variables as needed
       command: python your_script.py  # Replace with your actual entrypoint command
   ```

### Poetry Installation

1. **Install Poetry** by following [Poetry's installation instructions](https://python-poetry.org/docs/#installation).
2. **In the project directory, install dependencies:**
   ```bash
   poetry install
   ```
3. **Activate the Poetry shell:**
   ```bash
   poetry shell
   ```
4. **Run the application:**
   ```bash
   python run.py
   ```

---

## Windows Installation Scripts

For Windows users, you can streamline the setup using provided Batch (BAT) and PowerShell (PS1) scripts.

### Batch Script (install.bat)

```bat
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
```

### PowerShell Script (install.ps1)

```powershell
$downloadUrl = "https://ollama.com/download/OllamaSetup.exe"
$installFolder = "C:\Ollama"
$installerPath = "$installFolder\OllamaSetup.exe"

# Ensure the installation directory exists
if (-not (Test-Path $installFolder)) {
    Write-Host "[INFO] Creating directory: $installFolder"
    New-Item -ItemType Directory -Path $installFolder -Force | Out-Null
}

# Download the installer if it doesn't exist
if (-not (Test-Path $installerPath)) {
    try {
        Write-Host "[INFO] Downloading OllamaSetup.exe..."
        Invoke-WebRequest -Uri $downloadUrl -OutFile $installerPath -ErrorAction Stop
        Write-Host "[INFO] Download complete."
    }
    catch {
        Write-Host "[ERROR] Failed to download the installer: $_"
        exit 1
    }
}
else {
    Write-Host "[INFO] Installer already exists, skipping download."
}

try {
    # Install Ollama silently
    Write-Host "[INFO] Installing Ollama silently..."
    $installProcess = Start-Process -FilePath $installerPath -ArgumentList "/silent" -NoNewWindow -Wait -PassThru
    if ($installProcess.ExitCode -ne 0) {
        throw "Installation failed with exit code: $($installProcess.ExitCode)"
    }
    Write-Host "[INFO] Installation complete."

    # Verify installation by checking if the 'ollama' command is available
    if (-not (Get-Command "ollama" -ErrorAction SilentlyContinue)) {
        throw "Ollama command not found. Installation might have failed."
    }

    # Pull model: llama3.2 non-interactively
    Write-Host "[INFO] Pulling model: llama3.2..."
    $pullLlama = Start-Process -FilePath "ollama" -ArgumentList "pull llama3.2" -NoNewWindow -Wait -PassThru
    if ($pullLlama.ExitCode -ne 0) {
        throw "Failed to pull model llama3.2. Exit code: $($pullLlama.ExitCode)"
    }
    Write-Host "[INFO] Model llama3.2 pulled successfully."

    # Pull model: nomic-embed-text non-interactively
    Write-Host "[INFO] Pulling model: nomic-embed-text..."
    $pullEmbed = Start-Process -FilePath "ollama" -ArgumentList "pull nomic-embed-text" -NoNewWindow -Wait -PassThru
    if ($pullEmbed.ExitCode -ne 0) {
        throw "Failed to pull model nomic-embed-text. Exit code: $($pullEmbed.ExitCode)"
    }
    Write-Host "[INFO] Model nomic-embed-text pulled successfully."
}
catch {
    Write-Host "[ERROR] $_"
    exit 1
}
finally {
    # Clean up installer file only; retain the installation folder for Ollama
    Write-Host "[INFO] Cleaning up installer file..."
    if (Test-Path $installerPath) {
        Remove-Item -Path $installerPath -Force
        Write-Host "[INFO] Installer file removed."
    }
}

Write-Host "[INFO] Ollama installation and model pulls finished successfully."
```

---

## Verifying Installation

1. **Start Ollama** in the background (if needed).  
2. **Run the application** (for standard installations):
   ```bash
   python run.py
   ```
3. **Open your browser** and navigate to `http://localhost:8501`.

---

## Troubleshooting

### Common Issues

#### ONNX DLL Error

If you see an error like:
```
DLL load failed while importing onnx_copy2py_export: a dynamic link library (DLL) initialization routine failed.
```
try the following:

1. **Install the latest Microsoft Visual C++ Redistributable** (both x64 and x86) from [Microsoft's website](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist) and restart your system.
2. **Reinstall ONNX Runtime:**
   ```bash
   pip uninstall onnxruntime onnxruntime-gpu
   pip install onnxruntime
   ```

#### CPU-Only Systems

For systems without a GPU:

1. Uninstall the GPU version:
   ```bash
   pip uninstall onnxruntime-gpu
   ```
2. Install the CPU version:
   ```bash
   pip install onnxruntime
   ```
3. Adjust processing chunk sizes if needed (reduce chunk size or increase overlap for better context).

---

## Next Steps

- Follow the [Quick Start Guide](quickstart.md) to begin using the application.
- Read the [User Guide](../user-guide/pdf-processing.md) for detailed usage instructions.

