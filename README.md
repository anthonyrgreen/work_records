#records
This is a program designed to store and query module load records for the flux cluster. 

##install
Install is quite simple. Just clone and then run the `install.sh` file in the root directory. 

`install.sh` creates a symlink for the utility provided: `module-query`

You can, optionally, give `install.sh` a single argument, which will specify where you want that symlink to end up. For instance, if you are in the directory `work_records`, you might use the invocation:

    [grundoon]$ ./install.sh ../bin/

The install script would then place the symlinks inside the `../bin` directory.

##use
Running `./module-query -h` will give a fairly thorough description of the query utility. Nonetheless, here are some example commands:

####`module-query query`

* query all records between Jan 1, 2014, and Feb 15, 2014, by day, aggregated by module, version, for modules `R` or `openmpi`, by user `grundoon`:

        [grundoon]$ ./module-query query -b 01/02/2014 \
                                         -e 15/02/2014 \
                                         -p day -a m v \
                                         -fm R openmpi \
                                         -fu grundoon

* query all records between Feb and Apr 2015, by month, aggregated by module and user, sorted by module, displaying only records with count less than 50:

        [grundoon]$ ./module-query query -b 02/2015 \
                                         -e 04/2015 \
                                         -p month   \
                                         -a m u     \
                                         -s m       \
                                         -fc lt 50

* display help for the query utility:
    
        [grundoon] $ ./module-query query -h

####`module-query add-logs`
* Add a single module log:

        [grundoon] $ ./module-query add-logs ./logs/flux_module_log-2014-02.gz
 
* Add an entire folder of module logs (those already added and those with improper filenames will be skipped) with verbose output

        [grundoon] $ ./module-query add-logs -v ./logs/*

* display help for the add-logs utility:
    
        [grundoon] $ ./module-query add-logs -h

####`module-query delete-logs`
* Delete a single module log:

        [grundoon] $ ./module-query delete-logs ./logs/flux_module_log-2014-02.gz

* Delete all module logs found in a folder (those not present in the database will simply be skipped) with verbose output:

        [grundoon] $ ./module-query delete-logs -v ./logs/*

* display help for the delete-logs utility:
    
        [grundoon] $ ./module-query delete-logs -h
