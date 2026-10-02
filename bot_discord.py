"""
Bot Discord Decifrando - Integração com Discord
Requer: pip install discord.py python-dotenv
"""

import discord
from discord.ext import commands
from bot_decifrando import BotDecifrando
from groq_helper import eh_mensagem_quiz, groq_configurado
import os
from dotenv import load_dotenv

load_dotenv()

# Configuração do bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

# Inicializa o bot de decifrando
decifrando = BotDecifrando()


@bot.event
async def on_ready():
    """Evento disparado quando o bot conecta ao Discord"""
    print(f'✅ Bot conectado como {bot.user}')
    if groq_configurado():
        print('🤖 Groq configurado — respostas automáticas de quiz ativadas.')
    else:
        print('⚠️  Groq NÃO configurado (GROQ_API_KEY ausente no .env) — só o dicionário local responde.')
    print(f'📊 Aguardando comandos...\n')


@bot.event
async def on_message(message):
    """Item pedido: o bot fica inativo (não responde nada) até perceber uma
    mensagem que parece um quiz (palavra embaralhada em maiúsculas, ou uma
    expressão matemática) solta no chat — SEM precisar digitar um comando
    como /desembaralha ou /math. Só dispara nesse caso bem específico, pra
    não ficar respondendo conversa normal do servidor."""
    # Nunca reage à própria mensagem (nem a de outros bots) — evita loop.
    if message.author.bot:
        return

    # Deixa os comandos de sempre (/desembaralha, /math, /auto, /help)
    # funcionando normalmente.
    await bot.process_commands(message)

    # Se já era um comando (começa com o prefixo), não processa de novo.
    if message.content.startswith('/'):
        return

    if eh_mensagem_quiz(message.content):
        resultado = decifrando.processar_entrada(message.content, idioma='pt')
        resposta_formatada = decifrando.formatar_resposta(resultado)
        await message.channel.send(resposta_formatada)


@bot.command(name='desembaralha', description='Desembaralha uma palavra')
async def desembaralha(ctx, *, palavra):
    """
    Comando: /desembaralha PALAVRA
    Exemplo: /desembaralha OTEPMOC
    """
    # Detecta idioma a partir de uma flag opcional
    args = palavra.split()
    idioma = 'pt'  # padrão

    # Procura flag de idioma (--es para espanhol)
    if '--es' in args:
        idioma = 'es'
        args.remove('--es')
        palavra = ' '.join(args)

    resultado = decifrando.desembaralhar_palavra(palavra, idioma)

    # Formata resposta
    if resultado[0] != "Nenhuma palavra encontrada":
        resposta_texto = ', '.join(resultado[:5])
        if len(resultado) > 5:
            resposta_texto += f"\n... e mais **{len(resultado)-5}** opções"

        embed = discord.Embed(
            title="🔤 Palavra Desembaraçada",
            description=f"**Input**: `{palavra}`",
            color=discord.Color.green()
        )
        embed.add_field(
            name="✅ Possíveis soluções",
            value=resposta_texto,
            inline=False
        )
    else:
        embed = discord.Embed(
            title="❌ Nenhuma palavra encontrada",
            description=f"Não consegui desembaraçar: `{palavra}`",
            color=discord.Color.red()
        )
        embed.add_field(
            name="💡 Dica",
            value="Verifique a palavra ou tente com `--es` para espanhol",
            inline=False
        )

    await ctx.send(embed=embed)


@bot.command(name='math', description='Resolve expressões matemáticas')
async def math(ctx, *, expressao):
    """
    Comando: /math EXPRESSÃO
    Exemplos:
    - /math 2+2
    - /math (10*5)+20
    - /math 100/4
    """
    resultado = decifrando.resolver_matematica(expressao)

    if "❌" in resultado or "Erro" in resultado:
        embed = discord.Embed(
            title="❌ Erro na Expressão",
            description=resultado,
            color=discord.Color.red()
        )
    else:
        embed = discord.Embed(
            title="🧮 Resultado Matemático",
            description=f"**Expressão**: `{expressao}`\n**Resultado**: `{resultado}`",
            color=discord.Color.blue()
        )

    await ctx.send(embed=embed)


@bot.command(name='auto', description='Processa automaticamente palavra ou matemática')
async def auto(ctx, *, texto):
    """
    Comando: /auto QUALQUER_TEXTO
    O bot detecta automaticamente se é palavra ou matemática
    """
    idioma = 'es' if '--es' in texto else 'pt'
    resultado = decifrando.processar_entrada(texto, idioma)
    resposta_formatada = decifrando.formatar_resposta(resultado)

    # Envia como embed
    if resultado['tipo'] == 'palavra_embaralhada':
        soluções = resultado['resultado']
        if isinstance(soluções, list):
            resposta_texto = ', '.join(soluções[:5])
            if len(soluções) > 5:
                resposta_texto += f"\n... +{len(soluções)-5} mais"
        else:
            resposta_texto = soluções

        embed = discord.Embed(
            title="🔤 Desembaralhar",
            color=discord.Color.green()
        )
        embed.add_field(name="Palavra", value=f"`{resultado['input']}`", inline=False)
        embed.add_field(name="Soluções", value=resposta_texto, inline=False)

    elif resultado['tipo'] == 'matematica':
        embed = discord.Embed(
            title="🧮 Matemática",
            color=discord.Color.blue()
        )
        embed.add_field(name="Expressão", value=f"`{resultado['input']}`", inline=False)
        embed.add_field(name="Resultado", value=f"`{resultado['resultado']}`", inline=False)

    else:
        embed = discord.Embed(
            title="❓ Comando não reconhecido",
            description=resultado['resultado'],
            color=discord.Color.orange()
        )

    await ctx.send(embed=embed)


@bot.command(name='help', description='Mostra ajuda')
async def help_command(ctx):
    """Mostra comandos disponíveis"""
    embed = discord.Embed(
        title="📚 Comandos Disponíveis",
        description="Bot Decifrando - Desembaralha palavras e resolve matemática",
        color=discord.Color.purple()
    )

    embed.add_field(
        name="/desembaralha PALAVRA",
        value="Desembaralha uma palavra\n*Exemplo: `/desembaralha OTEPMOC`*\n*Use `--es` para espanhol*",
        inline=False
    )

    embed.add_field(
        name="/math EXPRESSÃO",
        value="Resolve expressões matemáticas\n*Exemplo: `/math (10*5)+20`*",
        inline=False
    )

    embed.add_field(
        name="/auto TEXTO",
        value="Detecta automaticamente se é palavra ou matemática\n*Exemplo: `/auto desembaralha OTEPMOC`*",
        inline=False
    )

    embed.add_field(
        name="💡 Dicas",
        value="• Use `--es` para espanhol\n• Matemática: suporta +, -, *, /, (), %\n• Pode usar espaços e parênteses",
        inline=False
    )

    await ctx.send(embed=embed)


# ============================================================================
# CONFIGURAÇÃO E EXECUÇÃO
# ============================================================================

if __name__ == "__main__":
    TOKEN = os.getenv('DISCORD_TOKEN')

    if not TOKEN:
        print("❌ Erro: DISCORD_TOKEN não encontrado em .env")
        print("📝 Crie um arquivo .env com:")
        print("   DISCORD_TOKEN=seu_token_aqui")
        exit(1)

    print("🚀 Iniciando Bot Discord Decifrando...")
    bot.run(TOKEN)
