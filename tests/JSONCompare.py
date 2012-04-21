

class JSONCompare(object):
    """ A class to compare two JSON objects 
        Usage:  
              first = json.loads(first_json_string) 
              second= json.loads(second_json_string) 
              diff = JSONCompare(first,second)
              if diff.status != True:
                 print diff.error
         NOTE: Make any field of "first" to "DO_NOT_MATCH" to skip comparison 
    """                         

    def __init__(self, first, second):
       self.error = "No Error"
       self.status =  self.compare(first, second,0)

        
    def compare(self, first, second,level):  
        if second == None:
           self.error =  "second field is NULL(value mismatch) at " + str(level)
           return False;          
        if isinstance(first , dict): 
           if not isinstance(second,dict):
              self.error =  "Dict: No dictionary found at level " + str(level)
              return False;
           if len(first) != len(second):
              self.error =  "Dict: Unequal length at level " + str(level)
              return False;
           for key in first:
              if not second.has_key(key):
                self.error =  "Dict: missing key "+ str(key) +  "  at level " + str(level)
                return False;
              if self.compare(first[key],second[key],level+1) == False:
                return False; 
        elif isinstance(first,list):
           if not isinstance(second,list):
              self.error =  "List: No List found at level " + str(level)
              return False;
           if len(first) != len(second):
              self.error =  "List: Unequal length at level " + str(level)
              return False;
           for index in range(len(first)):
              if self.compare(first[index],second[index],level+1) == False:
                 return False;
        else: 
           if str(first) != "DO_NOT_MATCH" and str(first) != str(second):
              self.error =  "Final value mismatch at level " + str(level) + " Expected: " + str(first) + " GOT: " + str(second)
              return False;
           else: 
              return True;
        return True;


        
