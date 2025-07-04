import os
from typing import Optional
from typing import Any

from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain.agents.agent_types import AgentType


def get_env_var(name: str, default: Optional[str] = None) -> str:
    value = os.getenv(name, default)
    if value is None:
        raise EnvironmentError(f"Variável de ambiente {name} não encontrada.")
    return value


def create_agent() -> Any:
    """Cria e retorna o agente LangChain configurado para consultas SQL."""
    db_host = get_env_var("DB_HOST", "localhost")
    db_port = get_env_var("DB_PORT", "5432")
    db_name = get_env_var("DB_NAME", "flights")
    db_user = get_env_var("DB_USER", "postgres")
    db_password = get_env_var("DB_PASSWORD", "postgres")
    openai_api_key = get_env_var("OPENAI_API_KEY")

    database_url = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    db = SQLDatabase.from_uri(database_url)

    llm = ChatOpenAI(openai_api_key=openai_api_key, temperature=0)

    agent = create_sql_agent(
        llm=llm,
        db=db,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )

    return agent


agent = create_agent()


def ask_ai(question: str) -> str:
    """
    Envia a pergunta para o agente e retorna a resposta em português.
    
    Args:
        question (str): Pergunta a ser respondida pelo agente.

    Returns:
        str: Resposta do agente ou mensagem de erro.
    """
    try:
        prompt = f"Responda apenas em português pt-br: {question}"
        return agent.run(prompt)
    except Exception as e:
        return f"❌ Erro ao processar a pergunta: {str(e)}"
