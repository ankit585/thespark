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
