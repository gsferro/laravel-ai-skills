> Referência da feature-wiki 3.6.0. Lida em: step 9 (antes de varrer a wiki atrás de candidatos a rule e antes de apresentá-los ao usuário). Fonte única de: fontes de candidatos dentro da wiki e formato de apresentação.

# Candidatos a rule — fontes e apresentação

Os 4 gates, o teto de 3 por feature, a preferência por atualizar rule existente e o que fazer com a
resposta ficam no corpo do `SKILL.md`, step 9.

## Fontes de candidatos dentro da wiki


| Fonte | O que procurar | Exemplo |
|---|---|---|
| `02-decisoes-arquiteturais.md` | ADR cuja **consequência generaliza** além desta feature | "Todo valor monetário é `integer` em centavos" |
| `03-progresso.md` → Notas de Implementação | **Armadilha descoberta no código** que não se infere lendo o arquivo | "`Enrollment::find()` aplica scope global de tenant" |
| `01-plano-acao.md` | Padrão obrigatório que a wiki repetiu e que vale para o projeto todo | Padrão de log `[Classe@Método]` + channel por feature |

## Como apresentar

**Como apresentar**:

```text
Candidatos a rule desta feature (decisão sua):

1. [ADR-02] Valores monetários em centavos (integer)
   Glob: app/Models/**, app/Services/Billing/**
   Evidência: 02-decisoes-arquiteturais.md ADR-02 + app/Models/Invoice.php:34
   Gates: durável ✅ | escopável ✅ | não-inferível ✅ | não-redundante ✅

2. [Nota] Enrollment::find() aplica scope global de tenant
   Glob: app/Models/Enrollment.php, app/Services/Enrollment/**
   Evidência: 03-progresso.md → Notas de Implementação
   Gates: durável ✅ | escopável ✅ | não-inferível ✅ | não-redundante ✅

Virar rule? (1, 2, ambos, nenhum)
```
