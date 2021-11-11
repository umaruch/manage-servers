var current_server_id = null;
var current_server_name = null;
var current_server_div = null;
var commands = [];

// Получение списка комманд сервера
function load_server_commands(server_element, server_id, server_name){
    if (current_server_div != null) {
        current_server_div.classList.remove("active");
        close_command_form();
        clear_console();
    }
    current_server_div = server_element.parentNode.parentNode;
    current_server_div.classList.add("active");

    current_server_id = server_id;
    current_server_name = server_name;
    const request = new XMLHttpRequest();
    request.open(
        "GET",
        `http://${window.location.host}/api/v1/commands/all/${server_id}`,
        true
    );

    request.addEventListener("readystatechange", ()=>{

        if (request.readyState === 4 && request.status === 200){
            // Сохранение и отрисовка полученного списка серверов
            commands = JSON.parse(request.responseText);
            console.log(commands);
            render_commands(commands);
        }
    });

    request.send(); 
}

// Создание новой команды
function create_new_command(){
    let command_name = document.getElementById("cmd_name_input").value;
    let script = document.getElementById("cmd_script_input").value;
    let command_args = document.getElementById("cmd_args_input").value;
    let args = [script, command_args].join(" ");
    console.log(args);

    const request = new XMLHttpRequest();
    request.open(
        "POST",
        `http://${window.location.host}/api/v1/commands/0`,
        true
    );
    request.setRequestHeader("Content-Type", "application/json");

    request.addEventListener("readystatechange", ()=>{

        if (request.readyState === 4 && request.status === 200){
            // Сохранение и отрисовка полученного списка серверов
            command = JSON.parse(request.responseText);
            commands.push(command);
            render_commands(commands);
            close_command_form();
        }
    });

    request.send(JSON.stringify({
        server_id: current_server_id,
        name: command_name,
        args: args
    }));
}

// Изменение выбранной команды
function change_command(command_id){
    let command_name = document.getElementById("cmd_name_input").value;
    let script = document.getElementById("cmd_script_input").value;
    let command_args = document.getElementById("cmd_args_input").value;
    let args = [script, command_args].join(" ");
    console.log(args);
    const request = new XMLHttpRequest();
    request.open(
        "POST",
        `http://${window.location.host}/api/v1/commands/${command_id}`,
        true
    );
    request.setRequestHeader("Content-Type", "application/json");

    request.addEventListener("readystatechange", ()=>{

        if (request.readyState === 4 && request.status === 200){
            // Сохранение и отрисовка полученного списка серверов
            for (cmd of commands){
                if (cmd.id === command_id){
                    data = JSON.parse(request.responseText);
                    cmd.args = data.args;
                    cmd.name = data.name;
                    break;
                }
            }
            render_commands(commands);
            close_command_form();
        }
    });

    request.send(JSON.stringify({
        server_id: current_server_id,
        name: command_name,
        args: args
    }));
}

// Удаление выбранной команды
function delete_command(command_id){
    const request = new XMLHttpRequest();
    request.open(
        "POST",
        `http://${window.location.host}/api/v1/commands/delete/${current_server_id}/${command_id}`,
        true
    );

    request.addEventListener("readystatechange", ()=>{

        if (request.readyState === 4 && request.status === 200){
            commands = JSON.parse(request.responseText);
            render_commands(commands);
            close_command_form();
        }
    });

    request.send();
}

// Воспроизведение команды
function run_command(){
    let script = document.getElementById("cmd_script_input").value;
    let command_args = document.getElementById("cmd_args_input").value;
    let args = [script, command_args].join(" ");

    const request = new XMLHttpRequest();
    request.open(
        "POST",
        `http://${window.location.host}/api/v1/commands/run`,
        true
    );
    request.setRequestHeader("Content-Type", "application/json");

    request.addEventListener("readystatechange", ()=>{

        if (request.readyState === 4){
            if (request.status === 200){
                data = JSON.parse(request.responseText);
                // console.log(data);
                var check = document.getElementById("clear_output_check");
                if (check.checked){
                    document.getElementById("cmd_output").value = `${data.server_name}: ${get_current_datetime()} > ${data.output}`;
                    return
                }
                document.getElementById("cmd_output").value += `${data.server_name}: ${get_current_datetime()} > ${data.output}`;
            } else {
                data = JSON.parse(request.responseText);
                alert(data.error);
            }
        }
    });

    request.send(JSON.stringify({
        server_id: current_server_id,
        args: args
    }));   
}