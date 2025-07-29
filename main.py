"""
Я понимаю что структура может поменяться,
и так на пролом пробивать тэги не правильно
(например для ссылок), можно и даже следует
добавить проверок на значения и ошибок, но
если нужен результат и простое получение 
результата ТЗ.
"""


import requests
from bs4 import BeautifulSoup


def login():
    base_url = "http://185.244.219.162/phpmyadmin/"
    login_url = base_url + "index.php"

    login_data = {
        "pma_username": "test",
        "pma_password": "JHFBdsyf2eg8*",
        "server": "1"
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": login_url
    }

    session = requests.Session()

    try:
        login_page = session.get(login_url)
        soup = BeautifulSoup(login_page.text, "html.parser")

        csrf_token = soup.find("input", {"name": "token"})
        if not csrf_token:
            print("Токен не удалось найти")
            return False

        login_data["token"] = csrf_token["value"]

        response = session.post(
            login_url, data=login_data, headers=headers, allow_redirects=True
        )

        if "route=/" not in response.url:
            print("Не удалось войти")
            return False
        
        print("Переход на главную")
        soup = BeautifulSoup(response.text, "html.parser")
        testDB_href = (
            soup.find_all(class_="database")[-1]
            .find(class_="hover_show_full")
            .attrs["href"]
        )


        print("Переход на страницу testDB")
        soup = BeautifulSoup(session.get(base_url + testDB_href).text, "html.parser")
        users_table_href = soup.find("tbody").find("th").find("a").attrs["href"]


        print("Переход на страницу таблицы users")
        soup = BeautifulSoup(
            session.get(base_url + users_table_href).text, "html.parser"
        )
        users_table = soup.find("table", class_="table").find_all("td", class_="data")

        print("ID\tName")
        for i in range(0, len(users_table), 2):
            print(users_table[i].text + "\t" + users_table[i+1].text)
        
        return True

    except Exception as e:
        print(e)

    return False


login()
