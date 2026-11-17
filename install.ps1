# ReCord installer for Windows (PowerShell 5.1 or newer).
#
#   irm https://raw.githubusercontent.com/leriart/ReCord/main/install.ps1 | iex
#   & ([scriptblock]::Create((irm https://raw.githubusercontent.com/leriart/ReCord/main/install.ps1))) -Uninstall
param(
    [switch]$Uninstall,
    [switch]$NoEnable
)

$ErrorActionPreference = "Stop"
$raw = "https://raw.githubusercontent.com/leriart/ReCord/main"
$theme = "ReCord.theme.css"
$legacy = "Retroless.theme.css"

$clients = foreach ($name in "Vencord", "vesktop", "Equicord", "equibop", "BetterDiscord") {
    $path = Join-Path $env:APPDATA $name
    if (Test-Path $path) { $path }
}

function Set-ThemeState([string]$file, [bool]$on) {
    if (-not (Test-Path $file)) { return $false }
    $data = Get-Content $file -Raw | ConvertFrom-Json
    $enabled = @($data.enabledThemes | Where-Object { $_ -and $_ -ne $theme -and $_ -ne $legacy })
    if ($on) { $enabled += $theme }
    $links = @($data.themeLinks | Where-Object { $_ -and $_ -notmatch "leriart/(Retroless|ReCord)" })
    $data | Add-Member -NotePropertyName enabledThemes -NotePropertyValue $enabled -Force
    $data | Add-Member -NotePropertyName themeLinks -NotePropertyValue $links -Force
    $json = $data | ConvertTo-Json -Depth 32
    [System.IO.File]::WriteAllText($file, $json, (New-Object System.Text.UTF8Encoding $false))
    return $true
}

if (-not $clients) {
    Write-Host "No Vencord, Vesktop, Equicord, Equibop or BetterDiscord folder found."
    Write-Host "Add this link in Themes > Online Themes instead:"
    Write-Host "  $raw/$theme"
    return
}

if ($Uninstall) {
    Write-Host "ReCord uninstall"
    foreach ($client in $clients) {
        $themes = Join-Path $client "themes"
        Remove-Item (Join-Path $themes $theme), (Join-Path $themes $legacy) -Force -ErrorAction SilentlyContinue
        [void](Set-ThemeState (Join-Path $client "settings\settings.json") $false)
        Write-Host "  removed: $client"
    }
} else {
    Write-Host "ReCord install"
    $tmp = Join-Path $env:TEMP $theme
    Invoke-WebRequest "$raw/$theme" -OutFile $tmp -UseBasicParsing
    if (-not (Select-String -Path $tmp -Pattern "@name ReCord" -Quiet)) { throw "Downloaded file is not the ReCord theme" }

    foreach ($client in $clients) {
        $themes = Join-Path $client "themes"
        New-Item -ItemType Directory -Force -Path $themes | Out-Null
        Copy-Item $tmp (Join-Path $themes $theme) -Force
        Remove-Item (Join-Path $themes $legacy) -Force -ErrorAction SilentlyContinue
        if (-not $NoEnable -and (Set-ThemeState (Join-Path $client "settings\settings.json") $true)) {
            Write-Host "  installed and enabled: $client"
        } else {
            Write-Host "  installed: $client (enable ReCord in Settings > Themes)"
        }
    }
    Remove-Item $tmp -Force
}

Write-Host ""
Write-Host "Done. Fully close Discord (also from the tray) and open it again."
