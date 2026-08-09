from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from app.core.config import settings


def create_report(analysis):

    llm = ChatGroq(
        model=settings.GROQ_MODEL,
        temperature=0.2,
        api_key=settings.GROQ_API_KEY
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
Você é um especialista em arquitetura,
composição visual, proporção áurea,
teoria das cores e análise de imagens.

Sua função é interpretar métricas matemáticas
produzidas por um sistema de visão computacional.

Você NÃO deve inventar métricas.

Utilize exclusivamente os dados fornecidos.

O sistema considera:

90% da harmonia:
- proporções áureas;
- retângulos;
- pontos focais;
- aproximação da espiral áurea.

10% da harmonia:
- harmonia cromática.

Produza um relatório técnico,
mas compreensível.

Explique:

1. O nível geral de harmonia.
2. A influência do segmento áureo.
3. As proporções detectadas.
4. A distribuição dos pontos focais.
5. A influência da espiral áurea.
6. A harmonia das cores.
7. Os principais pontos positivos.
8. Os principais pontos que reduzem a harmonia.
9. Uma conclusão arquitetônica.

Não trate o resultado como uma verdade
científica absoluta. Trata-se de uma métrica
computacional baseada no modelo definido.
"""
            ),
            (
                "human",
                """
Dados matemáticos da análise:

{analysis}
"""
            )
        ]
    )

    chain = prompt | llm

    response = chain.invoke(
        {
            "analysis": str(analysis)
        }
    )

    return response.content