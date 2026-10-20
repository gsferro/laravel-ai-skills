# Decisões Arquiteturais — FERRO-845

Nenhuma decisão passou nos três portões.

A leitura de configuração dentro de `PiiRedactor`, a conservação do fallback e o reaproveitamento do canal de IA são mudanças locais e reversíveis. Não justificam uma ADR. As escolhas e suas fontes estão em `Decisões de Desenho` do plano.

As dúvidas sobre configuração incompleta e inválida pertencem ao solicitante. Não se adotou política de erro ou desativação como decisão arquitetural.

## Superfície Livewire

Não aplicável nesta feature: não cria nem modifica página, widget, componente, método público de componente, propriedade hidratada ou estado de framework consumido pela UI. O redator é uma classe de backend. O chat existente apenas continua consumindo o mesmo pipeline.

Os greps de propriedades e ações Livewire não foram executados, pois não há superfície de componente em escopo. Não se apresenta uma varredura ausente como prova de segurança do chat inteiro. Se o escopo crescer para o componente, reabrir o planejamento e preencher a tabela antes de derivar seus testes.
