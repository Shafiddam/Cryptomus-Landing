from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from .data.data import *


@pytest.mark.parametrize("email", [
                                    "Москва@Москва.РФ",
                                    "firstname.lastname@domain.com", "email@subdomain.domain.com",
                                    "firstname+lastname@domain.com", '"email"@domain.com', '1234567890@domain.com',
                                    'email@domain-one.com', '______@domain.com', 'email@domain.name',
                                    'email@domain.co.jp', 'firstname-lastname@domain.com',
                                   ])
def test_positive_email(driver, email):
    """
    ПРОВЕРКА ПОЛЯ ЕМЭЙЛ -  ПОЗИТИВНЫЕ ТЕСТЫ: ПРАВИЛЬНЫЙ ЕМЭЙЛ
    1. Открыть ссылку
    2. В поле "Email" ввести правильную почту
    Ожид.результат: Ошибок нет, выводится сообщение "Message sent"
    """
    try:
        # открытие страницы
        driver.get(link)
        # кликаем на кнопку конфирма в окне принятия кукис
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, btn_cookies))).click()
        # кликаем на кнопку "Contact us":
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, btn_contact_us))).click()
        # вводим валидное имя
        WebDriverWait(driver, 10).until(EC.presence_of_element_located
                                        ((By.CSS_SELECTOR, input_name))).send_keys("Тестирование")
        # поле ввода "Email"
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, input_email))).send_keys(email)
        sleep(1)  #
        # кликаем чек-бокс согласия PRIVACY_POLICY
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, privacy_policy))).click()
        sleep(1)  #
        # кликаем на кнопку отсылки "сенд"
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, btn_send))).click()
        sleep(1)  #
        # поиск текста всплывающего сообщения об успехе
        pop_up_text = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'notistack-snackbar')))
        pop_up_text_color = pop_up_text.value_of_css_property("color")  # work: 'rgba(255, 255, 255, 1)'
        # Проверка, что цвет текста всплывающего собщения БЕЛЫЙ
        assert pop_up_text_color == 'rgba(255, 255, 255, 1)', "ОШИБКА: цвет текста не БЕЛЫЙ !!!"
        # получим цвет плашки (нам нужен зеленый, а не красный)
        pop_up_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located
                                                         ((By.CLASS_NAME, 'SnackbarContent-root')))
        bg_color = pop_up_element.value_of_css_property("background-color")
        # Проверка, что цвет плашки зеленый
        assert bg_color == 'rgba(67, 160, 71, 1)', "ОШИБКА: цвет плашки не ЗЕЛЕНЫЙ !!!"
        # поиск элемента, содержащего сообщение "Message sent"
        message_text = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="notistack-snackbar"]')))
        # проверка, что сообщение "Message sent" вывелось на плашке
        assert "Message sent" in message_text.text, "ОШИБКА: нет сообщения об отправке !!!"
        # Проверка, что плашка появилась на странице
        assert pop_up_element.is_displayed()
        # sleep(1) # Задержка чтобы сообщение исчезло
    except Exception as e:
        # обработка исключений
        pytest.fail(f"ERROR: {str(e)}")
    finally:
        # закрытие браузера в любом случае
        sleep(20) # ----------  3 ЗАПРОСА В МИНУТУ ОГРАНИЧИЛИ БЭКИ, ПОЭТОМУ 20 СЕК ПАУЗА МЕЖДУ ТЕСТАМИ !!!!!!!!
        # --------------------  иначе 503 ошибка сервера на втором запросе будет
        driver.quit()


