# Modelo conceitual do banco de dados

**Projeto:** PokéAnalyzer  
**Etapa:** modelo conceitual inicial  
**Notação:** Entidade-Relacionamento (ER)

## 1. Objetivo do modelo

Representar os dados necessários para manter o catálogo da Pokédex, as contas dos usuários, suas coleções e os perfis usados pelo analisador.

O modelo conceitual descreve entidades, atributos e relacionamentos. Chaves estrangeiras e tabelas associativas serão detalhadas no modelo lógico.

## 2. Entidades

### USUARIO

Representa uma conta no website.

- **id_usuario:** identificador do usuário.
- nome_usuario: nome público/identificação.
- email: endereço usado para acesso.
- senha_hash: hash da senha, nunca a senha original.
- data_cadastro: data de criação da conta.

### ESPECIE

Representa uma espécie da Pokédex Nacional.

- **numero_nacional:** número nacional da espécie.
- nome_pt: nome em português.
- nome_en: nome em inglês.
- geracao: geração de estreia.

A espécie é separada de suas formas para evitar tratar cada variação como uma espécie independente.

### FORMA

Representa uma forma ou variação catalogada de uma espécie.

- **id_forma:** identificador da forma.
- nome_forma: nome ou identificação da forma.
- categoria: classificação, como forma padrão, regional ou especial.
- altura: altura de referência.
- peso: peso de referência.
- hp_base: HP base.
- ataque_base: Ataque base.
- defesa_base: Defesa base.
- ataque_especial_base: Ataque Especial base.
- defesa_especial_base: Defesa Especial base.
- velocidade_base: Velocidade base.
- imagem_url: referência visual, quando disponível.

A forma padrão também deve ser registrada. Variações apenas cosméticas podem compartilhar os mesmos dados de batalha, evitando duplicação desnecessária.

### TIPO

Representa um tipo elemental.

- **id_tipo:** identificador do tipo.
- nome_tipo: nome do tipo.

### HABILIDADE

Representa uma habilidade existente no catálogo.

- **id_habilidade:** identificador da habilidade.
- nome: nome da habilidade.
- descricao: descrição resumida.

### NATUREZA

Representa uma das naturezas existentes nos jogos compatíveis.

- **id_natureza:** identificador da natureza.
- nome: nome da natureza.
- atributo_aumentado: atributo favorecido.
- atributo_reduzido: atributo prejudicado.

Naturezas neutras não aumentam nem reduzem atributos; nesse caso, os dois campos podem representar ausência de alteração.

### POKEMON_CAPTURADO

Representa um exemplar registrado por um usuário.

- **id_capturado:** identificador do registro.
- apelido: apelido opcional.
- nivel: nível atual.
- iv_hp, iv_ataque, iv_defesa, iv_atq_especial, iv_def_especial, iv_velocidade: valores individuais.
- ev_hp, ev_ataque, ev_defesa, ev_atq_especial, ev_def_especial, ev_velocidade: valores de esforço.

Cada registro pertence a um usuário, corresponde a uma forma, possui uma natureza e registra a habilidade selecionada.

### PERFIL_ANALISE

Representa uma configuração usada como objetivo de comparação.

- **id_perfil:** identificador do perfil.
- nome_perfil: nome do perfil.
- descricao: finalidade e estratégia.
- tipo_perfil: competitivo ou personalizado.
- iv_hp_ideal, iv_ataque_ideal, iv_defesa_ideal, iv_atq_especial_ideal, iv_def_especial_ideal, iv_velocidade_ideal: referências de IV, quando aplicáveis.
- ev_hp, ev_ataque, ev_defesa, ev_atq_especial, ev_def_especial, ev_velocidade: distribuição de EV de referência.

Um perfil competitivo é mantido pelo sistema e pode estar relacionado a um regulamento. Um perfil personalizado pertence a um usuário. A entidade também se relaciona com a forma para a qual foi criada.

### REGULAMENTO

Representa um conjunto publicado de regras competitivas.

- **id_regulamento:** identificador.
- nome: nome ou código oficial.
- jogo: título/jogo aplicável.
- formato: formato competitivo.
- temporada: temporada ou série.
- data_inicio: início de vigência, quando informado.
- data_fim: fim de vigência, quando informado.
- fonte_oficial: URL ou referência documental.
- ativo: indicador administrativo de vigência no catálogo.

## 3. Identificadores

Os atributos em negrito são os identificadores conceituais de cada entidade. No modelo lógico serão convertidos em chaves primárias.

## 4. Decisões de simplificação

- Os seis IVs e seis EVs ficam como atributos de POKEMON_CAPTURADO e PERFIL_ANALISE nesta versão didática. Uma futura versão poderia normalizá-los em uma entidade de atributo/valor, mas isso aumentaria a complexidade.
- A relação entre forma e tipo é N:N, pois uma forma pode ter um ou dois tipos e cada tipo aparece em muitas formas.
- A relação entre forma e habilidade é N:N, pois uma habilidade pode estar disponível em várias formas e uma forma pode disponibilizar várias habilidades.
- A habilidade selecionada no Pokémon capturado será uma relação separada. A regra de negócio exige que ela esteja entre as habilidades disponíveis para a forma.
- Uma análise pode ser calculada na hora e não precisa ser armazenada nesta primeira versão.
- Não haverá entidade de equipe, golpes ou itens na primeira entrega.

## 5. Regras de negócio importantes

1. Uma espécie possui uma ou mais formas catalogadas.
2. Uma forma pertence a exatamente uma espécie.
3. Uma forma possui um ou dois tipos.
4. Um Pokémon capturado pertence a exatamente um usuário.
5. Um Pokémon capturado corresponde a exatamente uma forma.
6. Um Pokémon capturado possui exatamente uma natureza e uma habilidade selecionada.
7. A habilidade selecionada deve ser compatível com a forma.
8. Um perfil de análise corresponde a uma forma.
9. Um perfil personalizado pertence a exatamente um usuário.
10. Um perfil competitivo pode estar associado a um regulamento e não pertence a um usuário.
11. Um perfil pode aceitar uma ou mais naturezas.
12. A permissão de uma forma em um regulamento deve ser registrada apenas quando houver fonte oficial verificável.
