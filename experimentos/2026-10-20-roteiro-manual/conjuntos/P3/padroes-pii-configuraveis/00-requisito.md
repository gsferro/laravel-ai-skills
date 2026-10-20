# Requisito — FERRO-845: Padrões de PII configuráveis

## Fonte

- **Origem**: CARD FERRO-845 colado pelo desenvolvedor no chat desta sessão.
- **Data**: 2026-10-20.
- **Autor / solicitante**: solicitante do card; identidade não informada. O desenvolvedor apenas encaminhou o texto.
- **Fidelidade**: alta (texto escrito, transcrito literalmente).

## Texto Original

<!-- IMUTÁVEL. Não editar, corrigir, resumir ou reordenar. -->

```text
CARD FERRO-845 — Padrões de PII configuráveis

Hoje os padrões que o redator de PII usa para mascarar dados pessoais nos prompts de IA ficam
fixos dentro da classe. Queremos mover esses padrões para a configuração, para o time ajustar
sem mexer no código.

O comportamento atual não pode mudar: os mesmos tipos, na mesma ordem, com o mesmo marcador
[REDIGIDO:tipo]. Se a configuração não existir, usar os padrões de hoje.

Sem tela nova.
```

## Decomposição em Cláusulas

| ID | Cláusula | Trecho literal de origem | Tipo | Estado |
|----|----------|--------------------------|------|--------|
| RQ-01 | Disponibilizar os padrões do redator de PII na configuração, permitindo ao time ajustá-los sem alterar a classe. | "Queremos mover esses padrões para a configuração"; "sem mexer no código." | funcional | fechada |
| RQ-02 | Preservar os resultados atuais de mascaramento e detecção com a configuração padrão. | "O comportamento atual não pode mudar" | restrição | fechada |
| RQ-03 | Preservar os tipos atuais de PII. | "os mesmos tipos" | restrição | fechada |
| RQ-04 | Preservar a ordem atual de processamento dos tipos. | "na mesma ordem" | restrição | fechada |
| RQ-05 | Preservar o marcador de substituição por tipo. | "com o mesmo marcador"; "[REDIGIDO:tipo]." | restrição | fechada |
| RQ-06 | Usar os padrões atuais quando a configuração não existir. | "Se a configuração não existir, usar os padrões de hoje." | funcional | fechada |
| RQ-07 | Não criar uma tela para a feature. | "Sem tela nova." | restrição | fechada |

`fechada` significa que a obrigação escrita está determinada, não que foi implementada. Q1 e Q2 deixam pendentes somente os casos adicionais descritos abaixo. Não suspendem a configuração padrão, a configuração completa válida nem a ausência da configuração.

## Perguntas ao Solicitante

Somente a raia requisito. As recomendações não são respostas nem autorização para implementar os casos pendentes.

| ID | Pergunta | Afeta | Recomendação | Estado |
|----|----------|-------|--------------|--------|
| Q1 | Se a configuração vier parcial ou vazia, devemos completar os tipos com os padrões atuais ou recusar a execução? | RQ-01, RQ-03, RQ-06; somente configuração presente parcial/vazia | Recusar a execução antes de enviar o prompt à IA; falha fechado e evita desativar proteção por omissão. | aberta — solicitante indisponível |
| Q2 | Se a configuração presente tiver valor nulo, estrutura inválida ou regex inválida, devemos interromper a execução ou retornar aos padrões atuais? | RQ-01, RQ-02, RQ-06; somente configuração presente inválida | Interromper antes de enviar o prompt à IA, sem expor o conteúdo no erro; falha fechado e torna o erro de configuração visível. | aberta — solicitante indisponível |

### Rodada 1 — fronteira de requisito

❓ Q1 · raia: requisito · afeta: RQ-01, RQ-03, RQ-06 · depende de: —
Se a configuração vier parcial ou vazia, devemos completar os tipos com os padrões atuais ou recusar a execução?
➡️ Recomendação: recusar a execução antes de enviar o prompt à IA — falha fechado e evita desativar proteção por omissão.

❓ Q2 · raia: requisito · afeta: RQ-01, RQ-02, RQ-06 · depende de: —
Se a configuração presente tiver valor nulo, estrutura inválida ou regex inválida, devemos interromper a execução ou retornar aos padrões atuais?
➡️ Recomendação: interromper antes de enviar o prompt à IA, sem expor o conteúdo no erro — falha fechado e torna o erro de configuração visível.

Sem resposta, os dois recortes permanecem bloqueados. A resposta futura deve entrar como Adendo, com fonte e texto literal. Nenhuma cláusula fica integralmente `aberta — Qn`, pois as obrigações determinadas sobrevivem independentemente dessas respostas.

As sementes de papéis, visibilidade, notificações e teto de texto livre não se aplicam: o card não cria nenhum desses contratos. O prompt existente é contexto da feature, não um novo campo de texto livre.

## Premissas

Nenhuma premissa de comportamento adotada. As políticas de erro e de configuração incompleta são perguntas abertas, não premissas assumidas.

## Fora de Escopo (declarado)

- Tela nova, conforme RQ-07.
- Nesta sessão, por instrução do desenvolvedor: implementação e execução de steps posteriores ao 4; escrita fora desta pasta da wiki.

