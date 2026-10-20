# Segurança — FERRO-845: Padrões de PII configuráveis

Extra condicional do step 4, conforme `estrutura-criada.md`, porque a configuração controla a redação de dados pessoais. Não é especificação de testes, relatório de QA nem autorização para endurecer o comportamento além do card.

## Fronteira da mudança

RQ-01 permite ajustar os padrões; RQ-02 a RQ-06 preservam o comportamento padrão, tipos, prioridade, marcador e fallback na ausência da configuração. A configuração pertence à instalação, não ao texto de um prompt nem a um formulário novo.

O mapa não deve ser construído a partir de entrada de navegador, retorno do modelo ou requisição arbitrária. Não há requisito para execução de callback, classe configurável, biblioteca nova ou persistência de padrões em banco.

## Preservação de proteção

Copiar literalmente os defaults atuais e usar a mesma fonte nos dois métodos evita que o prompt seja mascarado por uma política e o log descreva outra. A prioridade existente importa para sobreposições. O filtro de saída sensível tem finalidade própria; converter suas regras junto com o redator ampliaria o escopo.

A configuração ausente usa os padrões legados. Configuração presente parcial/vazia e configuração presente inválida permanecem sob Q1/Q2 no `00`. As recomendações de falha fechada são propostas ao solicitante; não foram adotadas como política sem resposta. Não assumir que mapa vazio significa desligar a proteção.

O mecanismo legado de PCRE não garante cobertura de toda PII. Não se promete eliminar falsos positivos, falsos negativos ou qualquer risco de expressão patológica pela mera extração da configuração.

## Observabilidade segura

Reutilizar o canal `ai` e os pontos definidos no PRD. A allowlist dos novos contextos limita-se à origem controlada dos padrões, operação/status, contagens e eventual código de erro seguro após definição do requisito.

Não registrar prompts, dados em claro, texto resultante, tokens, credenciais, padrões configurados ou mensagens/traces brutos de exceção. Não versionar screenshot de dados sensíveis. A preservação do warning existente do middleware não autoriza acrescentar payload ao log.

## Operação e validação futura

Alterações em configuração devem seguir o ciclo de cache/deploy existente e passar pela prova de compatibilidade. Esta nota não introduz hot reload, revisão por painel ou comando operacional novo.

Os testes serão derivados do requisito no step 7. Os casos pendentes não recebem expectativas até o Adendo. O QA deverá verificar os logs reais e a fronteira de configuração após implementação autorizada. Nenhum teste, scanner, navegação ou ataque foi executado nesta sessão.
