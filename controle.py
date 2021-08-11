from PyQt5 import uic, QtWidgets
import mysql.connector
from reportlab.pdfgen import canvas

numero_id = 0

banco = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="cadastro_prod"
)

categoria = ""
def pesquisa():
    global numero_id

    menu.show()

    linha = listagem.lineEdit.text().strip()
    cursor = banco.cursor()
    cursor.execute("SELECT * FROM produtos where id =" + str(linha))
    dados_lidos = cursor.fetchall()
    menu.lineEdit.setText(str(dados_lidos[0][0]))
    menu.lineEdit_3.setText(str(dados_lidos[0][1]))
    menu.lineEdit_2.setText(str(dados_lidos[0][2]))
    menu.lineEdit_4.setText(str(dados_lidos[0][3]))
    menu.lineEdit_5.setText(str(dados_lidos[0][4]))
    numero_id = dados_lidos[0][0]
    listagem.lineEdit.setText("")




def excluir_dados():
    linha = listagem.tableWidget.currentRow()
    listagem.tableWidget.removeRow(linha)

    cursor = banco.cursor()
    cursor.execute("SELECT id FROM produtos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("DELETE FROM produtos WHERE id=" + str(valor_id))
    aviso.close()
    print(f'Você exclui os dados de ID {valor_id}')

def chamar_editar():
    global numero_id

    linha = listagem.tableWidget.currentRow()
    cursor = banco.cursor()
    cursor.execute("SELECT id FROM produtos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("SELECT * FROM produtos WHERE id=" + str(valor_id))
    produto = cursor.fetchall()
    menu.show()

    menu.lineEdit.setText(str(produto[0][0]))
    menu.lineEdit_3.setText(str(produto[0][1]))
    menu.lineEdit_2.setText(str(produto[0][2]))
    menu.lineEdit_4.setText(str(produto[0][3]))
    menu.lineEdit_5.setText(str(produto[0][4]))
    numero_id = valor_id

def gerar_pdf():
    cursor = banco.cursor()
    comandosql = "SELECT * FROM produtos order by nomeprod"
    cursor.execute(comandosql)
    dados_lidos = cursor.fetchall()
    y = 0
    pdf = canvas.Canvas("pdfs\cadastramento_estoque.pdf")
    pdf.setFont("Times-Bold", 25)
    pdf.drawString(200,800, "Produtos Cadastrados:")
    pdf.setFont("Times-Bold", 10)

    pdf.drawString(10,750, "ID")
    pdf.drawString(110,750, "Nome do Produto")
    pdf.drawString(210,750, "Quantidade")
    pdf.drawString(310,750, "Preço")
    pdf.drawString(410,750, "Categoria")

    for i in range(0, len(dados_lidos)):
        y = y +50
        pdf.drawString(10,750 - y, str(dados_lidos[i][0]))
        pdf.drawString(110,750 - y, str(dados_lidos[i][1]))
        pdf.drawString(210,750 - y, str(dados_lidos[i][2]))
        pdf.drawString(310,750 - y, str(dados_lidos[i][3]))
        pdf.drawString(410,750 - y, str(dados_lidos[i][4]))

    pdf.save()

def funcao_principal():
    linha1 = formulario.caixanomep.text().lower().strip()
    linha2 = formulario.caixaquant.text().strip()
    linha3 = formulario.caixapreco.text().strip()
    print(f'Nome do produto {linha1}')
    print(f'Quantidade : {linha2}')
    print(f' Preço : {linha3}')
    if formulario.alimentos.isChecked():
        print("Categoria Alimentos selecionada")
        categoria = "Alimentos"
    elif formulario.bebidas.isChecked():
        print("Categoria bebidas selecionada")
        categoria = "Bebidas"
    else:
        print("Categoria Mercearia em Geral  selecionada")
        categoria = "Mercearia em Geral"

    cursor = banco.cursor()
    comandosql = "INSERT INTO produtos (nomeprod, quantidade, preco, categoria) VALUES(%s, %s, %s, %s)"
    dados = (str(linha1), str(linha2), str(linha3), str(categoria))
    cursor.execute(comandosql,dados)
    banco.commit()
    formulario.caixanomep.setText("")
    formulario.caixaquant.setText("")
    formulario.caixapreco.setText("")

def chama_listagem():
    listagem.show()
    cursor = banco.cursor()
    comandosql = "SELECT * FROM produtos order by nomeprod"
    cursor.execute(comandosql)
    dados_lidos = cursor.fetchall()
    listagem.tableWidget.setRowCount(len(dados_lidos))
    listagem.tableWidget.setColumnCount(5)

    for l in range (0, len(dados_lidos)):
        for c in range(0,5):
            listagem.tableWidget.setItem(l,c,QtWidgets.QTableWidgetItem(str(dados_lidos[l][c])))


def chamar_aviso():
    aviso.show()

def salvar_valor_editado():
    global numero_id

    nomeprod = menu.lineEdit_3.text()
    quantidade = menu.lineEdit_2.text()
    preco = menu.lineEdit_4.text()
    categoria = menu.lineEdit_5.text()
    cursor = banco.cursor()
    cursor.execute(
        "UPDATE produtos SET nomeprod = '{}', quantidade = '{}', preco = '{}', categoria ='{}' WHERE id = {}".format(
            nomeprod, quantidade, preco, categoria, numero_id))
    banco.commit()
    menu.close()
    listagem.close()
    chama_listagem()

app = QtWidgets.QApplication([])
formulario = uic.loadUi("formulario.ui")
listagem = uic.loadUi("listagemtela.ui")
aviso = uic.loadUi("aviso.ui")
menu = uic.loadUi("menueditar.ui")
formulario.pushButton.clicked.connect(funcao_principal)
formulario.pushButton2.clicked.connect(chama_listagem)
listagem.pushButton3.clicked.connect(gerar_pdf)
listagem.pushButton4.clicked.connect(chamar_aviso)
aviso.excluir.clicked.connect(excluir_dados)
listagem.editar.clicked.connect(chamar_editar)
menu.salvar.clicked.connect(salvar_valor_editado)
listagem.pushButton.clicked.connect(pesquisa)
formulario.show()
app.exec()