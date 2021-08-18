import requests
from werkzeug.wrappers import response

# def test_empty_servers_list():
#     # Получение пустого списка серверов
#     response = requests.get("http://localhost:8080/api/v1/servers/all")
#     assert response.status_code == 200
#     assert response.json() == []


# def test_add_server_1_success():
#     # Добавление сервера 1
#     data = {
#         "name": "Xiaomi top za svoi money",
#         "address": "172.17.17.215"
#     }
#     response = requests.post("http://localhost:8080/api/v1/servers/0", 
#         json=data
#     )

#     assert response.status_code == 200
#     assert response.json().get("name") != None


# def test_add_server_2_success():
#     # Добавление сервера 2
#     data = {
#         "name": "Huawei pizda",
#         "address": "222.222.222.222"
#     }
#     response = requests.post("http://localhost:8080/api/v1/servers/0", 
#         json=data
#     )

#     assert response.status_code == 200
#     assert response.json().get("name") != None


# def test_add_server_failed_method():
#     # Попытка отправки данных для добавления сервера с неправильным методом
#     data = {
#         "name": "Huawei pizda",
#         "address": "222.222.222.222"
#     }
#     response = requests.delete("http://localhost:8080/api/v1/servers/0", 
#         data=data
#     )

#     assert response.status_code != 200


# def test_add_server_failed_unknown_args():
#     # ОТправка неправилньх данных
#     data = {
#         "name": "Huawei pizda",
#         "address": "222.222.222.222"
#     }
#     response = requests.post("http://localhost:8080/api/v1/servers/0", 
#         json=data
#     )

#     assert response.status_code == 500


# def test_servers_list():
#     # Проверка добавленных серверов
#     response = requests.get("http://localhost:8080/api/v1/servers/all")
#     assert response.status_code == 200
#     assert len(response.json()) == 2


# def test_one_server_info():
#     # Получение данных единственного сервера
#     response = requests.get("http://localhost:8080/api/v1/servers/1")
#     assert response.status_code == 200
#     assert response.json().get("address") == '172.17.17.215'


# def test_change_on_server():
#     # Изменение существующего сервера
#     data = {
#         "name": "v2.0",
#         "address": "222.222.222.222"
#     }
#     response = requests.post("http://localhost:8080/api/v1/servers/2", 
#         json=data
#     )

#     assert response.status_code == 200
#     assert response.json().get("name") == "v2.0"


# def test_add_command_1_success():
#     # Добавить команду к серверу
#     data = {
#         "server_id": 1,
#         "name": "Hello",
#         "args": "hello.sh"
#     }
#     response = requests.post("http://localhost:8080/api/v1/commands/0",
#         json=data
#     )

#     assert response.status_code == 200
#     assert response.json().get("name") == "Hello" 


# def test_get_commands_list():
#     response = requests.get("http://localhost:8080/api/v1/commands/all/1")

#     assert response.status_code == 200
#     assert len(response.json()) == 1
#     assert response.json()[0].get("name") == "Hello"


# def test_run_command_1_success():
#     response = requests.post("http://localhost:8080/api/v1/commands/1/run")

#     assert response.status_code == 200
#     assert response.json().get("output") == "Hell\n"


def test_change_command_1_success():
    data = {
        "server_id": 8,
        "name": "test",
        "args": "hello2.sh"
    }
    response = requests.post("http://localhost:8080/api/v1/commands/2",
        json=data
    )

    assert response.status_code == 200
    assert response.json().get("name") == "test" 


# def test_long_time_running_1_success():
#     response = requests.post("http://localhost:8080/api/v1/commands/1/run")

#     assert response.status_code == 200
#     assert response.json().get("output") == "bulka\n"


# def test_delete_command_1_success():
#     response = requests.post("http://localhost:8080/api/v1/commands/delete/1/1")

#     assert response.status_code == 200
#     assert type(response.json()) == list
#     assert len(response.json()) == 0


# def test_delete_server_1_success():
#     response = requests.post("http://localhost:8080/api/v1/servers/2/delete", )

#     assert response.status_code == 200
#     assert len(response.json()) == 1