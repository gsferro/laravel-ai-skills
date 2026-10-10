# Casos de Teste — FERRO-812: Cupons de desconto

> Derivado do **00-requisito.md**, não do plano. Nenhuma implementação de Cupom foi lida.
> Fonte: `wikis/specs/oraculo/cupons-de-desconto/00-requisito.md`; paths, rotas e superfície: `01-plano-acao.md` da mesma pasta.
> feature-wiki **4.1.0** · feature-test-design **1.17.0** · entrada pelo step 7.
> Revisão adversarial: **RODADA 1 executada, 7 achados fechados; RODADA 2 PENDENTE por CT-43/44/45 novos; sem autorrevisão**.
> Esta entrega especifica testes; não executa, implementa ou certifica a feature.

## Perfil de Derivação

Perfis decididos pelo **passo 0**, sem perfil imposto pela rodada. Impacto 3 presente em todas as áreas abaixo: dinheiro e autorização tornam a revisão adversarial obrigatória mesmo nas áreas padrão.

| Área | P | I | P×I | Perfil | Motivo |
|---|---|---|---|---|---|
| Cadastro e domínio dos campos | 2 | 3 | 6 | padrão | Integra com formulário existente; valor monetário e dados de organização |
| Cálculo e representação do desconto | 3 | 3 | 9 | completo | Duas unidades, truncamento e piso zero, com consequência monetária |
| Aplicação, validade, contador e trilha | 3 | 3 | 9 | completo | Condições combinadas, relógio, concorrência e efeitos persistidos |
| Autorização, isolamento e listagem | 2 | 3 | 6 | padrão | Permissões e tenancy existentes; vazamento ou escrita por terceiro |
| Interação JavaScript e unidade visível | 3 | 3 | 9 | completo | Estado reativo liga duas unidades de dinheiro; tela incorreta induz cadastro errado |

- Técnicas: EP; BVA 2-valores no cadastro; BVA 3-valores no uso e no dinheiro; decisão completa; matriz estado × operação; matriz papel × ação; rastreio de efeito; partições dos dois tipos.
- O tipo porcentagem usa o literal **1–100**, conforme P-05; não é limite injetado pelo teste.
- Normalização de código não foi presumida. A unicidade provada usa códigos exatamente iguais, em colação sensível a caixa para não mascarar decisões futuras.
- Cenários no 04: **45** · Regras: **14** · CT-B no 05: **2** · Mutantes previstos no 04: **55** · Mutantes sem matador: **0**. Os três mutantes de R14 apontam para o 05; não são mortes medidas.

## Condições e lacunas da entrada

O `00` usa A-01…A-09 com P-01…P-09 e perguntas assumidas, em vez do template atual com coluna Estado. O prompt fixa essas premissas como dadas; suas perguntas históricas não bloqueiam esta execução. Não se reabre P-01 nem se inventa Pedido. Extensões ainda não determinadas ficam nas perguntas abaixo, sem cenário direcional.

**02 ausente:** `Test-Path wikis/specs/oraculo/cupons-de-desconto/02-decisoes-arquiteturais.md` retornou `False`. Não foi criado. A tabela obrigatória de Superfície Livewire não foi fornecida; a cobertura de cada método/propriedade/consumo final não pode ser afirmada. As provas de payload e de IDOR descritas aqui não substituem esse inventário.

Costuras confirmadas por esta sessão executora em 2026-10-09, usando a autorização explícita do prompt e as convenções instaladas. Não foi solicitada confirmação adicional. O despacho independente será feito pela sessão orquestradora, conforme disponibilidade real de concorrência.

## Varredura SFDIPOT

| Letra | O que entra na derivação | Resultado |
|---|---|---|
| S | Dois models/tabelas, enum, páginas CRUD, policy, recorte de permissões e tenancy; nomes são mecanismos do 01 | R1–R3, R6, R9–R13 |
| F | Criar, editar, excluir, listar, encontrar, validar, calcular, consumir e registrar autoria/instante | CT-01…CT-45, CT-B01/02 |
| D | Campos ausentes/nulos/vazios; enum inválido; inteiros; centavos; códigos duplicados; outro tenant; 0/1/N registros | R2–R6, R12–R13; perguntas Q1/Q3 |
| I | Tela do /app, ações Livewire, rotas de leitura e motor chamado diretamente por model; sem tela de aplicação nem endpoint de Pedido | Gates de gravação e por fora da UI; lacuna de inventário do 02 |
| P | Laravel 13.25.0, Filament 5.7.6, Livewire 4.4.0, Pest 5.1.1, browser 5.0.1, mutate 5.0.2; SQLite do arnês e banco concorrente compartilhado | APIs locais conferidas; concorrência exige DB compartilhado real |
| O | Admin da organização, master, admin da instalação, usuário comum, infra, sem papel; papéis acumulados; dois tenants e dois atores distintos | R10–R13, matriz de papéis |
| T | Expiração por instante, segundo exato, stale object, resgates simultâneos, janela de fuso e trilha com timestamp | R5, R8–R9 |

Não há notificações, e-mails, relatório de uso, upload nem checkout nesta entrega: exclusões explícitas do 00. Não se transforma essa ausência de escopo em dispensa de barreiras para `cupons` ou `cupom_usos`.

## Matriz única estado × operação

Estados derivados das duas condições de P-03 e RQ-10/RQ-11, mais removido/inexistente. Não existe enum de ciclo de vida no requisito; não se inventa um. **7 estados × 5 operações = 35 células**, incluindo as células não aplicáveis e as abertas. A criação tem uma célula válida no estado inexistente; não é operação sobre o cupom já cadastrado.

| Estado de partida | Criar | Editar | Excluir | Aplicar | Listar, usuário comum |
|---|---|---|---|---|---|
| Futuro, usos abaixo do limite | n.a. A | ✅ CT-03 | ✅ CT-33 | ✅ CT-13/22/26 | ✅ CT-38/40 |
| Expirado, usos abaixo do limite | n.a. A | ✅ CT-03, novos dados futuros | ✅ CT-33, sem uso anterior | ❌ CT-13/27 | ❌ CT-38/40 |
| Futuro, esgotado | n.a. A | ✅ CT-03, contador preservado | lacuna Q4 | ❌ CT-22/27 | ❌ CT-38/40 |
| Expirado e esgotado | n.a. A | ✅ CT-03, contador preservado | lacuna Q4 | ❌ CT-27 | ❌ CT-38/40 |
| Validade exatamente no instante observado, usos disponíveis | n.a. A | ✅ CT-03, novos dados futuros | ✅ CT-33, sem uso anterior | ❌ CT-13 | ❌ CT-38/40 |
| Removido | n.a. A | ❌ CT-21 | ❌ CT-34 | ❌ CT-20 | ❌ CT-38/40 |
| Inexistente | ✅ CT-02 | ❌ CT-21 | ❌ CT-34 | ❌ CT-19 | ❌ CT-38/40 |

Legenda auditável: A = criar não opera sobre registro existente. ✅ identifica operação executada com seu observável, não visita. ❌ aplicar = nenhum total descontado, contador persistido igual e nenhuma nova linha em `cupom_usos`; ❌ editar = campos e contador preservados, sem ressurreição e sem novo uso; ❌ excluir = controle existente não removido e nenhuma exclusão adicional; ❌ listar = IDs/códigos daquele estado ausentes da lista retornada. Nenhuma célula de escrita usa a listagem como prova. Q4 mantém duas células abertas, em vez de presumir retenção ou destruição da trilha.

A dimensão persona aparece na matriz de autorização; a dimensão campo aparece na edição de tipo, valor, validade e limite **também fora do estado inicial** em CT-03/08/25. O campo gravado é afirmado nas recusas, inclusive quando o contador já tem usos.

## Tabela completa da decisão de aplicação

| Existe no contexto | Dentro da validade | Tem uso disponível | Resultado | Prova |
|---|---|---|---|---|
| não | — | — | recusar, sem efeito | CT-19/20/36 |
| sim | sim | sim | aplicar uma vez e registrar | CT-13/22/26 |
| sim | não | sim | recusar, sem efeito | CT-13/14/27 |
| sim | sim | não | recusar, sem efeito | CT-22/23/27 |
| sim | não | não | recusar, sem efeito | CT-27 |

As quatro células com existência falsa colapsam porque não há validade ou contador de um recurso inexistente. Nas restantes, nenhum AND/OR fica sem exemplo. Os dois inválidos combinados na última linha são condições de uma decisão, não dois erros de validação de payload mascarando-se mutuamente.

## Índice de cenários

| ID | Regra | Grupo | Camada principal | Mutantes previstos | Arquivo futuro |
|---|---|---|---|---|---|
| CT-01 | R1 | Rotas e recuperação | Feature HTTP | M01, M54 | `tests/Tenancy/CuponsTest.php` |
| CT-02 | R1 | Cadastro no componente | componente Livewire/Filament | M02 | `tests/Tenancy/CuponsTest.php` |
| CT-03 | R1 | Cadastro no componente | componente Livewire/Filament | M03 | `tests/Tenancy/CuponsTest.php` |
| CT-43 | R1 | Cadastro no componente | componente Livewire/Filament | M50, M54 | `tests/Tenancy/CuponsTest.php` |
| CT-04 | R2 | Cadastro no componente | componente Livewire/Filament | M05 | `tests/Kit/CuponsTest.php` |
| CT-05 | R2 | Cadastro no componente | componente Livewire/Filament | M04 | `tests/Kit/CuponsTest.php` |
| CT-06 | R2 | Domínio e efeitos | Feature: domínio + banco | M05, M06 | `tests/Kit/CuponsTest.php` |
| CT-07 | R3 | Cadastro no componente | componente Livewire/Filament | M07, M51 | `tests/Kit/CuponsTest.php` |
| CT-08 | R3 | Cadastro no componente | componente Livewire/Filament | M07, M08, M51 | `tests/Kit/CuponsTest.php` |
| CT-09 | R3 | Domínio e efeitos | Feature: domínio + banco | M07, M09, M51 | `tests/Kit/CuponsTest.php` |
| CT-10 | R4 | Domínio e efeitos | Feature: domínio + banco | M10 | `tests/Kit/CuponsTest.php` |
| CT-11 | R4 | Domínio e efeitos | Feature: domínio + banco | M11 | `tests/Kit/CuponsTest.php` |
| CT-12 | R4 | Domínio e efeitos | Feature: domínio + banco | M12, M13 | `tests/Kit/CuponsTest.php` |
| CT-13 | R5 | Domínio e efeitos | Feature: domínio + banco | M14, M15 | `tests/Kit/CuponsTest.php` |
| CT-14 | R5 | Domínio e efeitos | Feature: domínio + banco | M16 | `tests/Kit/CuponsTest.php` |
| CT-15 | R5 | Domínio e efeitos | Feature: domínio + banco | M17 | `tests/Kit/CuponsTest.php` |
| CT-16 | R6 | Cadastro no componente | componente Livewire/Filament | M18 | `tests/Tenancy/CuponsTest.php` |
| CT-17 | R6 | Cadastro no componente | componente Livewire/Filament | M19 | `tests/Tenancy/CuponsTest.php` |
| CT-18 | R6 | Domínio e efeitos | Feature: domínio + banco | M18, M20 | `tests/Tenancy/CuponsTest.php` |
| CT-19 | R7 | Domínio e efeitos | Feature: domínio + banco | M21 | `tests/Kit/CuponsTest.php` |
| CT-20 | R7 | Domínio e efeitos | Feature: domínio + banco | M22 | `tests/Kit/CuponsTest.php` |
| CT-21 | R7 | Domínio e efeitos | Feature: domínio + banco | M23, M24 | `tests/Kit/CuponsTest.php` |
| CT-22 | R8 | Domínio e efeitos | Feature: domínio + banco | M25, M26 | `tests/Kit/CuponsTest.php` |
| CT-23 | R8 | Domínio e efeitos | Feature: domínio + banco | M28 | `tests/Kit/CuponsTest.php` |
| CT-24 | R8 | Domínio e efeitos | Feature: domínio + banco | M27 | `tests/Kit/CuponsTest.php` |
| CT-25 | R8 | Domínio e efeitos | Feature: domínio + banco; também escrita direta | M29 | `tests/Kit/CuponsTest.php` |
| CT-26 | R9 | Domínio e efeitos | Feature: domínio + banco | M26, M30, M31 | `tests/Kit/CuponsTest.php` |
| CT-27 | R9 | Domínio e efeitos | Feature: domínio + banco | M32 | `tests/Kit/CuponsTest.php` |
| CT-28 | R9 | Domínio e efeitos | Feature: domínio + banco | M33 | `tests/Kit/CuponsTest.php` |
| CT-29 | R9 | Domínio e efeitos | Feature: domínio + banco | M34 | `tests/Kit/CuponsTest.php` |
| CT-41 | R9 | Domínio e efeitos | Feature: domínio + banco | M31 | `tests/Kit/CuponsTest.php` |
| CT-30 | R10 | Ações e listagem no componente | componente Livewire/Filament | M53 | `tests/Tenancy/CuponsTest.php` |
| CT-31 | R10 | Ações e listagem no componente | componente Livewire/Filament | M36 | `tests/Tenancy/CuponsTest.php` |
| CT-32 | R10 | Domínio e efeitos | Feature: domínio + banco | M37 | `tests/Tenancy/CuponsTest.php` |
| CT-44 | R10 | Rotas e recuperação | Feature HTTP | M52 | `tests/Tenancy/CuponsTest.php` |
| CT-33 | R11 | Ações e listagem no componente | componente Livewire/Filament | M38, M40 | `tests/Tenancy/CuponsTest.php` |
| CT-34 | R11 | Domínio e efeitos | Feature: domínio + banco | M39 | `tests/Tenancy/CuponsTest.php` |
| CT-35 | R12 | Rotas e recuperação | Feature HTTP; também componente | M41 | `tests/Tenancy/CuponsTest.php` |
| CT-36 | R12 | Domínio e efeitos | Feature: domínio + banco | M41 | `tests/Tenancy/CuponsTest.php` |
| CT-37 | R12 | Ações e listagem no componente | componente Livewire/Filament; também escrita direta | M42 | `tests/Tenancy/CuponsTest.php` |
| CT-42 | R12 | Domínio e efeitos | Feature: domínio + banco | M43 | `tests/Tenancy/CuponsTest.php` |
| CT-38 | R13 | Ações e listagem no componente | componente Livewire/Filament | M35, M44 | `tests/Tenancy/CuponsTest.php` |
| CT-39 | R13 | Ações e listagem no componente | componente Livewire/Filament | M45, M46 | `tests/Tenancy/CuponsTest.php` |
| CT-40 | R13 | Domínio e efeitos | Feature: domínio + banco | M35, M44, M45 | `tests/Tenancy/CuponsTest.php` |
| CT-45 | R13 | Ações e listagem no componente | componente Livewire/Filament; também fonte direta Feature | M55 | `tests/Tenancy/CuponsTest.php` |
| CT-B01 | R14 | Unidade e reação no navegador | browser | M47 | `tests/BrowserTenancy/CupomTest.php` |
| CT-B02 | R14 | Unidade e reação no navegador | browser | M48, M49 | `tests/BrowserTenancy/CupomTest.php` |

