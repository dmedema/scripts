configuration RemoveSMB1 {
    param([string[]]$ComputerName='localhost')

    Import-DscResource -ModuleName PSDesiredStateConfiguration

    Node $ComputerName {

	#Ensure SMB1 feature is not installed
	WindowsFeature 'SMB1' {
	    Name 	= 'FS-SMB1'
	    Ensure	= 'Absent'
	}
    }
}

RemoveSMB1 -OutputPath .\
