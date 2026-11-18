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

# Clients with their own theme format. Paths and formats come from their source code.
$others = @(foreach ($name in "dorion", "legcord", "replugged", "goofcord") {
    $path = Join-Path $env:APPDATA $name
    if (Test-Path $path) { [pscustomobject]@{ Kind = $name; Path = $path } }
})

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

function Get-ThemeVersion([string]$css) {
    $match = Select-String -Path $css -Pattern "@version (\S+)" | Select-Object -First 1
    if ($match) { return $match.Matches[0].Groups[1].Value }
    return "0.0.0"
}

function Install-Other($client, [string]$css) {
    switch ($client.Kind) {
        "dorion" {
            # Dorion keeps themes under the home folder on Windows, and its config in AppData.
            $themes = Join-Path $env:USERPROFILE "dorion\themes"
            New-Item -ItemType Directory -Force -Path $themes | Out-Null
            Copy-Item $css (Join-Path $themes $theme) -Force
            if (-not $NoEnable) {
                $file = Join-Path $client.Path "config.json"
                $data = Read-Json $file
                $list = @($data.themes | Where-Object { $_ -and $_ -ne $theme }) + $theme
                $data | Add-Member -NotePropertyName themes -NotePropertyValue $list -Force
                Write-Json $file $data
            }
            Write-Host "  installed: $($client.Path) (Dorion)"
        }
        "legcord" {
            $target = Join-Path $client.Path "themes\ReCord"
            New-Item -ItemType Directory -Force -Path $target | Out-Null
            Copy-Item $css (Join-Path $target "src.css") -Force
            $manifest = [ordered]@{
                id = "ReCord"; name = "ReCord"; author = "leriart"
                description = "A REPLACED-inspired terminal for Discord."
                version = (Get-ThemeVersion $css); source = "https://github.com/leriart/ReCord"
                theme = "src.css"; enabled = (-not $NoEnable)
            }
            Write-Json (Join-Path $target "manifest.json") $manifest
            Write-Host "  installed: $($client.Path) (Legcord)"
        }
        "replugged" {
            $target = Join-Path $client.Path "themes\dev.leriart.record"
            New-Item -ItemType Directory -Force -Path $target | Out-Null
            Copy-Item $css (Join-Path $target $theme) -Force
            $manifest = [ordered]@{
                id = "dev.leriart.record"; name = "ReCord"
                description = "A REPLACED-inspired terminal for Discord."
                author = [ordered]@{ name = "leriart"; github = "leriart" }
                version = (Get-ThemeVersion $css); license = "Apache-2.0"
                type = "replugged-theme"; main = $theme; source = "https://github.com/leriart/ReCord"
            }
            Write-Json (Join-Path $target "manifest.json") $manifest
            Write-Host "  installed: $($client.Path) (Replugged; enable ReCord in Settings > Themes)"
        }
        "goofcord" {
            # GoofCord loads every .css in this folder.
            $target = Join-Path $client.Path "GoofCord\assets"
            New-Item -ItemType Directory -Force -Path $target | Out-Null
            Copy-Item $css (Join-Path $target $theme) -Force
            Write-Host "  installed: $($client.Path) (GoofCord)"
        }
    }
}

function Uninstall-Other($client) {
    switch ($client.Kind) {
        "dorion" {
            $file = Join-Path $env:USERPROFILE "dorion\themes\$theme"
            if (-not (Test-Path $file)) { return }
            Remove-Item $file -Force
            $config = Join-Path $client.Path "config.json"
            $data = Read-Json $config
            $data | Add-Member -NotePropertyName themes -NotePropertyValue @($data.themes | Where-Object { $_ -and $_ -ne $theme }) -Force
            Write-Json $config $data
        }
        "legcord" { $dir = Join-Path $client.Path "themes\ReCord"; if (-not (Test-Path $dir)) { return }; Remove-Item $dir -Recurse -Force }
        "replugged" { $dir = Join-Path $client.Path "themes\dev.leriart.record"; if (-not (Test-Path $dir)) { return }; Remove-Item $dir -Recurse -Force }
        "goofcord" { $file = Join-Path $client.Path "GoofCord\assets\$theme"; if (-not (Test-Path $file)) { return }; Remove-Item $file -Force }
    }
    Write-Host "  removed: $($client.Path)"
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

if (-not $clients -and -not $others) {
    Write-Host "No supported client folder found (Vencord, Vesktop, Equicord, Equibop,"
    Write-Host "BetterDiscord, Dorion, Legcord, GoofCord, Replugged)."
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
    foreach ($client in $others) { Uninstall-Other $client }
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
    foreach ($client in $others) { Install-Other $client $tmp }
    Remove-Item $tmp -Force

    Install-Splash
    if (-not $NoPlugin) { Install-Plugin }
}

Write-Host ""
Write-Host "Done. Fully close Discord (also from the tray) and open it again."
