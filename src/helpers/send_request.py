from requests import request


def sendRequest(url, method="get", data=None, files=None, headers=None, cookies=None):
    try:
        if files:
            return request(
                method, url, data=data, files=files, headers=headers, cookies=cookies
            )
        return request(method, url, json=data, headers=headers, cookies=cookies)
    except Exception as e:
        # Handle exceptions and return None
        print(f"Error occurred during request: {e}")
        return None
