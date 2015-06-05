destinationDir="/tmp/argreen/tempDB"
cd $( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
cd dbFiles
test -d "$destinationDir" || mkdir -p "$destinationDir" 
filename="/app.db"
fullpath=$destinationDir$filename
if [[ app.db -nt $fullpath ]]; then
  #echo "COPYING"
  cp app.db "$fullpath"
#else
  #echo "NOT COPYING"
fi
