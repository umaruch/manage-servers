var servers = []; // Список серверов

// Подгрузка списка серверов
function update_servers_list(){
    const request = new XMLHttpRequest();
    request.open(
        "GET",
        `http://${window.location.host}/api/v1/servers/all`,
        true
    );

    request.addEventListener("readystatechange", ()=>{

        if (request.readyState === 4 && request.status === 200){
            // Сохранение и отрисовка полученного списка серверов
            servers = JSON.parse(request.responseText);
            render_servers_list(servers);
        }
    });

    request.send();
}

// Сохранение нового сервера
function save_new_server(){
    const request = new XMLHttpRequest();
    request.open(
        "POST",
        `http://${window.location.host}/api/v1/servers/0`,
        true
    );
    request.setRequestHeader("Content-Type", "application/json");
    address = document.getElementById("server_address_input").value;
    if (!ValidateIPaddress(address)){
        alert("Введите IP адрес в правильном формате");
        return
    }
    sname = document.getElementById("server_name_input").value;

    request.addEventListener("readystatechange", ()=>{
        if (request.readyState === 4 && request.status === 200){
            // Сохранение и отрисовка полученного списка серверов
            server = JSON.parse(request.responseText);
            servers.push(server);
            render_servers_list(servers);
            close_server_form();
        }
    });

    request.send(JSON.stringify({
        address: address,
        name: sname
    }));
}

// Изменение данных сервера
function change_server(id){
    const request = new XMLHttpRequest();
    request.open(
        "POST",
        `http://${window.location.host}/api/v1/servers/${id}`,
        true
    );
    request.setRequestHeader("Content-Type", "application/json");
    address = document.getElementById("server_address_input").value;
    if (!ValidateIPaddress(address)){
        alert("Введите IP адрес в правильном формате");
        return
    }
    sname = document.getElementById("server_name_input").value;

    request.addEventListener("readystatechange", ()=>{
        if (request.readyState === 4 && request.status === 200){
            // Сохранение и отрисовка полученного списка серверов
            for (server of servers){
                if (server.id === id){
                    data = JSON.parse(request.responseText);
                    server.address = data.address;
                    server.name = data.name;
                    break;
                }
            }
            render_servers_list(servers);
            close_server_form();
        }
    });

    request.send(JSON.stringify({
        address: address,
        name: sname
    }));
}

// Удаление сервера
function delete_server(id){
    const request = new XMLHttpRequest();
    request.open(
        "POST",
        `http://${window.location.host}/api/v1/servers/${id}/delete`,
        true
    );

    request.addEventListener("readystatechange", ()=>{
        if (request.readyState === 4 && request.status === 200){
            // Сохранение и отрисовка полученного списка серверов
            servers = JSON.parse(request.responseText);
            close_command_form();
            clear_console();
            render_blank_commands();
            render_servers_list(servers);
            close_server_form();
        }
    });

    request.send();
}

// Проверка доступности сервера
function ping_server(address){
    const request = new XMLHttpRequest();
    request.open(
        "GET",
        `http://${window.location.host}/api/v1/servers/ping?address=${address}`,
        true
    );

    request.addEventListener("readystatechange", ()=>{
        if (request.readyState === 4 && request.status === 200){
            // Сохранение и отрисовка полученного списка серверов
            res = JSON.parse(request.responseText);
   
            if (res.status){
                alert("Доступ к серверу есть");
            } else {
                alert("Нет доступа к серверу");
            }
        }
    });

    request.send();
}