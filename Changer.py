import json

class Changer:
    def __init__(self, nome_file: str) -> None:
        self.nome_file = nome_file
        self.leggi_json()

    def leggi_json(self) -> None:
        with open(self.nome_file, 'r', encoding='utf-8') as file:
            self.contenuto = json.loads(file.read())

    def aggiorna(self, nome_campo, campo_aggiornato) -> None:
        self.contenuto[nome_campo] = campo_aggiornato

    def scrivi_file(self) -> None:
        with open(self.nome_file, 'w', encoding='utf-8') as file:
            file.write(json.dumps(self.contenuto))

    def controlla_modifiche(self) -> bool:
        return Changer(self.nome_file).contenuto == self.contenuto
    