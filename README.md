
# API do SALV(Sistema de Alerta Laboratorial com Visão)

Este repositório tem como objetivo descrever o funcionamento da API do SALV, suas funcionalidades, formas de comunicação e demais aspectos técnicos.

Nossa API foi desenvolvida para automatizar protocolos laboratoriais, tornando os processos mais eficientes, ágeis e seguros, além de ser de baixo custo.

Utilizamos a plataforma **PythonAnywhere** para o desenvolvimento e hospedagem da API. Essa plataforma baseada em nuvem oferece um ambiente completo para desenvolvimento, incluindo suporte para banco de dados, execução de scripts via linha de comando (Bash),hospedagem de aplicações e muito mais.

## Objetivo

Precisávamos de uma solução que permitisse a execução dos nossas requisições HTTP sem a necessidade de armazenar o código localmente nos computadores dos laboratórios. Encontramos no PythonAnywhere a ferramenta ideal para essa necessidade, facilitando a configuração e execução dos nossos serviços na nuvem.

## Como funciona nossa API?

Nosso projeto tem foco em segurança e detecção de movimentos [recomendamos conferir nosso projeto completo](https://github.com/WesleyS08/SALV). O objetivo principal é realizar reconhecimento facial, autenticação, gravação e notificação para nosso aplicativo.

Caso um indivíduo entre no laboratório sem se identificar previamente, o sistema iniciará automaticamente a gravação do ambiente e enviará notificações para o aplicativo. A comunicação é realizada via linha de comando utilizando os serviços de nuvem do PythonAnywhere.

## Automação

Os protocolos implementados asseguram a operação contínua e autônoma do sistema, permitindo a inicialização automática e o controle remoto de dispositivos para maior eficiência e segurança.

| **Tecnologia**           | **Descrição**                                                               |
|--------------------------|:----------------------------------------------------------------------------:|
| **Wake-on-Lan (WOL)**     | Permite ligar o PC remotamente usando o ESP32, caso o PC esteja desligado ( Garanta que seu computador seja compatível). |
| **Task Scheduler**        | Automatiza a inicialização do programa Python ao ligar o PC.                |
| **AutoStart (Python Script)** | Configuração para iniciar automaticamente os serviços ao ligar a máquina. |

## Documentações da API

 - [PythonAnywhere](https://www.pythonanywhere.com/)
 - [Wikipédia](https://pt.wikipedia.org/wiki/PythonAnywhere)




| API   | Linguagem      | Descrição                           |
| :---------- | :--------- | :---------------------------------- |
| PythonAnywhere | `Python` | plataforma online para escrever, executar e hospedar aplicações Python diretamente do navegador, sem necessidade de instalação. |





## Autores

- [@WESLEY SILVA DOS SANTOS](https://www.github.com/WesleyS08)
- [@DAVI BRITO JUNIOR](https://www.github.com/DaveBrito)

