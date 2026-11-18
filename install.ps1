# ReCord installer for Windows (PowerShell 5.1 or newer).
#
#   irm https://raw.githubusercontent.com/leriart/ReCord/main/install.ps1 | iex
#   & ([scriptblock]::Create((irm https://raw.githubusercontent.com/leriart/ReCord/main/install.ps1))) -NoPlugin
#   & ([scriptblock]::Create((irm https://raw.githubusercontent.com/leriart/ReCord/main/install.ps1))) -Uninstall
#   & ([scriptblock]::Create((irm https://raw.githubusercontent.com/leriart/ReCord/main/install.ps1))) -Doctor
param(
    [switch]$Uninstall,
    [switch]$NoEnable,
    [switch]$NoPlugin,
    [switch]$Doctor
)

$ErrorActionPreference = "Stop"
# Windows PowerShell 5.1 still defaults to old TLS versions on some machines and
# GitHub only accepts TLS 1.2 and newer.
try {
    [Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12
} catch { }
$raw = "https://raw.githubusercontent.com/leriart/ReCord/main"
$pluginRelease = "https://github.com/leriart/ReCord/releases/download/plugin"
$pluginFiles = "vencordDesktopMain.js", "vencordDesktopPreload.js", "vencordDesktopRenderer.js", "vencordDesktopRenderer.css"
$cachebust = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
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

function Get-DiscordProcesses {
    $names = "Vesktop", "Discord", "DiscordCanary", "DiscordPTB", "Equibop", "Dorion", "Legcord", "GoofCord"
    @(Get-Process -Name $names -ErrorAction SilentlyContinue)
}

# Invoke-WebRequest is tried twice, then curl.exe, which ships with Windows 10
# and later. Windows PowerShell turns any stderr from a native command into a
# terminating error while $ErrorActionPreference is Stop, so curl.exe runs with
# it relaxed.
function Get-Remote([string]$url, [string]$file) {
    $last = "unknown error"
    for ($try = 1; $try -le 2; $try++) {
        try {
            Remove-Item $file -Force -ErrorAction SilentlyContinue
            Invoke-WebRequest $url -OutFile $file -UseBasicParsing -ErrorAction Stop
            if ((Get-Item $file).Length -gt 512) { return }
            throw "the downloaded file is empty"
        } catch {
            $last = $_.Exception.Message
        }
    }
    $curl = Get-Command curl.exe -ErrorAction SilentlyContinue
    if ($curl) {
        Remove-Item $file -Force -ErrorAction SilentlyContinue
        $code = 1
        $previous = $ErrorActionPreference
        $ErrorActionPreference = "Continue"
        try {
            & curl.exe -fsSL --retry 2 --connect-timeout 20 -o $file $url 2>$null
            $code = $LASTEXITCODE
        } finally {
            $ErrorActionPreference = $previous
        }
        if ($code -eq 0 -and (Test-Path $file) -and (Get-Item $file).Length -gt 512) { return }
        $last = "curl.exe exit code $code"
    }
    throw "could not download $url ($last)"
}

function Test-Release {
    try {
        $response = Invoke-WebRequest "$pluginRelease/vencordDesktopMain.js?$cachebust" -UseBasicParsing -ErrorAction Stop
        return "reachable (HTTP $($response.StatusCode))"
    } catch {
        return "unreachable: $($_.Exception.Message)"
    }
}

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
            Remove-Item (Join-Path $themes $legacy) -Force -ErrorAction SilentlyContinue
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
            if (Test-Path $target) { Remove-Item $target -Recurse -Force }
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
            if (Test-Path $target) { Remove-Item $target -Recurse -Force }
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
            Remove-Item (Join-Path $target $legacy) -Force -ErrorAction SilentlyContinue
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
    try {
        Get-Remote "$raw/assets/brand/splash.gif?$cachebust" $tmp
    } catch {
        Write-Host "  The splash could not be downloaded: $($_.Exception.Message)"
        Write-Host "  The theme and the plugin are not affected."
        return
    }
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
    Remove-Item $tmp -Force -ErrorAction SilentlyContinue
}

