# Revisão e fechamento do DER

**Versão revisada:** 2.0  
**Data:** 03/11/2026

## Problemas encontrados na versão anterior

1. Estatísticas-base ficavam diretamente em FORMA, embora possam variar entre jogos.
2. Tipos e habilidades não tinham contexto de jogo.
3. Um único atributo de captura não representava captura, transferência, recrutamento e transformação.
4. A relação REGULAMENTO–FORMA não guardava condição nem fonte da decisão.
5. POKEMON_CAPTURADO não representava jogos em que Pokémon são recrutados ou transferidos.
6. O modelo pressupunha IV/EV de forma genérica.
7. Transformações de batalha não eram relacionadas à forma original.
8. O catálogo global não era separado da disponibilidade em cada jogo.

## Correções da versão 2.0

- JOGO separa títulos e edições. Scarlet e Violet permanecem como jogos distintos para registrar disponibilidade específica de cada edição.
- MECANICA_JOGO registra versões documentadas de regras.
- DADOS_FORMA_JOGO guarda estatísticas, disponibilidade e contexto.
- HABILIDADE_FORMA_JOGO registra habilidade e slot por jogo.
- POKEMON_CAPTURADO foi substituída por POKEMON_COLECAO.
- ELEGIBILIDADE_REGULAMENTO registra estado, condição, fonte e data.
- TRANSFORMACAO_FORMA liga forma de origem e destino.
- PERFIL_ANALISE aponta para um contexto específico.
- IV/EV podem ficar nulos quando não forem aplicáveis ou informados.

## Decisão sobre jogos

- Scarlet/Violet (Geração IX) é a referência principal da calculadora de IV, EV e natureza.
- Pokémon Champions é registrado como jogo de batalha separado, com seu recrutamento e treinamento por Pontos de Vitória.
- Champions não terá seus valores de treinamento convertidos automaticamente em IV/EV.
- Legends: Z-A terá contexto próprio, sem herdar automaticamente as regras de Scarlet/Violet.
- Winds e Waves não terão regras cadastradas antes do lançamento e da documentação oficial.

## Checklist do fechamento

- [x] Separar espécie e forma.
- [x] Catalogar formas sem presumir disponibilidade em todos os jogos.
- [x] Separar dados de forma por jogo/mecânica.
- [x] Separar tipos e habilidades por contexto.
- [x] Registrar método de obtenção e jogo de origem.
- [x] Representar transformações de forma.
- [x] Separar regulamento de elegibilidade.
- [x] Permitir perfil competitivo e personalizado.
- [x] Diferenciar nulo de zero.
- [ ] Desenhar o DER em ferramenta visual e conferir cardinalidades.
- [ ] Fazer revisão final visual antes de aprovar o modelo.

## Casos de teste conceituais

1. Uma forma regional possui dados diferentes da forma padrão.
2. Uma forma Mega existe no catálogo, mas não é cadastrada como captura independente quando só pode ser alcançada por transformação.
3. Um Pokémon transferido para Champions pode ser registrado sem inventar valores de IV/EV.
4. Uma espécie aparece na Pokédex, mas não é elegível em um regulamento.
5. Um perfil personalizado existe sem regulamento.
6. Um perfil competitivo específico aponta para o regulamento e as mecânicas corretos.

O DER só será considerado definitivamente fechado quando a representação visual corresponder a esta documentação e as cardinalidades forem conferidas.