Arquivos são destinos para materialização, não testes existentes. O índice indica a costura principal; CT-25/35/37/45 exigem também as entradas explicitadas no Gherkin. Cada linha de dataset é execução independente. O corpo do cenário contém os dados e o observável discriminante.

## Mapa de Regras

| Regra | Área e perfil herdado | Origem | Técnica | Cenários |
|---|---|---|---|---|
| R1 — CRUD grava os cinco dados | cadastro, padrão | RQ-01…RQ-06, RQ-14, P-04/09 | EP e par visita/gravação | CT-01…03, CT-43 |
| R2 — campos e tipos indispensáveis | cadastro, padrão | RQ-02…RQ-06, P-05 | EP em criação, edição e fora da UI | CT-04…06 |
| R3 — unidade e domínio dependem do tipo | cadastro, padrão | RQ-03/04, P-05 | EP + BVA 2-valores condicionado | CT-07…09 |
| R4 — cálculo exato, truncado e sem negativo | cálculo, completo | RQ-12, P-01/05/06/07 | BVA 3-valores e EP | CT-10…12 |
| R5 — validade é instante, reconferido no uso | aplicação, completo | RQ-05/10, pressuposto final do 00 | BVA 3-valores e tempo | CT-13…15 |
| R6 — unicidade por organização | cadastro/isola­mento, padrão | RQ-14, P-04 | identidade exata e criação ≠ edição | CT-16…18; código novo CT-43 |
| R7 — cupom inexistente/removido não funciona | aplicação, completo | RQ-09, P-01 | EP e estado × operação | CT-19…21 |
| R8 — contador representa usos e respeita limite | aplicação, completo | RQ-06/11/13 | BVA 3-valores, concorrência, não-efeito | CT-22…25 |
| R9 — cada aplicação registra quem e quando | aplicação, completo | RQ-15, P-01/08, RQ-13 | rastreio de efeito, duas partições, atomicidade | CT-26…29, CT-41 |
| R10 — somente admins escrevem e usuário comum não abre edit | autorização, padrão | RQ-07/08, P-02/03/09 | matriz papel × ação/entrada, ação efetiva | CT-30…32, CT-44; positivos CT-02/03/33 |
| R11 — admin exclui e a remoção não age em outro registro | autorização, padrão | RQ-01/07, RQ-09 | estado × operação, ID inexistente | CT-33/34 |
| R12 — dado/efeito permanece na organização | isolamento, padrão | P-02/04/08, RQ-07/09/13/15 | IDOR e mass assignment por entrada | CT-35…37, CT-42 |
| R13 — usuário comum lista só os ativos | autorização/listagem, padrão | RQ-08/15, P-03/08 | decisão, cardinalidade, escopo e participante histórico | CT-38…40, CT-45 |
| R14 — UI opera a unidade correta com JS | JS, completo | RQ-01/03/04, P-05/09 | EP do tipo, erro reativo | CT-B01/02 no 05 |

As regras padrão não usam pairwise. As regras completas de cálculo têm dois parâmetros; a aplicação usa a decisão exaustiva acima em vez de reduzir condições por pairwise. Nenhuma garantia de configuração com três parâmetros independentes foi criada. A edição de R3 é escalada para a mudança entre partições porque repetir somente valores no mesmo tipo deixaria a fronteira condicionada sem prova.

## Costuras de Teste

| Grupo | Regras | Costura | Existente ou nova | Por quê | Confirmada |
|---|---|---|---|---|---|
| Domínio e efeitos | R2–R9, R10–R13 | Pest feature HTTP | existente, `tests/Kit` e `tests/Tenancy` | Banco, actor e scopes; model chamado diretamente; inclui todos os gates por fora da UI | sessão executora, autorização do prompt, 2026-10-09 |
| Rotas e recuperação | R1, R7, R10–R12 | Pest feature HTTP | existente, smoke e tenancy | HTTP prova binding, conteúdo específico e destino depois de 403/404 | sessão executora, 2026-10-09 |
| Cadastro no componente | R1–R3, R6, R8 | componente Livewire/Filament | existente, `PaginasInfraTest` e `AdminDaOrganizacaoTest` | Validação e banco, sem navegador | sessão executora, 2026-10-09 |
| Ações e listagem no componente | R10–R13 | componente Livewire/Filament | existente, tests de tenancy | Ação efetiva, registros visíveis e payload; sem Node | sessão executora, 2026-10-09 |
| Unidade e reação no navegador | R14 | browser | existente, `tests/BrowserTenancy` | JS deve atualizar a unidade no DOM sem recarregar e apresentar o erro após transição de tipo | sessão executora, 2026-10-09 |

`Unit` não foi usado: `tests/Pest.php` não conecta `tests/Unit` ao TestCase da aplicação e não há contrato de calculadora pura exposto pelo requisito. A superfície acordada P-01 é o motor do model; o teste mais barato **existente** para a observação é o Feature com aplicação. Não foi criada infraestrutura para conseguir uma etiqueta Unit.

## Fronteira com o Plano

| Item do 01 | Tratamento |
|---|---|
| Cupom, CupomUso, TipoDeDesconto, métodos, nomes das colunas e páginas, paths e UUID | Nomes/mecanismos, nunca critério de resultado sem RQ/P correspondente |
| Maiúsculas/trim e teto de 40 caracteres | Não vêm do 00: Q1; nenhum teste espera essa normalização ou esse teto |
| Cadastro/edição só com validade futura; limite mínimo 1; redução de limite abaixo dos usos | Q2/Q3. O uso vencido/esgotado continua recusado; contador e trilha não são corrigidos pela edição |
| Strings de situação, precedência Esgotado/Expirado, ordem descendente, cores e mensagens | Não usados como oráculo. RQ-08/P-03 afirmam pertencimento à lista, não a string ou o pixel |
| Rótulo/sufixo exato do valor | Não imposto. O 05 afirma unidade visível coerente com P-05; frases concretas só auxiliam locators |
| Gate do 05 por toda linha usar Livewire e atravessar telas | Recusado: só o observável de JS da costura confirmada justifica browser |
| RQ-15 como logs e campos monetários adicionais de cupom_usos | O oráculo é autor e instante em registro persistido; logs e valores extras de auditoria não são novos requisitos |
| Cascade de cupom_usos ao excluir cupom | Q4: o 00 pede auditoria posterior e permite exclusão, sem determinar retenção |
| Admin da instalação sem acesso a /app | Diverge de P-02, que diz que `admin` e `master_global` alcançam a tela. CT-02/30 usam P-02; o 01 imutável não substitui o oráculo |
| aplicarEm com User opcional | Diverge da assinatura de P-01 e de registrar quem em RQ-15. CT-41 exige recusa sem autor, sem consumo |

## Perguntas para o 00-requisito.md

Desvio autorizado: `00` imutável; perguntas devolvidas aqui, prontas para colagem, sem alterar a fonte. O 00 não usa Qn; esta derivação inicia Q1. As perguntas referem os **ramos adicionais não determinados**, não anulam os fatos e premissas fixos da rodada. Não existe cenário afirmando a resposta direcional desses ramos.

| ID | Pergunta | Afeta | Recomendação | Estado |
|---|---|---|---|---|
| Q1 | Código ignora caixa/espaços, aceita Unicode e tem qual teto de caracteres? | extensão de RQ-02/RQ-14 | Fechar domínio e teto explícitos antes de aceitar entradas de origem arbitrária; não inferir 40 do plano | aberta; ramos de normalização/teto sem cenário |
| Q2 | Pode criar ou editar para validade já passada ou exatamente agora? | extensão de RQ-05 na gravação | Recusar a gravação desses instantes, pois RQ-10 já recusa o uso; o invariante de aplicação está em CT-13/14 | aberta; direção de cadastro passado sem cenário |
| Q3 | Limite zero é permitido? Pode reduzir limite abaixo dos usos feitos? Fixo zero/valor total negativo são entradas de negócio admitidas? | extensões de RQ-04/RQ-06/RQ-12 | Recusar valores que criam estado inválido; preservar contador e trilha independentemente da resposta | aberta; limites adicionais sem cenário direcional |
| Q4 | Após excluir cupom já usado ou excluir o autor, como manter quem/quando para auditoria posterior? | interação RQ-07/RQ-15 | Preservar a evidência de aplicação; bloquear destruição enquanto retenção não for definida | aberta; duas células de exclusão com trilha sem cenário direcional |
| Q5 | O futuro chamador deve aplicar uma única vez por Pedido, usando qual identidade persistida? | P-01 e extensão de RQ-12/RQ-13 | Falhar fechado em retry identificado; definir o agregado antes de prometer idempotência | aberta; idempotência de Pedido não testável nesta entrega |

Formato para encaminhamento:

❓ Q1 · raia: requisito · afeta: extensão de RQ-02/RQ-14 · depende de: —
A unicidade usa código literal ou normalizado, e qual o domínio/teto do código?
➡️ Recomendação: definir domínio e teto explícitos; recusar entradas não validadas fora do domínio acordado.

❓ Q2 · raia: requisito · afeta: extensão de RQ-05 na gravação · depende de: —
O cadastro/edição aceita validade passada ou igual ao instante atual?
➡️ Recomendação: recusar; o cupom já seria inaplicável por RQ-10.

❓ Q3 · raia: requisito · afeta: extensões de RQ-04/RQ-06/RQ-12 · depende de: —
Quais são os domínios ainda não definidos para limite zero, redução abaixo dos usos, fixo zero e total negativo?
➡️ Recomendação: recusar estado inválido; a edição nunca diminui contador nem apaga a trilha.

❓ Q4 · raia: requisito · afeta: interação RQ-07/RQ-15 · depende de: —
Que evidência permanece depois de excluir cupom usado ou autor?
➡️ Recomendação: preservar quem/quando e falhar fechado contra destruição até definir retenção.

❓ Q5 · raia: requisito · afeta: P-01, extensão de RQ-12/RQ-13 · depende de: —
Qual agregado persistido e chave definem repetição da mesma aplicação?
➡️ Recomendação: confirmar escopo do chamador e impedir retry duplicado ali; não usar retorno puro ou contador como prova de idempotência.

## Setup Global

- **Arnês confirmado:** `tests/Kit` usa TestCase + RefreshDatabase; `tests/Tenancy` e `tests/BrowserTenancy` usam TenancyTestCase + RefreshDatabase, com teams configurado **antes** das migrations. Não ligar tenancy num beforeEach do TestCase single-tenant.
- **Versões efetivas:** extraídas de composer.lock. Mutate consta no lock/vendor, mas não foi encontrado como dependência direta em composer.json; isso é risco de instalação, não ausência do plugin. Nenhum Composer, Artisan, Pest, build ou mutation run foi executado nesta cópia.
- **Setup das permissões na futura materialização:** padrão `$this->seed([ShieldPermissionsSeeder::class, PapeisSeeder::class])`, na ordem, depois do Resource existir. Não contar permissões de nome inventado como prova de autoridade.
- **Personas e fixtures existentes:** `tenant()`, `usuario()`, `usuarioDoKit()`, `usuarioComPapel()`, `papelNaOrganizacao()`, `noPainelDa()`, `fronteiraDeRequest()` em tests/Pest.php. Acme e Globex, Ana admin da Acme, Beto usuário comum da Acme, Bruno admin da Globex; autores da aplicação diferentes de quem cadastrou. Associar usuários a tenants e gravar papéis no team correto; limpar relações/cache de permissões ao trocar contexto.
- Não há CupomFactory instalada na listagem de `database/factories`. Fixtures futuras criam Cupom pelos dados públicos válidos; o factory previsto no 01 não é tomado por existente. Estados ativos começam com zero; esgotado nasce por aplicações reais, expirado por relógio; removido por exclusão real. A fixture acima do limite é **dado legado deliberadamente inconsistente**, inserido pela camada de DB do teste, não simulador da lógica de produção. Não forçar uma coluna `situacao` inexistente.
- **Dados válidos base:** código `PROMO-A`, tipo porcentagem, valor 10, expiração `2026-10-10T18:00:00Z`, limite 3; total 10.000 centavos. Fixo base 1.000 centavos. Todos os dados não apontados como inválidos em cada cenário permanecem válidos.
- **Fakes:** nenhum Event::fake global, para preservar UUID/scopes. Nenhum fake de log, e-mail, job ou HTTP, pois não há requisito de tais efeitos. A falha de CT-29 é listener de teste restrito a CupomUso, registrado depois das fixtures e removido em finally.
- **APIs conferidas:** fillForm, assertHasFormErrors e call create/save; assertSchemaStateSet; callAction(TestAction::make('delete')->table($record)); assertActionHidden; loadTable; assertCanSeeTableRecords/assertCanNotSeeTableRecords. Usar nomes reais de classes ao materializar; os helpers antigos callTableAction/assertFormSet estão deprecated no vendor.
- **Fora da UI:** chamada de escrita do model ou motor com autenticação/contexto real; não basta chamar `Gate::allows`. Se não existe escrita pública que aplique a regra, manter o CT vermelho como divergência ou lacuna de desenho; não criar rota, service ou autorização fictícios nesta especificação.
- **Concorrência CT-24:** duas conexões/processos contra o **mesmo DB persistido**, com fixture committed e barreira antes do consumo. SQLite `:memory:` por processo e duas chamadas sequenciais não servem. Testar arquivo SQLite compartilhado com WAL e busy timeout em fixture temporária; lock/busy não é recusa de negócio. Se a pilha não expuser o interleaving, executar o mesmo CT no engine de produção/CI e declarar pendência até isso acontecer. Não certificar atomicidade por objetos stale de CT-23.
- Relógio fixo por travelTo/freezeTime; restaurar no finally. Usar instantes com offset explícito e comparar epochs; variar app São Paulo × DB UTC × preferência do usuário somente no CT temporal. O fuso default lido de config/app.php é UTC.
- **Erro HTTP e saída:** depois de recusa 403/404, cenário irmão CT-01/38 prova que a lista própria continua alcançável, contém o controle esperado e não redireciona de volta ao erro. As recusas do motor são erros de domínio, sem inventar status HTTP ou mensagem.
- `.ai/rules/testes-browser.md` vence a possibilidade genérica de paralelismo: browser sempre em série neste projeto; TIA não é exigido na entrega documental. build/manifest existe em disco, mas build atual não foi rodado. Capturas não versionadas; gitignore já lista tests/Browser/Screenshots.

