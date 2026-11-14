# UML de classes Python — Etapa 2

Fonte editável: [classes.puml](classes.puml). Exportações: [classes.svg](classes.svg) (vetorial, preferida para leitura/ampliação) e [classes.png](classes.png). Renderização com PlantUML 1.2025.7, usando Smetana embutido e Java 21, sem depender de Graphviz.

O diagrama contém as **15 classes existentes** em `models.py`, `dao.py` e `services.py`, seus atributos relevantes, todos os métodos exceto construtores e as dependências. `db.py` é módulo; `api.py` contém um Blueprint Flask e funções, não classes de domínio. O analisador `ComparacaoService`, CRUD de perfis e persistência de atributos agora estão implementados e representados. O diagrama não contém classes planejadas como se existissem.

As dataclasses são projeções da aplicação e não pretendem representar uma classe para cada tabela. As 26 entidades persistidas e suas cardinalidades ficam nos modelos brModelo. Chaves numéricas nas projeções representam referências SQL; as dependências de serviços/DAOs representam referências a objetos Python.

Regeneração após editar a fonte:

```sh
python docs/uml/generate_uml.py
java -Djava.awt.headless=true -jar /caminho/plantuml-1.2025.7.jar -tsvg docs/uml/classes.puml
java -Djava.awt.headless=true -jar /caminho/plantuml-1.2025.7.jar -tpng docs/uml/classes.puml
```

Obtenha o renderer na [distribuição oficial do PlantUML](https://github.com/plantuml/plantuml/releases/tag/v1.2025.7). Revise as duas exportações visualmente a 100%/com ampliação antes de registrar novos hashes:

```sh
python docs/uml/check_uml.py --record
python docs/uml/check_uml.py
```

O verificador compara inventário e métodos contra AST Python, confere atributos desenhados e dependências injetadas, verifica ausência de execução SQL nas rotas e valida hashes das exportações revisadas. Ele não substitui revisão visual nem prova todas as relações possíveis por análise estática.

Revisão visual desta entrega: caixas completas, texto sem clipping, métodos legíveis em tamanho integral, pacotes nomeados corretamente e relações separadas de rótulos. O layout foi ajustado após a primeira exportação para reduzir cruzamentos e separar a infraestrutura do modelo de dados.