# #  -------------------------------           НЕГАТИВНЫЕ ТЕСТЫ        --------------------------------------------
# @pytest.mark.skip(reason = " Тест пропускается!!! ")
def test_all_inputs_is_empty(driver):
    """
    ВСЕ ПОЛЯ ПУСТЫЕ
    1. Открыть ссылку https://cryptomus.com/tariffs и спуститься ниже.
    2. Или открыть ссылку https://cryptomus.com/gateway и кликнуть на любой кнопке ""Contact sales""
    3. Или открыть ссылку https://cryptomus.com/
    4. Кликнуть на кнопку "Send"
    Ожидаемый результат: Бордер поля инпута "Full name" меняет цвет: был серый  #e8e8e8, стал красный #c53a3a
    """
    try:
        # открытие страницы
        driver.get(link)
        # кликаем на кнопку конфирма в окне принятия КУКИС
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, btn_cookies))).click()
        # кликаем на кнопку "Contact us":
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, btn_contact_us))).click()

        # поиск поля ввода имени - оно первое и оно изменит цвет на красный
        input_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, input_name)))
        # запоминание начального цвета границы поля ввода (был серый  #e8e8e8, станет красный #c53a3a)
        initial_color = input_element.value_of_css_property("border")
        # проверка print(initial_color)  1px solid rgb(68, 68, 68) #серый
        # кликаем на кнопку отсылки "сенд"
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, btn_send))).click()
        # получение текущего цвета поля ввода после ввода значения
        current_color = input_element.value_of_css_property("border")
        # проверка print(current_color)  1px solid rgb(197, 58, 58) #красный
        # проверка, что цвет поля ввода изменился
        assert current_color != initial_color, "ОШИБКА: нет подсветки первого поля ввода !!!"
    except Exception as e:
        # обработка исключений
        pytest.fail(f"ERROR: {str(e)}")
    finally:
        # закрытие браузера в любом случае
        sleep(20) # ----------  3 ЗАПРОСА В МИНУТУ ОГРАНИЧИЛИ БЭКИ, ПОЭТОМУ 20 СЕК ПАУЗА МЕЖДУ ТЕСТАМИ !!!!!!!!
        # --------------------  иначе 503 ошибка сервера на втором запросе будет
        driver.quit()


# @pytest.mark.skip(reason = " Тест пропускается!!! ")
def test_checkbox_agree_terms(driver):
    """
    ПРОВЕРКА ОБЯЗАТЕЛЬНОСТИ ВКЛЮЧЕНИЯ ЧЕК-БОКСА PRIVACY POLICY
    1. Открыть ссылку https://cryptomus.com/tariffs
    2. В поле "Full name" ввести валидное имя (от 2 до 60 символов), например "Тестирование"
    3. В поле емэйл ввести валидный ящик, например email@domain.com
    4. Кликнуть на кнопку "Send"
    Ожидаемый результат: текст "I have read and agree to the Privacy Policy" выделяется другим цветом (красный).
    """
    try:
        # открытие страницы
        driver.get(link)
        # кликаем на кнопку конфирма в окне принятия кукис
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, btn_cookies))).click()
        # кликаем на кнопку "Contact us":
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, btn_contact_us))).click()

        # вводим валидное имя
        WebDriverWait(driver, 10).until(EC.presence_of_element_located
                                        ((By.CSS_SELECTOR, input_name))).send_keys("Тестирование")
        # поле ввода "Email"
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, input_email))).\
                            send_keys("email@domain.com")
        # поиск чек-бокса - текст изменит цвет на красный
        element =  WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, privacy_policy)))
        # запоминание начального цвета (был серый  #e8e8e8, станет красный #c53a3a)
        initial_color = element.value_of_css_property("color")
        # проверка print(initial_color)  1px solid rgb(68, 68, 68) #серый
        # кликаем на кнопку отсылки "сенд"
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, btn_send))).click()
        # получение текущего цвета текста чек-бокса
        current_color = element.value_of_css_property("color")
        # проверка print(current_color)  1px solid rgb(197, 58, 58) #красный
        # проверка, что цвет текста изменился
        assert current_color != initial_color, "ОШИБКА: нет подсветки 'I have read and agree to the Privacy Policy' !!!"
    except Exception as e:
        # обработка исключений
        pytest.fail(f"ERROR: {str(e)}")
    finally:
        # закрытие браузера в любом случае
        sleep(20)  # ----------  3 ЗАПРОСА В МИНУТУ ОГРАНИЧИЛИ БЭКИ, ПОЭТОМУ 20 СЕК ПАУЗА МЕЖДУ ТЕСТАМИ !!!!!!!!
        # --------------------  иначе 503 ошибка сервера на втором запросе будет
        driver.quit()


