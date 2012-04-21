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

To run:

    cd humansinc/scripts
    ./startup.sh 8080

To run regressions:
 
    cd humansinc/tests
    ./runRegression.sh
