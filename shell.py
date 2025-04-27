import asyncio
import os
from rasa.core.agent import Agent
from rasa.shared.utils.io import raise_warning

async def main():
    # Verificar se o diretório models existe e contém arquivos
    if not os.path.exists("models") or not os.listdir("models"):
        print("Erro: Diretório 'models' não encontrado ou vazio.")
        print("Por favor, execute 'rasa train' primeiro.")
        return

    try:
        # Carregar o agente Rasa
        print("Carregando o modelo...")
        agent = Agent.load("models")
        
        if not agent:
            print("Erro: Não foi possível carregar o modelo.")
            return
            
        print("Bot: Olá! Sou um bot especialista em VALORANT. Como posso ajudar? (Digite 'sair' para encerrar)")
        
        while True:
            try:
                # Obter entrada do usuário
                message = input("Você: ")
                
                if message.lower() == 'sair':
                    print("Bot: Até mais! Foi um prazer ajudar!")
                    break
                
                # Processar a mensagem usando o Rasa
                print("\nProcessando mensagem...")
                responses = await agent.handle_text(message)
                print(f"Debug - Resposta completa do Rasa: {responses}")
                
                # Exibir as respostas do bot
                if responses:
                    for response in responses:
                        if "text" in response:
                            print(f"Bot: {response['text']}")
                        else:
                            print(f"Debug - Resposta sem texto: {response}")
                else:
                    print("Bot: Desculpe, não consegui processar sua mensagem.")
                    
            except Exception as e:
                print(f"Erro ao processar mensagem: {str(e)}")
                print("Bot: Desculpe, ocorreu um erro. Tente novamente.")
                
    except Exception as e:
        print(f"Erro ao inicializar o bot: {str(e)}")
        print("Certifique-se de que:")
        print("1. Você executou 'rasa train' primeiro")
        print("2. O servidor de ações está rodando ('rasa run actions')")
        print("3. Todos os arquivos de configuração estão corretos")

if __name__ == "__main__":
    asyncio.run(main()) 