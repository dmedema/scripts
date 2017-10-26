

md edited
Get-Children -Filter *.bat | ForEach-Object { $_ | % { $_ -replace "20170721.ald",20170731.ald" } > edited\$_ }

