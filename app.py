

from flask import Flask, render_template, request, session
import funcoes as fc
from flask_session import Session



app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

heading = ("id","Demandante","setor do demandante","setor de destino","Título","Status")
head_detalhes = ["Data","Houve Entrega?","Status","Servidor","Detalhamento"]



gestor = fc.Gestor(2,"user")

@app.route("/")
def index():
    if request.method == "POST":
        session["user"] = request.form.get("user")
    return render_template("index.html")

@app.route("/greet", methods=["GET","POST"])
def greet():

       # return render_template("greet.html", name = session["user"], heading=heading,datas=datas)
    if request.method == "POST":
            if request.form.get('delete') == 'sim':
                gestor.clearTables()
            #elif request.form.get('delete') == 'não':
                #pass
            elif request.form.get("user"):
                session["user"] = request.form.get("user")
            else:
                pass
       
    if request.method == "GET":
        name = request.args.get("name")
        setor_ori = request.args.get("setor_ori")
        setor_dest = request.args.get("setor_dest","")
        titulo = request.args.get("titulo","")
        descricao = request.args.get("descricao","")
        gestor.gravaGeral((name,setor_ori,setor_dest,titulo,descricao))
    match session["user"]:
        case "SUPEEC":
            datas = gestor.loadGeral(setor="SUPEEC")
        case "SUPNOR":
            datas = gestor.loadGeral(setor="SUPNOR")
        case _:
            datas = gestor.loadGeral()
    
    return render_template("greet.html", name = session["user"], heading=heading,datas=datas)
    

@app.route("/detalhe", methods=["GET","POST"])
def detalhe():
    if request.args.get('id'):
        session["id"] = request.args.get('id')
    osgeral = gestor.loadGeral(row_id=session["id"] )
    if request.method == "POST":
        nome = request.form.get("nome","")
        atualiza = request.form.get("atualiza","")
        gestor.gravaDetalhe((nome,atualiza,session["id"]))
    detalhes = gestor.loadDetalhe(id=session["id"])
    return render_template("detalhe.html",id=session["id"],detalhes=detalhes,osgeral=osgeral[0],head_detalhes=head_detalhes)
    #return render_template("detalhe.html",id=session["id"],detalhes=detalhes)

@app.route("/novaos", methods=["GET","POST"])
def novaos():
    return render_template("novaos.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
 



