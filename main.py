from flet import *
import mysql.connector as mysql

#conectando ao db

conexao = mysql.connect(
    user = 'root',
    host = 'monorail.proxy.rlwy.net',
    password ='hGd32H-5H5e5Ca4d3ABBcdcf1G44aCGa',
    database ='railway',
    port = 47046
)
cursor = conexao.cursor()

# criar tabela

cursor.execute("CREATE TABLE IF NOT EXISTS agendamentos (id INTEGER PRIMARY KEY AUTO_INCREMENT, nome varchar(40), dia INT, hora INT)")

class App(UserControl):
    def __init__(self):
        super().__init__()

        self.todos_dados = Column(auto_scroll=True)
        self.nome = TextField(label='Seu Nome')
        self.editar_dados = TextField(label='Editar')

    #funcao de deletar dados
    def deletar(self, x, y):
        cursor.execute(f"DELETE FROM agendamentos WHERE id = {x}")
        conexao.commit()
        y.open = False

        #chamando a funcao de renderizar dados
        self.todos_dados.controls.clear()
        self.renderizar_todos()
        self.page.update()

    def atualizar(self,x, y, z):
        cursor.execute(f"UPDATE agendamentos SET nome = '{y}' WHERE id = '{x}'")
        conexao.commit()
        z.open = False

        #chamando a funcao de renderizar dados
        self.todos_dados.controls.clear()
        self.renderizar_todos()
        self.page.update()


        #chamando a funcao de renderizar dados
        self.todos_dados.controls.clear()
        self.renderizar_todos()
        self.page.update()

    def abrir_acoes(self,e):
        id_user = e.control.subtitle.value
        self.editar_dados.value = e.control.title.value
        self.update()
        alerta_dialogo = AlertDialog ( 
            title= Text(f"Editar ID {id_user}"),
            content= self.editar_dados,

            #botoes de acaoes
            actions=[
                ElevatedButton('deletar', color='white',bgcolor='red',on_click= lambda e:self.deletar(id_user,alerta_dialogo)),
                ElevatedButton('Atualizar',on_click=lambda e:self.atualizar(id_user,self.editar_dados.value,alerta_dialogo))
            ],
            actions_alignment='spaceBetween'
        )
        self.page.dialog = alerta_dialogo
        alerta_dialogo.open = True

        #atualizar a pagina
        self.page.update()

    def renderizar_todos(self):
        cursor.execute("SELECT * FROM agendamentos")
        meus_dados = cursor.fetchall()
        for dado in meus_dados:
            self.todos_dados.controls.append(
                ListTile(
                    subtitle=Text(dado[0]),
                    title=Text(dado[1]),
                    on_click=self.abrir_acoes
                )
            )
        conexao.commit()
        self.update()


    def adicionar_novo_dado(self,e):

        cursor.execute(f"INSERT INTO agendamentos (id ,nome,dia,hora) VALUES(id,'{self.nome.value}',10,10)")
        conexao.commit()
        self.todos_dados.controls.clear()
        self.renderizar_todos()
        self.page.update()


    def ciclo(self):
        self.renderizar_todos()

    def build(self):
        return Column([
        Text("AGENDE SEU CORTE",size=20, weight='bold'),
        self.nome,
        ElevatedButton("Adicionar Dados",on_click=self.adicionar_novo_dado,),
        self.todos_dados],)
        






def main(page:Page):
    page.vertical_alignment = MainAxisAlignment.SPACE_AROUND
    page.update()
    minha_aplicacao = App()

    page.add(minha_aplicacao)

app(target=main,view=WEB_BROWSER)