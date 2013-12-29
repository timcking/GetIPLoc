awk '{print $1, $4, $5 }' sitedata.txt | sed 's/.\{7\}$//'
