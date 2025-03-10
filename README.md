# API do SALV (Sistema de Alerta Laboratorial com Visão)

Este repositório tem como objetivo descrever o funcionamento da API do SALV, suas funcionalidades, formas de comunicação e demais aspectos técnicos.

Nossa API foi desenvolvida para automatizar protocolos laboratoriais, tornando os processos mais eficientes, ágeis e seguros, além de ser de baixo custo.

Utilizamos a plataforma **PythonAnywhere** para o desenvolvimento e hospedagem da API. Essa plataforma baseada em nuvem oferece um ambiente completo para desenvolvimento, incluindo suporte para banco de dados, execução de código via linha de comando (Bash), hospedagem de aplicações e muito mais.

## Objetivo

Precisávamos de uma solução que permitisse a execução das nossas requisições HTTP sem a necessidade de armazenar o código localmente nos computadores dos laboratórios. Encontramos no PythonAnywhere a ferramenta ideal para essa necessidade, facilitando a configuração e execução dos nossos serviços na nuvem.

## Como funciona nossa API?

Nosso projeto tem foco em segurança e detecção de movimentos, [recomendamos conferir nosso projeto completo](https://github.com/WesleyS08/SALV). O objetivo principal é realizar autenticação, gravação e notificação para nosso aplicativo.

Caso um indivíduo entre no laboratório sem se identificar previamente, o sistema iniciará automaticamente a gravação do ambiente e enviará notificações para o aplicativo. A comunicação é realizada via linha de comando utilizando os serviços de nuvem do PythonAnywhere.

### Frameworks Utilizadas

- **Flask**: Framework web para Python que facilita a criação de aplicações web.
- **Supabase**: Plataforma de banco de dados que fornece uma alternativa ao Firebase, com suporte para PostgreSQL.


### Endpoints da API

A API possui os seguintes endpoints:

- **`GET /`**: Rota de teste para verificar se a API está funcionando.
- **`GET /teste-supabase`**: Rota para testar a conexão com o banco de dados Supabase.
- **`GET /verificar-cartao`**: Rota para verificar as informações de um cartão (UID) e determinar se é uma entrada ou saída.
- **`POST /registro-entrada`**: Rota para registrar uma nova entrada no banco de dados.
- **`POST /registro-acesso`**: Rota para registrar a saída de um usuário, atualizando o registro existente com a hora de saída.

### Exemplos de Uso
#### Verificar se a API está funcionando

```bash
curl -X GET "https://<seu-dominio>.pythonanywhere.com/"
```

#### Conexão com Banco
```bash
curl -X GET "https://<seu-dominio>.pythonanywhere.com/teste-supabase"
```
#### Verificar Cartão

```bash
curl -X GET "https://<seu-dominio>.pythonanywhere.com/verificar-cartao?uid=<UID>"
```

#### Regisrar Entrada

```bash
curl -X POST "https://<seu-dominio>.pythonanywhere.com/registro-entrada" -H "Content-Type: application/json" -d '{
  "uid": "<UID>",
  "nome_usuario": "<Nome do Usuário>",
  "dispositivo_id": "<ID do Dispositivo>",
  "entrada": "<Hora de Entrada>"
}'
```
#### Registrar Saída

```bash
curl -X POST "https://<seu-dominio>.pythonanywhere.com/registro-acesso" -H "Content-Type: application/json" -d '{
  "uid": "<UID>",
  "saida": "<Hora de Saída>"
}'
```

## Rodando os testes

Para rodar os testes, rode o seguinte comando

```bash
  git clone git https://github.com/WesleyS08/API_SALV.git
```
Importações para execução e depuração.
```bash
 pip install flash
```
OBS: Utilizamos o Supabase como banco, caso estiver usando outro, apenas troque o código abaixo.
```bash
pip install supabase
```