# @pytest.mark.skip(reason = " Тест пропускается!!! ")
def test_email_more_60_simbols(driver):
    """
    ПОЛЕ "FULL NAME" "БОЛЬШЕ 60 СИМВОЛОВ"
    """
    try:
        # открытие страницы
        driver.get(link)
        # кликаем на кнопку КОНФИРМА в окне ПРИНЯТИЯ КУКИС
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, btn_cookies))).click()
        # кликаем на кнопку "Contact us":
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, btn_contact_us))).click()

        # вводим больше 60 символов - 61 символ
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, input_name))).\
                        send_keys("1234567890123456789012345678901234567890123456789012345678901")
        # пишем валидный емэйл
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, input_email))). \
                        send_keys("email@domain.com")
        # кликаем чек-бокс согласия PRIVACY_POLICY
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, privacy_policy))).click()
        # кликаем на кнопку отсылки "СЕНД"
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, btn_send))).click()
        # поиск элемента, содержащего текст ошибки
        error_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="leave-contact"]/form/div[1]/div[1]/p')))
        # проверка, что текст ошибки появился на странице
        assert "The name must not be greater than 60 characters" in error_element.text, \
                        "ОШИБКА: текст ошибки не найден на странице !!!"
    except Exception as e:
        # обработка исключений
        pytest.fail(f"ERROR: {str(e)}")
    finally:
        # закрытие браузера в любом случае
        sleep(20)  # ----------  3 ЗАПРОСА В МИНУТУ ОГРАНИЧИЛИ БЭКИ, ПОЭТОМУ 20 СЕК ПАУЗА МЕЖДУ ТЕСТАМИ !!!!!!!!
        # --------------------  иначе 503 ошибка сервера на втором запросе будет
        driver.quit()


# @pytest.mark.skip(reason = " Тест пропускается!!! ")
def test_email_less_two_simbols(driver):
    """
    ПОЛЕ "FULL NAME" МЕНЬШЕ 2 СИМВОЛОВ
    """
    try:
        # открытие страницы
        driver.get(link)
        # кликаем на кнопку КОНФИРМА в окне ПРИНЯТИЯ КУКИС
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, btn_cookies))).click()
        # кликаем на кнопку "Contact us":
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, btn_contact_us))).click()

        # вводим меньше 2 символов - 1 символ "1"
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, input_name))).send_keys("1")
        # пишем валидный емэйл
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, input_email))). \
            send_keys("email@domain.com")
        # кликаем чек-бокс согласия PRIVACY_POLICY
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, privacy_policy))).click()
        # кликаем на кнопку отсылки "СЕНД"
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, btn_send))).click()
        # поиск элемента, содержащего текст ошибки
        error_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located
                            ((By.XPATH, '//*[@id="leave-contact"]/form/div[1]/div[1]/p')))
        # проверка, что текст ошибки появился на странице
        assert "The name must be at least 2 characters" in error_element.text, "ОШИБКА: текст ошибки не найден на странице !!!"
    except Exception as e:
        # обработка исключений
        pytest.fail(f"ERROR: {str(e)}")
    finally:
        # закрытие браузера в любом случае
        sleep(20)  # ----------  3 ЗАПРОСА В МИНУТУ ОГРАНИЧИЛИ БЭКИ, ПОЭТОМУ 20 СЕК ПАУЗА МЕЖДУ ТЕСТАМИ !!!!!!!!
        # --------------------  иначе 503 ошибка сервера на втором запросе будет
        driver.quit()


