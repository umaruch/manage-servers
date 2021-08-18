import sqlite3

from server.extensions import db_connection
from .models import Server, Script
from . import exceptions

class ServerSerializer:
    @staticmethod
    def all():
        try:
            servers_list = []
            cursor = db_connection.cursor()
            for server_data in cursor.execute("SELECT * FROM servers").fetchall():
                servers_list.append(Server(
                    server_data[0],
                    server_data[1],
                    server_data[2]
                ))
                
            return servers_list

        except sqlite3.IntegrityError:
            raise exceptions.ServerException("Ошибка получения данных")

        except sqlite3.OperationalError:
            raise exceptions.ServerException("Ошибка подключения к БД." \
                "Пожайлуйста перезагрузите сервер")


    @staticmethod
    def get(id: int):
        try:
            cursor = db_connection.cursor()
            cursor.execute("SELECT * FROM servers WHERE id=?", (id,))
            rows = cursor.fetchone()
            print(rows)
            return Server(rows[0], rows[1], rows[2])

        except sqlite3.IntegrityError:
            raise exceptions.ServerException("Данные не найдены")

        except sqlite3.OperationalError:
            raise exceptions.ServerException("Ошибка подключения к БД." \
                "Пожайлуйста перезагрузите сервер")

    @staticmethod
    def create(address: str, name: str) -> Server:
        try:
            cursor = db_connection.cursor()
            cursor.execute("INSERT INTO servers (address, name) VALUES (?, ?)", (address, name,))
            server_id = cursor.lastrowid
            db_connection.commit()
            return Server(server_id, address, name)
        except sqlite3.IntegrityError:
            raise exceptions.ServerException("Имя и адрес должны быть уникальными")

        except sqlite3.OperationalError:
            raise exceptions.ServerException("Ошибка подключения к БД." \
                "Пожайлуйста перезагрузите сервер")

    @staticmethod
    def change(id: int, address: str, name: str) -> Server:
        try:
            cursor = db_connection.cursor()
            cursor.execute("UPDATE servers SET address = ?, name = ? WHERE id = ?",
                (address, name, id)
            )
            db_connection.commit()
            return Server(id, address, name)

        except sqlite3.IntegrityError:
            raise exceptions.ServerException("Имя и адрес должны быть уникальными")

        except sqlite3.OperationalError:
            raise exceptions.ServerException("Ошибка подключения к БД." \
                "Пожайлуйста перезагрузите сервер")

    @staticmethod
    def delete(id: int):
        try:
            cursor = db_connection.cursor()
            cursor.execute("DELETE FROM servers WHERE id=?", (id,))
            db_connection.commit()
            servers_list = []
            for server_data in cursor.execute("SELECT * FROM servers").fetchall():
                servers_list.append(Server(
                    server_data[0],
                    server_data[1],
                    server_data[2]
                ))
            return servers_list
        
        except sqlite3.IntegrityError:
            raise exceptions.ServerException("ОШибка в удалении данных, проверьте верность id сервера")

        except sqlite3.OperationalError:
            raise exceptions.ServerException("Ошибка подключения к БД." \
                "Пожайлуйста перезагрузите сервер")


class ScriptSerializer:
    @staticmethod
    def by_server(server_id: int):
        try:
            commands = []
            cursor = db_connection.cursor()
            cursor.execute("SELECT * FROM commands WHERE server_id=?", (server_id,))
            for command_data in cursor.fetchall():
                commands.append(Script(
                    command_data[0],
                    command_data[1],
                    command_data[2],
                    command_data[3]
                ))
            return commands

        except sqlite3.IntegrityError:
            raise exceptions.CommandException("Ошибка получения данных")

        except sqlite3.OperationalError:
            raise exceptions.CommandException("Ошибка подключения к БД." \
                "Пожайлуйста перезагрузите сервер")

    @staticmethod
    def get(id: int):
        try:
            cursor = db_connection.cursor()
            cursor.execute("SELECT * FROM commands WHERE id=?", (id,))
            rows = cursor.fetchone()
            return Script(
                rows[0],
                rows[1],
                rows[2],
                rows[3]
            )

        except sqlite3.IntegrityError:
            raise exceptions.CommandException("Данных по полученному id не найдено")

        except sqlite3.OperationalError:
            raise exceptions.CommandException("Ошибка подключения к БД." \
                "Пожайлуйста перезагрузите сервер")
    
    @staticmethod
    def create(server_id: int, name:str, args: str):
        try:
            print(f"{server_id} {name} {args}")
            cursor = db_connection.cursor()
            cursor.execute("INSERT INTO commands (server_id, name, args) VALUES (?,?,?)",
                (server_id, name, args)
            )
            command_id = cursor.lastrowid
            db_connection.commit()

            return Script(
                command_id, server_id,
                name, args
            )

        except sqlite3.IntegrityError:
            raise exceptions.CommandException("Название должно быть уникальным")

        except sqlite3.OperationalError:
            raise exceptions.CommandException("Ошибка подключения к БД." \
                "Пожайлуйста перезагрузите сервер") 

    @staticmethod
    def change(id: int, server_id: int, name: str, args: str):
        try:
            cursor = db_connection.cursor()
            cursor.execute("UPDATE commands SET name=?, args=? WHERE id=?",
                (name, args, id)
            )
            db_connection.commit()
            print("Новое имя:", name)
            print("Данные сохранены")
            return Script(
                id, server_id,
                name, args
            )

        except sqlite3.IntegrityError:
            raise exceptions.CommandException("Название должно быть уникальным")

        except sqlite3.OperationalError:
            raise exceptions.CommandException("Ошибка подключения к БД." \
                "Пожайлуйста перезагрузите сервер")

    @staticmethod
    def delete(id: int, server_id: int):
        try:
            commands = []
            cursor = db_connection.cursor()
            cursor.execute("DELETE FROM commands WHERE id=?", (id,))
            db_connection.commit()
            cursor.execute("SELECT * FROM commands WHERE server_id=?", (server_id,))
            for command_data in cursor.fetchall():
                commands.append(Script(
                    command_data[0],
                    command_data[1],
                    command_data[2],
                    command_data[3]
                ))
            return commands

        except sqlite3.IntegrityError:
            raise exceptions.CommandException("Название должно быть уникальным")

        except sqlite3.OperationalError:
            raise exceptions.CommandException("Ошибка подключения к БД." \
                "Пожайлуйста перезагрузите сервер")