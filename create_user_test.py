import data
import configuration
import requests


def post_new_user(body):
    response = requests.post(configuration.URL_SERVICE + configuration.CREATE_USER_PATH, json=body, headers=data.headers)
    return response

def get_users_table():
    return requests.get(configuration.URL_SERVICE + configuration.GET_USER_TABLE_PATH)


def get_user_body(first_name):
    current_body = data.user_body.copy()
    current_body["firstName"] = first_name
    return current_body

def positive_assert(first_name):
    user_body = get_user_body(first_name)
    user_response = post_new_user(user_body)
    assert user_response.status_code == 201
    assert user_response.json()["authToken"] != ""
    #print(user_response.status_code)
    #print(user_response.json())
    users_table_response = get_users_table()
    #print(users_table_response.text)
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
                + user_body["address"] + ",,," + user_response.json()["authToken"]
    assert users_table_response.text.count(str_user) == 1

def test_create_user_2_letter_in_first_name_get_success_response():
    print("Старт тест 1")
    positive_assert("Аа")

def test_create_user_15_letter_in_first_name_get_success_response():
    print("Старт тест 2")
    positive_assert("Ааааааааааааааа")

def test_create_user_eng_letter_in_first_name_get_success_response():
    print("Старт тест 5")
    positive_assert("QWErty")

def test_create_user_rus_letter_in_first_name_get_success_response():
    print("Старт тест 6")
    positive_assert("Мария")

def negative_assert_symbol(first_name):
    user_body = get_user_body(first_name)
    user_response = post_new_user(user_body)
    assert user_response.status_code == 400
    assert user_response.json()["message"] == "Имя пользователя введено некорректно. " \
                                         "Имя может содержать только русские или латинские буквы, " \
                                         "длина должна быть не менее 2 и не более 15 символов"
    assert user_response.json()["code"] == 400


def test_create_user_1_letter_in_first_name_get_failed_response():
    print("Старт тест 3")
    negative_assert_symbol("A")


def test_create_user_16_letter_in_first_name_get_failed_response():
    print("Старт тест 4")
    negative_assert_symbol("Аааааааааааааааа")

def test_create_user_space_letter_in_first_name_get_failed_response():
    print("Старт тест 7")
    negative_assert_symbol("Человек и Ко")

def test_create_user_simvols_letter_in_first_name_get_failed_response():
    print("Старт тест 8")
    negative_assert_symbol("№%@")

def test_create_user_numb_letter_in_first_name_get_failed_response():
    print("Старт тест 9")
    negative_assert_symbol("123")





def negative_assert_no_first_name(user_body):
    user_response = post_new_user(user_body)
    assert user_response.status_code == 400
    assert user_response.json()["message"] == "Не все необходимые параметры были переданы"
    assert user_response.json()["code"] == 400


def test_create_user_no_first_name_get_failed_response():
    print("Старт тест 10")
    user_body = data.user_body.copy()
    user_body.pop("firstName")
    negative_assert_no_first_name(user_body)


def test_create_user_empty_first_name_get_error_response():
    print("Старт тест 11")
    user_body = get_user_body("")
    negative_assert_no_first_name(user_body)

def test_create_user_number_first_name_get_error_response():
    print("Старт тест 12")
    user_body = get_user_body(12)
    user_response = post_new_user(user_body)
    print(user_response.status_code)
    assert user_response.status_code == 400
    assert user_response.json()["code"] == 400




test_create_user_2_letter_in_first_name_get_success_response()
test_create_user_15_letter_in_first_name_get_success_response()
test_create_user_eng_letter_in_first_name_get_success_response()
test_create_user_rus_letter_in_first_name_get_success_response()
test_create_user_1_letter_in_first_name_get_failed_response()
test_create_user_16_letter_in_first_name_get_failed_response()
test_create_user_space_letter_in_first_name_get_failed_response()
test_create_user_simvols_letter_in_first_name_get_failed_response()
test_create_user_numb_letter_in_first_name_get_failed_response()
test_create_user_no_first_name_get_failed_response()
test_create_user_empty_first_name_get_error_response()
test_create_user_number_first_name_get_error_response()