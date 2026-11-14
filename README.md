# mecalc — Calculadora Técnica de Engenharia Mecânica

> Cálculos de engenharia mecânica confiáveis, rastreáveis e abertos — com memorial de cálculo, unidades verificadas e validação contra a literatura técnica.

**Status:** 🚧 em planejamento (Fase 0 — Fundação)

---

## O que é

O **mecalc** é uma ferramenta open source para cálculos técnicos de engenharia mecânica — resistência dos materiais, elementos de máquinas, mecânica dos fluidos, transferência de calor e tolerâncias dimensionais.

Ela foi pensada para ser usada por **alunos e profissionais de engenharia sem exigir conhecimento de programação**, e ao mesmo tempo oferecer uma **biblioteca Python** para quem quiser automatizar cálculos em scripts e notebooks.

### Diferenciais

- **Memorial de cálculo:** cada resultado mostra os passos intermediários, as fórmulas, as hipóteses adotadas e a referência bibliográfica.
- **Unidades verificadas:** entradas e saídas com unidades explícitas, o que evita erros de conversão (mm × m, MPa × psi).
- **Validado contra a literatura:** os testes automatizados reproduzem exemplos resolvidos de livros clássicos (Shigley, Norton, Hibbeler etc.).
- **Rastreabilidade dos dados:** toda propriedade de material ou valor tabelado indica sua fonte.
- **Histórico de cálculos:** permite salvar, reabrir e exportar os cálculos realizados.

## Formas de uso

| Público | Como usar |
| --- | --- |
| Alunos e engenheiros | Pelo navegador, no app web *(link em breve)* |
| Quem programa em Python | `pip install mecalc` *(em breve)* |
| Equipes e empresas | `docker run` com histórico persistente *(em breve)* |


## Documentação

A pasta [docs/](docs/) reúne os detalhes do projeto:

- [Visão geral](docs/visao-geral.md)
- [Arquitetura](docs/arquitetura.md)

## Stack

Python 3.12 · Streamlit · SQLAlchemy 2.0 + Alembic · pint · NumPy/SciPy · Plotly · pytest · ruff · mypy · uv · Docker · MkDocs Material

## Aviso de responsabilidade

O mecalc é uma ferramenta de **apoio** ao cálculo de engenharia. Ele não substitui o julgamento técnico nem a responsabilidade profissional do engenheiro habilitado. Sempre verifique os resultados e as hipóteses adotadas antes de aplicá-los em projetos reais.

## Licença

MIT *(arquivo LICENSE a ser adicionado na Fase 0)*
