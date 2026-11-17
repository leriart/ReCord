# ReCord installer for Windows (PowerShell 5.1 or newer).
#
#   irm https://raw.githubusercontent.com/leriart/ReCord/main/install.ps1 | iex
#   & ([scriptblock]::Create((irm https://raw.githubusercontent.com/leriart/ReCord/main/install.ps1))) -NoPlugin
#   & ([scriptblock]::Create((irm https://raw.githubusercontent.com/leriart/ReCord/main/install.ps1))) -Uninstall
param(
    [switch]$Uninstall,
    [switch]$NoEnable,
    [switch]$NoPlugin
)

$ErrorActionPreference = "Stop"
$raw = "https://raw.githubusercontent.com/leriart/ReCord/main"
$pluginRelease = "https://github.com/leriart/ReCord/releases/download/plugin"
$pluginFiles = "vencordDesktopMain.js", "vencordDesktopPreload.js", "vencordDesktopRenderer.js", "vencordDesktopRenderer.css"
$theme = "ReCord.theme.css"
$legacy = "Retroless.theme.css"
$utf8 = New-Object System.Text.UTF8Encoding $false

$clients = @(foreach ($name in "Vencord", "vesktop", "Equicord", "equibop", "BetterDiscord") {
    $path = Join-Path $env:APPDATA $name
    if (Test-Path $path) { $path }
})
$vesktop = @($clients | Where-Object { (Split-Path $_ -Leaf) -eq "vesktop" })

function Read-Json([string]$file) {
    if (Test-Path $file) { return Get-Content $file -Raw | ConvertFrom-Json }
    return New-Object PSObject
}

function Write-Json([string]$file, $data) {
    New-Item -ItemType Directory -Force -Path (Split-Path $file -Parent) | Out-Null
    [System.IO.File]::WriteAllText($file, ($data | ConvertTo-Json -Depth 32), $utf8)
}

function Set-ThemeState([string]$file, [bool]$on) {
    if (-not (Test-Path $file)) { return $false }
    $data = Read-Json $file
    $enabled = @($data.enabledThemes | Where-Object { $_ -and $_ -ne $theme -and $_ -ne $legacy })
    if ($on) { $enabled += $theme }
    $links = @($data.themeLinks | Where-Object { $_ -and $_ -notmatch "leriart/(Retroless|ReCord)" })
    $data | Add-Member -NotePropertyName enabledThemes -NotePropertyValue $enabled -Force
    $data | Add-Member -NotePropertyName themeLinks -NotePropertyValue $links -Force
    Write-Json $file $data
    return $true
}

function Set-PluginState([string]$file, [bool]$on) {
    $data = Read-Json $file
    if (-not $data.plugins) { $data | Add-Member -NotePropertyName plugins -NotePropertyValue (New-Object PSObject) -Force }
    if ($on) {
        $entry = if ($data.plugins.ReCord) { $data.plugins.ReCord } else { New-Object PSObject }
        $entry | Add-Member -NotePropertyName enabled -NotePropertyValue $true -Force
        $data.plugins | Add-Member -NotePropertyName ReCord -NotePropertyValue $entry -Force
    } else {
        $data.plugins.PSObject.Properties.Remove("ReCord")
    }
    Write-Json $file $data
}

function Install-Splash {
    Write-Host "== Startup splash"
    if (-not $vesktop) { Write-Host "  Vesktop not found; only Vesktop has a replaceable splash."; return }
    $tmp = Join-Path $env:TEMP "record-splash.gif"
    Invoke-WebRequest "$raw/assets/brand/splash.gif" -OutFile $tmp -UseBasicParsing
    foreach ($client in $vesktop) {
        $assets = Join-Path $client "userAssets"
        New-Item -ItemType Directory -Force -Path $assets | Out-Null
        Copy-Item $tmp (Join-Path $assets "splash") -Force
        $file = Join-Path $client "settings.json"
        $data = Read-Json $file
        $data | Add-Member -NotePropertyName splashTheming -NotePropertyValue $true -Force
        $data | Add-Member -NotePropertyName splashPixelated -NotePropertyValue $true -Force
        $data | Add-Member -NotePropertyName splashColor -NotePropertyValue "rgb(240, 222, 198)" -Force
        $data | Add-Member -NotePropertyName splashBackground -NotePropertyValue "rgb(5, 6, 5)" -Force
        Write-Json $file $data
        Write-Host "  installed: $client"
    }
    Remove-Item $tmp -Force
}

function Install-Plugin {
    Write-Host "== Plugin"
    if (-not $vesktop) { Write-Host "  Vesktop not found, so the plugin was skipped. The theme works without it."; return }
    $stage = Join-Path $env:TEMP "record-vencord"
    New-Item -ItemType Directory -Force -Path $stage | Out-Null
    try {
        foreach ($file in $pluginFiles) {
            Invoke-WebRequest "$pluginRelease/$file" -OutFile (Join-Path $stage $file) -UseBasicParsing
        }
    } catch {
        Write-Host "  The ready-made plugin build could not be downloaded; skipped. The theme is still installed."
        return
    }
    foreach ($client in $vesktop) {
        $target = Join-Path $client "record-vencord"
        New-Item -ItemType Directory -Force -Path $target | Out-Null
        foreach ($file in $pluginFiles) { Copy-Item (Join-Path $stage $file) (Join-Path $target $file) -Force }
        [System.IO.File]::WriteAllText((Join-Path $target "package.json"), "{}", $utf8)
        $state = Join-Path $client "state.json"
        $data = Read-Json $state
        $data | Add-Member -NotePropertyName vencordDir -NotePropertyValue $target -Force
        Write-Json $state $data
        Set-PluginState (Join-Path $client "settings\settings.json") $true
        Write-Host "  installed and enabled: $target"
    }
    Remove-Item $stage -Recurse -Force
}

if (-not $clients) {
    Write-Host "No Vencord, Vesktop, Equicord, Equibop or BetterDiscord folder found."
    Write-Host "Start your client once, or add this link in Themes > Online Themes:"
    Write-Host "  $raw/$theme"
    return
}

if ($Uninstall) {
    Write-Host "ReCord uninstall"
    Write-Host "== Theme"
    foreach ($client in $clients) {
        $themes = Join-Path $client "themes"
        Remove-Item (Join-Path $themes $theme), (Join-Path $themes $legacy) -Force -ErrorAction SilentlyContinue
        [void](Set-ThemeState (Join-Path $client "settings\settings.json") $false)
        Write-Host "  removed: $client"
    }
    foreach ($client in $vesktop) {
        $splash = Join-Path $client "userAssets\splash"
        if (Test-Path $splash) {
            Remove-Item $splash -Force
            $file = Join-Path $client "settings.json"
            $data = Read-Json $file
            foreach ($key in "splashTheming", "splashPixelated", "splashColor", "splashBackground") { $data.PSObject.Properties.Remove($key) }
            Write-Json $file $data
        }
        $target = Join-Path $client "record-vencord"
        if (Test-Path $target) {
            Remove-Item $target -Recurse -Force
            $state = Join-Path $client "state.json"
            $data = Read-Json $state
            $data.PSObject.Properties.Remove("vencordDir")
            Write-Json $state $data
            Set-PluginState (Join-Path $client "settings\settings.json") $false
            Write-Host "  plugin removed: $client (stock Vencord will load again)"
        }
    }
} else {
    Write-Host "ReCord install"
    Write-Host "== Theme"
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

    Install-Splash
    if (-not $NoPlugin) { Install-Plugin }
}

Write-Host ""
Write-Host "Done. Fully close Discord (also from the tray) and open it again."
