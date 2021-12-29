


def get_APItoken_fromWebDriverURL(webDriverUrl:str) -> str:

    token = webDriverUrl[webDriverUrl.find("v0/")+3:webDriverUrl.find("/wd/hub")]

    if token:
        if token.isalnum():
            return token
        else:
            raise Exception("  ! Failed to extract token from Web Driver URL, TOKEN:{}".format(token))
    else:
        raise Exception("  ! Failed to extract token from Web Driver URL, TOKEN:{}".format(token))

    
    




    

