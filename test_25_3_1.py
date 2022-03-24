import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome('C:\drivers\Chrome//chromedriver.exe')
    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends1.herokuapp.com/login')
    # Вводим email
    pytest.driver.find_element('email').send_keys('1234iop@mail.com')
    # Вводим пароль
    pytest.driver.find_element('pass').send_keys('1234iop')
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element('by=By.CSS_SELECTOR, button[type="submit"]').click()
    # Переходим в список "моих питомцев"
    pytest.driver.find_element('by=By.CSS_SELECTOR, a[href="/my_pets"').click()

    yield

    pytest.driver.quit()


def test_card_desk_my_pets():
    """тест 1 - присутствуют все питомцы"""
    # получаем количество карточек питомцев в списке "мои питомцы"
    pet_cards = pytest.driver.find_elements_by_xpath('//tbody/tr')
    # ожидаем загркузки и получаем поле, в котором указаны данные пользователя, втч количество питомцев
    number_of_pets = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class=".col-sm-4 left"]')))
    # переводим полученный веб-элемент в текст, забираем число питомцев с помощью индекса
    # (индекс индивидуален для каждого пользователя), переводим строку в число
    number_of_pets = int(number_of_pets.text[18])
    # сверяем количество карточек и число питомцев, указанное сбоку от таблицы карточек
    assert len(pet_cards) == number_of_pets

    """тест 2 - хотя бы у половины питомцев есть фото"""
    # получаем количество карточек с питомцами, у которых есть фото
    pet_photos = pytest.driver.find_elements_by_xpath('//tbody/tr/th/img')
    # проверяем, равно ли количество питомцев с фото хотя бы половине числа всех питомцев
    assert len(pet_photos) >= len(pet_cards) / 2

    """тест 3 - у всех питомцев есть имя, возраст и порода"""
    # ожидаем загрузки элементов на странице "Мои Питомцы"
    pytest.driver.implicitly_wait(10)
    # получаем общее количество тегов из каждой карточки питомца
    pet_info = pytest.driver.find_elements_by_xpath('//tbody/tr/td')
    # т.к. интересующий нас тег помечает не только имена, породу и возраст, а еще и кнопку удаления
    # в каждой карточке питомца, отдельно вычленяем эту кнопку с помощью ее уникального класса
    delete_pet_button = pytest.driver.find_elements_by_css_selector('td.smart_cell')
    # вычитаем из множества всех тегов, те, которые отвечают за кнопку удаления карточки
    # и проверяем, что теги имён, пород и возрастов не пусты
    assert set(pet_info) - set(delete_pet_button) != ''
    # проверяем, что количество тегов с именами, породами и возрастами в три раза больше, чем карточек питомцев
    # (т.е. в каждой карточке содержутся все три интересующие нас поля)
    assert len(pet_info) - len(delete_pet_button) == 3 * len(pet_cards)

    """тест 4 - у всех питомцев разные имена"""
    # заводим переменную, в которую будем заносить уникальные имена питомцев
    pet_names = [None]
    # заводим переменную, в которую будем заносить повторяющиеся имена питомцев
    repeating_names = [None]

    # заводим цикл, который будет перебирать имена по xpath
    for name in pytest.driver.find_elements_by_xpath('//tbody/tr/td[1]'):

        # переводим полученный WebElement в текст
        name = name.text

        # если проверяемого имени нет в списке уникальных имен, добавляем его туда
        if name not in pet_names:
            pet_names[0] = pet_names.append(name)
        # если проверяемое имя есть в списке уникальных имен, добавляем в список повторяющихся
        else:
            repeating_names[0] = repeating_names.append(name)

    # проверяем, что количество уникальных имен равно количеству карточек с питомцами
    # (отнимаем единицу от количества карточек в списке pets, т.к. в нём еще хранится объект None),
    # а список для повторяющихся имен пустой
    assert len(pet_names) - 1 == len(pet_cards) and repeating_names == [None]

    """тест 5 - нет повторяющихся питомцев"""
    # заводим список, в котором будут храниться уникальные питомцы
    pets = [None]
    # заводим список, в котором будут храниться повторяющиеся питомцы (с одинаковыми именем, породой и возрастом)
    repeating_pets = [None]

    # заводим цикл, для отбора карточек с животными
    for pet in pytest.driver.find_elements_by_xpath('//tbody/tr'):

        # переводим полученный WebElement в текст
        pet = pet.text

        # если питомца нет в списке уникальных питомцев, добавляем его туда
        if pet not in pets:
            # # для корректности отображения переводим данные питомца из WebElement в текст
            # pet = pet.text
            # добавление питомца
            pets[0] = pets.append(pet)
        # если питомец есть в списке уникальных питомцев, добавляем его в список повторяющихся
        else:
            repeating_pets[0] = repeating_pets.append(pet)

    # проверяем, что количество питомцев в списке равно количеству карточек с питомцами
    # (отнимаем единицу от количества карточек в списке pets, т.к. в нём еще хранится объект None),
    # а список для повторяющихся питомцев пуст
    assert len(pets) - 1 == len(pet_cards) and repeating_pets == [None]
