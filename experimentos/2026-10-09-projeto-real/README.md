# Comparação cega no projeto Laravel real — 2026-10-09

Esta rodada compara a derivação de testes pelas skills anteriores e pela revisão de portabilidade
em cópias descartáveis do projeto local `gsferro/starter-kit-easy` (`demo-r8`). O aplicativo usa
Laravel, Filament, Livewire, Pest e SQLite reais; o teste de navegador usa Chromium real.
As duas features são implementações experimentais nesse kit, não uma validação em produção.

O [pré-registro](PLANO.md) define a pergunta, os braços, os controles e os critérios antes dos
vereditos. A [análise do instrumento](VALIDADE-INSTRUMENTO.md) registra contradições e limites
que impedem tratar uma pontuação documental como prova universal de qualidade.
O [relatório final](RELATORIO.md) apresenta o antes/depois honesto: o gate não foi aprovado.
As [métricas centrais](../README.md#projeto-laravel-real--2026-10-09) separam julgamento,
conferência secundária e execução física selecionada.

## Tratamentos e cegamento

- Baseline: commit `6e9222c0f12769795dd4321e4f47f6509dbc2d9e`, feature-wiki 4.0.0 e
  feature-test-design 1.16.0.
- Candidata: snapshot após a auditoria de portabilidade, feature-wiki 4.1.0 e
  feature-test-design 1.17.0. As correções posteriores FW4.1.1 e FTD1.17.1/1.17.2/1.17.3 não entram nele.
- Cada derivação nasce em contexto novo, lê o próprio tratamento e o oráculo congelado.
  Não recebe catálogo, conjunto rival, implementação nova ou resultados.
- A revisão adversarial recebe 00 + 04/05. O juiz recebe somente catálogo e conjunto completo
  anonimizado. O implementador recebe 00/01, sem os conjuntos ou o catálogo.
- O host tem filesystem irrestrito. Contexto novo, cópias limpas e contrato de caminhos são
  controles procedimentais; não se declara isolamento técnico de leitura.
- Todos os despachos pedem esforço `ultra` na família GPT-6. O deployment exato não é exposto.
  O experimento usa ferramentas de colaboração do host; não prova carregamento nativo dos TOML.

As alterações permanecem na árvore de trabalho: esta execução não criou commit, tag, release
ou publicação externa. Referência “publicada” nos instrumentos significa texto disponível na
fonte, sem alegar distribuição de uma release.

## Arquivos e proveniência

| Artefato | Conteúdo |
|---|---|
| [tratamentos/manifest.json](tratamentos/manifest.json) | Hashes dos ZIP completos; cada entrada também foi conferida contra o snapshot |
| [baseline.zip](tratamentos/baseline.zip), [candidata.zip](tratamentos/candidata.zip) | Skills inteiras realmente instaladas nos braços |
| [preparacao.json](preparacao.json) | Hashes individuais e preparação das cópias |
| [projeto.json](projeto.json) | Identidade dos arquivos comuns do projeto nos dois braços |
| [instrumentos.json](instrumentos.json) | Hashes dos prompts, oráculos e catálogos usados |
| `instrumentos-congelados/` | Cópias integrais dos instrumentos e dos quatro prompts de derivação |
| `preliminares/`, `intermediarios/`, `revisoes/` | Derivações antes do fechamento, estados intermediários e revisões independentes |
| `conjuntos/` | Conjuntos completos congelados e cópias anonimizadas, depois do fechamento |
| [implementacao.patch](implementacao.patch), `implementacao/` | Patch e arquivos da implementação independente; ambiente original não é arquivado |
| [execucao-controle/implementacao.json](execucao-controle/implementacao.json) | Validações, falhas de bootstrap e limites do implementador |
| [controle-root.xml](execucao-controle/controle-root.xml) | Reexecução independente do controle, com resultado JUnit real |
| [arnes/registro.json](arnes/registro.json) | Registro separado dos testes comparativos em TenancyTestCase |
| [correcao-instrumento.json](correcao-instrumento.json) | Distinção entre prompt histórico usado e versão 2 corrigida para futuras rodadas |
| [comparacao-documental.json](comparacao-documental.json), `vereditos/` | Quatro vereditos primários brutos, citações literais e comparação por defeito |
| [PLANO-ADJUDICACAO.md](PLANO-ADJUDICACAO.md) | Conferência pareada adicional posterior aos vereditos; não substitui a medição primária |
| `referencia-v2/`, `referencia-v3/` | Correções independentes, arquivos integrais, patches e manifestos antes da execução |
| `testes/cuponsv1/`, `testes/cuponsv2/`, `testes/comprasv1/`, `testes/comprasv2/`, `testes/controleenumv1/` | Traduções e mapas congelados; o último é controle próprio, fora da comparação |
| `execucao-derivada/`, `execucao-mutantes/` | Comandos reais, logs integrais, JUnit e resultados de todas as tentativas |
| [resultado-executavel.json](resultado-executavel.json), [integridade-final.json](integridade-final.json) | Classificação manual das falhas de asserção, sobreviventes e restauração dos arquivos |
| [regressões principais finais](regressoes-coletanea-final.json), [auxiliares finais](regressoes-adicionais-final.json), [log auxiliar](regressoes-adicionais-final.log) | Checks da fonte atual, separados da comparação comportamental |
| [validação dos artefatos](validacao-artefatos-final.json), [precisão final](precisao-referencia-final-1.17.3.json) | Integridade dos instrumentos/traduções, sintaxe dos scripts/perfis e expressão publicada |
| [REVISAO-INDEPENDENTE.md](REVISAO-INDEPENDENTE.md), [REVISAO-FINAL.md](REVISAO-FINAL.md) | Revisão inicial e conferência final em contextos independentes; alcance explícito |

Nenhum `.env` original, banco real, log original ou credencial é usado. As fixtures e o ambiente
de execução são descartáveis. O runtime usa arquivos de dependências com hardlinks imutáveis;
metadados e caches que podem mudar foram separados. Não publique a pasta externa inteira.

Os diretórios datados desta rodada e da auditoria têm `-text` em `.gitattributes`: o Git
preserva os bytes arquivados, incluindo finais de linha históricos. Converter esses arquivos
para LF ou CRLF invalidaria os hashes de proveniência. A conferência antes do commit compara
os blobs do índice com os arquivos locais.

## Reprodução e execução

`prepare.py` documenta a preparação Windows desta rodada e recusa um destino já existente.
Para uma nova rodada, copie os scripts para outra pasta datada e ajuste `SOURCE`, `BASE` e
`RUNTIME`; não sobrescreva estes resultados. Para repetir exatamente A/B, use os ZIP arquivados,
não a fonte atual. Confira `preparacao.json`, `projeto.json`, o lock do projeto e as versões
instaladas antes de comparar. O CLI Pest anuncia 5.0.5, enquanto Composer anuncia 5.1.1;
essa divergência de fontes permanece declarada.

1. Prepare duas cópias com os mesmos arquivos do kit e os dois tratamentos arquivados.
2. Use os quatro prompts preservados, sem catálogo ou resultado nos contextos de derivação.
3. Feche a revisão adversarial independente prevista em cada skill; preserve todos os estágios.
4. Execute `freeze.py project-71 1 identificador-aleatorio` e os equivalentes dos demais braços
   somente depois do fechamento. O script recusa revisão pendente, ID de catálogo e arquivo já congelado;
   dívida de materialização/execução pode continuar pendente e é preservada integralmente.
5. Despache cada juiz em contexto novo usando literalmente o prompt original arquivado e os
   dois arquivos da pasta anônima. Preserve o veredito bruto; confira citações e cálculos.
6. Materialize as asserções dos conjuntos sobre o contrato público, sem ler código da feature
   ou converter comportamento observado em novo oráculo. Registre o CT de origem e toda limitação.
7. Execute Pest/Chromium em série no runtime. Arquive comando, saída, exit code e JUnit.
8. `run_mutants.py` só aplica os defeitos concretos selecionados após controle verde e não vazio.
   Cada alteração afeta uma expressão e é restaurada byte a byte, mesmo se o teste falhar.
   Falha de bootstrap ou erro de sintaxe não é automaticamente mutante morto.

O runtime final usa a **referência v3**. O v1 aceitava ator nulo contra o requisito; v2 corrigiu
essa assinatura. Chromium encontrou um segundo defeito comum: Get do Filament retornava enum,
mas callbacks comparavam string. V3 corrigiu rótulo e teto percentual sem mudar os CT-B.
As primeiras falhas permanecem arquivadas. Os controles anteriores não são rebatizados como v3.

O primeiro operador exploratório de mínimo fixo negativo tinha a mesma comparação inválida:
não liberava a entrada negativa. Seus verdes não provam sobrevivência de um defeito manifestado.
O operador corrigido tem nome separado `c1-negative-fixed-input-enum` e mantém o teto/mínimo
percentual. Esse subestudo continua posterior aos vereditos, sem MSI do catálogo completo.

Comandos para uma cópia restaurada da referência v3, usando novos identificadores de saída:

```powershell
python experimentos/2026-10-09-projeto-real/verify_integrity.py --implementation-manifest experimentos/2026-10-09-projeto-real/referencia-v3/manifest.json
python experimentos/2026-10-09-projeto-real/run_mutants.py novoidentificador tests/ExperimentoReal/K7/CuponsTest.php --mutants c1-float c1-negative c1-no-increment c1-expiry-inclusive c1-limit-inclusive c1-negative-fixed-input-enum --implementation-manifest experimentos/2026-10-09-projeto-real/referencia-v3/manifest.json
python experimentos/2026-10-09-projeto-real/run_control.py novobrowser tests/BrowserTenancy/ComparacaoK7Test.php
python experimentos/2026-10-09-projeto-real/compare_verdicts.py
```

Os mapas limitam a prova: os CT-B selecionados exercitam unidade/seleção/operabilidade, mas não
gravam o cupom. O probe DOM é diagnóstico, não CT comparativo. Os materializadores receberam
ambos os conjuntos de seu cenário e viram texto comportamental no contrato público; foram
instruídos a usar esse contrato apenas como API. A exposição e o desvio inicial de perfil
PowerShell estão declarados, sem alegar cegamento técnico do materializador. A auditoria
confronta cada asserção com seu CT literal. Derivadores e juízes não receberam essa referência.

As regressões da coletânea são executadas separadamente:

```powershell
python tests/run.py --report experimentos/2026-10-09-projeto-real/regressoes-coletanea.json
python -m unittest discover -s tests -p 'test_*.py' -v
python experimentos/2026-10-09-projeto-real/check_precision.py .
```

Esta rodada não estima variância, tokens, custo financeiro, equivalência entre hosts, entrega
SMTP, nem mutation score do catálogo completo. Testes do próprio implementador validam seu
controle; somente os conjuntos e testes comparativos sustentam a avaliação antes/depois das skills.
