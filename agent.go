package main

import (
        "log"
        "os/exec"
        "encoding/json"
        "net/http"
)

type Command struct {
        Args []string `json:"args"`
}

type Response struct {
        Ok bool `json:"ok"`
        Message string `json:"message"`
}


func main(){
        http.HandleFunc("/api/run", func(w http.ResponseWriter, r *http.Request){
                if r.Method == "POST" {
                        // преобразование тела запроса в структуру
                        var newCommand Command
                        err := json.NewDecoder(r.Body).Decode(&newCommand)
                        if err!=nil {
                                error_json, _  := json.Marshal(Response{Ok: false, Message: "Request parsing error"})
                                http.Error(w, string(error_json), http.StatusBadRequest)
                                return
                        }
                        // Выполнение команды
                        cmd := exec.Command("sh", newCommand.Args...)
                        stdout, err := cmd.Output()
                        if err!=nil {
                                error_json, _ := json.Marshal(Response{Ok: false, Message: "Script run error"})
                                http.Error(w, string(error_json), http.StatusBadRequest)
                                return
                        }

                        success_json, _ := json.Marshal(Response{Ok: true, Message: string(stdout)})
                        w.Write(success_json)
                }
        })
        http.HandleFunc("/api/ping", func(w http.ResponseWriter, r *http.Request){
                if r.Method == "GET" {
                        success_json, _ := json.Marshal(Response{Ok: true, Message: "ping"})
                        w.Write(success_json)
                }
        })

        log.Fatal(http.ListenAndServe(":8080", nil))
}
