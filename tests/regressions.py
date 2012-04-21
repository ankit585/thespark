from xml.dom.minidom import parseString
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy import create_engine
from RestClient import RestClient
from JSONCompare import JSONCompare
import sys
import json
 
#open the xml file for reading:
file = 'tests.xml'
if (len(sys.argv) > 1):
   file = sys.argv[1]
file = open(file,'r')
data = file.read()
file.close()
dom = parseString(data)
test_count = 0;
test_status = True;
test_failures = 0;
regressions = dom.getElementsByTagName("regression")
for i in  regressions:

   mysql_str =  'mysql://' + i.getElementsByTagName('db_user')[0].firstChild.data + ':' + \
                  i.getElementsByTagName('db_pass')[0].firstChild.data + '@' + \
                  i.getElementsByTagName('db_host')[0].firstChild.data + '/' + \
                  i.getElementsByTagName('db_name')[0].firstChild.data   
   engine = create_engine(
                mysql_str,
                isolation_level="READ UNCOMMITTED"
            )
   Session = scoped_session(sessionmaker(bind=engine))
   connection = Session.connection()

   statements = i.getElementsByTagName('mysql')[0].getElementsByTagName('statement')
   for st in statements:
      connection.execute(st.firstChild.data)  

   conn = RestClient(i.getElementsByTagName('api_host')[0].firstChild.data)

   tests = i.getElementsByTagName('tests')[0].getElementsByTagName('test')
   data = "" 
   for test in tests:
      test_count += 1;
      id = test.getElementsByTagName('test_id')[0].firstChild.data
      uri = test.getElementsByTagName('test_url')[0].firstChild.data
      type= test.getElementsByTagName('test_method')[0].firstChild.data
      expected_response = test.getElementsByTagName('expected_response')[0].firstChild.data   
      expected_content = json.loads(test.getElementsByTagName('expected_content')[0].firstChild.data)   
      if test.getElementsByTagName('test_data')[0].firstChild is not None: 
         data= test.getElementsByTagName('test_data')[0].firstChild.data
      if type == "GET":
        method = RestClient.GET
      elif type == "POST":    
        method = RestClient.POST
      elif type == "PUT":    
        method = RestClient.PUT
      elif type == "DELETE":    
        method = RestClient.DELETE
      else:
        print "Invalid Test Case"
        sys.exit(1) 

      (resp , content) = conn.request(uri,method,data)
      result = json.loads(content) 
      diff = JSONCompare(expected_content,result)
      if str(expected_response) == str(resp) and diff.status == True:
        print "Test Case: " + id + " Status: OK"
      else:
        test_failures +=1;
        test_status = False;
        print "Test Case:"  + id + " Status: ERROR , Message: "+ diff.error  +",  Expected Response:" + str(expected_response) + " GOT: " +str(resp)  + " Expected Json:" + str(expected_content) + " GOT: " + str(content)

print "\n\n\nRegression Summary: "
print "Total Tests : " + str(test_count) + " Failures: " + str(test_failures) + "\n\n"
if test_status == False:
   sys.exit(1)
