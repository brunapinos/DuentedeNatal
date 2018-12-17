# Duente de Natal
Telegram Bot para sorteios de amigo oculto

# Implantação do Bot
## Heroku
Para realizar o deploy do bot, crie um bot no Telegram através do [BotFather](http://t.me/botfather). Copie o Token fornecido por ele ao final do processo e guarde para usar no Heroku.

Crie uma aplicação no Heroku e escolha o repositório do seu código. Os passos de Deploy ficam a seu critério. Dentro da sua aplicação do Heroku, selecione **'Settings'** > **'Reveal config vars'** e escreva no espaço **KEY**:
```
PP_BOT_TOKEN
```
No campo **VALUE** preencha com o Token do bot criado anteriormente no BotFather.

## Testar localmente
Para rodar o bot localmente, no arquivo **duentebot.py**, comente ou apague a linha *import heroku.app*. Ainda no mesmo arquivo, no final, substitua *TOKEN = heroku.app.TOKEN* por *TOKEN = '[token do seu bot]'*, sem as chaves.

Para executar pela primeira vez, rode o seguinte comando dentro de um virtualenv para instalar os requisitos do projeto:

```
pip install -r requirements.txt
```

Para iniciar o bot, execute:
```
python3 duentebot.py
```

# Uso do bot
Para iniciar um sorteio, adicione o bot a um grupo. Comandos:
- **/start** inicializa o bot dentro do grupo/ permite que o bot envie mensagens privadas ao usuário que digitar o comando na conversa exclusiva do bot
- **/comesa** abre um novo sorteio para que os membros do grupo possam entrar
- **/sortia** realiza o sorteio com os participantes listados