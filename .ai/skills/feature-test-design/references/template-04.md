> Referência da feature-test-design 1.15.0. Lida em: passo 6 (formato da tabela de mutantes), passo
> 7 (tabela de cogitado e cortado), escrita do `04` (o template inteiro) e pós-implementação (teste
> de arquitetura de sincronia de IDs). Fonte única de: o template do arquivo `04-casos-de-teste.md`.

# Template do arquivo 04 — Casos de Teste

**Path**: `wikis/specs/{branch}/{feature}/04-casos-de-teste.md`. As regras que o template carrega
estão no `SKILL.md` §Arquivo 04 e valem mesmo que o template seja adaptado.

## Template

```markdown
# Casos de Teste — {Card}: {Título}

> Requisito: `00-requisito.md` · Plano: `01-plano-acao.md`
> Derivado do **requisito**, não do plano. Nenhum cenário foi escrito olhando implementação.

## Perfil de Derivação

| Área | P | I | P×I | Perfil |
|---|---|---|---|---|
| {cálculo do desconto} | 3 | 3 | 9 | completo |
| {listagem} | 1 | 1 | 1 | mínimo |

- Técnicas aplicadas: {EP, BVA 3-valores, tabela de decisão, tabela estado × evento}
- Cenários: {n} · Regras: {n} · Mutantes previstos: {n} · Sem matador: {n}
<!-- derivado do Índice de Cenários; recalcular a cada cenário novo — ou apagar a linha. Contagem manual defasada é a mentira mais barata de produzir -->

## Varredura SFDIPOT

| Letra | O que existe nesta feature | Cenários gerados |
|---|---|---|
| S | {…} | — |
| F | {…} | CT-01, CT-02 |
| D | {…} | CT-03…CT-08 |
| I | {…} | CT-09 |
| P | {não se aplica: sem dependência de plataforma além do banco} | — |
| O | {…} | CT-10 |
| T | {…} | CT-11, CT-12 |

## Mapa de Regras

| Regra | Área (perfil herdado) | Origem (`RQ`) | Técnica | Cenários |
|---|---|---|---|---|
| R1 — {…} | cálculo (completo) | RQ-01, RQ-04 | BVA 3-valores | CT-01…CT-04 |
| R2 — {…} | listagem (mínimo) | RQ-02 | tabela de decisão | CT-05, CT-06 |

<!-- Técnica escalada acima do perfil da área: declarar aqui, em uma linha, com o motivo. -->

## Fronteira com o Plano

<!-- O que veio do 01-plano-acao.md e foi RECUSADO como oráculo, para o cenário não virar
     teste do PRD. Item que só o PRD determina e é visível ao usuário vira pergunta. -->

| Item do PRD | Recusado como oráculo porque | Destino |
|---|---|---|
| {nome do método `aplicarEm()`} | escolha de implementação | detalhe do cenário |
| {texto do erro na tela} | comportamento visível que o requisito não determina | pergunta ao usuário |

**Perguntas em aberto** (replicadas em `00-requisito.md` → `## Ambiguidades e Perguntas Abertas`):
- {pergunta} — bloqueia R{n}; premissa adotada: {…} (cenários marcados `@premissa`)

## Setup Global

### Personas
- `{papel}` — {como criar, com o helper real do projeto}

### Fixtures
- `{Model}::factory()->{state}()` — {estado}
- **Situação de partida com ciclo de vida: por transições reais.** Helper `{entidade}Em('{situacao}', [...])`
  em `tests/Pest.php` que chama a máquina de estados do domínio (`enviar()`, `aprovar()`…) em vez de
  gravar `situacao` à força. Reimplementar a transição no teste esconde o defeito que o teste existe
  para pegar. Medido (2026-09-21): a fixture por transição expôs que a notificação real exigia
  contexto de painel — um `create(['situacao' => …])` nunca mostraria

### Fakes
- `Queue::fake()` / `Mail::fake()` / `Notification::fake()` / `Http::fake()` + `Http::preventStrayRequests()`

### Estratégia de DB
- {`RefreshDatabase` global no `tests/Pest.php`, ou o que o projeto usa}

---

## Regra R1 — {enunciado da regra}

> `RQ-01`, `RQ-04` · perfil **completo** · técnica: **BVA 3-valores** (fronteira: {campo}, granularidade {tipo})

