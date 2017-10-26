
$batch_files = Get-ChildItem "~\Desktop\BatchFiles"
$data_files = Get-ChildItem "~\Desktop\DataFiles" 
$good_dir = "~\Desktop\Good_$((Get-Date).ToString('yyy-MM-dd'))"


#Write-Host "Batch Files : " $batch_files
#Write-Host "Data Files : " $data_files
#Write-Host "Good Directory : " $good_dir

If (!(test-path $good_dir))
{
  New-Item -ItemType Directory -Force -Path $good_dir
}

#This will print a list of files that exist in both $batch_files and $data_files
Compare-Object $batch_files $data_files -IncludeEqual | 
  Where-Object {$_.SideIndicator -eq '=='} | Select-Object -ExpandProperty inputobject |
  foreach-object -process{
    copy-item $_.FullName -destination $good_dir
  }