# @pytest.mark.skip(reason = " Тест пропускается!!! ")
def test_empty_email(driver):
    """ ---------              ПУСТОЙ ЕМЭЙЛ
    1. Открыть ссылку https://cryptomus.com/
    2. В поле "Full name" ввести валидное имя (от 2 до 60 символов), например "Тестирование"
    3. Оставить поле ввода "Email" пустым
    4. Включить чек-бокс "I have read and agree to the Privacy Policy"
    5. Кликнуть на кнопку "Send"
    Ожидаемый результат: Бордер поля инпута окрашивается в красный цвет #c53a3a
    """
    try:
        # открытие страницы
        driver.get(link)
        # кликаем на кнопку КОНФИРМА в окне ПРИНЯТИЯ КУКИС
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, btn_cookies))).click()
        # кликаем на кнопку "Contact us":
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, btn_contact_us))).click()

        # вводим валидное ИМЯ
        WebDriverWait(driver, 10).until(EC.presence_of_element_located
                                        ((By.CSS_SELECTOR, input_name))).send_keys("Тестирование")
        # поиск поля ввода email:
        input_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, input_email)))
        # запоминание начального цвета поля ввода (был серый  #e8e8e8, станет красный #c53a3a)
        initial_color = input_element.value_of_css_property("border")
        # проверка print(initial_color)  1px solid rgb(68, 68, 68) #серый
        # Оставить поле ввода ""Email"" пустым
        input_element.send_keys("")
        # кликаем чек-бокс согласия PRIVACY_POLICY
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, privacy_policy))).click()
        # кликаем на кнопку отсылки "СЕНД"
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, btn_send))).click()
        # получение текущего цвета поля ввода после ввода значения
        current_color = input_element.value_of_css_property("border")
        # проверка print(current_color)  1px solid rgb(197, 58, 58) #красный
        # проверка, что цвет поля ввода изменился
        assert current_color != initial_color, "ОШИБКА: нет подсветки поля ввода емэйла !!!"
    except Exception as e:
        # обработка исключений
        pytest.fail(f"ERROR: {str(e)}")
    finally:
        # закрытие браузера в любом случае
        sleep(20)  # ----------  3 ЗАПРОСА В МИНУТУ ОГРАНИЧИЛИ БЭКИ, ПОЭТОМУ 20 СЕК ПАУЗА МЕЖДУ ТЕСТАМИ !!!!!!!!
        # --------------------  иначе 503 ошибка сервера на втором запросе будет
        driver.quit()


# @pytest.mark.skip(reason = " Тест пропускается!!! ")
@pytest.mark.parametrize("email",   [
                                    "email@@domain.com", "email@domain.c", "email@domain..com",
                                    "email@.domain.com", 'email@-domain.com', "email..email@domain.com",
                                    "email.@domain.com", ".email@domain.com", "email@domain.com (Joe Smith)",
                                    "Joe Smith <email@domain.com>",  "@domain.com", "email.domain.com",
                                    "plainaddress"
                                    ])
def test_negative_email(email, driver):
    """
    НЕГАТИВНЫЕ ТЕСТЫ: НЕПРАВИЛЬНЫЙ ЕМЭЙЛ
    1. Открыть ссылку https://cryptomus.com/
    2. В поле ""Email"" ввести неправильные емэйлы
    Должен появиться текст ошибки "The email must be a valid email address" и ГРАНИЦА инпута почты окрасится в красный
    """
    try:
        # открытие страницы
        driver.get(link)
        # кликаем на кнопку КОНФИРМА в окне ПРИНЯТИЯ КУКИС
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, btn_cookies))).click()
        # кликаем на кнопку "Contact us":
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, btn_contact_us))).click()

        # вводим валидное имя
        WebDriverWait(driver, 10).until(EC.presence_of_element_located
                                        ((By.CSS_SELECTOR, input_name))).send_keys("Тестирование")
        # поиск поля ввода email:
        input_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, input_email)))
        # запоминание начального цвета поля ввода (был серый  #e8e8e8, станет красный #c53a3a)
        initial_color = input_element.value_of_css_property("border")
        # поле ввода ""Email""
        input_element.send_keys(email)
        # кликаем чек-бокс согласия PRIVACY_POLICY
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, privacy_policy))).click()
        # кликаем на кнопку отсылки "СЕНД"
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, btn_send))).click()
        # получение текущего цвета поля ввода после ввода значения
        current_color = input_element.value_of_css_property("border")
        # проверка, что цвет поля ввода изменился
        assert current_color != initial_color, "ОШИБКА: нет подсветки поля ввода емэйла !!!"
        # поиск элемента, содержащего текст ошибки
        error_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="leave-contact"]/form/div[1]/div[2]/p')))
        # проверка, что текст ошибки появился на странице
        assert "The email must be a valid email address" in error_element.text, \
                                "ОШИБКА: текст ошибки не найден на странице !!!"
    except Exception as e:
        # обработка исключений
        pytest.fail(f"ERROR: {str(e)}")
    finally:
        # закрытие браузера в любом случае
        sleep(20)  # ----------  3 ЗАПРОСА В МИНУТУ ОГРАНИЧИЛИ БЭКИ, ПОЭТОМУ 20 СЕК ПАУЗА МЕЖДУ ТЕСТАМИ !!!!!!!!
        # --------------------  иначе 503 ошибка сервера на втором запросе будет
        driver.quit()


