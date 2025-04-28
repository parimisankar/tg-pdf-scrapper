$Action = New-ScheduledTaskAction -Execute "C:\Users\JaiParimi\TG_PDF_Scrapper\dist\TG_PDF_Scrapper.exe"
$Trigger = New-ScheduledTaskTrigger -AtStartup
$Principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -RunLevel Highest
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -MultipleInstances IgnoreNew
Register-ScheduledTask -TaskName "TG_PDF_Scrapper_AutoRun" -Action $Action -Trigger $Trigger -Principal $Principal -Settings $Settings
Write-Output "✅ TG PDF Scrapper AutoRun task created successfully."