---
## Regra R1 — O CRUD do painel grava os cinco dados do cupom

> Origem: RQ-01…RQ-06, RQ-14, P-04/09 · padrão · EP · cadastro e rotas. Quatro cenários: o gate de edição de código novo e validade preservada acrescenta CT-43, sem substituir a edição que altera os demais campos.

```gherkin
# language: pt
Funcionalidade: Cadastro de cupons no painel de negócio
  Regra: O administrador consegue acessar e gravar os dados do cupom
    Esquema do Cenário: [CT-01] A tela de escrita mostra os cinco dados específicos e tem saída alcançável
      Dado Ana administradora da Acme e PROMO-A ativo, porcentagem 10, validade 2026-10-10T18:00:00Z e limite 3
      Quando Ana visita a rota <tela> da Acme, inclusive depois de uma recusa na rota de Globex
      Então aparecem os campos código, tipo, valor, validade e limite com <dados>
      E a listagem própria é alcançável com PROMO-A e sem redirecionamento de volta ao erro
      Exemplos:
        | tela                               | dados                                                           | classe  |
        | /app/acme/cupons/create             | cinco entradas editáveis                                        | criação |
        | /app/acme/cupons/{uuid_PROMO-A}/edit | PROMO-A, porcentagem, 10, instante 2026-10-10T18:00:00Z e limite 3 | edição  |

    Esquema do Cenário: [CT-02] O administrador cria um cupom pelo componente
      Dado <admin> da Acme autorizado por P-02 e nenhuma linha com código NOVO
      Quando o administrador grava no componente código NOVO, tipo <tipo>, valor <valor>, validade 2026-10-10T18:00:00Z e limite 3
      Então existe exatamente um cupom NOVO da Acme com todos esses valores e contador 0
      E o componente não tem erros de formulário e nenhum uso de cupom foi criado
      Exemplos:
        | admin              | tipo        | valor | classe                     |
        | admin_organizacao  | porcentagem | 29    | percentual                 |
        | admin_organizacao  | fixo        | 1500  | fixo acima de 100 centavos  |
        | master_global      | porcentagem | 29    | exceção global de P-02      |
        | admin              | fixo        | 1500  | admin da instalação, P-02   |

    Esquema do Cenário: [CT-03] A edição altera dados sem recomeçar a contabilidade
      Dado <admin> autorizado na Acme e PROMO-A no estado <estado>, com <usos> usos e igual número de registros de aplicação
      Quando esse administrador grava pelo componente tipo <tipo>, valor <valor>, validade futura 2026-10-12T18:00:00Z e limite 5 mantendo o código PROMO-A
      Então a mesma chave possui os novos valores, o código PROMO-A e exatamente <usos> usos
      E os registros de aplicação anteriores mantêm autor e instante, sem novo registro
      Exemplos:
        | admin             | estado                      | usos | tipo        | valor | classe               |
        | admin_organizacao | futuro com saldo            | 0    | fixo        | 1500  | inicial              |
        | admin_organizacao | expirado com saldo           | 1    | porcentagem | 29    | fora do inicial      |
        | admin_organizacao | futuro esgotado              | 3    | fixo        | 1500  | esgotado             |
        | admin_organizacao | expirado e esgotado          | 3    | porcentagem | 29    | ambas condições      |
        | admin_organizacao | expiração igual ao instante | 0    | fixo        | 1500  | fronteira temporal   |
        | master_global     | futuro com saldo            | 1    | porcentagem | 29    | exceção global P-02   |
        | admin             | futuro com saldo            | 1    | fixo        | 1500  | instalação P-02      |
    Cenário: [CT-43] Editar somente o código disponível preserva a validade hidratada e a contabilidade
      Dado Ana administradora da Acme com edit carregado de PROMO-A ativo, porcentagem 10, validade 2026-10-10T18:00:00Z, limite 3, contador 1 e uma aplicação de Beto em 2026-10-09T11:00:00Z
      E NOVO está livre na Acme, embora exista um NOVO na Globex com outra chave
      Quando Ana altera somente o campo código para NOVO e salva pelo componente, sem preencher os outros quatro campos
      Então a mesma chave da Acme possui código NOVO, porcentagem 10, validade no mesmo instante 2026-10-10T18:00:00Z, limite 3 e contador 1
      E a aplicação anterior conserva chave, autor Beto e instante; nenhuma aplicação nova nasce e o NOVO da Globex permanece idêntico

```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M01 | Resource só registra índice, ou edit carrega outro registro | CT-01 | Create tem cinco entradas; edit contém PROMO-A, 10 e 3, não só HTTP 200 |
| M02 | Campo tipo/valor/limite não é desidratado na criação | CT-02 | Linha NOVO é fixo, 1500, limite 3 e contador 0, exatamente uma vez |
| M03 | Save reimplementa criação e reinicia usos ou deixa campos antigos | CT-03 | Mesma chave muda valor para 1500/29, usos 3 permanece 3 e a trilha anterior permanece |
| M50 | Valida o novo código livre mas o exclui dos dados gravados em edit | CT-43 | Mesma chave passa de PROMO-A para NOVO; a linha da Globex não muda |
| M54 | Edit hidrata validade com data futura padrão e a grava ao mudar outro campo | CT-01/43 | Edit carrega 2026-10-10T18:00:00Z; mudar só código conserva exatamente esse instante |

## Regra R2 — Campos indispensáveis e seus tipos são verificados também fora da tela

> Origem: RQ-02…RQ-06, P-05 · padrão · EP. Cada linha inválida é execução independente; nunca juntar dois erros de payload.

```gherkin
# language: pt
Funcionalidade: Integridade do cadastro
  Regra: Um cupom tem código, um dos dois tipos, valor inteiro, data válida e contagem inteira
    Esquema do Cenário: [CT-04] A criação recusa um único campo indispensável inválido
      Dado Ana administradora da Acme e um formulário com os cinco dados válidos de base
      Quando Ana tenta criar trocando somente <campo> por <entrada>
      Então o componente informa erro no campo <campo> e nenhum novo cupom é persistido
      E nenhum registro em cupom_usos é criado
      Exemplos:
        | campo          | entrada             | classe                         |
        | codigo         | ausente             | ausente                        |
        | codigo         | null                | nulo                           |
        | codigo         | string vazia        | vazio                          |
        | tipo           | ausente             | ausente                        |
        | tipo           | null                | nulo                           |
        | tipo           | string vazia        | vazio                          |
        | tipo           | outro               | fora dos dois tipos            |
        | tipo           | array [porcentagem] | tipo de dado errado            |
        | valor          | ausente             | ausente                        |
        | valor          | null                | nulo                           |
        | valor          | string vazia        | vazio                          |
        | valor          | texto abc           | tipo errado                    |
        | expira_em      | ausente             | ausente                        |
        | expira_em      | null                | nulo                           |
        | expira_em      | string vazia        | vazio                          |
        | expira_em      | não-é-data          | domínio temporal inválido      |
        | expira_em      | array [2026-10-10]  | tipo errado                    |
        | limite_de_usos | ausente             | ausente                        |
        | limite_de_usos | null                | nulo                           |
        | limite_de_usos | string vazia        | vazio                          |
        | limite_de_usos | texto abc           | tipo errado                    |
        | limite_de_usos | string 3.5          | contagem fracionária            |

    Esquema do Cenário: [CT-05] A edição não contorna a validação indispensável
      Dado Ana administradora e PROMO-A ativo com cinco dados válidos, 1 uso e sua trilha existente
      Quando Ana salva alterando somente <campo> para <entrada>
      Então o componente informa erro em <campo> e os cinco campos persistidos continuam nos valores anteriores
      E contador continua 1 e a trilha existente continua idêntica, sem novo uso
      Exemplos:
        | campo          | entrada             | classe                  |
        | codigo         | null                | código nulo             |
        | codigo         | string vazia        | código vazio            |
        | tipo           | outro               | tipo fora do domínio    |
        | tipo           | array [fixo]        | tipo errado             |
        | valor          | null                | valor nulo              |
        | valor          | texto abc           | valor errado            |
        | expira_em      | null                | validade nula           |
        | expira_em      | não-é-data          | data inválida           |
        | expira_em      | array [2026-10-10]  | tipo temporal errado    |
        | limite_de_usos | null                | limite nulo             |
        | limite_de_usos | texto abc           | limite errado           |
        | limite_de_usos | string 3.5          | limite fracionário      |

    Esquema do Cenário: [CT-06] A escrita direta não depende da validação do formulário
      Dado Ana autenticada no contexto Acme e PROMO-A ativo com 1 uso e sua trilha existente
      Quando Ana executa a escrita de domínio <via> com somente <campo> inválido como <entrada>, por fora da UI
      Então a escrita é recusada antes de persistir um cupom inválido; em edição todos os valores antigos permanecem
      E contador e cupom_usos permanecem idênticos ao Dado
      Exemplos:
        | via    | campo          | entrada              | classe                    |
        | criar  | codigo         | null                 | código indispensável      |
        | editar | codigo         | string vazia         | edição indispensável      |
        | criar  | tipo           | outro                | enum inválido             |
        | editar | tipo           | outro                | enum inválido na edição   |
        | criar  | valor          | string vazia         | valor indispensável       |
        | editar | valor          | texto abc            | valor inteiro             |
        | criar  | expira_em      | não-é-data           | data válida               |
        | editar | expira_em      | array [2026-10-10]   | tipo temporal             |
        | criar  | limite_de_usos | null                 | limite indispensável      |
        | editar | limite_de_usos | string 3.5           | limite inteiro            |
```

Os Exemplo de edição com `ausente` são substituídos pelos nulos/vazios efetivamente enviados: a semântica de PATCH parcial não é inventada. O tratamento de `codigo = só espaços` fica em Q1. Rejeitar não impõe texto específico de mensagem nem classe de exceção do 01.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M04 | Campo obrigatório verificado somente em create | CT-05 | Data/valor/tipo inválido na edição produz erro e o valor antigo continua persistido |
| M05 | Cast/validação aceita terceiro tipo ou perde fração de contagem silenciosamente | CT-04/06 | outro não vira Cupom; 3.5 não se persiste como limite 3 |
| M06 | Regras existem somente no schema de UI | CT-06 | Escrita direta não grava código vazio, valor inválido ou data inválida |

## Regra R3 — O domínio do valor acompanha a unidade do tipo

> Origem: RQ-03/04, P-05 · padrão · EP + BVA 2-valores: 0/1 e 100/101 pontos percentuais. Fixo é centavos inteiros, sem teto percentual de 100.

