#!/usr/bin/env pwsh

# SPDX-FileCopyrightText: Copyright 2025 Arm Limited and/or its affiliates <open-source-office@arm.com>
# SPDX-License-Identifier: Apache-2.0

$PSNativeCommandUseErrorActionPreference = $true
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

# Usage
if ($args.Count -gt 0 -and ($args[0] -eq "-h" -or $args[0] -eq "--help")) {
    $scriptName = if ($PSCommandPath) { Split-Path -Leaf $PSCommandPath } else { "ci_build.ps1" }
    Write-Host "Usage: $scriptName"
    Write-Host
    Write-Host "Environment:"
    Write-Host "  REPO           (required)  path to the 'repo' Python script"
    Write-Host "  MANIFEST_URL   (optional)  default: https://github.com/arm/ai-ml-sdk-manifest.git"
    Write-Host "  REPO_DIR       (optional)  default: ./sdk"
    Write-Host "  INSTALL_DIR    (optional)  default: ./install"
    Write-Host "  CHANGED_REPO   (optional)  manifest project name to pin and resync"
    Write-Host "  CHANGED_SHA    (optional)  commit SHA to pin CHANGED_REPO to (required if CHANGED_REPO is set)"
    Write-Host "  OVERRIDES      (optional)  JSON object: { ""org/repo"": ""40-char-sha"", ... }"
    exit 0
}

# Environment defaults
$ManifestUrl = if ($env:MANIFEST_URL) { $env:MANIFEST_URL } else { "https://github.com/arm/ai-ml-sdk-manifest.git" }
$RepoDir     = if ($env:REPO_DIR)     { $env:REPO_DIR }     else { Join-Path (Get-Location) "sdk" }
$InstallDir  = if ($env:INSTALL_DIR)  { $env:INSTALL_DIR }  else { Join-Path (Get-Location) "install" }
$ChangedRepo = $env:CHANGED_REPO
$ChangedSha  = $env:CHANGED_SHA
$Overrides   = $env:OVERRIDES
$RepoEnvPath = $env:REPO

Write-Host "Using manifest URL: $ManifestUrl"
Write-Host "Using repo directory: $RepoDir"
Write-Host "Using install directory: $InstallDir"
Write-Host "find CHANGED_REPO: $ChangedRepo"
Write-Host "find CHANGED_SHA: $ChangedSha"
Write-Host "find OVERRIDES: $Overrides"

$cores = (Get-CimInstance Win32_ComputerSystem).NumberOfLogicalProcessors
Write-Host "CPUs: $cores"

if (-not $RepoEnvPath) {
    Write-Error "REPO environment variable must be set to the path of the 'repo' script."
    exit 1
}

if (-not (Test-Path -LiteralPath $RepoEnvPath)) {
    Write-Error "The REPO path '$RepoEnvPath' does not exist. Please provide a valid path."
    exit 1
}

$RepoScriptPath = (Resolve-Path -LiteralPath $RepoEnvPath).Path
Write-Host "Using repo script path: $RepoScriptPath"

New-Item -Path $RepoDir -ItemType Directory -Force
New-Item -Path $InstallDir -ItemType Directory -Force

$RepoDir    = (Resolve-Path $RepoDir).Path
$InstallDir = (Resolve-Path $InstallDir).Path

Push-Location $RepoDir
try {
    python $RepoScriptPath init --no-repo-verify -u $ManifestUrl --depth=1
    python $RepoScriptPath sync --no-repo-verify --no-clone-bundle -j $cores

    # Local manifests
    New-Item -ItemType Directory -Path ".repo/local_manifests" -Force | Out-Null

    if ($Overrides) {
        # OVERRIDES: JSON object: { "org/repo": "sha", ... }
        $manifestArgs = @($RepoScriptPath, "manifest", "-r")
        $manifestText = python @manifestArgs
        $manifestXml = $manifestText -join "`n"

        $overridesObj = $Overrides | ConvertFrom-Json

        foreach ($prop in $overridesObj.PSObject.Properties) {
            $name = $prop.Name
            $revision = [string]$prop.Value

            $xpath = "//project[@name='$name']/@path"
            $projectPath = $manifestXml | xml.exe sel -t -v $xpath

            if (-not $projectPath) {
                Write-Error "ERROR: project path for $name not found in manifest"
                exit 1
            }

            $overrideFile = ".repo/local_manifests/override.xml"
            if (Test-Path $overrideFile) {
                Remove-Item $overrideFile -Force
            }

            $overrideContent = @"
<manifest>
  <project name="$name" revision="$revision" remote="github"/>
</manifest>
"@
            $overrideContent | Set-Content -Path $overrideFile -Encoding UTF8

            Write-Host "Syncing $name ($projectPath)"
            python $RepoScriptPath sync -j $cores --force-sync $projectPath
        }
    }
    elseif ($ChangedRepo) {
        if (-not $ChangedSha) {
            Write-Error "CHANGED_REPO is set but CHANGED_SHA is empty"
            exit 1
        }

        $manifestArgs = @($RepoScriptPath, "manifest", "-r")
        $manifestText = python @manifestArgs
        $manifestXml = $manifestText -join "`n"

        $xpath = "//project[@name='$ChangedRepo']/@path"
        $projectPath = $manifestXml | xml.exe sel -t -v $xpath

        if (-not $projectPath) {
            Write-Error "Could not find project path for $ChangedRepo in manifest"
            exit 1
        }
        Write-Host "Changed project path: $projectPath"

        $overrideFile = ".repo/local_manifests/override.xml"
        $overrideContent = @"
<manifest>
  <project name="$ChangedRepo" revision="$ChangedSha" remote="github"/>
</manifest>
"@
        $overrideContent | Set-Content -Path $overrideFile -Encoding UTF8
        python $RepoScriptPath sync -j $cores --force-sync $projectPath
    }

    $path="HKLM:\SOFTWARE\Khronos\Vulkan\ExplicitLayers"
    if(-not(Test-Path $path)) {
        New-Item $path -Force | Out-Null
    }
    New-ItemProperty -Path $path -Name "$InstallDir\bin" -Value 0 -PropertyType DWord -Force | Out-Null

    $env:VK_INSTANCE_LAYERS = "VK_LAYER_ML_Graph_Emulation;VK_LAYER_ML_Tensor_Emulation"

    Write-Host "Build VGF-Lib"
    python "./sw/vgf-lib/scripts/build.py" -j $cores --test

    Write-Host "Build Model Converter"
    python "./sw/model-converter/scripts/build.py" -j $cores --test

    Write-Host "Build Emulation Layer"
    python "./sw/emulation-layer/scripts/build.py" -j $cores --test --install $InstallDir

    Write-Host "Build Scenario Runner"
    python "./sw/scenario-runner/scripts/build.py" -j $cores --test

    Write-Host "Build SDK Root"
    python "./scripts/build.py" -j $cores
}
finally {
    Pop-Location
}
