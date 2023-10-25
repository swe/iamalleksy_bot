#!venv/bin/python
import requests
from requests.exceptions import HTTPError

def buttonone():
    test1 = "this is btn1"
    return(test1)
    
def buttontwo():
    try:
        response = requests.get('https://toncenter.com/api/v2/getAddressBalance?address=EQDnRzHz7T4X8zjso6CV0tuHNf42GrxCdlU78ijc6d6Y6AbO')
        response.raise_for_status()
        # access JSON content
        jsonResponse = response.json()
        print("Entire JSON response")
        print(jsonResponse)
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')

    print(jsonResponse["result"])