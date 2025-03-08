from flask import Flask, jsonify, request
from supabase import create_client, Client
from datetime import datetime

app = Flask(__name__)

# Configurações do Supabase
SUPABASE_URL = "https://hyqdwihyectbkguvsjtd.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imh5cWR3aWh5ZWN0YmtndXZzanRkIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0MDc4NDc0NiwiZXhwIjoyMDU2MzYwNzQ2fQ.YgHCN1ZZvqaoZnyKAPs4PKVlhCAhJTeSTLbgUTCBF1s"
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
        # Verifica se o cartão está registrado
        response = supabase.table("TB_user").select("Nome").eq("UID", uid).execute()

        if not response.data:
            return jsonify({"status": "error", "message": "Acesso negado"}), 404

        nome_usuario = response.data[0]["Nome"]

        # Verifica se há uma entrada sem saída para esse UID
        acesso_response = supabase.table("TB_acessos").select("*").eq("UID", uid).is_("saida", "null").execute()

        if acesso_response.data:
            # Se houver uma entrada sem saída, é uma saída
            return jsonify({
                "status": "success",
                "message": "Saída registrada",
                "Nome": nome_usuario,
                "tipo": "saida"
            })
        else:
            # Se não houver, é uma entrada
            return jsonify({
                "status": "success",
                "message": "Entrada registrada",
                "Nome": nome_usuario,
                "tipo": "entrada"
            })

    except Exception as e:
        return jsonify({"status": "error", "message": f"Erro: {str(e)}"}), 500

# Rota para registrar uma entrada
@app.route('/registro-entrada', methods=['POST'])
def registrar_entrada():
    data = request.get_json()

    uid = data.get("uid")
    nome_usuario = data.get("nome_usuario")
    dispositivo_id = data.get("dispositivo_id")
    entrada = data.get("entrada")

    # Verifica se os dados essenciais estão presentes
    if not uid or not nome_usuario or not dispositivo_id or not entrada:
        return jsonify({"status": "error", "message": "Dados incompletos"}), 400

    try:
        # Registra uma nova entrada
        novo_registro = {
            "UID": uid,
            "Nome_usuario": nome_usuario,
            "Dispositivo_id": dispositivo_id,
            "entrada": entrada,
            "saida": None
        }
        supabase.table("TB_acessos").insert(novo_registro).execute()
        return jsonify({"status": "success", "message": "Entrada registrada com sucesso!"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Rota para registrar uma saída
@app.route('/registro-acesso', methods=['POST'])
def registrar_acesso():
    data = request.get_json()

    uid = data.get("uid")
    saida = data.get("saida")

    # Verifica se os dados essenciais estão presentes
    if not uid or not saida:
        return jsonify({"status": "error", "message": "Dados incompletos"}), 400

    try:
        # Verifica se há uma entrada sem saída para esse UID
        response = supabase.table("TB_acessos").select("*").eq("UID", uid).is_("saida", "null").execute()

        if response.data:
            # Atualiza o registro com a hora de saída
            acesso = response.data[0]
            acesso_id = acesso["id"]

            # Formata a saída para o formato adequado
            try:
                saida = datetime.strptime(saida, "%H:%M:%S").replace(year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
            except ValueError:
                return jsonify({"status": "error", "message": "Formato de saída inválido, use HH:MM:SS"}), 400

            # Atualiza a hora de saída
            supabase.table("TB_acessos").update({"saida": saida.isoformat()}).eq("id", acesso_id).execute()

            return jsonify({"status": "success", "message": "Saída registrada com sucesso!", "hora_saida": saida.isoformat()})
        else:
            return jsonify({"status": "error", "message": "Nenhuma entrada encontrada para esse UID"}), 404

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)