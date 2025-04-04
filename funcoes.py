

import sqlite3



class Gestor:
    def __init__(self, os, user):
        self.os = os
        self.user = user

    def gravaGeral(self,data):
        con = sqlite3.connect("tutorial.db")
        cur = con.cursor()
        cur.execute("""
        INSERT INTO osgeral (nome, setor_origem,setor_destino,titulo, descricao) VALUES
            (:nome, :setor_origem,:setor_destino,:titulo, :descricao)
        """,data)
        osgeral_id = cur.lastrowid
        cur.execute("""
        INSERT INTO osdetalhes (status,osgeral_id) VALUES
            (:status,:osgeral_id)
        """,("Aguardando inicio",osgeral_id))
        con.commit()
        cur.close()
        con.close()
        
    def gravaDetalhe(self,data):
        con = sqlite3.connect("tutorial.db")
        cur = con.cursor()
        cur.execute("""
        INSERT INTO osdetalhes (nome,atualiza,osgeral_id) VALUES
            (:nome,:atualiza,:osgeral_id)
        """,data)
        con.commit()
        cur.close()
        con.close()

    def gravaStatus(self,osgeral_id,status="Aguardando inicio"):
        con = sqlite3.connect("tutorial.db")
        cur = con.cursor()
        cur.execute("""
        INSERT INTO osstatus (status,osgeral_id) VALUES
            (:status,:osgeral_id)
        """,(status,osgeral_id))
        con.commit()
        cur.close()
        con.close()
        
    def loadGeral(self,row_id=0,setor=" "):
        sql_osgeral_status = """
            SELECT ge.id, ge.nome, ge.setor_origem,ge.setor_destino,ge.titulo, st.status FROM osgeral ge left join
                (SELECT status,
                    osgeral_id

                FROM (
                    SELECT status,
                    osgeral_id,
                        ROW_NUMBER() OVER (PARTITION BY osgeral_id ORDER BY id DESC) AS rn
                    FROM osdetalhes
                ) 
                WHERE rn = 1) as st on ge.id = st.osgeral_id
                """

        con = sqlite3.connect("tutorial.db")
        cur = con.cursor()
        if row_id == 0:
            if setor in ["SUPEEC","SUPNOR"]:
                res = cur.execute(sql_osgeral_status + " WHERE setor_origem = ?",(setor,))
            else:
                res = cur.execute(sql_osgeral_status)
        else:
            res = cur.execute("SELECT id, nome, setor_origem,setor_destino,titulo, descricao FROM osgeral WHERE id = ?",(row_id,))
        data = res.fetchall()
        cur.close()
        con.close()
        return data


    def loadDetalhe(self,id):
        con = sqlite3.connect("tutorial.db")
        cur = con.cursor()
        res = cur.execute("SELECT data, entrega, status, nome,atualiza FROM osdetalhes where osgeral_id = ? ",(id,))
        data = res.fetchall()
        data = [tuple(" " if element is None else element for element in tup) for tup in data]
        cur.close()
        con.close()
        return data
    
    def loadStatus(self):
        con = sqlite3.connect("tutorial.db")
        cur = con.cursor()
        res = cur.execute("SELECT * FROM osstatus ")
        data = res.fetchall()
        cur.close()
        con.close()
        return data
    
    def clearTables(self):
        con = sqlite3.connect("tutorial.db")
        cur = con.cursor()

        geral = [("fulano","SUPNOR","powerbi","criar novo workspace", "Preciso de um workspace com o nome 'SSER_teste' para desenvolvimento de alguns BI de teste. Neste workspace deverão ter acesso os funcionários Elvis, Edie e Tiririca."),
                ("ciclano","SUPEEC","powerbi","criar painel X", "descrição detalhada"),
                ("beltrano","INOVAÇÃO","powerbi","Adicionar botão ao painel Y", "descrição detalhada"),
                ("fulano","ASSESSORIA","extração de dados","extrair dados tais", "descrição detalhada"),
                ("ciclano","SUPEEC","extração de dados","extrair dados para PMPF", "descrição detalhada")]

        detalhes = [("P.O.","","Aguardando inicio","Demanda alocada para peão01",1),
                    ("peão01","","Em execução","Reunião marcada para dia 08/05/2024 para detalhar a demanda",1),
                    ("peão01","entrega","Em execução","Resultado preliminar enviado via e-mail para o demandante",1),
                    ("demandante","","Em execução","Solicito retificações, conforme e-mail enviado",1),
                    ("peão01","entrega","Em execução","Alterações providenciadas. Arquivo disponível em tal diretório",1),
                    ("P.O.","","concluido","Demanda concluida",1)]
        
        status = [("Aguardando inicio",1),
                  ("Aguardando inicio",2),
                  ("Aguardando inicio",3),
                  ("Aguardando inicio",4),
                  ("Aguardando inicio",5),
                  ("Em execução",1)
                  ]

      #  tipos_status = ["Aguardando inicio","Em execução","concluido"]

        try:
            cur.execute("DROP TABLE osgeral")
        except:
            pass

        try:
            cur.execute("DROP TABLE osdetalhes")
        except:
            pass

        try:
            cur.execute("DROP TABLE osstatus")
        except:
            pass


        cur.execute("""CREATE TABLE osgeral(id INTEGER PRIMARY KEY, 
                        nome varchar(20), 
                        setor_origem varchar(10),
                        setor_destino varchar(20),
                        titulo varchar(80), 
                        descricao varchar(500))""")
        
        cur.execute("""CREATE TABLE osstatus(id INTEGER PRIMARY KEY, 
                        data DATETIME DEFAULT (datetime('now','localtime')),
                        status varchar(20), 
                        osgeral_id INTEGER, 
                    FOREIGN KEY(osgeral_id) REFERENCES osgeral(id))""")

        cur.execute("""CREATE TABLE osdetalhes(id INTEGER PRIMARY KEY, 
                        data DATETIME DEFAULT (datetime('now','localtime')),
                        nome varchar(20), 
                        entrega varchar(20),
                        status varchar(20),
                        atualiza varchar(80),
                        dt_prazo DATETIME,
                        osgeral_id INTEGER, 
                    FOREIGN KEY(osgeral_id) REFERENCES osgeral(id))""")

        cur.executemany(""" INSERT INTO osgeral(
                        nome, 
                        setor_origem,
                        setor_destino,
                        titulo, 
                        descricao) VALUES (? , ? , ? , ? , ?)
                    """,geral)
        con.commit()

        cur.executemany(""" INSERT INTO osdetalhes(
                        nome,
                         entrega,
                        status, 
                        atualiza,
                        osgeral_id) VALUES (? , ? , ? , ? , ?)
                    """,detalhes)
        con.commit()

        cur.executemany(""" INSERT INTO osstatus(
                        status, 
                        osgeral_id) VALUES (? , ? )
                    """,status)
        con.commit()

        cur.close()
        con.close()




if __name__ == "__main__":
    gestor = Gestor(os=2,user="user")
    gestor.clearTables()
    data = gestor.loadDetalhe(id=1)
    print(data)
    

