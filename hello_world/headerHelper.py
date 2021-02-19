@staticmethod
def GetAuthorizationToken(headers):
    if headers is None:
        return None
    
    if "Authorization" in headers.keys():
        return headers["Authorization"]
    else:
        return None
    
    
@staticmethod
def RemoveAuthorizationHeader(headers):
    if headers is not None:  
        return {key:val for key, val in headers.items() if key != 'Authorization'}     
    else:
        return headers
    