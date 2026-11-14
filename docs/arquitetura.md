# Arquitetura

## Visão em camadas

O projeto é dividido em camadas com dependências em **um único sentido**: as camadas de cima conhecem as de baixo, nunca o contrário.

```text
┌─────────────────────────────────────────────────────┐
│  ui/  — Interface (Streamlit)                       │
│  Coleta entradas, chama o núcleo, exibe resultados  │
└──────────────┬────────────────────────┬─────────────┘
               │                        │
┌──────────────▼──────────┐  ┌──────────▼─────────────┐
│  data/  e  history/     │  │  Núcleo de cálculo     │
│  Consulta de referência │  │  strength/, fluids/... │
│  e histórico            │  │  Python puro           │
└──────────────┬──────────┘  └────────────────────────┘
               │
┌──────────────▼──────────┐
│  db/  — SQLAlchemy      │
│  Modelos, engine,       │
│  migrations (Alembic)   │
└─────────────────────────┘
```

**Regra fundamental:** o núcleo de cálculo **não depende** de banco de dados nem de interface. As funções recebem números e devolvem resultados. Com isso:

- os testes são simples e rápidos, sem banco envolvido;
- quem usa a biblioteca pode passar valores próprios (de um ensaio de laboratório, por exemplo);
- a interface pode ser trocada no futuro sem reescrever os cálculos.

## Estrutura de pastas

```text
calculadora_tecnica/
├── pyproject.toml              # dependências e metadados (uv)
├── README.md
├── LICENSE
├── CHANGELOG.md
├── src/mecalc/
│   ├── config.py               # Settings (pydantic-settings), variáveis MECALC_*
│   ├── dependencies.py         # montagem das dependências (injeção)
│   ├── units.py                # registro de unidades (pint)
│   ├── report.py               # CalcReport: memorial de cálculo
│   ├── strength/               # resistência dos materiais
│   ├── machine_elements/       # elementos de máquinas
│   ├── fluids/                 # mecânica dos fluidos
│   ├── thermal/                # transferência de calor
│   ├── tolerances/             # ajustes ISO 286
│   ├── db/
│   │   ├── engine.py           # engine e sessão; URL via variável de ambiente
│   │   ├── models.py           # modelos ORM
│   │   └── migrations/         # Alembic
│   ├── data/
│   │   ├── sources/*.csv       # tabelas de referência (fonte da verdade)
│   │   ├── seed.py             # carga dos CSVs no banco
│   │   └── reference.py        # consultas; devolve modelos Pydantic
│   └── history/
│       ├── base.py             # interface HistoryRepository
│       ├── memory.py           # histórico em memória
│       └── sql.py              # histórico persistente (SQLAlchemy)
├── ui/
│   ├── Home.py                 # página inicial
│   ├── pages/                  # uma página por cálculo
│   └── components/             # widgets reaproveitáveis
├── tests/                      # espelha a estrutura de src/mecalc
├── docs/                       # documentação (MkDocs Material)
└── .github/workflows/          # integração contínua
```

## Modelos e configuração

- **Pydantic v2** define as entradas e saídas dos cálculos. Cada campo tem validação (`Field(gt=0)`), símbolo da literatura como `alias` (`L`, `E`, `Sy`), descrição e unidade. A interface usa esses metadados para montar os formulários.
- Os campos usam unidades do **SI**; a conversão de unidades acontece na interface, antes de criar o modelo.
- Os modelos do banco continuam no **SQLAlchemy**, separados dos modelos Pydantic.
- **pydantic-settings** centraliza a configuração em `config.py`. Todas as variáveis de ambiente usam o prefixo `MECALC_` e podem vir de um arquivo `.env`.

## Injeção de dependências

As classes recebem suas dependências pelo construtor, tipadas por `Protocol`. O módulo `dependencies.py` é o **único lugar** que decide qual implementação usar (por exemplo, histórico em memória ou em SQL, conforme `MECALC_HISTORY_BACKEND`). A injeção é manual, sem biblioteca externa.

```python
# na interface
history = get_history_repository(store=st.session_state)

# nos testes
service = HistoryService(repo=MemoryHistory({}))
```