```gherkin
# language: pt
Funcionalidade: Domínio do desconto
  Regra: Porcentagem admite somente inteiros de 1 a 100; fixo não usa esse teto
    Esquema do Cenário: [CT-07] A criação usa o domínio do tipo escolhido
      Dado Ana administradora da Acme e todos os demais campos válidos
      Quando Ana grava pelo componente tipo <tipo> e valor <valor>
      Então o resultado é <resultado> e, se aceito, o tipo e o inteiro <valor> são persistidos exatamente
      E se recusado nenhum cupom nem registro em cupom_usos é criado
      Exemplos:
        | tipo        | valor        | resultado | classe                |
        | porcentagem | 0            | recusado  | abaixo do mínimo      |
        | porcentagem | 1            | aceito    | mínimo literal        |
        | porcentagem | 100          | aceito    | máximo literal        |
        | porcentagem | 101          | recusado  | acima do máximo       |
        | porcentagem | string 12.5  | recusado  | fração proibida       |
        | fixo        | 100          | aceito    | centavos              |
        | fixo        | 101          | aceito    | não é 101 por cento   |
        | fixo        | 102          | aceito    | além do teto indevido |
        | fixo        | string 12.5  | recusado  | fração de centavo proibida |

    Esquema do Cenário: [CT-08] A edição revalida valor quando o tipo muda
      Dado Ana administradora e o cupom ativo de tipo <anterior>, valor <valor_antigo>, contador 1 e uma trilha
      Quando Ana salva pelo componente o tipo <novo> e valor <valor>
      Então o resultado é <resultado>; aceite persiste o novo par e recusa preserva exatamente o par anterior
      E contador continua 1 e a trilha continua a anterior, sem novo uso
      Exemplos:
        | anterior    | valor_antigo | novo        | valor       | resultado | classe                         |
        | fixo        | 150          | porcentagem | 0           | recusado  | mínimo condicionado            |
        | fixo        | 150          | porcentagem | 1           | aceito    | novo mínimo                    |
        | fixo        | 150          | porcentagem | 100         | aceito    | novo máximo                    |
        | fixo        | 150          | porcentagem | 101         | recusado  | mudança que exige novo teto    |
        | fixo        | 150          | porcentagem | string 12.5 | recusado  | fração                         |
        | porcentagem | 10           | fixo        | 150         | aceito    | teto percentual deixa de valer |
        | fixo        | 150          | fixo        | string 12.5 | recusado  | fração no fixo sem troca de tipo |
        | porcentagem | 10           | fixo        | string 12.5 | recusado  | fração ao mudar para centavos |

    Esquema do Cenário: [CT-09] A mesma fronteira existe na escrita por fora da UI
      Dado Ana autenticada na Acme, dados válidos de base e um cupom ativo existente para edição
      Quando Ana grava diretamente por <via> o tipo <tipo> e o valor <valor>
      Então o resultado é <resultado>; em aceite o par exato é persistido e em recusa não há novo cupom ou alteração do par antigo
      E o contador e a trilha de uso não mudam
      Exemplos:
        | via    | tipo        | valor       | resultado | classe                   |
        | criar  | porcentagem | 0           | recusado  | mínimo na criação        |
        | editar | porcentagem | 0           | recusado  | mínimo na edição         |
        | criar  | porcentagem | 1           | aceito    | mínimo                   |
        | editar | porcentagem | 100         | aceito    | máximo                   |
        | criar  | porcentagem | 101         | recusado  | teto na criação          |
        | editar | porcentagem | 101         | recusado  | teto na edição           |
        | criar  | porcentagem | string 12.5 | recusado  | fração                   |
        | editar | porcentagem | string 12.5 | recusado  | fração na edição         |
        | criar  | fixo        | 150         | aceito    | centavos sem teto 100    |
        | editar | fixo        | 150         | aceito    | centavos na edição       |
        | criar  | fixo        | string 12.5 | recusado  | fração de centavo na criação direta |
        | editar | fixo        | string 12.5 | recusado  | fração de centavo na edição direta |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M07 | max 100 aplicado ao campo valor dos dois tipos | CT-07/08/09 | Fixo 150 ou 101 é aceito como esse número de centavos |
| M08 | min/max calculado apenas do tipo original na edição | CT-08 | Fixo 150 → porcentagem 101 é recusado; porcentagem 10 → fixo 150 é aceito |
| M09 | numeric substitui a validação inteira ou a regra existe só na UI | CT-09 | 12.5 nos dois tipos e 101 percentual são recusados pela escrita direta |
| M51 | Somente o fixo aceita numeric e trunca 12.5 centavos para 12 | CT-07/08/09 | Criar ou editar fixo com string 12.5 é recusado, inclusive diretamente, sem cupom novo nem alteração do par anterior |

## Regra R4 — O total com desconto é inteiro, truncado e nunca negativo

> Origem: RQ-12, P-01/05/06/07 · completo · cálculo via motor existente; todos partem de cupom ativo. Os testes de valor não se tornam provas únicas do contador/trilha.

```gherkin
# language: pt
Funcionalidade: Valor com desconto
  Regra: A unidade depende do tipo e a fração percentual é truncada
    Esquema do Cenário: [CT-10] O percentual opera em pontos inteiros e mantém o centavo exato
      Dado cupom ativo de porcentagem <valor> com usos disponíveis
      Quando Beto aplica ao total inteiro <total> centavos pelo motor
      Então o retorno é exatamente o inteiro <final> centavos
      Exemplos:
        | valor | total | final | classe                         |
        | 1     | 9999  | 9900  | mínimo e fração                |
        | 29    | 10000 | 7100  | cálculo inteiro usual          |
        | 29    | 100   | 71    | distingue razão float primeiro |
        | 100   | 9999  | 0     | percentual máximo literal      |

    Esquema do Cenário: [CT-11] A borda de meio centavo não arredonda o desconto para cima
      Dado cupom ativo de porcentagem 5 com usos disponíveis
      Quando Beto aplica ao total <total> centavos pelo motor
      Então o desconto efetivo é 2 centavos e o retorno é exatamente <final> centavos
      Exemplos:
        | total | final | classe                         |
        | 49    | 47    | antes de meio centavo          |
        | 50    | 48    | meio centavo, não dá desconto 3|
        | 51    | 49    | depois de meio centavo         |

    Esquema do Cenário: [CT-12] O valor fixo é centavos e o piso do total é zero
      Dado cupom fixo ativo de 1000 centavos com usos disponíveis
      Quando Beto aplica ao total <total> centavos pelo motor
      Então o retorno é exatamente o inteiro <final> centavos
      Exemplos:
        | total | final | classe             |
        | 999   | 0     | desconto maior     |
        | 1000  | 0     | igualdade          |
        | 1001  | 1     | sobra um centavo   |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M10 | Calcula desconto como (int)(total * (percentual / 100)), com a razão em ponto flutuante | CT-10 | 29% de 100 retorna exatamente 71; o mutante em binary64 trunca 28.999999999999996 para 28 e retorna 72 |
| M11 | Arredonda a fração em vez de truncar | CT-11 | 5% de 50 desconta 2; retorno 48, não 47 |
| M12 | Valor fixo tratado como reais ou como percentual | CT-12 | 1000 sobre 1001 deixa 1 centavo, não zero ou outro total |
| M13 | Subtrai sem limitar em zero ou aplica o piso ao desconto | CT-12 | Total 999 retorna 0, e 1001 retorna 1 |

**Prova documental de M10, sem executar a aplicação:** a ordem da expressão foi corrigida após ADV-06. `(10000 * 29) / 100` não perde centavo nesse exemplo; nenhuma morte é atribuída à expressão antiga. Para o mutante agora descrito, o controle racional inteiro dá desconto `intdiv(100 * 29, 100) = 29` e retorno 71. Uma expressão autocontida em Python/Decimal e binary64 confirmou `100 * (29 / 100) = 28.999999999999996`, desconto truncado 28 e retorno 72. Os dados válidos do cenário continuam inteiros. Essa prova da expressão não executou PHP/Pest e não certifica morte no motor futuro; a materialização deverá preservar a ordem exata do mutante ao verificar a discriminação.

## Regra R5 — Validade termina no instante gravado e é conferida no consumo

> Origem: RQ-05/10 e pergunta histórica final assumida do 00 (`expira_em > now()`) · completo · BVA 3-valores, incremento de **1 segundo**. Data passada na gravação continua Q2.

```gherkin
# language: pt
Funcionalidade: Validade na aplicação
  Regra: O motor usa instantes e reconfere validade no momento do efeito
    Esquema do Cenário: [CT-13] O segundo da expiração já não permite aplicar
      Dado cupom <tipo> com expiração 2026-10-09T18:00:00Z, 1 uso de limite 3, autor Beto e uma trilha anterior
      Quando Beto tenta aplicar 10000 centavos no instante <agora>
      Então o resultado é <resultado> com <final> centavos se aceito, contador <usos> e exatamente <trilhas> registros de aplicação
      E na recusa nenhum total descontado é devolvido e a trilha anterior conserva autor e instante
      Exemplos:
        | tipo        | agora                | resultado | final | usos | trilhas | classe     |
        | porcentagem | 2026-10-09T17:59:59Z | aceito    | 9000  | 2    | 2       | borda−1 s  |
        | porcentagem | 2026-10-09T18:00:00Z | recusado  | —     | 1    | 1       | borda      |
        | porcentagem | 2026-10-09T18:00:01Z | recusado  | —     | 1    | 1       | borda+1 s  |
        | fixo        | 2026-10-09T17:59:59Z | aceito    | 9000  | 2    | 2       | fixo antes |
        | fixo        | 2026-10-09T18:00:00Z | recusado  | —     | 1    | 1       | fixo borda |
        | fixo        | 2026-10-09T18:00:01Z | recusado  | —     | 1    | 1       | fixo depois|

    Esquema do Cenário: [CT-14] Um objeto previamente validado não atravessa a expiração
      Dado Beto possui objeto <tipo> validado às 17:59:59Z, expiração 18:00:00Z, contador 1 e uma trilha
      Quando Beto aplica esse mesmo objeto às 18:00:00Z sem reconsultar validade pelo chamador
      Então a aplicação é recusada sem retorno descontado, o contador persistido continua 1 e a trilha continua exatamente a anterior
      Exemplos:
        | tipo        | classe              |
        | porcentagem | objeto percentual   |
        | fixo        | objeto fixo         |

    Esquema do Cenário: [CT-15] O mesmo instante mantém validade ao divergir os fusos
      Dado cupom ativo de 10%, expiração <expira>, app America/Sao_Paulo, armazenamento UTC e preferência do usuário <fuso_usuario>
      Quando Beto aplica 10000 centavos no instante explícito <agora>
      Então o resultado é <resultado>; aceite retorna 9000, contador 1 e uma linha com o instante epoch exato, e recusa deixa contador 0 e nenhuma linha
      Exemplos:
        | expira                    | agora                     | fuso_usuario        | resultado | classe                         |
        | 2026-10-09T23:59:59-03:00 | 2026-10-09T23:30:00-03:00 | UTC                 | aceito    | janela UTC contra hora local   |
        | 2026-10-09T23:59:59-03:00 | 2026-10-10T00:00:00-03:00 | America/Los_Angeles | recusado  | virada local                   |
        | 2018-11-04T01:30:00-02:00 | 2018-11-04T01:29:59-02:00 | UTC                 | aceito    | offset explícito após DST      |
```

Em CT-15 o armazenamento deve usar a representação UTC do mesmo epoch; não escrever uma hora local sem offset e esperar que o teste adivinhe a intenção. Ainda não houve tentativa executada de mudar o arnês nesta entrega; materialização temporal e prova discriminante estão pendentes, não declaradas impossíveis.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M14 | Usa >= no instante de expiração | CT-13 | Às 18:00:00Z recusa, contador 1 e trilha 1 |
| M15 | Compara somente o dia da validade | CT-13 | 18:00:01Z do mesmo dia já recusa |
| M16 | Valida antes mas não reconfere no aplicarEm | CT-14 | Mesmo objeto válido há um segundo é recusado na borda, contador não move |
| M17 | Compara texto de hora local como se fosse UTC | CT-15 | 23:30−03 com expiração 23:59:59−03 aceita e retorna 9000; interpretação sem offset expiraria |

## Regra R6 — O código exato é único na organização, inclusive por fora da UI

> Origem: RQ-14, P-04 · padrão · identidade exata; normalização e teto de texto ficam em Q1. Repetir o mesmo código noutra organização é permitido por P-04.

```gherkin
# language: pt
Funcionalidade: Identidade de cupom
  Regra: Unicidade depende da organização e ignora o próprio registro na edição
    Esquema do Cenário: [CT-16] A criação distingue colisão própria de código de outro tenant
      Dado Ana administradora da Acme e PROMO-A já cadastrado no contexto <origem>
      Quando Ana cria pelo componente outro cupom de código PROMO-A na Acme
      Então o resultado é <resultado> e há exatamente <linhas_acme> cupons PROMO-A na Acme
      E o registro inicial de <origem> mantém todos os campos, contador e trilha
      Exemplos:
        | origem | resultado | linhas_acme | classe              |
        | Acme   | recusado  | 1           | duplicado próprio   |
        | Globex | aceito    | 1           | igualdade permitida |

    Esquema do Cenário: [CT-17] Editar sem mudar o código não colide com o próprio registro
      Dado Ana administradora, PROMO-A ativo e OUTRO ativo na Acme, ambos com valores conhecidos
      Quando Ana salva PROMO-A pelo componente com código <novo_codigo> e valor 29
      Então o resultado é <resultado> e PROMO-A mantém sua chave com código <persistido> e valor <valor>
      E OUTRO não muda, o número de cupons não aumenta e contador/trilha dos dois não mudam
      Exemplos:
        | novo_codigo | resultado | persistido | valor | classe                |
        | PROMO-A     | aceito    | PROMO-A    | 29    | colisão contra si     |
        | OUTRO       | recusado  | PROMO-A    | 10    | colisão contra outro  |

    Esquema do Cenário: [CT-18] A escrita direta preserva unicidade nos dois modos de tenancy
      Dado um cupom PROMO-A no contexto <origem> e um administrador autorizado no contexto <destino>
      Quando o administrador escreve diretamente <via> outro registro com código PROMO-A em <destino>
      Então o resultado é <resultado> e o número de linhas PROMO-A em <destino> é <linhas>
      E cupom original, contador e registros de aplicação não mudam
      Exemplos:
        | origem       | destino      | via    | resultado | linhas | classe                  |
        | Acme         | Acme         | criar  | recusado  | 1      | duplicação no model     |
        | Acme         | Acme         | editar | recusado  | 1      | edição de OUTRO          |
        | Globex       | Acme         | criar  | aceito    | 1      | outro tenant             |
        | single null  | single null  | criar  | recusado  | 1      | NULL não vira exceção    |
        | single null  | single null  | editar | recusado  | 1      | edição single-tenant     |
```

