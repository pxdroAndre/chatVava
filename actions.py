import pandas as pd
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionBuscarJogador(Action):
    def name(self) -> Text:
        return "action_buscar_jogador"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Carregar dados do CSV
        df = pd.read_csv('Players.csv')
        
        # Pegar o nome do jogador da mensagem
        player = next(tracker.get_latest_entity_values("player"), None)
        
        if player:
            # Buscar jogador no DataFrame
            jogador = df[df['Player'].str.lower() == player.lower()]
            
            if not jogador.empty:
                jogador = jogador.iloc[0]
                resposta = (f"Aqui estão as informações sobre {jogador['Player']}:\n"
                          f"Ranking: {jogador['Rank']}\n"
                          f"Medalhas: {jogador['Gold']} Ouro, {jogador['Silver']} Prata, {jogador['Bronze']} Bronze\n"
                          f"Ganhos: {jogador['Earnings']}")
                
                dispatcher.utter_message(text=resposta)
            else:
                dispatcher.utter_message(text=f"Desculpe, não encontrei informações sobre {player}")
        else:
            dispatcher.utter_message(text="Por favor, me diga qual jogador você quer conhecer.")
        
        return []

class ActionTopJogadores(Action):
    def name(self) -> Text:
        return "action_top_jogadores"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        df = pd.read_csv('Players.csv')
        top5 = df.head(5)
        
        resposta = "Top 5 jogadores por ganhos:\n\n"
        for _, jogador in top5.iterrows():
            resposta += f"{jogador['Player']}: {jogador['Earnings']}\n"
        
        dispatcher.utter_message(text=resposta)
        return []