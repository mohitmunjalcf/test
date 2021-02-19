import json

class ApiGatewayResponseHelper:
    
    def __init__(self, event):
        self.event = event
    
    
    def BuildAPIGatewayProxyResponse(self, allowedOrigin = "*"):
        aPIGatewayProxyResponse = {
            "isBase64Encoded" : False,
            "headers": self.event.headers       
        }
        self.__BuildCorsHeader(aPIGatewayProxyResponse, allowedOrigin);
        return aPIGatewayProxyResponse;
    
    
    def __BuildCorsHeader(self, aPIGatewayProxyResponse, allowedOrigin):
        if aPIGatewayProxyResponse.headers is not None:
            aPIGatewayProxyResponse.headers["Access-Control-Allow-Origin"] = allowedOrigin
        else:
            aPIGatewayProxyResponse.headers = {"Access-Control-Allow-Origin" : allowedOrigin}
            
    
    def UpdateResponseStatus(self, aPIGatewayProxyResponse, status):
        if status == "Success":
            aPIGatewayProxyResponse.statusCode = "200"
            aPIGatewayProxyResponse.body = {"message" : status}
        elif status == "Failed":
            aPIGatewayProxyResponse.statusCode = "500"
            aPIGatewayProxyResponse.body = {"message" : status}
            
            
    def UpdateResponseBody(self, aPIGatewayProxyResponse, status, body):
        if status == "Success":
            aPIGatewayProxyResponse.statusCode = "200"
            aPIGatewayProxyResponse.body = json.dumps(body)
        elif status == "Failed":
            aPIGatewayProxyResponse.statusCode = "500"
            aPIGatewayProxyResponse.body = {"message" : status}
            
            
    def UpdateResponseBodywithMessage(self, aPIGatewayProxyResponse, status, response, responsemessages):
        if status == "Success":
            aPIGatewayProxyResponse.statusCode = "200"
            aPIGatewayProxyResponse.body = json.dumps(response)
        elif status == "Failed":
            exception = {
                "responseCode" : "DPB999",
                "responseMessage" : "Unhandled Exception or System Error"
            }
            responsemessage = {
                "responseCode" : exception["responseCode"],
                "responseMessage" : exception["responseMessage"]
            }
            responsemessages.append(responsemessage)
            aPIGatewayProxyResponse.statusCode = "200"
            aPIGatewayProxyResponse.body = json.dumps(responsemessages)
        elif status == "ValidationError":
            aPIGatewayProxyResponse.statusCode = "400"
            aPIGatewayProxyResponse.body = json.dumps(response)
        elif status == "InternalServerError":
            aPIGatewayProxyResponse.statusCode = "500"
            aPIGatewayProxyResponse.body = json.dumps(response)
        

    
    

        
        
        
        
