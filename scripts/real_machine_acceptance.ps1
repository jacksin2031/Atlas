[CmdletBinding()]
param(
  [string]$InstallerPath,
  [string]$AtlasExe,
  [string]$ProjectPath,
  [string]$EvidenceDir = (Join-Path (Get-Location) "atlas-real-machine-evidence"),
  [ValidateRange(1, 100)]
  [int]$LifecycleCycles = 10,
  [ValidateRange(1, 1440)]
  [int]$SoakMinutes = 60,
  [ValidateRange(1, 60)]
  [int]$SoakSampleMinutes = 15,
  [switch]$RunLifecycle,
  [switch]$RunSoak,
  [switch]$PlanOnly
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Write-JsonFile {
  param([Parameter(Mandatory)][object]$Value, [Parameter(Mandatory)][string]$Path)
  $Value | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $Path -Encoding UTF8
}

function Get-AtlasOwnedProcesses {
  param([Parameter(Mandatory)][string]$InstallRoot)
  $root = [IO.Path]::GetFullPath($InstallRoot)
  return @(Get-CimInstance Win32_Process | Where-Object {
    $_.ExecutablePath -and
    $_.ExecutablePath.StartsWith($root, [StringComparison]::OrdinalIgnoreCase) -and
    $_.Name -match '^(atlas-desktop|python|pythonw)\.exe$'
  })
}

function Get-ProcessEvidence {
  param([Parameter(Mandatory)][string]$InstallRoot)
  return @(Get-AtlasOwnedProcesses -InstallRoot $InstallRoot | ForEach-Object {
    $workingSet = $null
    try { $workingSet = (Get-Process -Id $_.ProcessId -ErrorAction Stop).WorkingSet64 } catch {}
    [ordered]@{
      pid = $_.ProcessId
      parentPid = $_.ParentProcessId
      name = $_.Name
      executablePath = $_.ExecutablePath
      workingSetBytes = $workingSet
    }
  })
}

function Assert-NoAtlasOwnedProcesses {
  param([Parameter(Mandatory)][string]$InstallRoot, [Parameter(Mandatory)][string]$Context)
  $left = @(Get-AtlasOwnedProcesses -InstallRoot $InstallRoot)
  if ($left.Count -gt 0) {
    throw "$Context left Atlas-owned processes: $($left.ProcessId -join ', ')"
  }
}

function Get-MachineEvidence {
  $os = Get-CimInstance Win32_OperatingSystem
  $computer = Get-CimInstance Win32_ComputerSystem
  $video = @(Get-CimInstance Win32_VideoController | ForEach-Object {
    [ordered]@{
      name = $_.Name
      driverVersion = $_.DriverVersion
      currentHorizontalResolution = $_.CurrentHorizontalResolution
      currentVerticalResolution = $_.CurrentVerticalResolution
      currentRefreshRate = $_.CurrentRefreshRate
    }
  })
  $monitors = @(Get-CimInstance Win32_DesktopMonitor | ForEach-Object {
    [ordered]@{
      name = $_.Name
      pnpDeviceId = $_.PNPDeviceID
      screenWidth = $_.ScreenWidth
      screenHeight = $_.ScreenHeight
      status = $_.Status
    }
  })
  $dpi = Get-ItemProperty -LiteralPath "HKCU:\Control Panel\Desktop" -ErrorAction SilentlyContinue
  $screenLayout = @()
  try {
    Add-Type -AssemblyName System.Windows.Forms
    $screenLayout = @([System.Windows.Forms.Screen]::AllScreens | ForEach-Object {
      [ordered]@{
        deviceName = $_.DeviceName
        primary = $_.Primary
        bounds = [ordered]@{ x = $_.Bounds.X; y = $_.Bounds.Y; width = $_.Bounds.Width; height = $_.Bounds.Height }
        workingArea = [ordered]@{ x = $_.WorkingArea.X; y = $_.WorkingArea.Y; width = $_.WorkingArea.Width; height = $_.WorkingArea.Height }
      }
    })
  } catch {
    $screenLayout = @([ordered]@{ unavailable = $true; reason = "System.Windows.Forms screen enumeration unavailable" })
  }

  $webView2 = @()
  $uninstallRoots = @(
    "HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*",
    "HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*",
    "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*"
  )
  foreach ($root in $uninstallRoots) {
    $webView2 += @(Get-ItemProperty -Path $root -ErrorAction SilentlyContinue | Where-Object {
      $_.DisplayName -like "*WebView2*Runtime*"
    } | ForEach-Object {
      [ordered]@{ displayName = $_.DisplayName; displayVersion = $_.DisplayVersion; installLocation = $_.InstallLocation }
    })
  }

  $identity = [Security.Principal.WindowsIdentity]::GetCurrent()
  $principal = [Security.Principal.WindowsPrincipal]::new($identity)
  $isAdministrator = $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
  $perMonitor = @()
  if (Test-Path -LiteralPath "HKCU:\Control Panel\Desktop\PerMonitorSettings") {
    $perMonitor = @(Get-ChildItem -LiteralPath "HKCU:\Control Panel\Desktop\PerMonitorSettings" | ForEach-Object {
      $values = Get-ItemProperty -LiteralPath $_.PSPath
      [ordered]@{
        monitorKey = $_.PSChildName
        dpiValue = $values.DpiValue
      }
    })
  }

  [ordered]@{
    capturedAt = (Get-Date).ToUniversalTime().ToString("o")
    windows = [ordered]@{
      caption = $os.Caption
      version = $os.Version
      buildNumber = $os.BuildNumber
      architecture = $os.OSArchitecture
    }
    machine = [ordered]@{
      manufacturer = $computer.Manufacturer
      model = $computer.Model
      totalPhysicalMemory = $computer.TotalPhysicalMemory
    }
    processArchitecture = [Runtime.InteropServices.RuntimeInformation]::ProcessArchitecture.ToString()
    gpu = $video
    monitors = $monitors
    screenLayout = $screenLayout
    webView2Runtime = $webView2
    account = [ordered]@{
      userName = $identity.Name
      elevatedAdministrator = $isAdministrator
    }
    desktopDpi = [ordered]@{
      logPixels = $dpi.LogPixels
      win8DpiScaling = $dpi.Win8DpiScaling
      perMonitorSettings = $perMonitor
      note = "Registry values are captured as evidence only; RM-E still requires visual/coordinate verification on the physical displays."
    }
  }
}

function Invoke-LifecycleAcceptance {
  param(
    [Parameter(Mandatory)][string]$Exe,
    [Parameter(Mandatory)][string]$InstallRoot,
    [Parameter(Mandatory)][int]$Cycles,
    [Parameter(Mandatory)][string]$OutputPath
  )
  $records = @()
  for ($cycle = 1; $cycle -le $Cycles; $cycle++) {
    Assert-NoAtlasOwnedProcesses -InstallRoot $InstallRoot -Context "Before lifecycle cycle $cycle"
    $started = Get-Date
    $process = Start-Process -FilePath $Exe -WorkingDirectory $env:TEMP -PassThru
    Start-Sleep -Seconds $(if ($cycle -eq 1) { 8 } else { 4 })

    if ($process.HasExited) {
      throw "Atlas exited early during lifecycle cycle $cycle with code $($process.ExitCode)"
    }

    $running = Get-ProcessEvidence -InstallRoot $InstallRoot
    $closedNormally = $process.CloseMainWindow()
    if (-not $closedNormally) {
      Stop-Process -Id $process.Id -Force -ErrorAction SilentlyContinue
      throw "Atlas did not expose a closable main window during lifecycle cycle $cycle"
    }
    if (-not $process.WaitForExit(10000)) {
      Stop-Process -Id $process.Id -Force -ErrorAction SilentlyContinue
      throw "Atlas did not exit within 10 seconds of a normal close request during lifecycle cycle $cycle"
    }

    Start-Sleep -Seconds 2
    Assert-NoAtlasOwnedProcesses -InstallRoot $InstallRoot -Context "Lifecycle cycle $cycle"
    $records += [ordered]@{
      cycle = $cycle
      startedAt = $started.ToUniversalTime().ToString("o")
      closedAt = (Get-Date).ToUniversalTime().ToString("o")
      processTreeWhileRunning = $running
      exitCode = $process.ExitCode
      normalClose = $true
      orphanCountAfterClose = 0
    }
  }
  Write-JsonFile -Value $records -Path $OutputPath
}

function Invoke-SoakMonitor {
  param(
    [Parameter(Mandatory)][string]$Exe,
    [Parameter(Mandatory)][string]$InstallRoot,
    [Parameter(Mandatory)][int]$Minutes,
    [Parameter(Mandatory)][int]$SampleMinutes,
    [Parameter(Mandatory)][string]$OutputPath
  )
  $process = Start-Process -FilePath $Exe -WorkingDirectory $env:TEMP -PassThru
  Start-Sleep -Seconds 8
  if ($process.HasExited) { throw "Atlas exited before soak monitoring began" }

  Write-Host "Atlas soak started. Use the installed UI during this period for workspace switching, Workflow, Vision, Knowledge, and Marketplace acceptance."
  $samples = @()
  $deadline = (Get-Date).AddMinutes($Minutes)
  $sampleIndex = 0
  while ((Get-Date) -lt $deadline) {
    $sampleIndex++
    $samples += [ordered]@{
      sample = $sampleIndex
      capturedAt = (Get-Date).ToUniversalTime().ToString("o")
      processes = Get-ProcessEvidence -InstallRoot $InstallRoot
    }
    Write-JsonFile -Value $samples -Path $OutputPath

    $remaining = [Math]::Max(0, ($deadline - (Get-Date)).TotalSeconds)
    if ($remaining -le 0) { break }
    $sleepSeconds = [Math]::Min($remaining, $SampleMinutes * 60)
    Start-Sleep -Seconds ([int][Math]::Ceiling($sleepSeconds))
  }

  $samples += [ordered]@{
    sample = $sampleIndex + 1
    capturedAt = (Get-Date).ToUniversalTime().ToString("o")
    processes = Get-ProcessEvidence -InstallRoot $InstallRoot
    final = $true
  }
  Write-JsonFile -Value $samples -Path $OutputPath
  Write-Host "Soak sampling complete. Leave Atlas open if further interactive acceptance is still in progress."
}

$plan = [ordered]@{
  evidenceDirectory = [IO.Path]::GetFullPath($EvidenceDir)
  installerPath = $InstallerPath
  atlasExe = $AtlasExe
  projectPath = $ProjectPath
  lifecycleCycles = $LifecycleCycles
  soakMinutes = $SoakMinutes
  soakSampleMinutes = $SoakSampleMinutes
  runLifecycle = [bool]$RunLifecycle
  runSoak = [bool]$RunSoak
  safety = @(
    "This helper never arms Input, clicks third-party applications, edits project data, or supplies credentials.",
    "Interactive Vision/Input/DPI/Narrator/Marketplace interruption gates remain human-observed.",
    "Use only disposable Atlas-owned test targets and synthetic secrets."
  )
}

if ($PlanOnly) {
  $plan | ConvertTo-Json -Depth 8
  exit 0
}

New-Item -ItemType Directory -Path $EvidenceDir -Force | Out-Null
Write-JsonFile -Value $plan -Path (Join-Path $EvidenceDir "plan.json")
Write-JsonFile -Value (Get-MachineEvidence) -Path (Join-Path $EvidenceDir "machine.json")

if ($ProjectPath) {
  $resolvedProject = [IO.Path]::GetFullPath($ProjectPath)
  Write-JsonFile -Value ([ordered]@{
    path = $resolvedProject
    exists = (Test-Path -LiteralPath $resolvedProject)
    containsNonAscii = [bool]($resolvedProject -match '[^\x00-\x7F]')
    containsSpaces = $resolvedProject.Contains(' ')
  }) -Path (Join-Path $EvidenceDir "project-path.json")
}

if ($InstallerPath) {
  $resolvedInstaller = (Resolve-Path -LiteralPath $InstallerPath).Path
  $installer = Get-Item -LiteralPath $resolvedInstaller
  Write-JsonFile -Value ([ordered]@{
    path = $resolvedInstaller
    fileName = $installer.Name
    sizeBytes = $installer.Length
    sha256 = (Get-FileHash -LiteralPath $resolvedInstaller -Algorithm SHA256).Hash.ToLowerInvariant()
  }) -Path (Join-Path $EvidenceDir "installer.json")
}

if ($RunLifecycle -or $RunSoak) {
  if (-not $AtlasExe) { throw "-AtlasExe is required with -RunLifecycle or -RunSoak" }
  $resolvedExe = (Resolve-Path -LiteralPath $AtlasExe).Path
  $installRoot = Split-Path -Parent $resolvedExe
  Write-JsonFile -Value ([ordered]@{
    atlasExe = $resolvedExe
    installRoot = $installRoot
    executableSha256 = (Get-FileHash -LiteralPath $resolvedExe -Algorithm SHA256).Hash.ToLowerInvariant()
  }) -Path (Join-Path $EvidenceDir "installed-product.json")

  if ($RunLifecycle) {
    Invoke-LifecycleAcceptance -Exe $resolvedExe -InstallRoot $installRoot -Cycles $LifecycleCycles -OutputPath (Join-Path $EvidenceDir "lifecycle.json")
  }
  if ($RunSoak) {
    Invoke-SoakMonitor -Exe $resolvedExe -InstallRoot $installRoot -Minutes $SoakMinutes -SampleMinutes $SoakSampleMinutes -OutputPath (Join-Path $EvidenceDir "soak.json")
  }
}

$checklist = [ordered]@{
  schemaVersion = 1
  generatedAt = (Get-Date).ToUniversalTime().ToString("o")
  gates = [ordered]@{
    "RM-A" = "NOT RUN"
    "RM-B" = "NOT RUN"
    "RM-C" = "NOT RUN"
    "RM-D" = "NOT RUN"
    "RM-E" = "NOT RUN"
    "RM-F" = "NOT RUN"
    "RM-G" = $(if ($RunLifecycle) { "PARTIAL - lifecycle automation recorded; 60-minute interactive soak still requires review" } else { "NOT RUN" })
    "RM-H" = "NOT RUN"
    "RM-I" = "NOT RUN"
    "RM-J" = "NOT RUN"
  }
  note = "Statuses are initialized conservatively. Update them only from observed evidence; this helper does not grant PASS."
}
Write-JsonFile -Value $checklist -Path (Join-Path $EvidenceDir "acceptance-session.json")
Write-Host "Evidence scaffold written to $([IO.Path]::GetFullPath($EvidenceDir))"
