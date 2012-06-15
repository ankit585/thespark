Packages to be installed on the server (`yum install <package-name>`)

httpd  
python  
git  
mysql  
mysql-server    
python-devel  
gcc  
mysql-devel  

Apart from this install all packages in external/ by using `python setup.py install`

To install:

    cd thespark/SparkBackend
    sudo python setup.py install

To Start Server:

    cd thespark/SparkBackend
    pserve development.ini
    (This will start the API server on port 6543. The port can be configured in development.ini)

To run regressions:
 
    cd thespark/tests
    ./runRegression.sh

Pending Tasks
1)[Task][P1][owner][status- yet to start] Add a config class/object to read general config variables like API hostname , API version etc. 
2)[Task][P1][owner][status- yet to start] Add a config class/object to real all secret config variables like mysql passwords,salt value. 
3)[Task][P2][owner][status- yet to start] Evaluate AWS and identify/do work needed for migration to AWS.
4)[Defect][P2][owner][status- yet to start] Read all salt value from config.
5)[Defect][P2][owner][status- yet to start] Read all DB information from config.
6)[Task][P2][owner][status- yet to start] Add a logging framework and implement proper logging.
7)[Task][P2][owner][status- yet to start] Add Memcache support so frequent api queries like frontpage can be cached. 