destinationDir="/tmp/argreen/tempDB"
cd $(pwd)
cd ../dbFiles
test -d "$destinationDir" || mkdir -p "$destinationDir" 
filename="/app.db"
fullpath=$destinationDir$filename
if [[ app.db -nt $fullpath ]]; then
  #echo "COPYING"
  cp app.db "$fullpath"
  #echo "NOT COPYING"
fi