Na linha editar existe previamente OUTRO, a operação altera esse registro e a recusa preserva seu código OUTRO. O contador/trilha são checados por identidade do cupom, não por count global. A ausência de unique eficaz para NULL no plano não autoriza enfraquecer RQ-14: CT-18 testa a regra pelo ponto direto.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M18 | Unique global deixa código de Globex bloquear Acme | CT-16/18 | PROMO-A de Globex permite exatamente uma linha própria de Acme |
| M19 | Edição aplica unique sem ignorar o próprio registro | CT-17 | Save com PROMO-A inalterado aceita e grava valor 29 na mesma chave |
| M20 | Unique existe somente no form ou aceita duplicados quando tenant_id é NULL | CT-18 | Criação/edição direta em single-tenant recusa e continua uma linha PROMO-A |

---
## Regra R7 — Existência é reconferida e o removido não volta a funcionar

> Origem: RQ-09, P-01 · completo · EP e células de escrita no estado terminal. Não se presume que exclusão física dispense teste sobre objeto stale.

```gherkin
# language: pt
Funcionalidade: Existência do cupom
  Regra: O motor não concede desconto por identidade inexistente
    Esquema do Cenário: [CT-19] Código inexistente não concede desconto nem consome o cupom de controle
      Dado Beto existe na Acme e há o cupom ativo CONTROLE de 10%, contador 0 e trilha vazia
      Quando Beto tenta aplicar 10000 centavos usando <codigo> no contexto da Acme
      Então nenhum cupom válido é obtido e nenhum total descontado é devolvido
      E CONTROLE mantém contador 0, seus campos e nenhuma linha de aplicação, sem qualquer uso órfão novo
      Exemplos:
        | codigo       | classe              |
        | NÃO-EXISTE   | código ausente      |
        | null         | entrada nula        |
        | string vazia | nenhuma identidade  |

    Esquema do Cenário: [CT-20] Objeto de cupom removido não pode ser aplicado
      Dado Beto existe, carregou um cupom <tipo> ativo ainda sem uso, e esse cupom foi realmente excluído
      Quando Beto tenta aplicar pelo objeto antigo a 10000 centavos
      Então a aplicação é recusada sem retorno descontado e sem recriar o cupom
      E nenhum contador de cupom de controle muda e nenhum registro órfão de aplicação é criado
      Exemplos:
        | tipo        | classe               |
        | porcentagem | removido percentual  |
        | fixo        | removido fixo        |

    Esquema do Cenário: [CT-21] Save sobre identidade removida ou inexistente não ressuscita o cadastro
      Dado Ana administradora, CONTROLE ativo com valor 10 e a identidade <alvo> sem linha persistida
      Quando Ana dispara save com valor 29 sobre <alvo>, pelo componente stale ou escrita direta correspondente
      Então <alvo> continua sem linha e CONTROLE conserva valor 10, contador e trilha
      E a operação é recusada ou não encontra o alvo, sem criar outro cupom e sem novo registro de aplicação
      Exemplos:
        | alvo                          | classe                               |
        | cupom excluído após mount     | ação de edição após exclusão          |
        | UUID bem formado inexistente  | escrita direta de identidade ausente |
```

Para o UUID inexistente, executar a operação efetiva de atualização/binding de save; não contar apenas GET como a célula editar. Se a API não puder ser alcançada após mount, manter essa célula como lacuna de arnês, sem substituir por ausência na lista. O pareamento de qualquer 404 de rota com recuperação usa CT-01/38.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M21 | Código não encontrado cai num cupom default | CT-19 | NÃO-EXISTE não dá retorno descontado e CONTROLE permanece em 0 |
| M22 | Consumo usa somente o estado do objeto, não sua existência persistida | CT-20 | Cupom excluído não devolve 9000 nem gera uso órfão |
| M23 | Save reidrata objeto stale como nova criação | CT-21 | Identidade removida continua sem linha; nenhuma nova linha com valor 29 |
| M24 | Ausência de id descarta filtro e atualiza primeiro registro | CT-21 | CONTROLE permanece com valor 10 e não há criação |

## Regra R8 — Um uso aceito move o contador uma vez e nenhum uso excede o limite

> Origem: RQ-06/11/13 · completo · BVA 3-valores (2,3,4 contra limite 3), sequência stale e concorrência real.

```gherkin
# language: pt
Funcionalidade: Consumo de usos
  Regra: O limite é do cupom, e o contador só representa aplicações aceitas
    Esquema do Cenário: [CT-22] O último uso disponível é aceito; a borda e o legado acima dela são recusados
      Dado cupom ativo no tempo de tipo <tipo>, limite 3, contador <antes> e <antes> registros de aplicação, com Beto existente
      Quando Beto aplica o cupom a 10000 centavos
      Então o resultado é <resultado>; aceite retorna 9000, contador vira <depois> e trilha tem <depois> linhas
      E recusa não devolve total descontado e preserva exatamente contador e linhas anteriores
      Exemplos:
        | tipo        | antes | depois | resultado | classe             |
        | porcentagem | 2     | 3      | aceito    | borda−1            |
        | porcentagem | 3     | 3      | recusado  | borda              |
        | porcentagem | 4     | 4      | recusado  | borda+1, legado    |
        | fixo        | 2     | 3      | aceito    | fixo borda−1       |
        | fixo        | 3     | 3      | recusado  | fixo borda         |
        | fixo        | 4     | 4      | recusado  | fixo legado        |

    Esquema do Cenário: [CT-23] A segunda cópia stale não reaproveita o último uso
      Dado dois objetos <tipo> carregados com limite 1 e usos 0, Beto existente, e o primeiro objeto já aplicado com sucesso
      Quando Beto aplica pelo segundo objeto sem recarregar
      Então a segunda aplicação é recusada sem retorno descontado
      E no banco usos permanece 1 e existe exatamente a linha da primeira aplicação, com o mesmo autor e instante
      Exemplos:
        | tipo        | classe                  |
        | porcentagem | stale após percentual   |
        | fixo        | stale após fixo         |

    Esquema do Cenário: [CT-24] Duas execuções simultâneas disputam uma única vaga real
      Dado cupom <tipo> futuro, limite <limite>, usos <antes>, trilhas anteriores reais e Beto e Carla existentes na mesma organização
      Quando Beto e Carla executam a aplicação a 10000 centavos em paralelo, por conexões distintas do mesmo banco, sincronizadas antes do consumo
      Então exatamente um retorna 9000 e o outro recebe recusa de negócio, sem total descontado
      E o banco termina com usos <limite> e somente uma linha nova, atribuída ao vencedor; a trilha anterior permanece idêntica
      Exemplos:
        | tipo        | limite | antes | classe                      |
        | porcentagem | 1      | 0     | primeira e última vaga      |
        | fixo        | 1      | 0     | vaga do tipo fixo           |
        | porcentagem | 3      | 2     | último uso num limite N     |
        | fixo        | 3      | 2     | limite N do tipo fixo       |

    Esquema do Cenário: [CT-25] A edição não corrige usos nem apaga evidência ao receber contador forjado ou limite menor
      Dado Ana administradora e cupom <tipo> esgotado com contador 3, limite 3 e três linhas de aplicação identificadas
      Quando Ana envia pela <via> uma alteração com <payload>
      Então o contador persistido continua exatamente 3 e as três linhas mantêm autores e instantes
      E nenhum novo uso é criado, independentemente de a alteração de limite ser aceita ou recusada
      Exemplos:
        | tipo        | via        | payload                 | classe                               |
        | porcentagem | componente | usos = 0                | contador fora do formulário           |
        | fixo        | direta     | usos = 0                | mass assignment direto                |
        | porcentagem | componente | limite_de_usos = 1      | invariante de Q3                      |
        | fixo        | direta     | limite_de_usos = 1      | invariante direto de Q3               |
```

CT-25 **não** decide se a redução de limite passa; mata o mutante que faz `usos = min(usos, novo_limite)` em qualquer implementação que execute essa redução. Se a validação recusar antes, o ramo de aceitação permanece Q3 e essa parte do matador não é certificada. CT-23 cobre stale sequencial; somente CT-24 cobre corrida, e lock/busy/subprocesso que não rodou não é vencedor ou perdedor de negócio.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M25 | Usa usos <= limite ou ignora limite no consumo | CT-22 | Contador 3 de limite 3 recusa e continua 3 |
| M26 | Não incrementa, ou incrementa duas vezes no sucesso | CT-22/26 | Aceite na borda−1 termina em 3, exatamente uma linha nova |
| M27 | Faz leitura-comparação-salvamento vulnerável à concorrência | CT-24 | Duas operações reais deixam exatamente um retorno descontado e uma linha nova |
| M28 | Testa limite só no objeto previamente carregado | CT-23 | Segunda cópia stale recusa; contador e trilha terminam em 1 |
| M29 | Campo usos passa por mass assignment da edição | CT-25 | Payload usos=0 deixa contador persistido 3 e três registros intactos |

## Regra R9 — Todo uso aceito tem autor e instante persistidos, na mesma unidade de efeito

> Origem: RQ-15, P-01/08 e RQ-13 · completo · rastreio de efeito: aconteceu, não aconteceu, uma vez, atomicidade. Ambos os tipos participam de todas as direções.

```gherkin
# language: pt
Funcionalidade: Auditoria das aplicações
  Regra: A aplicação registra a pessoa que aplicou e quando aconteceu
    Esquema do Cenário: [CT-26] O uso do motor registra quem aplicou, não quem cadastrou
      Dado Ana cadastrou cupom <tipo> ativo com contador 0 e sem trilha, Beto é outra pessoa existente da Acme e o instante é 2026-10-09T18:00:00Z
      Quando Beto aplica 10000 centavos pelo motor
      Então o retorno é 9000, contador persistido é 1 e existe exatamente um registro de aplicação ligado ao cupom e a Beto naquele instante
      E nenhuma linha dessa aplicação atribui autoria a Ana ou deixa o autor nulo
      Exemplos:
        | tipo        | classe              |
        | porcentagem | percentual 10       |
        | fixo        | fixo 1000 centavos  |

    Esquema do Cenário: [CT-27] A aplicação recusada não deixa registro falso
      Dado cupom <tipo> no estado <estado>, Beto existente, contador <usos> e trilha anterior real identificada
      Quando Beto tenta aplicar a 10000 centavos
      Então não recebe total descontado, contador continua <usos> e o número de linhas de aplicação não aumenta
      E os autores e instantes das linhas anteriores permanecem idênticos, sem linha para a tentativa recusada
      Exemplos:
        | tipo        | estado                        | usos | classe                    |
        | porcentagem | expirado, limite 3            | 1    | recusa temporal           |
        | fixo        | expirado, limite 3            | 1    | efeito do fixo recusado    |
        | porcentagem | futuro esgotado, limite 3     | 3    | recusa por limite         |
        | fixo        | futuro esgotado, limite 3     | 3    | fixo esgotado             |
        | porcentagem | expirado e esgotado, limite 3 | 3    | duas condições falsas     |
        | fixo        | expirado e esgotado, limite 3 | 3    | fixo, duas condições      |

    Esquema do Cenário: [CT-28] Cada invocação aceita deixa exatamente sua própria linha
      Dado Beto aplicou cupom <tipo> ativo uma vez às 18:00:00Z, contador 1 de limite 3 e aquela linha persistida
      Quando Carla, outra pessoa da Acme, aplica às 18:00:01Z a 10000 centavos
      Então o retorno é 9000, contador 2 e há exatamente duas linhas: Beto às 18:00:00Z e Carla às 18:00:01Z
      E a linha de Beto permanece idêntica e não há terceira linha ou duplicação da aplicação de Carla
      Exemplos:
        | tipo        | classe              |
        | porcentagem | efeitos percentuais |
        | fixo        | efeitos fixos       |

    Esquema do Cenário: [CT-29] Uma falha depois da inserção da trilha desfaz contador e registro juntos
      Dado cupom <tipo> ativo com contador 1, uma trilha anterior real, Beto existente e listener de teste que lança após a nova linha CupomUso ser inserida
      Quando Beto aplica 10000 centavos e alcança essa falha tardia
      Então a operação falha sem retornar desconto aceito e o contador persistido volta exatamente a 1
      E permanece somente a linha anterior, com os mesmos autor e instante; a linha da tentativa falha não permanece
      Exemplos:
        | tipo        | classe                       |
        | porcentagem | rollback percentual tardio   |
        | fixo        | rollback fixo tardio         |

    Esquema do Cenário: [CT-41] Sem a pessoa exigida pelo contrato não existe uso auditável aceito
      Dado um cupom <tipo> ativo de contador 0 e uma pessoa de controle existente na Acme
      Quando o chamador tenta aplicar 10000 centavos passando null como pessoa aplicadora
      Então a aplicação é recusada sem retorno descontado, contador continua 0 e não existe nova linha em cupom_usos
      Exemplos:
        | tipo        | classe                  |
        | porcentagem | autor ausente percentual|
        | fixo        | autor ausente fixo      |
```

CT-28 não afirma idempotência: são duas operações legítimas diferentes, com duas autorias e instantes. CT-29 injeta falha **depois** da inserção, com cupom e autor reais; listener que apenas impediu validação ou fixture sem autor não serve. CT-41 deriva de `User $aplicadoPor` obrigatório em P-01 e de quem em RQ-15, independentemente do parâmetro opcional do plano.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M30 | Confia na auditoria genérica e não insere trilha do incremento | CT-26 | Um uso pelo motor produz linha em cupom_usos para Beto no instante exato |
| M31 | Insere trilha apenas no ramo percentual ou registra criador/nulo | CT-26/41 | Fixo também registra Beto; null recusa antes de qualquer uso |
| M32 | Registra tentativa antes de conferir validade/limite | CT-27 | Tentativa recusada não aumenta a trilha existente nem move contador |
| M33 | Insere duas vezes ou sobrescreve a linha da aplicação anterior | CT-28 | Exatamente duas linhas com autores/instantes diferentes; primeira permanece idêntica |
| M34 | Incremento e trilha estão fora da mesma transação | CT-29 | Após falha pós-inserção, contador 1 e somente a linha anterior persistem |

