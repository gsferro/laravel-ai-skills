> Referência da feature-wiki 3.6.0. Lida em: step 4 (antes de escrever o `02-decisoes-arquiteturais.md`). Fonte única de: template do `02-decisoes-arquiteturais.md` em formato ADR.

# Template do `02-decisoes-arquiteturais.md`

O propósito e o que incluir ficam no corpo do `SKILL.md`, seção *Arquivo 02*. A tabela
`## Superfície Livewire`, que também mora no `02`, tem formato e greps em
`references/pesquisa-step-3.md`.

**Template `02-decisoes-arquiteturais.md`**:
```markdown
# Decisões Arquiteturais — {Card}

## ADR-01: {Título da Decisão}

**Status**: Aceita | Proposta | Deprecada
**Data**: {YYYY-MM-DD}

### Contexto
{Por que esta decisão é necessária — problema, restrições, pressões}

### Decisão
{O que foi decidido — a escolha feita}

### Alternativas Consideradas
1. {Alternativa A} — {por que foi descartada}
2. {Alternativa B} — {por que foi descartada}

### Consequências
- **Positivas**: {benefícios da decisão}
- **Negativas**: {trade-offs aceitos}
- **Riscos**: {riscos introduzidos e mitigações}

### Referências
- {arquivo:linha ou link relacionado}
- Refine: ADR-{xx} (se aplicável)

---

## ADR-02: {Título da Decisão}
...
```
