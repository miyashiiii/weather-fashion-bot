import requests
from bs4 import BeautifulSoup


def parse_weather(weather_data):
    date = weather_data.find(class_="left-style").text
    index = weather_data.find(class_="indexes-telop-0").string
    comment = weather_data.find(class_="indexes-telop-1").string
    weather = weather_data.find(class_="weather-telop").string
    high_temp = weather_data.find(class_="high-temp").string
    low_temp = weather_data.find(class_="low-temp").string
    rain_prob = weather_data.find(class_="precip").string

    return date, index, comment, weather, high_temp, low_temp, rain_prob


def scrape_tenki(search_word):
    """

    tenki.jpから服装指数情報をスクレイピング
    """

    # 地域検索
    search_r = requests.get(f'https://tenki.jp/search/?keyword={search_word}')

    search_r_bs = BeautifulSoup(search_r.content, "html.parser")
    address_list = search_r_bs.find_all(class_="search-entry-data")
    # print(address_list)
    if len(address_list) == 0:
        return None

    match_address = address_list[0].find(class_="address").string.replace("以下に掲載がない場合", "")
    print(match_address)

    address_code = "/".join(address_list[0].find("a").get("href").split("/")[2:5])
    print(address_code)

    dress_r = requests.get(f"https://tenki.jp/indexes/dress/{address_code}/")
    search_r_bs = BeautifulSoup(dress_r.content, "html.parser")
    dress_area = [v for v in search_r_bs.find(id="delimiter").text.split("\n") if v][-2:]
    today_weather = parse_weather(search_r_bs.find(class_="today-weather"))
    # tomorrow_weather = parse_weather(search_r_bs.find(class_="tomorrow-weather"))

    return match_address, dress_area, today_weather


if __name__ == "__main__":
    area_weather = scrape_tenki("熊谷市")
    print(area_weather)
