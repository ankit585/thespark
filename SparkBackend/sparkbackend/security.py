USERS = {'editor':'editor',
          'viewer':'viewer'}
GROUPS = {'editor':['group:editors']}

def groupfinder(userid, request):
    return "view"

