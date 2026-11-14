# Visão geral

## Motivação

Os cálculos de engenharia mecânica do dia a dia — dimensionar um eixo, verificar a flambagem de uma coluna, calcular a perda de carga de uma tubulação — costumam ser feitos em planilhas soltas, calculadoras online sem referência ou códigos pessoais sem verificação. O resultado são cálculos difíceis de auditar, de reaproveitar e de confiar.

O **mecalc** propõe uma alternativa aberta, organizada e verificável.

## Objetivos

- Ser usável por **alunos e profissionais sem conhecimento de programação**, pelo navegador.
- Entregar resultados **confiáveis e rastreáveis**, com memorial de cálculo e referências.
- Permitir **documentar** o trabalho: histórico de cálculos e exportação do memorial.
- Ser **gratuito e open source**, aberto a contribuições de outros alunos e engenheiros.

## Públicos

| Público | Necessidade | Canal |
| --- | --- | --- |
| Alunos de engenharia | Estudar, conferir exercícios, entender a teoria | App web |
| Engenheiros | Cálculos rápidos e documentados no trabalho | App web |
| Engenheiros que programam | Automatizar cálculos em scripts e notebooks | Biblioteca (`pip`) |
| Equipes, laboratórios e empresas | Uso interno com histórico persistente | Docker |

## Princípios

1. **Qualidade antes de quantidade.** Poucos cálculos completos (testados, documentados e com memorial) valem mais que muitos pela metade.
2. **Todo resultado é explicável.** Nenhum número aparece sem a fórmula e a referência que o produziram.
3. **Unidades sempre explícitas.** Nenhuma grandeza física circula sem unidade definida.
4. **Toda fonte é citada.** Valores tabelados e propriedades de materiais indicam sua origem.
5. **Simplicidade para o usuário.** Quem não programa nunca deve precisar abrir um terminal.

## Escopo

### Dentro do escopo

- Cálculos analíticos clássicos de engenharia mecânica, conforme a literatura de graduação e a prática de projeto.
- Banco de dados de referência (materiais, tolerâncias, catálogos), com fontes citadas.
- Memorial de cálculo e histórico.

### Fora do escopo (por enquanto)

- Análise por elementos finitos (FEA) e CFD.
- Modelagem CAD.
- Substituir normas técnicas ou a responsabilidade técnica do engenheiro.

## Direitos autorais dos dados

Valores físicos isolados (por exemplo, o limite de escoamento de um aço) são fatos e podem ser usados com citação da fonte. Já a **reprodução integral de tabelas** de livros ou normas (ISO, ABNT) pode infringir direitos autorais. As tabelas do projeto devem ser montadas com valores pontuais, sempre com fonte, ou a partir de dados públicos e catálogos que permitam o uso.

## Aviso de responsabilidade

O mecalc é uma ferramenta de apoio. Ele não substitui o julgamento técnico nem a responsabilidade profissional do engenheiro habilitado.
