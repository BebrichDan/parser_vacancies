import requests
import pandas as pd 

class RequestError(BaseException):
    pass

count_response_string = 30
request = "junior-developer"
url = f"https://api.hh.ru/vacancies?text={request}&per_page={count_response_string}"
headers = ["name", "has_test", "experience", "salary_range", "alternate_url"] 

responce = requests.get(url)
if responce.status_code != 200:
    raise RequestError("Status code is note OK")

vacancies = responce.json().get("items", [])
print(vacancies)

jsonFrame = pd.DataFrame(vacancies)
jsonFrame["experience"] = jsonFrame["experience"].map(lambda x: x.get("name") if isinstance(x, dict) else x)
jsonFrame["salary_range"] = jsonFrame["salary_range"].map(lambda x: x.get("from") if isinstance(x, dict) else x)
jsonFrame = jsonFrame.reindex(columns=headers)
jsonFrame.to_csv("develop.csv", index=False)
