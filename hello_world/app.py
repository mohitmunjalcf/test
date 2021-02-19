import logging
import urllib
from asyncio.events import AbstractEventLoop
import requests, json, asyncio, aiohttp
from aiohttp  import ClientSession

import hello_world.headerHelper as headerHelper
import hello_world.apiGatewayResponseHelper as apigateway
import hello_world.env_variable as env
# import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    requestHeaders = event.headers
    token = headerHelper.GetAuthorizationToken(requestHeaders)
    event.headers = headerHelper.RemoveAuthorizationHeader(requestHeaders)
    apiGatewayResponseHelper = apigateway()
    aPIGatewayProxyResponse = apiGatewayResponseHelper.BuildAPIGatewayProxyResponse()
    try:
        environmentVariableValues = env.GetEnvVariables()
        response =  Process(event, environmentVariableValues, token)
        apiGatewayResponseHelper.UpdateResponseBody(aPIGatewayProxyResponse, "Success", response)
    except:
        pass
    
    
def Process(event, environmentVariableValues, token):
    userName = GetUserName(event)
    logger.info(f'username '.format(userName))
    return await GetClassCodes(environmentVariableValues, event.pathParameters, userName, token)
    
    
def GetUserName(event):
    claim = "cognito:username"
    claims = event.requestContext.authorizer.claims
    if claim in claims.keys():
        return claims[claim]
    else:
        return None
    

def GetClassCodes(environmentVariableValues, pathParameters, userName, token):
    base_url = environmentVariableValues["ClassCodeApiURL"]
    product = str(pathParameters["product"]).strip().upper()
    state = str(pathParameters["state"]).strip().upper()
    path = f'product/{product}/state/{state}'
    url_parts = list(urllib.parse.urlparse(base_url))
    url_parts[2] = path
    class_code_url = urllib.parse.urlunparse(url_parts)
    urls = {
        class_code_url : {
            "Content-Type" : "application/json",
            "Authorization" : token
        },
        environmentVariableValues["ProducerApiURL"] + userName : {
            "Content-Type" : "application/json",
            "Authorization" : ""
        }
    }
    event_loop: AbstractEventLoop = asyncio.get_event_loop()
    responses = event_loop.run_until_complete(downloads_all_sites(urls))
    return responses


async def downloads_all_sites(urls):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls.items():
            task = asyncio.ensure_future(download_site(session, url))
            tasks.append(task)
        return await asyncio.gather(*tasks,return_exceptions=True)


async def download_site(session: ClientSession, url):
    async with session.get(url.key,url.value) as response:
        return await response.json()