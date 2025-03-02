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
