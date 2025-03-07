from flask import Flask, jsonify, request
from supabase import create_client, Client 
from datetime import datetime 

app = Flask(__name__)

#Configuração do banco de dado 
SUPABASE_URL = "URL"
SUPABASE_KEY = "SENHA"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


#Rota de testes
@app.route('/')
def hello_world():
    return 'Tudo funcionado por aqui'

#rota de teste de conexão com o banco de dados
@app.route('/teste-supabase')
def test_supabase():
    try:
        response = supabase.table("TB_teste").select("*").limit(1).execute()
        if not response.data:
            return jsonify({"error":"Nenhum dado encontrado"}) , 404
    except Exception as e:
        return jsonify ({"error": str(e)}), 500 

#rota que verifica as infos do cartao
@app.route('/verificar-cartao')
def verificar_cartao():
    uid = request.args.get('uid')
    if not uid: 
        return jsonify({"error":"UID nao fornecido"}), 400
    try:
        response= supabase.table("TB_user").select("Nome").eq("UID", UID).execute()

        if response.data:
            Nome_usuario=response.data[0]["Nome"]

            hora_entrada = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            supabase.table("TB_acessos").insert({
                "UID":UID,
                "Nome_usuario": Nome_usuario,
                "entrada": hora_entrada,
                "saida": None
            }).execute()

            return jsonify({"Nome": Nome_usuario, "entrada":hora_entrada}) 

        else: 
            return jsonify("Acesso negado"),404

        except Exception as e: 
            return jsonify({"error": str(e)}) , 500 


if __name__ == '__main__':
    app.run(debug=True )