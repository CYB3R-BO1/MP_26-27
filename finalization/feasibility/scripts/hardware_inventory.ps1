$ErrorActionPreference = 'Stop'

$inventory = [ordered]@{
    captured_at = (Get-Date).ToUniversalTime().ToString('o')
    computer = Get-ComputerInfo | Select-Object WindowsProductName, WindowsVersion, OsBuildNumber, OsArchitecture, CsSystemType, CsTotalPhysicalMemory, CsProcessors
    cpu = Get-CimInstance Win32_Processor | Select-Object Name, NumberOfCores, NumberOfLogicalProcessors, MaxClockSpeed
    memory = Get-CimInstance Win32_OperatingSystem | Select-Object TotalVisibleMemorySize, FreePhysicalMemory
    gpu = @(Get-CimInstance Win32_VideoController | Select-Object Name, AdapterRAM, DriverVersion, VideoProcessor)
    volumes = @(Get-Volume | Where-Object DriveLetter | Select-Object DriveLetter, FileSystemLabel, FileSystem, Size, SizeRemaining)
    nvidia_smi = if (Get-Command nvidia-smi -ErrorAction SilentlyContinue) { nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader } else { 'NOT_FOUND' }
    wsl = wsl --status 2>&1
}

$inventory | ConvertTo-Json -Depth 6
