# Subestudo executável — seleção anterior à execução

Esta seleção complementa o pré-registro. Foi registrada depois de receber os conjuntos de cupons,
antes dos vereditos e antes de executar qualquer teste derivado. Portanto, é um subestudo exploratório,
não uma seleção independente dos resultados de derivação. Os sete operadores de `run_mutants.py`
foram escolhidos durante a derivação, antes dos julgamentos. Nenhum resultado desse subestudo será
apresentado como MSI do catálogo completo.

## Comparação executável

O mesmo materializador independente recebe os dois conjuntos anônimos de um cenário. Essa escolha
mantém tradutor, implementação e convenções de fixtures comuns. Ele não recebe identidade das
versões, catálogos, vereditos, `00`, `01`, implementação da feature ou os testes do implementador.
A exposição aos dois conjuntos é uma limitação explícita: ele deve traduzir asserções existentes
em cada conjunto, sem copiar um oráculo ausente do outro. Um mapa por CT permite auditar essa regra.

O contrato público serve exclusivamente para nomes de APIs, esquema e montagem técnica das fixtures.
As expectativas vêm do conjunto correspondente. Toda a especificação continua arquivada; somente
as famílias abaixo serão materializadas nesta execução. O inventário precisa distinguir CT não
selecionado, cenário bloqueado por pergunta, materializado integralmente e parcialmente materializado.
Linhas de Examples não executadas precisam permanecer explicitamente fora da prova.

### Cupons

- Cálculo percentual, truncamento e desconto fixo com piso zero.
- Expiração no instante exato e limite atingido, com controles de aceitação.
- Incremento e registro de aplicação, incluindo identidade do ator quando o CT exigir.
- Um CT-B de unidade/seleção de tipo, com navegação e interação reais em Chromium.

Aplicar cinco mudanças concretas: razão em float, remoção do piso zero, incremento zero,
comparação temporal inclusiva e comparação inclusiva do limite. O materializador não recebe
as expressões dos mutantes, para evitar desenhar testes em função delas.

### Aprovação de compra

- Alçada estritamente acima do limite, incluindo igualdade quando houver CT correspondente.
- Rejeição vazia e retorno ao rascunho, somente quando houver oráculo correspondente.
- Envio, ordem de aprovação e histórico nos recortes expressamente especificados.
- Notificação ao próximo aprovador, se o conjunto contiver cenário discriminante.

Aplicar duas mudanças concretas: exigir diretor na igualdade e aceitar justificativa vazia.
Ausência de CT para qualquer dessas regras é resultado da derivação; não será preenchida pelo
materializador nem transformada em teste novo com base no outro braço.

## Congelamento e execução

1. O materializador escreve os testes e o mapa CT → teste sem executar Artisan, Pest ou browser.
2. Arquivar e registrar hashes da primeira tradução antes de qualquer execução.
3. A sessão executora roda cada conjunto serialmente, preservando logs e JUnit completos.
4. Correções de namespace, montagem de tenant, autenticação, seletor ou API da biblioteca são
   permitidas com histórico da tentativa anterior. Não alterar valores esperados ou adicionar
   asserções de negócio para fazer o controle passar.
5. Falha de negócio no controle exige investigação e registro. Não é morte de mutante.
6. Mutações exigem controle verde, testes efetivamente executados e restauração byte a byte.
   Somente falha da asserção visada comprova detecção; erro de bootstrap não comprova nada.

O experimento não mede SMTP real, disputa multiprocesso, toda a UI, todas as linhas dos datasets,
todo o fluxo das cinco skills, variância entre gerações ou carregamento nativo dos perfis por host.

## Confirmação exploratória posterior aos vereditos de cupons

Depois dos dois vereditos de cupons, mas antes de executar os testes derivados, foi acrescentada
uma confirmação do recorte de criação por componente com valor fixo negativo. O materializador
continua sem acesso aos vereditos, identidades dos tratamentos ou operadores. Ele só traduz o
recorte se houver CT e valor negativo literais no conjunto correspondente; ausência no outro
conjunto permanece ausência, não cenário emprestado.

O operador adicional permite `-1` no mínimo do campo fixo, conservando o mínimo percentual.
Essa confirmação foi escolhida em função do resultado documental e deve ser reportada
separadamente dos sete operadores anteriores. Não é prova independente, não estima generalização
e não transforma as demais linhas do catálogo em defeitos executados.