## Regra R10 — Permissão de escrita não se deduz da visibilidade da tela

> Origem: RQ-07/08, P-02/03/09 · padrão · matriz de papel × ação, com cada verbo executado. Quatro cenários: CT-44 acrescenta a entrada HTTP de leitura de edit, que as recusas de escrita não provam. A regra não restringe quem pode aplicar o motor: o card restringe criar/editar/excluir.

| Persona default na organização | Criar | Editar | Excluir | Lista própria |
|---|---|---|---|---|
| admin_organizacao | CT-02 | CT-03 | CT-33 | CT-01 |
| master_global | CT-02/30 | CT-03/30 | CT-33/30 | acesso previsto em P-02; CT-30 prova escrita |
| admin da instalação | CT-02/30 (P-02) | CT-03/30 | CT-33/30 | acesso previsto em P-02; CT-30 prova escrita |
| panel_user | ❌ CT-31/32 | ❌ CT-31/32 | ❌ CT-31/32 | somente ativos CT-38/40 |
| infra sem papel admin | ❌ CT-31/32 | ❌ CT-31/32 | ❌ CT-31/32 | acesso a /app não decidido apenas por RQ-08 |
| sem papel admin | ❌ CT-31/32 | ❌ CT-31/32 | ❌ CT-31/32 | elegibilidade do painel não ampliada |

```gherkin
# language: pt
Funcionalidade: Administração de cupons
  Regra: A permissão é exercida na operação, não somente nos botões
    Esquema do Cenário: [CT-30] Cada papel ou acumulação exerce efetivamente cada verbo de escrita
      Dado Luis da Acme com <papeis> semeados pelo projeto, PROMO-A ativo porcentagem 10 com validade 2026-10-10T18:00:00Z, limite 3, contador 0, sem trilha, CONTROLE próprio e payload NOVO válido porcentagem 29
      Quando Luis dispara somente a operação <operacao> pelo componente real, sem depender da visibilidade do botão
      Então a escrita é <escrita> e a persistência é <persistencia>, com os campos não alterados preservados e contador 0 em todo cupom remanescente
      E CONTROLE mantém todos os dados e nenhuma linha em cupom_usos é criada; a recusa não muda PROMO-A nem cria NOVO
      Exemplos:
        | papeis | operacao | escrita | persistencia | classe |
        | admin_organizacao | create | permitida | NOVO próprio porcentagem 29 existe uma vez; PROMO-A igual | administrador local, create |
        | admin_organizacao | save | permitida | PROMO-A mesma chave porcentagem 20; NOVO ausente | administrador local, save |
        | admin_organizacao | delete | permitida | PROMO-A ausente; NOVO ausente | administrador local, delete |
        | master_global | create | permitida | NOVO próprio porcentagem 29 existe uma vez; PROMO-A igual | administrador global, create |
        | master_global | save | permitida | PROMO-A mesma chave porcentagem 20; NOVO ausente | administrador global, save |
        | master_global | delete | permitida | PROMO-A ausente; NOVO ausente | administrador global, delete |
        | admin | create | permitida | NOVO próprio porcentagem 29 existe uma vez; PROMO-A igual | premissa P-02, create |
        | admin | save | permitida | PROMO-A mesma chave porcentagem 20; NOVO ausente | premissa P-02, save |
        | admin | delete | permitida | PROMO-A ausente; NOVO ausente | premissa P-02, delete |
        | panel_user | create | negada | NOVO ausente; PROMO-A mesma chave e valor 10 | usuário comum, create |
        | panel_user | save | negada | NOVO ausente; PROMO-A mesma chave e valor 10 | usuário comum, save |
        | panel_user | delete | negada | NOVO ausente; PROMO-A mesma chave e valor 10 | usuário comum, delete |
        | infra | create | negada | NOVO ausente; PROMO-A mesma chave e valor 10 | outro papel, create |
        | infra | save | negada | NOVO ausente; PROMO-A mesma chave e valor 10 | outro papel, save |
        | infra | delete | negada | NOVO ausente; PROMO-A mesma chave e valor 10 | outro papel, delete |
        | nenhum | create | negada | NOVO ausente; PROMO-A mesma chave e valor 10 | sem admin, create |
        | nenhum | save | negada | NOVO ausente; PROMO-A mesma chave e valor 10 | sem admin, save |
        | nenhum | delete | negada | NOVO ausente; PROMO-A mesma chave e valor 10 | sem admin, delete |
        | master_global + admin | create | permitida | NOVO próprio porcentagem 29 existe uma vez; PROMO-A igual | acumulação 1, create |
        | master_global + admin | save | permitida | PROMO-A mesma chave porcentagem 20; NOVO ausente | acumulação 1, save |
        | master_global + admin | delete | permitida | PROMO-A ausente; NOVO ausente | acumulação 1, delete |
        | master_global + admin_organizacao | create | permitida | NOVO próprio porcentagem 29 existe uma vez; PROMO-A igual | acumulação 2, create |
        | master_global + admin_organizacao | save | permitida | PROMO-A mesma chave porcentagem 20; NOVO ausente | acumulação 2, save |
        | master_global + admin_organizacao | delete | permitida | PROMO-A ausente; NOVO ausente | acumulação 2, delete |
        | master_global + panel_user | create | permitida | NOVO próprio porcentagem 29 existe uma vez; PROMO-A igual | acumulação 3, create |
        | master_global + panel_user | save | permitida | PROMO-A mesma chave porcentagem 20; NOVO ausente | acumulação 3, save |
        | master_global + panel_user | delete | permitida | PROMO-A ausente; NOVO ausente | acumulação 3, delete |
        | master_global + infra | create | permitida | NOVO próprio porcentagem 29 existe uma vez; PROMO-A igual | acumulação 4, create |
        | master_global + infra | save | permitida | PROMO-A mesma chave porcentagem 20; NOVO ausente | acumulação 4, save |
        | master_global + infra | delete | permitida | PROMO-A ausente; NOVO ausente | acumulação 4, delete |
        | admin + admin_organizacao | create | permitida | NOVO próprio porcentagem 29 existe uma vez; PROMO-A igual | acumulação 5, create |
        | admin + admin_organizacao | save | permitida | PROMO-A mesma chave porcentagem 20; NOVO ausente | acumulação 5, save |
        | admin + admin_organizacao | delete | permitida | PROMO-A ausente; NOVO ausente | acumulação 5, delete |
        | admin + panel_user | create | permitida | NOVO próprio porcentagem 29 existe uma vez; PROMO-A igual | acumulação 6, create |
        | admin + panel_user | save | permitida | PROMO-A mesma chave porcentagem 20; NOVO ausente | acumulação 6, save |
        | admin + panel_user | delete | permitida | PROMO-A ausente; NOVO ausente | acumulação 6, delete |
        | admin + infra | create | permitida | NOVO próprio porcentagem 29 existe uma vez; PROMO-A igual | acumulação 7, create |
        | admin + infra | save | permitida | PROMO-A mesma chave porcentagem 20; NOVO ausente | acumulação 7, save |
        | admin + infra | delete | permitida | PROMO-A ausente; NOVO ausente | acumulação 7, delete |
        | admin_organizacao + panel_user | create | permitida | NOVO próprio porcentagem 29 existe uma vez; PROMO-A igual | acumulação 8, create |
        | admin_organizacao + panel_user | save | permitida | PROMO-A mesma chave porcentagem 20; NOVO ausente | acumulação 8, save |
        | admin_organizacao + panel_user | delete | permitida | PROMO-A ausente; NOVO ausente | acumulação 8, delete |
        | admin_organizacao + infra | create | permitida | NOVO próprio porcentagem 29 existe uma vez; PROMO-A igual | acumulação 9, create |
        | admin_organizacao + infra | save | permitida | PROMO-A mesma chave porcentagem 20; NOVO ausente | acumulação 9, save |
        | admin_organizacao + infra | delete | permitida | PROMO-A ausente; NOVO ausente | acumulação 9, delete |
        | panel_user + infra | create | negada | NOVO ausente; PROMO-A mesma chave e valor 10 | acumulação 10, create |
        | panel_user + infra | save | negada | NOVO ausente; PROMO-A mesma chave e valor 10 | acumulação 10, save |
        | panel_user + infra | delete | negada | NOVO ausente; PROMO-A mesma chave e valor 10 | acumulação 10, delete |

    Esquema do Cenário: [CT-31] Usuário sem admin não consegue disparar a escrita do componente
      Dado pessoa <persona> da Acme sem papel admin, cupom PROMO-A ativo com valor 10, contador 1 e trilha identificada, e dados válidos para criação
      Quando essa pessoa dispara a operação <operacao> pelo componente sem depender da visibilidade do botão
      Então a escrita é recusada: nenhum NOVO nasce, PROMO-A conserva valor 10 e permanece existente
      E contador continua 1 e a trilha conserva suas linhas, autores e instantes; a lista própria de ativos continua alcançável para panel_user
      Exemplos:
        | persona    | operacao | classe                  |
        | panel_user | create   | criar vedado            |
        | panel_user | save     | editar vedado           |
        | panel_user | delete   | excluir vedado          |
        | infra      | create   | outro papel cria        |
        | infra      | save     | outro papel edita       |
        | infra      | delete   | outro papel exclui      |
        | sem papel  | create   | sem papel cria          |
        | sem papel  | save     | sem papel edita         |
        | sem papel  | delete   | sem papel exclui        |

    Esquema do Cenário: [CT-32] A escrita direta também recusa cada verbo do usuário comum
      Dado Beto panel_user autenticado na Acme, cupom ativo PROMO-A de valor 10, contador 1, trilha existente e payload válido NOVO
      Quando Beto executa diretamente <operacao>, por fora de Resource e componente
      Então a operação é recusada: nenhum NOVO é criado, PROMO-A não muda valor e não é excluído
      E contador e trilha de PROMO-A continuam idênticos ao Dado
      Exemplos:
        | operacao | classe                 |
        | criar    | escrita direta create  |
        | editar   | escrita direta update  |
        | excluir  | escrita direta delete  |
    Esquema do Cenário: [CT-44] A identidade conhecida não autoriza o usuário comum a ler a tela edit
      Dado Beto panel_user da Acme, um ALVO próprio no estado <estado> com UUID conhecido e dados identificáveis, e CONTROLE próprio ativo
      Quando Beto faz GET direto em /app/acme/cupons/{uuid_ALVO}/edit
      Então a resposta é 403 ou 404 e não contém o código nem os dados preenchidos de ALVO
      E ALVO mantém campos, contador e trilha; a lista própria de Beto com CONTROLE continua alcançável e não inclui ALVO quando ele está inativo
      Exemplos:
        | estado                          | classe                         |
        | futuro com usos disponíveis     | leitura de edit também vedada  |
        | expirado com usos disponíveis   | identidade própria vencida     |
        | futuro esgotado                 | identidade própria esgotada    |
        | expirado e esgotado              | duas condições de inatividade |
        | expira no instante observado    | fronteira temporal da leitura |

```

CT-30 tem 16 combinações de papéis × 3 verbos = 48 execuções independentes. Create envia o payload NOVO porcentagem 29; save altera somente o valor de PROMO-A de 10 para 20; delete atua sobre PROMO-A sem uso anterior, mantendo Q4 fora do oráculo. Cada linha parte de fixture nova e realiza um único verbo. Aceite/recusa é confirmado no banco, não por can()/Gate::allows. CT-31 e CT-32 continuam separando o componente da escrita direta.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M35 | Recorte do panel_user inclui toda entidade, retirando também leitura | CT-38/40 | panel_user mantém leitura e recebe exatamente os ativos próprios |
| M36 | Botões escondidos mas create/save/delete não consultam autoridade | CT-31 | Ação efetivamente disparada recusa cada verbo; NOVO ausente e PROMO-A valor 10 existente |
| M37 | Policy no componente, sem proteção da escrita direta | CT-32 | Chamadas diretas de cada verbo recusam; estado persistido permanece idêntico |
| M52 | GET edit usa permissão de listagem e exibe cupom próprio ao usuário comum | CT-44 | Beto recebe 403/404 sem dados de ALVO em cada estado, apesar de conhecer o UUID |
| M53 | Consulta autoriza os pares mas handler exige exatamente um papel | CT-30 | Cada par com admin cria NOVO, altera PROMO-A para 20 e exclui o alvo em execuções distintas; o par panel_user + infra não muda dados |

---
## Regra R11 — Excluir um cupom autorizado remove somente o alvo

> Origem: RQ-01/07, RQ-09 · padrão · estado × operação. Exclusão de cupom com trilha anterior permanece Q4; não há assertion de cascade nem de retenção inventada.

```gherkin
# language: pt
Funcionalidade: Exclusão no painel
  Regra: O administrador exclui o cupom escolhido, sem atingir o cupom de controle
    Esquema do Cenário: [CT-33] O administrador exclui efetivamente pela ação da tabela
      Dado <admin> autorizado na Acme, cupom ALVO <tipo> no estado <estado> sem uso anterior e CONTROLE ativo de valor 10
      Quando o administrador dispara a ação delete da tabela para ALVO
      Então ALVO não existe mais no cadastro e CONTROLE mantém sua chave, valor 10 e contador 0
      E nenhum registro de aplicação é criado e os outros cupons não são excluídos
      Exemplos:
        | admin             | tipo        | estado                          | classe                  |
        | admin_organizacao | porcentagem | futuro com saldo                 | admin local percentual  |
        | admin_organizacao | fixo        | futuro com saldo                 | admin local fixo        |
        | master_global     | porcentagem | expirado com saldo               | master, expirado        |
        | master_global     | fixo        | expirado com saldo               | master fixo             |
        | admin             | porcentagem | expira no instante observado     | instalação, fronteira   |
        | admin             | fixo        | expira no instante observado     | instalação fixo         |

    Esquema do Cenário: [CT-34] Exclusão de identidade ausente não atinge um registro vizinho
      Dado Ana administradora, CONTROLE ativo de valor 10 e o alvo <identidade> sem linha persistida
      Quando Ana tenta excluir novamente ou diretamente <identidade>
      Então nenhum registro adicional é excluído e CONTROLE mantém chave, valor, contador e trilha
      E a identidade ausente não reaparece e nenhum registro de aplicação é criado
      Exemplos:
        | identidade                         | classe              |
        | UUID de cupom realmente excluído    | segundo delete      |
        | UUID bem formado que nunca existiu  | alvo inexistente    |
```