```gherkin
# language: pt
Funcionalidade: {…}

  Regra: {…}

    Cenário: [CT-01] {comportamento}
      Dado {…}
      Quando {…}
      Então {…}
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M1 | {…} | CT-01 |
| M2 | {…} | ⚠️ **sem matador** — {motivo / lacuna declarada} |

---

## Checklist de Taxonomia

<!-- Resposta válida: um ID de cenário, "não se aplica: {motivo}", ou
     "lacuna declarada: {o que foi tentado}". NUNCA "sim". -->

| Item | Cenário que mata |
|---|---|
| IDOR / autorização horizontal | CT-09 |
| Autorização exercida na ação (não só `can()`) | CT-19 |
| Idempotência (ancorada no agregado) | CT-07 |
| Concorrência | CT-08 |
| **Fronteira no ponto de entrada** (gravação) | CT-30, CT-31 |
| **Domínio condicionado** (tipo × valor) | CT-08 |
| **Estado × operação de escrita** (excluído ainda funciona?) | CT-21 |
| Ausente ≠ null ≠ vazio | não se aplica: sem campo opcional |
| Paginação / ordenação | … |
| Timezone / DST | lacuna declarada: tentado `config(['app.timezone'])` divergente; {resultado} |
| Unicode / limite de varchar | … |
| Unicidade + soft delete | … |
| CRUD combinado | … |
| Mass assignment | … |
| Upload | não se aplica: sem upload |
| Precisão monetária | CT-02 |
| **Superfície Livewire** (método público, prop pública, estado do framework) | CT-31, CT-32 |
| **Estado do framework usado sem validar** (índice de array, `parse`, coluna) | CT-33 |
| **IDOR por entidade** (uma linha por tabela persistida) | `dashboards`: CT-11 · `dashboard_widgets`: CT-31 |
| **Escopo com discriminante nulo** (fecha ou abre?) | CT-33 |
| **Saída do estado de erro** (4xx/redirect tem destino) | CT-30 |

## Índice de Cenários

| ID | Cenário | Regra | Técnica | Camada | Arquivo | Mata |
|----|---------|-------|---------|--------|---------|------|
| CT-01 | {…} | R1 | BVA | Unit | `tests/Unit/...` | M1 |
| CT-09 | {…} | R4 | matriz papel×ação | Feature | `tests/Feature/...` | M8, M9 |

## Sem CT-B

<!-- só quando o gate do 05 não passar -->
- Motivo: {…}
```

## Tabela de mutantes preenchida (passo 6)

Formato da tabela que cada `Regra:` recebe, com um exemplo preenchido:

```markdown
#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|--------------------------------|------------------|
| M1 | `<` no lugar de `<=` no limite de usos | CT-04 (linha "borda") |
| M2 | contador incrementado antes de validar | CT-06 |
| M3 | contador não incrementado no sucesso | CT-05 |
| M4 | limite lido do cupom mas não comparado | CT-04 |
```

## Teste de arquitetura de sincronia de IDs (pós-implementação)

**Teste de arquitetura sugerido** — barato, um por projeto e não por feature: lê os `[CT-nn]` dos
testes e dos `04`/`05` e falha com o ID que existe num lado só — nas **duas** direções: ID do teste
sem cenário na wiki, e ID do `04`/`05` sem `it('[CT-nn]…')`. O dataset é a lista declarada de
pares (arquivo de teste, pasta da wiki); declará-la à mão é o custo, e é também o que impede um
teste novo de nascer sem wiki.

```php
it('todo [CT-nn] existe nos dois lados: teste e 04/05 da wiki', function (string $teste, string $wiki): void {
    $ids = fn (string $arquivo): array => preg_match_all('/\[(CT-B?\d{2,})\]/', file_get_contents($arquivo), $m) ? array_unique($m[1]) : [];
    $noTeste   = $ids($teste);
    $naWiki    = array_merge([], ...array_map($ids, glob("$wiki/0[45]-*.md")));
    $soNoTeste = array_diff($noTeste, $naWiki);
    $soNaWiki  = array_diff($naWiki, $noTeste);

    expect($soNoTeste)->toBeEmpty('IDs só no teste: '.implode(', ', $soNoTeste))
        ->and($soNaWiki)->toBeEmpty('IDs só na wiki (sem it(\'[CT-nn]…\')): '.implode(', ', $soNaWiki));
})->with('pares teste ↔ wiki');
```

## Tabela de cogitado e cortado (passo 7, item 4)

| Cenário cogitado | Por que foi cortado |
|---|---|
| {…} | já provado por CT-07, mais barato |
| {…} | mata o mesmo mutante que CT-B01 |
| {…} | não mata nenhum mutante previsto |

Sem essa tabela, "só há 2 CT-B" é indistinguível de "só pensamos em 2", e a próxima pessoa
refaz a análise do zero.