function Install-Plugin {
    Write-Host "== Plugin"
    if (-not $vesktop) {
        Write-Host "  Vesktop not found, so the plugin was skipped."
        Write-Host "  The plugin is a Vencord user plugin and only Vesktop loads it without rebuilding."
        Write-Host "  The theme works without it."
        return
    }
    $stage = Join-Path $env:TEMP ("record-vencord-" + [guid]::NewGuid().ToString("N"))
    New-Item -ItemType Directory -Force -Path $stage | Out-Null
    try {
        foreach ($file in $pluginFiles) { Get-Remote "$pluginRelease/${file}?${cachebust}" (Join-Path $stage $file) }
    } catch {
        Write-Host "  The ready-made plugin build could not be downloaded."
        Write-Host "  $($_.Exception.Message)"
        Write-Host "  The theme is installed and works; the plugin needs this download."
        Write-Host "  Check the connection and run this again. If it keeps failing, report it at"
        Write-Host "  https://github.com/leriart/ReCord/issues"
        Remove-Item $stage -Recurse -Force -ErrorAction SilentlyContinue
        return
    }
    $small = @($pluginFiles | Where-Object {
        $file = Join-Path $stage $_
        (-not (Test-Path $file)) -or ((Get-Item $file).Length -lt 1024)
    })
    if ($small) {
        Write-Host "  The plugin build is incomplete: $($small -join ', ')"
        Remove-Item $stage -Recurse -Force -ErrorAction SilentlyContinue
        return
    }
    foreach ($client in $vesktop) {
        $target = Join-Path $client "record-vencord"
        $next = "$target.new"
        if (Test-Path $next) { Remove-Item $next -Recurse -Force }
        New-Item -ItemType Directory -Force -Path $next | Out-Null
        foreach ($file in $pluginFiles) { Copy-Item (Join-Path $stage $file) (Join-Path $next $file) -Force }
        [System.IO.File]::WriteAllText((Join-Path $next "package.json"), "{}", $utf8)
        if (Test-Path $target) { Remove-Item $target -Recurse -Force }
        Move-Item $next $target
        $state = Join-Path $client "state.json"
        $data = Read-Json $state
        $data | Add-Member -NotePropertyName vencordDir -NotePropertyValue $target -Force
        Write-Json $state $data
        [void](Set-PluginState (Join-Path $client "settings\settings.json") $true)
        $missing = @($pluginFiles | Where-Object { -not (Test-Path (Join-Path $target $_)) })
        if ($missing) {
            Write-Host "  failed: $target is missing $($missing -join ', ')"
        } else {
            Write-Host "  installed and enabled: $target"
        }
    }
    Remove-Item $stage -Recurse -Force -ErrorAction SilentlyContinue
}

function Show-Doctor {
    Write-Host "ReCord doctor"
    Write-Host "== Clients"
    if (-not $clients -and -not $others) { Write-Host "  none found in $env:APPDATA" }
    foreach ($client in $clients) {
        $name = Split-Path $client -Leaf
        $file = Join-Path $client "themes\$theme"
        if (Test-Path $file) {
            $match = Select-String -Path $file -Pattern "@version (\S+)" | Select-Object -First 1
            Write-Host "  $name`: theme installed ($($match.Matches[0].Groups[1].Value))"
        } else {
            Write-Host "  $name`: theme not installed"
        }
    }
    foreach ($client in $others) { Write-Host "  $($client.Kind): theme folder $($client.Path)" }
    if (-not $clients -and -not $others) { Write-Host "  run your client once, then run this again" }

    Write-Host "== Plugin"
    if (-not $vesktop) {
        Write-Host "  Vesktop not found. Only Vesktop loads the plugin without rebuilding Vencord."
    } else {
        Write-Host "  ready-made build: $(Test-Release)"
        foreach ($client in $vesktop) {
            $target = Join-Path $client "record-vencord"
            $missing = @($pluginFiles | Where-Object { -not (Test-Path (Join-Path $target $_)) })
            $state = Read-Json (Join-Path $client "state.json")
            $settings = Read-Json (Join-Path $client "settings\settings.json")
            $enabled = "not set"
            if ($settings.plugins -and $settings.plugins.ReCord) { $enabled = "$($settings.plugins.ReCord.enabled)" }
            Write-Host "  $client"
            if ($missing) { Write-Host "    build: missing $($missing -join ', ')" } else { Write-Host "    build: installed cleanly" }
            if ($state.vencordDir) { Write-Host "    Vesktop points at: $($state.vencordDir)" } else { Write-Host "    Vesktop points at: nothing (state.json has no vencordDir)" }
            Write-Host "    plugin enabled: $enabled"
        }
    }

    Write-Host "== Running"
    $running = Get-DiscordProcesses
    if ($running) {
        Write-Host "  $((($running | Select-Object -ExpandProperty ProcessName -Unique) -join ', '))"
        Write-Host "  Close it completely (also from the tray) before installing or uninstalling."
    } else {
        Write-Host "  nothing"
    }
}

if ($Doctor) {
    Show-Doctor
    return
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
    $running = Get-DiscordProcesses
    if ($running) {
        $names = ($running | Select-Object -ExpandProperty ProcessName -Unique) -join ", "
        Write-Host "Discord is running: $names"
        Write-Host "Close it completely, also from the tray, and run this again."
        Write-Host "Nothing has been changed: a running client rewrites its settings on exit"
        Write-Host "and would undo the plugin setup."
        return
    }
    Write-Host "== Theme"
    $tmp = Join-Path $env:TEMP $theme
    Get-Remote "$raw/${theme}?${cachebust}" $tmp
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
Write-Host "The plugin settings appear in Discord under Plugins > ReCord."