Se houver resposta 404 de rota, o par CT-01/38 prova recuperação na lista própria. Não impor “delete falha com FK” ou “trilha é apagada” com base no 01. A ausência de trilha nos positivos é explícita para deixar a interação Q4 aberta, não para provar atomicidade de aplicações.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M38 | Restringe delete a ativo, confundindo o recorte da listagem com autoridade do admin | CT-33 | Cupom expirado sem uso é efetivamente removido pelo administrador |
| M39 | Lookup sem resultado cai no primeiro registro da tabela | CT-34 | CONTROLE permanece com chave e valor 10 depois do segundo delete ou UUID ausente |
| M40 | Action abre mas seu handler não realiza exclusão | CT-33 | ALVO deixa de existir depois de callAction; visibilidade do botão não basta |

## Regra R12 — Identidade e contexto impedem escrita ou efeito em outra organização

> Origem: P-02/04/08, RQ-07/09/13/15 · padrão · IDOR e mass assignment; **4 cenários**, teto excedido porque o gate de fronteira com tenant nulo e o gate por fora da UI exigem entradas distintas. Não esconder esse custo numa célula de leitura.

```gherkin
# language: pt
Funcionalidade: Isolamento da organização
  Regra: Dados e efeitos da aplicação permanecem na organização corrente
    Esquema do Cenário: [CT-35] UUID conhecido de outro tenant não permite ação de edição ou exclusão
      Dado Ana admin da Acme, Bruno admin da Globex, cupom OUTRO da Globex de valor 10 e CONTROLE ativo da Acme
      Quando Ana dispara <operacao> para o UUID de OUTRO pelo ponto de entrada <entrada> da Acme
      Então a operação é recusada sem revelar os dados de OUTRO; seu valor 10, contador e trilha continuam idênticos
      E CONTROLE permanece intacto e a lista própria com CONTROLE é alcançável sem loop após a recusa
      Exemplos:
        | operacao | entrada                                      | classe                 |
        | editar   | rota /app/acme/cupons/{uuid_OUTRO}/edit        | binding HTTP de IDOR   |
        | editar   | componente save com record de Globex          | escrita de IDOR        |
        | excluir  | ação delete da tabela com record de Globex    | verbo irmão de IDOR    |

    Esquema do Cenário: [CT-36] Objeto estrangeiro carregado por código privilegiado não é aplicado na Acme
      Dado Ana está no contexto Acme, Beto aplicador da Acme existe, e um objeto <tipo> da Globex foi carregado fora do recorte com contador 0 e sem trilha
      Quando Beto aplica diretamente esse objeto estrangeiro a 10000 centavos no contexto Acme
      Então a aplicação é recusada sem retorno descontado; o cupom da Globex permanece com contador 0
      E nenhuma linha nova em cupom_usos é criada para ele ou para a Acme e nenhum cupom de controle muda
      Exemplos:
        | tipo        | classe                    |
        | porcentagem | foreign object percentual |
        | fixo        | foreign object fixo       |

    Esquema do Cenário: [CT-37] Payload de tenant não decide onde o cupom é gravado
      Dado Ana administradora no contexto Acme, Globex existente e um cupom próprio para edição
      Quando Ana grava dados válidos pela <via> enviando apenas o campo adicional tenant_id de Globex
      Então nenhum cupom é criado ou transferido para Globex; eventual escrita aceita pertence à Acme e contém os valores válidos enviados
      E o cupom estrangeiro de controle, os contadores e todas as linhas anteriores de aplicação ficam intactos
      Exemplos:
        | via                 | classe                         |
        | componente create   | fronteira de criação           |
        | componente save     | fronteira de edição            |
        | escrita direta criar| mass assignment por fora da UI |
        | escrita direta editar| edição por fora da UI         |

    Esquema do Cenário: [CT-42] Tenancy ligada sem organização corrente fecha a fronteira
      Dado tenancy ligada, Ana autenticada com papel na Acme, contexto de tenant nulo e cupons reais da Acme e Globex com autores e trilhas de controle
      Quando Ana executa <operacao> sem tenant corrente
      Então <resultado> e nenhum dado de cupom estrangeiro é devolvido
      E cupons, contadores e linhas de aplicação de Acme e Globex permanecem idênticos
      Exemplos:
        | operacao                          | resultado                                     | classe                  |
        | consultar a lista pelo domínio    | a lista é vazia ou há recusa de contexto       | scope com nulo          |
        | aplicar objeto ativo de Acme      | aplicação recusada sem total descontado        | consumo com nulo        |
        | criar diretamente dados válidos   | criação recusada, nenhum cupom global nasce    | escrita com nulo        |
```

CT-42 diferencia **tenancy ligada sem contexto** de **modo single-tenant válido**. Não confundir tenant_id NULL em CT-18 com permissão para abrir todo o banco quando um request multi-tenant perdeu seu discriminante. CT-36 obtém o objeto na fixture, não pela consulta que será testada; retirar scope só no setup e restaurar antes do Quando.

A entidade `cupom_usos` recebe linhas pelo motor em CT-26/36; não foi encontrado inventário autorizado de entrada direta da entidade filha porque o 02 não existe. **Não** se declara “filho protegido pelo pai”; sua leitura/escrita direta por cliente fica lacuna do inventário, e o CT do pai não fecha essa linha.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M41 | Listagem escopada, mas binding/handler/model aceitam record estrangeiro | CT-35/36 | UUID conhecido não muda Globex; objeto estrangeiro não incrementa nem gera trilha |
| M42 | tenant_id do payload passa por fill/save em vez do contexto confiável | CT-37 | Nenhuma transferência/criação em Globex; escrita aceita permanece Acme |
| M43 | Scope só filtra quando tenant é truthy; nulo abre o conjunto | CT-42 | Sem tenant em modo multi-tenant lista não retorna registros e consumo/criação não têm efeito |

## Regra R13 — O usuário comum lista apenas cupons próprios com validade e saldo

> Origem: RQ-08/15, P-03/08 · padrão · decisão completa, cardinalidade e persistência do recorte ao buscar/paginar. Quatro cenários: CT-45 fecha a sonda obrigatória de participante histórico; o autor da aplicação não ganha exceção ao recorte de ativos. Não se testa string de situação nem ordem escolhida pelo plano.

```gherkin
# language: pt
Funcionalidade: Leitura de cupons ativos
  Regra: A lista do usuário comum usa validade e usos disponíveis em conjunto
    Cenário: [CT-38] Todas as partições de situação são distinguidas na listagem
      Dado Beto panel_user da Acme e cupons próprios ATIVO-P e ATIVO-F futuros com saldo, VENCIDO com saldo, ESGOTADO futuro, AMBOS vencido/esgotado, BORDA com expiração agora e REMOVIDO já excluído; Globex possui ESTRANGEIRO ativo
      Quando Beto carrega a tabela da Acme
      Então os IDs/códigos visíveis são exatamente ATIVO-P e ATIVO-F, sem os outros seis códigos
      E as ações criar, editar e excluir não são oferecidas a Beto, e o próprio recorte de ativos continua alcançável após tentativa de rota vedada

    Esquema do Cenário: [CT-39] O recorte acompanha cardinalidade, busca e todas as páginas
      Dado Beto panel_user da Acme, <quantidade> cupons próprios ativos, cupons próprios vencidos/esgotados e um ativo de Globex, com tamanho de página P lido da tabela real
      Quando Beto lista todas as páginas da busca <busca>, reiniciando da página 1 se houve inserção entre visitas
      Então a união dos IDs corresponde exatamente a <conjunto> de ativos próprios, sem IDs de Globex ou inativos e sem duplicação nessa enumeração reiniciada
      E o contador de usos e as trilhas não mudam
      Exemplos:
        | quantidade | busca           | conjunto                           | classe                        |
        | 0          | vazia           | vazio                              | zero                          |
        | 1          | vazia           | único próprio                      | um                            |
        | P          | vazia           | P próprios                         | limite de página              |
        | P+1        | vazia           | P+1 próprios                       | atravessa página              |
        | P+1        | código completo | único ativo correspondente         | busca preserva escopo         |
        | P+1        | código de Globex| vazio                              | busca não revela outro tenant |
        | P+1 e novo inserido entre páginas | vazia | todos os ativos próprios do estado final | reenumeração após inserção |

    Cenário: [CT-40] A fonte de listagem por fora do componente aplica as mesmas duas condições
      Dado Beto panel_user no contexto Acme e as sete identidades próprias e uma estrangeira descritas em CT-38
      Quando o serviço de leitura ou query pública de listagem é invocado diretamente com esse contexto, sem montar o componente
      Então o conjunto devolvido contém exatamente os IDs de ATIVO-P e ATIVO-F e nenhum dos outros seis códigos
      E contador e trilha de cada cupom persistido ficam idênticos ao Dado
    Esquema do Cenário: [CT-45] O aplicador histórico não ganha acesso ao cupom que saiu do recorte de ativos
      Dado Beto panel_user da Acme aplicou ALVO <tipo> em 2026-10-09T11:00:00Z, gerando uma trilha identificada e contador 1; agora ALVO está <estado> e CONTROLE próprio permanece ativo
      Quando Beto lista os cupons pela <via> em 2026-10-09T12:00:00Z
      Então a lista tem exatamente o ID de CONTROLE e não contém o ID nem o código de ALVO
      E a trilha de ALVO mantém a mesma chave, autor Beto e instante 2026-10-09T11:00:00Z; seu contador permanece 1 e nenhuma linha de aplicação nova nasce
      Exemplos:
        | tipo        | estado                          | via                             | classe                    |
        | porcentagem | esgotado, validade futura       | tabela do componente            | autor histórico esgotado  |
        | fixo        | esgotado, validade futura       | tabela do componente            | fixo esgotado             |
        | porcentagem | vencido, com uso disponível     | tabela do componente            | autor histórico vencido   |
        | fixo        | vencido, com uso disponível     | tabela do componente            | fixo vencido              |
        | porcentagem | esgotado, validade futura       | fonte pública fora do componente| recorte direto, esgotado   |
        | fixo        | esgotado, validade futura       | fonte pública fora do componente| recorte direto, fixo       |
        | porcentagem | vencido, com uso disponível     | fonte pública fora do componente| recorte direto, vencido    |
        | fixo        | vencido, com uso disponível     | fonte pública fora do componente| recorte direto, fixo vencido|

```

Os conjuntos de CT-38/40 são fixtures independentes, apesar de compartilhar a especificação dos nomes. CT-39 usa P efetivo, não um 10 presumido. Ordenação entre empates, cursor durante inserção sem reinício e texto de vazio não foram determinados pelo requisito: registrar como lacunas, sem importar defaultSort do 01. Coluna de ordenação inválida/tipo errado continua no inventário Livewire pendente, não se declara sanitizada por hipótese.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M44 | Ativo significa validade OU saldo em vez de validade E saldo | CT-38/40 | VENCIDO com saldo e ESGOTADO futuro não aparecem |
| M45 | Filtra só na primeira carga da tabela, e busca/fonte direta não recebem o recorte | CT-39/40 | Busca por código estrangeiro é vazia; leitura direta só retorna ATIVO-P/ATIVO-F |
| M46 | Recorte ou enumeração abandona registros ao atravessar a primeira página | CT-39 | Com P+1 ativos, união reiniciada contém exatamente os P+1 IDs próprios |
| M55 | Usa ativo OU cupom já usado pelo usuário na consulta | CT-45 | ALVO usado por Beto não é listado depois de expirar ou esgotar; sua trilha continua persistida e CONTROLE ativo aparece |

Para CT-45, a aplicação de base é legítima: porcentagem 10 ou fixo 1000 sobre total 10000, no instante 11:00Z. O esgotado tem limite 1 e expiração 2026-10-10T18:00:00Z; o vencido tem limite 3 e expiração 2026-10-09T11:30:00Z. O relógio só avança para 12:00Z depois da aplicação. A fonte direta é a mesma consulta pública da tabela descrita em CT-40, com usuário/team correntes; não é query artificial escrita no teste. A fixture não depende da decisão de cadastro já vencido de Q2.

## Regra R14 — A interação JavaScript mantém a unidade visível coerente com o tipo

> Origem: RQ-01/03/04, P-05/09 · completo · cenários CT-B01 e CT-B02 no `05-casos-de-teste-browser.md`.

A precisão do texto do rótulo não é imposta pelo 01. O oráculo é a distinção entre porcentagem e **centavos**, que já existe em P-05, atualizada pelo navegador no campo operado. Gravação, validação de domínio e autorização continuam no 04; o 05 acrescenta somente a reação de JS em create e edit.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M47 | Select muda estado servidor, mas JS não atualiza a unidade do campo em create | CT-B01 | Sem recarregar a página, valor passa a indicar centavos e deixa de indicar percentual |
| M48 | Edit mantém a unidade do registro inicial ao trocar fixo para porcentagem | CT-B02 | Unidade visível passa a percentual antes da tentativa 101, sem reload |
| M49 | Resposta de validação após troca de tipo não é exibida ou JS trava o formulário | CT-B02 | Campo valor apresenta erro visível associado, continua operável e registro mantém fixo 150 |

