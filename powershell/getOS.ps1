# Get Operating System Info
$Computer = "10.101.0.30"
$WMIUser = "ipayment\svc.accelops"
Write-Host $WMIUser
$Password = Get-Content SecureString.txt | convertto-securestring
Write-Host $Password
$Creds = new-object -typename System.Management.Automation.PSCredential -argumentlist $WMIUser, $Password

#Get-WmiObject -Class Win32_Service -ComputerName $Computer -Filter "Name='ServiceName'" -Credential $Creds
#
Get-CimInstance Win32_OperatingSystem | FL *
