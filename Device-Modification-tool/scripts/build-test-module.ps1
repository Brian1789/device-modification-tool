$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$module = Join-Path $root "modules\device-tool-test"
$out = Join-Path $root "modules\device-tool-test.zip"
if (Test-Path $out) { Remove-Item $out -Force }
Compress-Archive -Path (Join-Path $module "*") -DestinationPath $out
Write-Output "Created $out"