## Checklist de Taxonomia

| Gatilho / item | Resposta | Grupo |
|---|---|---|
| Rota/ação com record ID; autorização horizontal | CT-35 e CT-21/34 para ID ausente | Rotas e recuperação; Ações e listagem no componente |
| Policy/permission; autorização exercida na ação | CT-31, CT-32, positivos CT-02/03/33 | Ações e listagem no componente; Domínio e efeitos |
| Idempotência de aplicação no agregado persistido | lacuna declarada: P-01 tira Pedido do escopo; nenhuma fixture de retorno/contador discrimina reaplicação no Pedido; Q5 | Domínio e efeitos |
| Retry de cadastro/exclusão com identidade existente | CT-16/18 e CT-34; não se confunde com idempotência do Pedido | Cadastro no componente; Domínio e efeitos |
| Domínio condicionado tipo × valor | CT-07/08/09, cálculo CT-10/12 | Cadastro no componente; Domínio e efeitos |
| Todo campo em criação, edição e uso | CT-04…09, CT-13…18 e CT-22; lacunas Q1/Q2/Q3 para domínios não definidos | Cadastro no componente; Domínio e efeitos |
| Contador/limite; concorrência | CT-24; CT-23 é outra prova, sequencial | Domínio e efeitos |
| Efeito com destinatário variável 0/1/N | CT-41 sem autor, CT-26 um registro, CT-28 duas aplicações distintas; o 0 não prova atomicidade | Domínio e efeitos |
| Ausente ≠ null ≠ string vazia | CT-04/05/06; campos indispensáveis; não presumir PATCH parcial | Cadastro no componente; Domínio e efeitos |
| Listagem 0/1/P/P+1 e inserção entre páginas | CT-39; lacuna declarada: estabilidade sem reiniciar não prometida por 00 | Ações e listagem no componente |
| Ordenação por coluna inexistente, nullable, empate | lacuna declarada: 02 ausente, sem lista de consumos públicos; ordem/default do 01 recusados como oráculo | Ações e listagem no componente |
| Data/hora e timezone/DST | CT-13/14/15; execução do arnês e prova temporal ainda pendentes | Domínio e efeitos |
| Texto livre: caixa/espaço/acento/emoji/teto n,n+1 no model | lacuna declarada: Q1; 00 não fixa normalização nem teto e não se importou 40 do 01 | Cadastro no componente; Domínio e efeitos |
| Unicidade + SoftDeletes | lacuna declarada: mecanismo de remoção não está no 00; Q4 e 02 ausente; não declarar ausência de SoftDeletes como prova | Domínio e efeitos |
| Removido/desativado ainda funciona | CT-20/21/34; inativos CT-13/22/27 | Domínio e efeitos; Rotas e recuperação |
| CRUD combinado: IDs inexistentes, delete repetido, edição do código livre sem mudar a chave | CT-21/34/17/43 | Domínio e efeitos; Cadastro no componente |
| Mass assignment, cupons | CT-25, CT-37 | Cadastro no componente; Domínio e efeitos |
| Upload | não se aplica: nenhuma interface/campo de upload faz parte do card ou das premissas; não dispensa controle de dado persistido | — |
| Precisão monetária, centavos e fração | CT-10/11/12, 29% de 100 e meio centavo; expressão float corrigida após ADV-06 | Domínio e efeitos |
| Superfície Livewire: fora do domínio e tipo errado por ponto | CT-04/05 cobrem campos conhecidos; lacuna declarada: inventário do 02 ausente, sem cobertura total de métodos/propriedades/ações finais | Cadastro no componente; Ações e listagem no componente |
| Estado de framework usado como índice/parse/coluna/operador | CT-04/05 para validade inválida; lacuna declarada para cada consumo de tabela não inventariado no 02 | Ações e listagem no componente |
| Método público de componente chamável com argumento fora da lista | CT-31/35 exercitam ações conhecidas; lacuna declarada: lista fechada de argumentos e métodos finais indisponível sem 02 | Ações e listagem no componente |
| IDOR por tabela: cupons | CT-35/36 | Rotas e recuperação; Domínio e efeitos |
| IDOR por tabela: cupom_usos | CT-36 impede efeito estrangeiro pelo motor; lacuna declarada: entradas/leitura direta da tabela-filha não inventariadas, pai não fecha filha | Domínio e efeitos |
| Mass assignment por tabela: cupons | CT-25/37 | Cadastro no componente; Domínio e efeitos |
| Mass assignment por tabela: cupom_usos | lacuna declarada: fronteira direta do cliente ausente do 02; CT-26 autoria do motor não é prova de payload arbitrário da filha | Domínio e efeitos |
| Scope com discriminante nulo | CT-42 em tenancy ligada; single-tenant separado em CT-18 | Domínio e efeitos |
| Saída de 4xx/redirect | CT-01 e CT-38 pareados às recusas HTTP de CT-21/31/35; lista com dado próprio e sem loop | Rotas e recuperação; Ações e listagem no componente |
| Trilha aconteceu/não aconteceu/uma vez/atomicidade | CT-26/27/28/29, ambos os tipos | Domínio e efeitos |
| Mudança de campo fora do estado inicial | CT-03/08/25 | Cadastro no componente; Domínio e efeitos |
| Acumulação de papéis, todos os dez pares da lista do 00 | CT-30 executa cada verbo nas 16 combinações, 48 linhas; CT-32 prova escrita direta | Ações e listagem no componente; Domínio e efeitos |
| Participante histórico e link de notificação | CT-45: quem aplicou não vê inativo por sua autoria, mantendo trilha; Q4 continua aberta para remoção; não há notificação/link no escopo literal do 00 | Ações e listagem no componente; Domínio e efeitos |

A leitura da taxonomia foi completa; o termo lacuna não significa controle dispensado. Nenhum grep que desconhece a implementação futura, nenhum read-only de prompt e nenhum git status foi tratado como prova de inexistência de superfície ou isolamento técnico.

## Gate de falsificabilidade e poda

Cada regra tem pelo menos três mutantes plausíveis, com valor/asserção discriminante. As tabelas são **previsão de especificação**, não mortes medidas. Os exemplos de precisão usam 29% de 100 para a razão float primeiro, 29% de 10000 como cálculo usual e 5% de 50; os de tempo usam o segundo exato e a janela UTC/local; os de identidade usam outro tenant e outro ator. Cada ausência de trilha tem cupom e usuário reais, ou declara explicitamente identidade ausente com controle real.

O gate conservou CT-24 separado de CT-23 porque duas cópias stale não expõem o interleaving de duas conexões. Conservou CT-32 por fora da UI e CT-06/09/18 por fora do form porque eles distinguem controles existentes somente no schema. Em R12, o cenário com tenant nulo excede o teto padrão por ser fronteira obrigatória distinta. R9 usa cinco cenários, dentro do teto completo; ausência do autor é fronteira de confiança, além das quatro direções do efeito.

| Cenário cogitado | Por que foi cortado ou declarado lacuna |
|---|---|
| Browser para CRUD inteiro, busca, paginação, validação e permissão | CT-02/03/07/31/33/38/39 provam mais barato; 05 fica com reação real de JS |
| Browser que só visita e confere console | Não discrimina gravação nem unidade; CT-01 faz visita e 05 tem observável específico |
| Percentual só com total redondo e 10% | Não discrimina float/truncamento; substituído por CT-10/11 |
| Assert de linha de log cupom | Não é RQ; auditoria persistida já em R9 |
| Idempotência com dois retornos puros do motor | Tautologia sem Pedido persistido; Q5 e lacuna declarada |
| Esperar normalização ou 40 caracteres do plano | Q1, fonte sem essa regra; sem cenário direcional |
| Criar vencido ou reduzir limite com resultado escolhido pelo dev | Q2/Q3; ficam apenas os invariantes de CT-13/14/25 |
| Apagar cupom com trilha e afirmar cascade | Q4; resultado não determinado pelo 00 |
| Atomicidade com falha na pré-validação ou autor ausente | Não alcança efeito; CT-29 falha após inserir com autor real |
| Provar proteção de cupom_usos com CT do pai | Não fecha a fronteira da filha; inventário ausente fica lacuna |

## Revisão adversarial

**Rodada 1 executada e sete achados fechados; rodada 2 PENDENTE.** Gatilho inicial: áreas completas e Impacto 3. Rota da revisão 1: `/root/adversarial_26_c1`, contexto novo via colaboração Codex, contrato instalado `fw-adversario-ct`; família GPT-6, ultra solicitado, deployment exato não exposto. Entradas de domínio: somente 00 e 04/05; sem 01, código, raciocínio de derivação, catálogos ou outros conjuntos. Glossário ausente. Relatório imutável desta revisão: `adversarial-1.md` nesta pasta. A sessão que derivou não se autorrevisou.

| Achado | Fechamento | Evidência no conjunto revisado |
|---|---|---|
| ADV-01 — edição ignora código novo | cenário novo CT-43; M50 | A mesma chave muda PROMO-A para NOVO livre na Acme, preservando a linha homônima da Globex |
| ADV-02 — fixed aceita fração | oráculos/datasets reescritos CT-07/08/09; M51 | String 12.5 no fixo recusa create, edit e escrita direta; nenhum cupom novo nem alteração silenciosa para 12 |
| ADV-03 — usuário comum lê edit próprio inativo | cenário novo CT-44; M52 | GET direto pelo UUID conhecido recusa com 403/404 sem conteúdo de ALVO nos cinco estados, incluindo ativo |
| ADV-04 — handler recusa admin acumulado | oráculo reescrito CT-30; M53 | 16 combinações × 3 verbos = 48 operações independentes; efeitos no banco distinguem papel isolado/par e escrita permitida/negada |
| ADV-05 — validade não é hidratada/preservada | CT-01 reescrito e âncora de CT-43; M54 | Edit mostra o instante específico, e salvar só o código conserva 2026-10-10T18:00:00Z |
| ADV-06 — matador float não diverge | CT-10 e M10 reescritos | Expressão antiga removida como mutante anunciado; 29% de 100 distingue a razão float calculada primeiro: retorno inteiro 71 contra 72 em binary64 |
| ADV-07 — autor histórico vê inativo | cenário novo CT-45; M55 | Após uso por Beto, vencido/esgotado permanece na trilha e sai da tabela/fonte direta; somente CONTROLE ativo aparece |

Todos os achados se apoiam em RQ/P vigentes, sem decisão nova nem alteração do 00. As lacunas de Q1–Q5 e de inventário do 02 permanecem declaradas; nenhum ADV foi encerrado como lacuna por conveniência. ADV-05 compartilha o cenário novo de ADV-01. No total, três cenários novos, quatro CT existentes reforçados (CT-01/07/08/09), CT-30 reescrito e CT-10/M10 corrigidos; seis novos mutantes previstos. As regras padrão R1/R10/R13 passam a quatro cenários, estouro justificado pelos três pontos de entrada/partições demonstrados pelo adversário, sem deslocar prova para browser.

O §Revisão Adversarial da skill exige uma segunda e última rodada porque o fechamento criou CT-43/44/45. A sessão orquestradora despachará subagente em contexto novo; o executor encerra este turno para liberar concorrência. A rodada 2 ainda tem zero revisões executadas, achados não apurados e nenhuma conclusão antecipada. O teto é duas rodadas; eventual achado estrutural da segunda deverá ser registrado e escalado, não gerar uma terceira revisão.

Controles efetivos: filesystem irrestrito, shell sem whitelist e nenhum hook Claude ativo; cegamento por contrato, não por sandbox. O adversário declarou que as duas leituras iniciais carregaram automaticamente o perfil PowerShell/PSReadLine, corrigindo consultas posteriores para `login:false`; isso impede alegar exclusão técnica de leituras externas. Nenhuma leitura foi negada. Foram permitidas apenas as entradas da revisão, o contrato e a existência do glossário; isso não transforma prompt/read-only em prova de bloqueio. A verificação por hashes detecta mudança dos artefatos, não bloqueia leitura da árvore inteira.


## Verificações e limites

- [x] SKILL feature-wiki e feature-test-design lidas integralmente, referências condicionais da etapa abertas, 2026-10-09.
- [x] 00 e 01 lidos integralmente; 01 limitado a paths, rotas, stack e superfície no oráculo, 2026-10-09.
- [x] 02 ausente verificado por Test-Path; não criado, 2026-10-09.
- [x] Arnês de testes, dependências efetivas e APIs do vendor conferidos sem Artisan, 2026-10-09.
- [x] Revisão adversarial independente rodada 1 executada; ADV-01…07 fechados no conjunto, 2026-10-09.
- [ ] Revisão adversarial rodada 2, obrigatória pelos três cenários novos; despacho pendente da orquestração.

## Execução posterior à implementação

- [ ] Pest/Browser e conferência dos seletores/rotas finais: não executados nesta entrega documental.
- [ ] Mutation testing com o driver/plugin efetivo, concorrência real e prova com/sem correção: posteriores à implementação, sem medição nesta rodada.
- [ ] Confirmar na futura materialização a expressão exata de M10; a prova isolada binary64 não é uma execução da feature.



## Contagens mecânicas após fechamento da rodada 1

Contagem por expressão regular sobre os arquivos, sem executar a aplicação: 45 cabeçalhos de cenário CT no 04, 14 cabeçalhos de regra, 2 cabeçalhos CT-B no 05 e 55 linhas de mutantes únicos no 04. O script também conferiu IDs únicos, referências de matadores existentes e ao menos um mutante previsto por CT, um Quando e ao menos um Então por cenário. Isso verifica estrutura documental; não substitui revisão adversarial nem execução de teste/mutação.
