import requests
from flask import Blueprint, json, request, jsonify

from .serializers import ServerSerializer, ScriptSerializer
from . import exceptions

api_bp = Blueprint("api", __name__)


#=================  Сервера
@api_bp.route("/servers/all")
def all_servers():
    # <= [{id, name, address}], [] || {error}
    try:
        servers = [server.json for server in ServerSerializer.all()]
        return jsonify(servers)
    except exceptions.ServerNotFoundError as exc:
        return jsonify({
            "error": exc.info
        }), 500


@api_bp.route("/servers/<int:server_id>")
def get_server(server_id: int):
    # <= {id, name, address} || {error}
    try:
        server = ServerSerializer.get(server_id)
        return jsonify(server.json)
    except exceptions.ServerException as exc:
        return jsonify({
            "error": exc.info
        }), 500


@api_bp.route("/servers/<int:server_id>", methods=["POST"])
def create_or_change_server(server_id: int):
    # => {address, name}
    # <= {id, name, address} || {error}
    try:
        if server_id == 0:
            # Создание новой записи
            new_server = ServerSerializer.create(**request.json)
            return jsonify(new_server.json)        
        
        changed_server = ServerSerializer.change(server_id, **request.json)
        return jsonify(changed_server.json)
    
    except exceptions.ServerException as exc:
        return jsonify({
            "error": exc.info
        }), 500


@api_bp.route("/servers/<int:server_id>/delete", methods=["POST"])
def delete_server(server_id: int):
    # <= [{id, name, address}]
    try:
        servers = [server.json for server in ServerSerializer.delete(server_id)]
        return jsonify(servers)
    except exceptions.ServerException as exc:
        return jsonify({
            "error": exc.info
        }), 500


@api_bp.route("/servers/ping")
def ping_server():
    # Проверка соединения с сервером
    url = f"http://{request.args.get('address')}:8080/api/ping"
    res = requests.get(url)

    if res.status_code == 200 and res.json().get("ok") == True:
        return jsonify({
            "status": True
        })
    
    return jsonify({
        "status": False
    })


#================   Команды
@api_bp.route("/commands/all/<int:server_id>")
def server_commands(server_id: int):
    try:
        commands = [command.json for command in ScriptSerializer.by_server(server_id)]
        return jsonify(commands)
    except exceptions.CommandException as exc:
        return jsonify({
            "error": exc.info
        }), 500
    

@api_bp.route("/commands/<int:command_id>")
def get_command(command_id: int):
    # <= {id, command_args, server} || {error}
    try:
        command = ScriptSerializer.get(command_id)
        return jsonify(command.json)
    except exceptions.ServerException as exc:
        return jsonify({
            "error": exc.info
        }), 500


@api_bp.route("/commands/<int:command_id>", methods=["POST"])   
def create_or_change_command(command_id: int):
    # => {server_id, name, command_args}
    # <= {id, server, name, command_args} || {error}
    try:
        if command_id == 0:
            command = ScriptSerializer.create(**request.json)
            print(command.name)
            return jsonify(command.json)

        command = ScriptSerializer.change(command_id, **request.json)
        return jsonify(command.json)
    
    except exceptions.CommandException as exc:
        return jsonify({
            "error": exc.info
        }), 500


@api_bp.route("/commands/run", methods=["POST"])
def run_command():
    # => {server_id, args}
    # <= {output}
    try:
        server_id = request.json["server_id"]
        args = request.json["args"].split()
        print(request.json)

        server = ServerSerializer.get(server_id)

        url = f"http://{server.address}:8080/api/run"
        data = {
            "args": args
        }
        print(data) 
        response =  requests.post(url, 
            json=data, timeout=20
        )

        return jsonify({
            "output": response.json()["message"],
            "server_name": server.name,
            "server_address": server.address
        })
    
    except exceptions.ServerException as exc:
        return jsonify({
            "error": exc.info
        }), 500

    except requests.exceptions.ConnectionError:
        return jsonify({
            "error": "Нет подключения к серверу"
        }), 500

    except KeyError:
        return jsonify({
            "error": "Неправильные аргменты в теле запроса"
        }), 400

    


@api_bp.route("/commands/delete/<int:server_id>/<int:command_id>", methods=["POST"])
def delete_command(server_id: int, command_id: int):
    try:
        commands = [command.json for command in ScriptSerializer.delete(command_id, server_id)]
        return jsonify(commands)
    except exceptions.ServerException as exc:
        return jsonify({
            "error": exc.info
        }), 500
