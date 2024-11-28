import flet
import os
from Changer import Changer

class Program:

    def __init__(self, page: flet.Page) -> None:
        # impostiamo i parametri della finestra
        page.title = 'JSONchanger'
        page.window.height = 400
        page.window.width = 600
        page.vertical_alignment = flet.MainAxisAlignment.CENTER
        page.horizontal_alignment = flet.CrossAxisAlignment.CENTER

        # creiamo la finestra di dialogo per il file errato
        errore_nome_file = flet.AlertDialog(
            modal=True,
            title=flet.Text('Nome del file errato!'),
            content=flet.Text('Prova a reinserire il nome del file'),
            actions=[
                flet.TextButton('Ok', on_click=lambda e: page.close(errore_nome_file))
            ],
            actions_alignment=flet.MainAxisAlignment.END,
            on_dismiss=lambda e: page.close(errore_nome_file)
        )

        # creiamo il campo di testo e il suo handler
        campo_nome_file = flet.TextField(label='Nome del file',border_color='blue')
        def setup_changer(e):
            
            # aggiungiamo, nel caso in cui mancasse, l'estensione .json
            nome_file_trattato = campo_nome_file.value
            if nome_file_trattato[-5:] != '.json':
                nome_file_trattato += '.json'

            if os.path.isfile(nome_file_trattato):
                self.nome_file = nome_file_trattato
                self.changer = Changer(self.nome_file)
                self.schermata_modifica(page)
            else:
                campo_nome_file.color='red'
                campo_nome_file.border_color='red'
                page.open(errore_nome_file)
                page.update()

        def svuota_nome_file(e):
            campo_nome_file.value = ''
            campo_nome_file.color = 'blue'
            campo_nome_file.border_color = 'blue'
            page.update()

        # creiamo la finestra
        page.add(flet.Row([
            campo_nome_file,
            flet.ElevatedButton(text='Leggi file', color='blue', on_click=setup_changer),
            flet.IconButton(icon=flet.icons.DELETE, on_click=svuota_nome_file)
        ],
        alignment=flet.MainAxisAlignment.CENTER
        ))


    def schermata_modifica(self, page: flet.Page):
        # puliamo la pagina dalla schermata di inserimento del nome del file
        page.clean()

        # definiamo l'alert iniziale che ricorda di salvare le modifiche
        alert_iniziale = flet.AlertDialog(
            modal = True,
            title = flet.Text('Modalità di modifica'),
            content = flet.Text('Ricorda di salvare le modifiche una volta terminate premendo l\'apposito tasto al fondo della pagina'),
            actions = [
                flet.TextButton('Ok', on_click=lambda e: page.close(alert_iniziale))
            ],
            actions_alignment=flet.MainAxisAlignment.END,
            on_dismiss=lambda e: page.close(alert_iniziale)
        )
        
        # definiamo gli alert di salvataggio
        alert_salvataggio_ok = flet.AlertDialog(
            modal = True,
            title = flet.Text('Salvataggio avvenuto correttamente'),
            content = flet.Text('Il salvataggio è avvenuto correttamente'),
            actions = [
                flet.TextButton('Ok', on_click=lambda e: page.close(alert_salvataggio_ok))
            ],
            actions_alignment=flet.MainAxisAlignment.END,
            on_dismiss=lambda e: page.close(alert_salvataggio_ok)
        )

        alert_salvataggio_ko = flet.AlertDialog(
            modal = True,
            title = flet.Text('Errore nel salvataggio'),
            content = flet.Text('Si è verificato un errore nel salvataggio delle informazioni, effettua un backup delle modifiche prima di riavviare il programma'),
            actions = [
                flet.TextButton('Ok', on_click=lambda e: page.close(alert_salvataggio_ko))
            ],
            actions_alignment=flet.MainAxisAlignment.END,
            on_dismiss=lambda e: page.close(alert_salvataggio_ko)
        )

        # definiamo le proprietà grafiche della pagina
        page.window.height = 350
        page.window.width = 600

        # funzioni event handler
        def salva_contenuto(e):
            for campo in self.campi:
                self.changer.aggiorna(campo, self.campi[campo].value)

            self.changer.scrivi_file()

            if self.changer.controlla_modifiche():
                page.open(alert_salvataggio_ok)
            else:
                page.open(alert_salvataggio_ko)

        # carichiamo i campi di testo e i bottoni
        def carica_interfaccia(mostra_reset: bool=True):
            page.clean()
            self.campi = dict()

            for campo in self.changer.contenuto:
                self.campi[campo] = flet.TextField(value=self.changer.contenuto[campo], border_color='blue', border='blue')
                page.add(flet.Row([flet.Text(campo)], alignment=flet.MainAxisAlignment.START))
                page.add(self.campi[campo])

            page.add(flet.Row([
                flet.ElevatedButton(text='Salva', color='blue', on_click=salva_contenuto),
                flet.IconButton(icon=flet.icons.RESTORE, icon_color='red', on_click=carica_interfaccia)
            ],
            alignment = flet.MainAxisAlignment.END
            ))

            alert_reset_ok = flet.AlertDialog(
                modal = True,
                title = flet.Text('Reset avvenuto correttamente'),
                content = flet.Text('Si è stati riportati allo stato precedente alle modifiche non salvate'),
                actions = [
                    flet.TextButton('Ok', on_click=lambda e: page.close(alert_reset_ok))
                ],
                actions_alignment=flet.MainAxisAlignment.END,
                on_dismiss=lambda e: page.close(alert_reset_ok)
            )

            if mostra_reset:
                page.open(alert_reset_ok)

        carica_interfaccia(False)
        page.open(alert_iniziale)