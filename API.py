from flask import Flask, jsonify, request
from supabase import create_client, Client
from datetime import datetime
import os

app = Flask(__name__)

# Configuração do banco de dados
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Rota de teste
@app.route('/')
def hello_world():
    return 'Tudo funcionando por aqui!'

# Rota de teste de conexão com o banco de dados
@app.route('/teste-supabase')
def test_supabase():
    try:
        response = supabase.table("TB_teste").select("*").limit(1).execute()
        if not response.data:
            return jsonify({"status": "error", "message": "Nenhum dado encontrado"}), 404
        return jsonify({"status": "success", "message": "Dados encontrados com sucesso", "data": response.data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Rota que verifica as informações do cartão
@app.route('/verificar-cartao')
def verificar_cartao():
    uid = request.args.get('uid')
    if not uid:
        return jsonify({"status": "error", "message": "UID não fornecido"}), 400

    try:
        response = supabase.table("TB_user").select("Nome").eq("UID", uid).execute()

        if response.data:
            nome_usuario = response.data[0]["Nome"]
            return jsonify({"status": "success", "message": "Acesso autorizado", "Nome": nome_usuario})
        else:
            return jsonify({"status": "error", "message": "Acesso negado"}), 404

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/registro-acesso', methods=['POST'])
def registrar_acesso():
    data = request.get_json()

    dispositivo_id = data.get("dispositivo_id")
    uid = data.get("uid")
    nome_usuario = data.get("nome_usuario")
    entrada = data.get("entrada")
    saida = data.get("saida")
    
    if not dispositivo_id or not uid or not (entrada or saida):
        return jsonify({"status": "error", "message": "Dados incompletos"}), 400

    try:
        if entrada:
            # Registrar a entrada no banco de dados
            supabase.table("TB_acessos").insert({
                "UID": uid,
                "Nome_usuario": nome_usuario,
                "Dispositivo_ID": dispositivo_id,
                "entrada": entrada,
                "saida": None,  # A saída será preenchida mais tarde
                "status": "Autorizado"  # Pode ser "Autorizado" ou "Não Autorizado" conforme sua lógica
            }).execute()

            return jsonify({"status": "success", "message": "Entrada registrada com sucesso!"})

        elif saida:
            # Registrar a saída e atualizar o horário de saída
            response = supabase.table("TB_acessos").select("id", "entrada").eq("UID", uid).order("entrada", desc=True).limit(1).execute()
            
            if response.data:
                acesso = response.data[0]
                acesso_id = acesso["id"]
                hora_entrada = acesso["entrada"]
                
                # Atualiza a hora de saída
                supabase.table("TB_acessos").update({"saida": saida}).eq("id", acesso_id).execute()

                return jsonify({"status": "success", "message": "Saída registrada com sucesso!", "hora_entrada": hora_entrada, "saida": saida})

            else:
                return jsonify({"status": "error", "message": "Entrada não encontrada para esse UID"}), 404

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
