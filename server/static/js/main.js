var current_command_div = null;

function open_create_server_form(){
    document.getElementById("server_form_title").innerText = "Регистрация нового сервера";
    document.getElementById("server_form").style.display = "block";
    document.getElementById("main").style.filter = "blur(4px)";
    document.getElementById("ping_server_but").onclick = function(){
        let address = document.getElementById("server_address_input").value;
        ping_server(address);
    }
    document.getElementById("del_server_but").style.display = "none";
    document.getElementById("save_server_but").onclick = function(){
        save_new_server();
    };   
}

function open_change_server_info_form(id, address, name){
    document.getElementById("server_form_title").innerText = "Редактирование сервера";
    document.getElementById("server_address_input").value = address;
    document.getElementById("server_name_input").value = name;
    document.getElementById("ping_server_but").onclick = function(){
        let address = document.getElementById("server_address_input").value;
        ping_server(address);
    }

    document.getElementById("server_form").style.display = "block";
    document.getElementById("main").style.filter = "blur(4px)";

    document.getElementById("del_server_but").style.display = "block";
    document.getElementById("del_server_but").onclick = function(){
        delete_server(id);
    }
    document.getElementById("save_server_but").onclick = function(){
        change_server(id);
    };   
}

function close_server_form(){
    document.getElementById("server_address_input").value = "";
    document.getElementById("server_name_input").value = "";

    document.getElementById("server_form").style.display = "none";
    document.getElementById("main").style.filter = "none";
}

// Отрисовка списка серверов на экране
function render_servers_list(servers_list){
    let list = document.getElementById("servers_list");
    list.innerHTML = "";
    for(server of servers_list){
        // Ячейка элемента
        let div = document.createElement("div");
        div.className = "list-group-item list-group-item-action py-3 lh-tight";
        div.setAttribute("aria-current", "true");

        // Контейнер, хранящий имя сервера и кнопку изменения
        let server_name_div = document.createElement("div");
        server_name_div.className = "d-flex w-100 align-items-center justify-content-between";

        // Имя сервера
        let name_strong = document.createElement("strong");
        name_strong.innerText = server.name;
        name_strong.className = "mb-1 clickable";
        name_strong.setAttribute("onclick", `load_server_commands(this, ${server.id}, '${server.name}')`);

        // Кнопка редактирования
        let change_server_but = document.createElement("small");
        change_server_but.innerText = "Изменить";
        change_server_but.className = "clickable";
        change_server_but.setAttribute("onclick",
            `open_change_server_info_form(${server.id}, '${server.address}', '${server.name}')`);

        server_name_div.appendChild(name_strong);
        server_name_div.appendChild(change_server_but);
        div.appendChild(server_name_div);

        // Адрес сервера
        let address_div = document.createElement("div");
        address_div.innerText = server.address;
        address_div.className = "col-10 mb-1 small";

        div.appendChild(address_div);

        list.appendChild(div);
    }
}

// Рендер кнопок команд  
function render_commands(cmds){
    document.getElementById("create_command_but").disabled = false;

    let list = document.getElementById("cmds_list");
    list.innerHTML = "";
    for(cmd of cmds){
        // Ячейка элемента
        let div = document.createElement("div");
        div.className = "list-group-item list-group-item-action py-3 lh-tight clickable";
        div.setAttribute("aria-current", "true");
        div.setAttribute("onclick",
         `open_change_command_form(this, ${cmd.id}, "${cmd.name}", "${cmd.args}")`);

        // Контейнер, хранящий имя сервера и кнопку изменения
        let cmd_name_div = document.createElement("div");
        cmd_name_div.className = "d-flex w-100 align-items-center justify-content-between";

        // Имя сервера
        let name_strong = document.createElement("strong");
        name_strong.innerText = cmd.name;
        name_strong.className = "mb-1";

        cmd_name_div.appendChild(name_strong);
        div.appendChild(cmd_name_div);

        // Аргументы команды
        let address_div = document.createElement("div");
        address_div.innerText = cmd.args;
        address_div.className = "col-10 mb-1 small";

        div.appendChild(address_div);

        list.appendChild(div);
    }
}

function open_create_command_form(){
    document.getElementById("cmd_form_title").innerText = "Создание команды";

    document.getElementById("cmd_name_input").disabled = false;
    document.getElementById("cmd_args_input").disabled = false;
    document.getElementById("cmd_name_input").value = "";
    document.getElementById("cmd_args_input").value = "";

    document.getElementById("del_cmd_but").disabled = true;

    document.getElementById("run_cmd_but").onclick = function(){
        run_command();
    }
    document.getElementById("run_cmd_but").disabled = false;

    // document.getElementById("delete-command").style.display = "none";
    document.getElementById("save_cmd_but").onclick = function(){
        create_new_command();
    };
    document.getElementById("save_cmd_but").disabled = false;   
}

function open_change_command_form(element, id, name, args){
    if (current_command_div != null) {
        current_command_div.classList.remove("active");
    }
    current_command_div = element;
    current_command_div.classList.add("active");

    document.getElementById("cmd_name_input").disabled = false;
    document.getElementById("cmd_args_input").disabled = false;

    document.getElementById("cmd_form_title").innerText = "Редактирование команды";

    document.getElementById("cmd_name_input").value = name;
    document.getElementById("cmd_args_input").value = args;

    document.getElementById("run_cmd_but").onclick = function(){
        run_command();
    }
    document.getElementById("run_cmd_but").disabled = false;

    document.getElementById("del_cmd_but").onclick = function(){
        delete_command(id);
    }
    document.getElementById("del_cmd_but").disabled = false;

    document.getElementById("save_cmd_but").onclick = function(){
        change_command(id);
    };
    document.getElementById("save_cmd_but").disabled = false;    
}

function close_command_form(){
    document.getElementById("cmd_name_input").value = "";
    document.getElementById("cmd_args_input").value = "";

    document.getElementById("run_cmd_but").disabled = true;
    document.getElementById("del_cmd_but").disabled = true;
    document.getElementById("save_cmd_but").disabled = true;

    document.getElementById("cmd_name_input").disabled = true;
    document.getElementById("cmd_args_input").disabled = true;
}

// Удаление списка команд и отключение формы ввода команды
function render_blank_commands(){
    document.getElementById("create_command_but").disabled = true;
    document.getElementById("cmds_list").innerHTML = "";
}

// Полная очистка вывода в консоли
function clear_console(){
    document.getElementById("cmd_output").value = "";
}