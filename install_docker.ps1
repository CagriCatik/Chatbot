# Set execution policy for the current process to bypass restrictions
Set-ExecutionPolicy Bypass -Scope Process -Force

# Set the appropriate security protocol (TLS 1.2 is required)
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072

# Attempt to install Chocolatey if it's not already installed
if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {
    Write-Output "Chocolatey not found. Installing Chocolatey..."
    Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
} else {
    Write-Output "Chocolatey is already installed."
}

# Attempt to install Docker Desktop using Chocolatey
Write-Output "Installing Docker Desktop..."
choco install docker-desktop --confirm

Write-Output "Installation complete. Please restart your computer if required."
