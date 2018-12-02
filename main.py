# coding: utf-8

import pandas as pd
import time
from selenium import webdriver
import random


def create_product_list(pageAddress):
    """
    """
    # перейти на страницу
    browser = webdriver.Firefox()
    # browser = webdriver.Firefox()
    # browser = webdriver.PhantomJS()
    browser.get(pageAddress)
    print("Страница загрузилась. Ожидание 30 сек.")
    time.sleep(30)

    # скролл страницы до конца
    last_height = browser.execute_script("return document.body.scrollHeight")
    # scrollEqualCounter = 0

    while True:

        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        scrollDelay = random.randint(5, 10)
        print("Задержка скрола {} сек.".format(scrollDelay))
        time.sleep(scrollDelay)
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print("Data scraped........")
            break
        else:
            last_height = new_height

    # подготовить данные
    page = browser.find_element_by_tag_name('html')
    table = page.find_elements_by_class_name("item")

    textTable = list()
    for i in range(0, len(table)):
        textTable.append(table[i].text)

    # закрыть браузер
    browser.close()

    # вернуть или сохранить данные
    return textTable


def parse_data(rawHTML):
    """
    """
    tocsvData = list()
    for i in range(0, len(rawHTML)):
        inside = rawHTML[i].split("\n")
        art = inside[1].split(" арт. ")
        line = []
        line.append(art[0])
        line.append(art[1])
        priceList = inside[3].split(" P")
        line.append(priceList[0])
        tocsvData.append(line)

    return tocsvData


def save_product_in_csv(prodictList, fileName):
    """
    """
    df = pd.DataFrame(prodictList, columns=["Название", "Артикул", "Цена"])
    df.to_csv("{}.csv".format(fileName), index=False)
    print("Сохранено {} записей".format(len(prodictList)))


def main():

    fileName = input("Введите имя файла (производителя) - ")

    url = input("Введите адресс страницы, с которой будут \
        собираться данные - ")

    pageData = create_product_list(url)
    tocsvData = parse_data(pageData)
    save_product_in_csv(tocsvData, fileName)


if __name__ == '__main__':
    main()
