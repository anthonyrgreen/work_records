records
=======
This is a program designed to store and query module load records for the flux cluster. 

install
-------
Install is quite simple. Just clone and then run the `install.sh` file in the root directory. 
`install.sh` creates a symlink for the utility provided:
* `module-query`
You can, optionally, give `install.sh` a single argument, which will specify where you want those symlinks to end up. For instance, if you are in the directory work_records, you might use the invocation:
    [grundoon]$ ./install.sh ../bin/
The install script would then place the symlinks inside the `../bin` directory.

use
---
Running `./module-query -h` will give a fairly thorough description of the query utility. Nonetheless, here are some example queries:
* all records between Jan 1, 2014, and Feb 15, 2014, by day, aggregated by module, version, for modules `R` or `openmpi`, by user `grundoon`:
    [grundoon]$ ./module-query query -b 01/02/2014 -e 15/02/2014 -p day -a m v -fm R openmpi -fu grundoon
* all records between Feb and Apr 2015, by month, aggregated by module and user, sorted by module, displaying only records with count less than 50:
    [grundoon]$ ./module-query query -b 02/2015 -e 04/2015 -p month -a m u -s m -fc lt 50
`addDirLogs` takes a directory and adds all cumulative module logs it finds within. Note that it will skip module log files which have already been added. Be patient during its running, as the cluster is fairly slow with read/write access.
