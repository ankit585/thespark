import pprint
import string
import random
from sparkbackend.util.Callable import Callable

class SystemUtils():

    def createRandomString():
       """ """
       chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
       size  = 30
       return ''.join(random.choice(chars) for x in range(size))
    
 
    createRandomString = Callable(createRandomString)