# @pytest.mark.skip(reason = " Тест пропускается!!! ")
def test_space_in_end_email(driver):
    """
    Пробел в конце емэйла
    1. Открыть ссылку https://cryptomus.com/
    2. В поле ""Email"" ввести пробел в конце емэйла, например "email@domain.com "
    Ожидаемый результат: инпут поля не позволяет ввести пробел
    """
    try:
        # открытие страницы
        driver.get(link)
        # кликаем на кнопку конфирма в окне принятия кукис
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, btn_cookies))).click()
        # кликаем на кнопку "Contact us":
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, btn_contact_us))).click()

        # вводим валидное имя
        WebDriverWait(driver, 10).until(EC.presence_of_element_located
                                        ((By.CSS_SELECTOR, input_name))).send_keys("Тестирование")
        # поле ввода "Email"
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, input_email))). \
            send_keys("email@domain.com ")
        # находим элемент ввода и получаем его значение
        email_input =  WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, input_email)))
        email_input_value = email_input.get_attribute("value")
        # сравниваем полученнное значение с "обрезанным" значением (без пробелов)
        assert email_input_value.strip() == email_input_value, "ОШИБКА: лишний пробел в конце емэйла !!! "
    except Exception as e:
        # обработка исключений
        pytest.fail(f"ERROR: {str(e)}")
    finally:
        # закрытие браузера в любом случае
        sleep(20)  # ----------  3 ЗАПРОСА В МИНУТУ ОГРАНИЧИЛИ БЭКИ, ПОЭТОМУ 20 СЕК ПАУЗА МЕЖДУ ТЕСТАМИ !!!!!!!!
        # --------------------  иначе 503 ошибка сервера на втором запросе будет
        driver.quit()


# @pytest.mark.skip(reason = " Тест пропускается!!! ")
def test_space_in_begin_email(driver):
    """
    Пробел в начале емэйла
    1. Открыть ссылку https://cryptomus.com/
    2. В поле ""Email"" ввести пробел в начале емэйла, например " email@domain.com"
    Ожидаемый результат: инпут поля не позволяет ввести пробел
    """
    try:
        # открытие страницы
        driver.get(link)
        # кликаем на кнопку конфирма в окне принятия кукис
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, btn_cookies))).click()
        # кликаем на кнопку "Contact us":
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, btn_contact_us))).click()

        # вводим валидное имя
        WebDriverWait(driver, 10).until(EC.presence_of_element_located
                                        ((By.CSS_SELECTOR, input_name))).send_keys("Тестирование")
        # поле ввода "Email"
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, input_email))). \
            send_keys(" email@domain.com")
        # находим элемент ввода и получаем его значение
        email_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, input_email)))
        email_input_value = email_input.get_attribute("value")
        # сравниваем полученнное значение с "обрезанным" значением (без пробелов)
        assert email_input_value.strip() == email_input_value, "ОШИБКА: лишний пробел в начале емэйла !!! "
    except Exception as e:
        # обработка исключений
        pytest.fail(f"ERROR: {str(e)}")
    finally:
        # закрытие браузера в любом случае
        sleep(20)  # ----------  3 ЗАПРОСА В МИНУТУ ОГРАНИЧИЛИ БЭКИ, ПОЭТОМУ 20 СЕК ПАУЗА МЕЖДУ ТЕСТАМИ !!!!!!!!
        # --------------------  иначе 503 ошибка сервера на втором запросе будет
        driver.quit()
