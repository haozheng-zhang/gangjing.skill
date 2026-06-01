$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

python -m pip install -e .
python -m pip install pyinstaller
python -m PyInstaller `
  --noconfirm `
  --clean `
  --onefile `
  --noconsole `
  --name gangjing-skill `
  gangjing_app.py

Write-Host "Built: $root\dist\gangjing-skill.exe"
