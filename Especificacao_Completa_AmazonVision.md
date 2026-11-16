# AmazonVision 4.0 — especificação completa do sistema

Este é um roteiro técnico e visual para entregar a um desenvolvedor ou usar como prompt de desenvolvimento. Define o que deve ser construído, as tecnologias selecionadas, as regras e as entregas. Não é um programa executável nem uma implementação do sistema.

## Instrução principal para quem vai desenvolver

Desenvolva o AmazonVision 4.0 conforme os requisitos deste documento. O produto final deve integrar inspeção visual de qualidade, controle de uma bancada com ESP32, rastreabilidade e uma interface profissional para apresentação em feira tecnológica. Use os critérios de aceite para demonstrar o funcionamento. Implemente por etapas, registrando o que está concluído, o que depende de dados/hardware e o que ainda não foi validado. Não declare funcionamento real de equipamentos ou desempenho da IA sem os respectivos ensaios.

O escopo confirmado é avaliar a qualidade de cada produto, com seleção de produto por lote. A proposta de implementação usa tucumã e castanha-do-pará, um item por ciclo, duas saídas físicas e funcionamento local. O objetivo visual é uma interface bonita, legível à distância e adequada ao monitor da feira. As escolhas técnicas abaixo são recomendações de arquitetura para este projeto, não tecnologias obrigatórias do PDF.

Revisão: 18 de outubro de 2026. Documento de planejamento; os módulos descritos abaixo ainda precisam ser implementados e validados na bancada.

## 1. Objetivo e situação atual

Construir um sistema que inspecione a qualidade visual externa de um produto por ciclo, decida sua classificação e coordene a separação física, apresentando o processo de forma clara e bonita na feira.

O usuário confirmou a avaliação de qualidade conforme o PDF, em lotes separados por produto. Tucumã e castanha-do-pará são a base de planejamento da primeira entrega; a composição final das amostras ainda deve ser confirmada. Separar tucumã de castanha misturados é outra aplicação e não comprova inspeção de qualidade.

Na pasta examinada existem o PDF de apresentação, o HTML da bancada 3D, o HTML de materiais e scripts ligados a essas visualizações. Não foram encontrados firmware da máquina, aplicativo de operação, dataset de imagens ou modelos treinados. Os HTMLs existentes são materiais de planejamento e apresentação; não executam o controle físico nem a inspeção.

Este levantamento usa como fonte principal `AmazonVision_4_0_Apresentacao_do_Projeto_v2.pdf`, especialmente as páginas 3–8 e 10–12. Os requisitos visuais são especificados em texto neste documento. Não é necessário usar uma prévia ou um HTML já criado como implementação do painel operacional.

## 2. Escopo proposto

| Parte | Primeira entrega funcional | Evolução posterior |
|---|---|---|
| Produtos | Dois perfis, processados em lotes separados | Caroço de açaí e outros produtos |
| Qualidade | Classes A, B e C por produto | Subtipos detalhados de defeitos |
| Fluxo | Uma peça por ciclo, com paradas para inspeção e separação | Várias peças, rastreamento e fila |
| Visão | Câmera fixa, região de inspeção e modelo por produto | Outras vistas e localização de defeitos |
| Saídas | Duas: aprovado e rejeitado | Terceira saída, se a mecânica for alterada |
| Execução | Local, com núcleo operacional sem internet | Consulta remota, se necessária |
| Interface | Operação, modo feira, histórico, coleta e diagnóstico | Copiloto com linguagem natural |
| Dados | Histórico local, imagens e exportação | Consolidação entre várias máquinas |

O PDF admite YOLO ou outras arquiteturas. Como há uma peça parada e enquadrada por vez, recomendo começar com classificação de imagem. A necessidade de localizar cada mancha ou rachadura exigiria anotações e modelos adicionais; um classificador A/B/C sozinho não fornece a localização nem a causa do defeito.

## 3. Regras de qualidade que precisam existir antes do treinamento

| Resultado | Significado operacional proposto | Destino |
|---|---|---|
| A | Dentro do padrão visual documentado | Aprovados |
| B | Defeito externo definido pela equipe | Rejeitados |
| C | Refugo visual definido, fragmento ou outra categoria explicitamente ensinada | Rejeitados |
| Inconclusivo | Imagem inválida, resultado abaixo do limiar ou caso que exige revisão | Máquina parada; revisão do operador |

A associação B → rejeitado é uma proposta para compatibilizar três classes com as duas saídas existentes. As três classes continuam separadas no banco e no painel. Inconclusivo é um estado de decisão, não uma quarta classe obrigatória do modelo. Não deve ser automaticamente registrado como C.

Para cada produto, elaborar uma ficha com fotos de referência, critérios mensuráveis quando possível, casos limítrofes e exemplos excluídos. Se duas pessoas não concordam sobre B e C, os rótulos ainda não estão prontos para treinar.

Para castanha, decidir se serão usadas amêndoas sem casca ou sementes com casca e padronizar o lote. Uma câmera voltada para a casca não comprova a condição interna. Para tucumã, definir quais variações naturais são aceitáveis e quais alterações externas contam como defeito.

Uma vista superior avalia a superfície visível, não toda a fruta. Danos escondidos na parte inferior exigem outra vista ou um mecanismo de reposicionamento. A interface deve usar “padrão visual”, sem prometer qualidade interna ou aprovação sanitária. A menção a identificação de fungos na página 6 do PDF não deve virar uma alegação do software sem estudo específico: o requisito aplicável aqui é registrar alterações externas observáveis.

Uma classe C supervisionada não detecta qualquer objeto desconhecido. O modelo pode errar com confiança alta em produtos não treinados; um limiar de confiança reduz certos erros, mas não resolve sozinho o problema de itens desconhecidos.

## 4. Arquitetura recomendada

```text
Câmera → captura de imagem → modelo de qualidade → regra A/B/C → decisão
                                  Computador                 ↕
Painel no navegador ← serviço local → banco e imagens     USB/serial
                                                            ↕
                                                          ESP32
                                                   sensores, motor, servo
```

O computador captura, classifica, registra e apresenta. O ESP32 é a autoridade sobre o estado físico e os tempos da máquina. O navegador solicita operações ao serviço local; não deve possuir sozinho a sequência ou os contadores oficiais.

Organizar o aplicativo local em captura, inferência, comunicação, coordenação, persistência e interface. Uma única instância deve ser dona da câmera e da porta serial. A análise da imagem não pode bloquear o recebimento de eventos e sinais de comunicação. Filas pequenas e tarefas separadas evitam acumular imagens antigas. Inicialmente, um processo servidor com um único worker e tarefas de trabalho controladas é suficiente.

Treinamento e operação são rotinas diferentes. O treinamento produz um modelo versionado. Na feira, o sistema apenas carrega esse modelo e faz previsões. Não haverá retreinamento automático com as próprias previsões durante a apresentação.

## 5. Tecnologias escolhidas e instalações

| Uso | Escolha recomendada | O que preparar |
|---|---|---|
| Aplicação principal | Python 3.12 | Ambiente virtual venv e dependências fixadas com pip |
| Captura e preparação das imagens | OpenCV | Testar a fonte de vídeo, resolução, atraso e reconexão |
| Treinamento e inferência | PyTorch + torchvision | Modelo pequeno, pré-processamento e pesos armazenados localmente |
| Modelo inicial | MobileNetV3 Small, via torchvision | Ajustar a saída para A/B/C e treinar com imagens próprias; avaliar ResNet18 apenas se o primeiro modelo não atender |
| Serviço local | FastAPI + Uvicorn | API de comandos, consulta e eventos em tempo real |
| Painel | HTML5, CSS3 e JavaScript com módulos ES | Interface responsiva, componentes organizados e recursos locais |
| Gráficos e ícones | Chart.js e Lucide, incluídos no pacote local | Gráficos ligados a dados reais e ícones com rótulos |
| Validação de contratos | Pydantic | Validar entradas da API, configurações e mensagens |
| Comunicação com ESP32 | pySerial | Identificação da porta, mensagens com prazo e reconexão |
| Histórico | SQLite, acessado pelo módulo sqlite3 do Python | Migrações versionadas, consultas parametrizadas e pasta separada de imagens |
| Firmware | C++ com Arduino core para ESP32 | Arduino IDE 2, versão do core e bibliotecas fixadas |
| Desenvolvimento | Git e Visual Studio Code | Histórico de alterações e versões de entrega |
| Avaliação | scikit-learn, NumPy e Matplotlib | Matriz de confusão, recall, precision, F1 e latência |
| Testes | pytest; Playwright para os fluxos principais da interface | Regras, integração, comunicação e operação no navegador |

A base proposta é Python 3.12; fixar as versões exatas das bibliotecas, inclusive o par torch/torchvision e o pacote compatível com CPU ou GPU, depois de verificar instalação e execução no computador da feira. Não usar dependências sem versão fixa na entrega. O painel pode ser servido pelo próprio FastAPI, sem necessidade de servidor Node.js em produção. Confirmar sistema operacional, modelo da GPU, memória disponível e compatibilidade do driver com o pacote PyTorch escolhido. A GPU ajuda no treinamento; a viabilidade da inferência em CPU será medida, não presumida.

Dependendo da placa, pode ser necessário um driver USB/serial específico. Um cabo USB conectado ao celular não garante que sua câmera apareça no computador: validar o modo webcam do aparelho ou o aplicativo de transmissão escolhido. Preferir uma conexão estável e ensaiada no mesmo equipamento da feira.

OpenCV oferece captura de câmeras e fluxos de vídeo; a compatibilidade concreta depende da fonte e do sistema. [Documentação oficial](https://docs.opencv.org/4.x/d8/dfe/classcv_1_1VideoCapture.html).

PyTorch documenta o ajuste de modelos pré-treinados e torchvision fornece arquiteturas e transformações associadas aos pesos. Essas ferramentas sustentam a proposta de transferência de aprendizado; o desempenho deste projeto dependerá dos seus dados. [Transfer learning](https://docs.pytorch.org/tutorials/beginner/transfer_learning_tutorial.html), [modelos torchvision](https://docs.pytorch.org/vision/stable/models.html).

FastAPI oferece WebSockets para atualizações da interface. A porta serial precisa de leituras com timeout para não ficar esperando indefinidamente. [FastAPI](https://fastapi.tiangolo.com/advanced/websockets/), [pySerial](https://pyserial.readthedocs.io/en/latest/shortintro.html).

SQLite é adequado ao armazenamento local de um aplicativo. O firmware pode usar recursos PWM do ESP32; motor e servo precisam de configuração compatível com seus requisitos, inclusive os temporizadores compartilhados. [SQLite](https://www.sqlite.org/whentouse.html), [Espressif LEDC](https://docs.espressif.com/projects/arduino-esp32/en/latest/api/ledc.html).

## 6. Captura, dataset e rotulagem

### Ferramenta de coleta a desenvolver

- Selecionar produto, lote de coleta, identificador da amostra física e classe.
- Visualizar a mesma região que será usada na inspeção.
- Capturar imagem original e recorte, com identificação automática.
- Registrar data, sessão, câmera, iluminação/configuração e autor do rótulo.
- Revisar, corrigir rótulos e marcar imagens ambíguas ou inutilizáveis.
- Exportar um manifesto que relacione arquivo, produto, amostra, classe e partição.

Coletar na bancada real, com o fundo e a iluminação previstos. Variar amostras físicas, posição e orientação, mantendo os defeitos visíveis na imagem rotulada. Não usar fotos com mãos, etiquetas ou fundos exclusivos de uma classe que permitam ao modelo aprender pistas erradas. Amostras que se alterarem entre dias devem ser reavaliadas.

Como orçamento inicial de coleta, planejar 300–500 imagens úteis por produto/classe: seis combinações resultam em aproximadamente 1.800–3.000 imagens. É uma estimativa de trabalho, não um mínimo universal nem garantia de acerto. Começar com uma coleta menor para verificar enquadramento e separabilidade das classes. Priorizar dezenas de amostras físicas diferentes por grupo, quando disponíveis, em vez de milhares de frames quase iguais da mesma peça. Ajustar a coleta conforme os erros de validação.

Separar aproximadamente 70% para treino, 15% para validação e 15% para teste por identidade da amostra física, preservando diversidade de lotes e sessões. Todas as fotos da mesma amostra ficam na mesma partição. Reservar também uma sessão de teste independente quando possível. Transformações artificiais são aplicadas apenas ao treino, depois da separação; mudanças de cor não podem apagar o próprio sinal de qualidade que será aprendido.

O agrupamento evita que imagens correlacionadas da mesma amostra apareçam tanto no treino quanto no teste. [Referência sobre avaliação por grupos](https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation-iterators-for-grouped-data).

### Entregáveis de dados

1. Manual de rotulagem dos dois produtos.
2. Fotografias originais e recortes, com identificação.
3. Manifesto de amostras, classes e divisões.
4. Registro de revisão e exclusão de imagens.
5. Conjunto de teste preservado, sem uso na escolha dos modelos.

## 7. Treinamento e avaliação da IA

Criar uma rotina reproduzível para carregar os dados, preparar as imagens, ajustar o classificador, validar e salvar o melhor modelo segundo um critério definido. Comparar um ou dois modelos pequenos, em vez de testar muitas arquiteturas sem necessidade.

Para cada produto, guardar pesos, ordem das classes, resolução, normalização, política de recorte, versão do dataset, parâmetros de treinamento, resultados e identificador da versão. Pré-processamento em operação deve coincidir com o validado. Evitar recortes automáticos que excluam bordas do produto e seus defeitos.

A avaliação deve informar:

- Matriz de confusão A/B/C e quantidade de amostras de cada classe.
- Precision, recall e F1 por classe, além de uma média entre classes.
- Quantos B/C foram incorretamente aprovados como A.
- Quantos A foram indevidamente rejeitados.
- Taxa de revisão manual e taxa de decisões automáticas.
- Tempo de captura, inferência e ciclo completo, incluindo o percentil 95.
- Resultados separados para tucumã e castanha.

Definir o limiar de aceitação na validação e congelá-lo antes do teste final. O valor “96%” produzido pelo modelo é um escore, não prova de 96% de acerto nem de qualidade do alimento. Na tela, identificar como confiança estimada do modelo. A métrica mAP citada no PDF só será relevante se houver uma tarefa de detecção/localização; não é necessária para o classificador proposto.

Se o modelo só aprende A/B/C, não exibir diagnósticos específicos como “rachadura”, “fungo” ou “deformação” como se tivessem sido detectados. Esses motivos exigem rótulos e avaliação próprios. Explicações visuais de atenção, se adotadas, também não equivalem a detecção validada do defeito.

## 8. Sequência da máquina e firmware

| Estado | Comportamento esperado | Condição para avançar |
|---|---|---|
| Inicialização | Motor sem acionamento; verificar comunicação e configurações | Verificações concluídas e liberação do operador |
| Pronto | Aguardar solicitação de ciclo e inserção de uma peça | Lote ativo e ciclo autorizado |
| Transporte para S1 | Levar a peça ao ponto de inspeção | S1 válido, dentro do prazo |
| Estabilização | Parar a esteira e aguardar estabilização da imagem | Tempo calibrado e captura nova disponível |
| Inspeção | Computador analisa; ESP32 mantém transporte parado | Decisão válida para aquele ciclo |
| Transporte para S2 | Memorizar destino e movimentar | S2 válido, dentro do prazo |
| Separação | Parar e executar rejeição, ou liberar passagem de aprovado | Sequência e tempos previstos concluídos |
| Liberação | Verificar sensores livres e tempo de saída | Ciclo encerrado e área livre |
| Revisão / falha | Parar transporte e informar o motivo | Intervenção e rearme explícitos |

A alimentação inicial até S1 precisa ser prevista no programa, mesmo que o operador coloque o produto bem perto do sensor. Também é necessário calibrar a inércia: desligar o motor não garante que o produto pare instantaneamente sob a câmera.

O firmware deverá implementar leitura estável de S1/S2, detecção de transições sem duplicar peças, limite de duração de movimentos, comando do motor conforme o controlador comprado, posições e tempos do servo, sinais de status e tratamento de comunicação perdida. Evitar esperas longas que impeçam a verificação de falhas.

Não presumir que a esteira comprada admite PWM, reversão ou controle de velocidade. Confirmar a interface real: habilitação liga/desliga, driver DC ou outra entrada. Essa definição muda o módulo de acionamento do firmware.

Com os dois sensores existentes, é possível observar presença nos pontos S1/S2 e executar uma sequência. Sem sensor na saída ou realimentação do servo, não é possível afirmar eletronicamente que a peça caiu no recipiente correto ou que o servo atingiu a posição. Registrar “sequência concluída” e “destino comandado”; validar a separação por observação nos ensaios. Se for exigida confirmação física automática, será necessário acrescentar essa medição.

O botão da tela é uma parada por software. O botão físico de emergência e o circuito de interrupção devem atuar independentemente do navegador e da IA. Na volta de energia ou comunicação, não reiniciar movimento nem recolher automaticamente o servo: interromper o ciclo anterior, reconciliar o estado e exigir rearme.

## 9. Protocolo USB/serial e coordenação

Definir um contrato simples, por exemplo mensagens JSON terminadas por quebra de linha, com tamanho máximo, versão e prazo. 115200 baud pode ser o ponto inicial de teste; não enviar imagens pela serial do ESP32.

Cada mensagem de operação deve vincular versão do protocolo, sessão de conexão, identificação de inicialização do ESP32, lote, ciclo e comando. Isso evita que uma decisão atrasada de uma peça anterior mova a peça atual.

| Grupo | Mensagens previstas |
|---|---|
| Identificação | Apresentação, versão, configuração e leitura do estado |
| Operação | Preparar lote, iniciar, pausar, parar, enviar decisão e rearmar |
| Eventos | S1, S2, captura solicitada, decisão aceita, ciclo concluído e falha |
| Comunicação | Confirmação de recebimento, rejeição de comando e sinal periódico de atividade |
| Manutenção | Testar sensor ou atuador, somente em modo de manutenção |

Confirmar recebimento não significa movimento concluído. São eventos diferentes. Comandos repetidos com o mesmo identificador devem retornar seu estado sem repetir o movimento; comandos fora do estado permitido devem ser recusados. Duplicatas de eventos não podem incrementar os contadores novamente.

Definir prazos de decisão, comunicação, chegada a S1/S2 e liberação. Os valores serão calibrados na bancada; não assumir uma velocidade fixa antes de comprar/testar a esteira. Ao perder comunicação, o ESP32 interrompe o transporte conforme o comportamento de falha definido. Ao reconectar, o computador consulta o estado real e marca ciclos interrompidos, sem reproduzir automaticamente ordens pendentes.

Somente um operador controla a sessão por vez. Atualizar a página não reinicia o lote nem reenvia movimentos. Uma tela de apresentação adicional recebe dados em modo de leitura. Se a tela do operador perder contato, a política proposta é concluir apenas o ciclo já autorizado, se todas as demais condições estiverem normais, e pausar antes do próximo; perda do serviço de controle provoca a parada de comunicação.

## 10. Banco, histórico e rastreabilidade

Separar pelo menos estas entidades conceituais:

- Perfis de produto: classes, modelo, limites e parâmetros calibrados.
- Versões de modelo: pesos, dataset, métricas e pré-processamento.
- Lotes/sessões: produto, início, fim, operador e configurações congeladas.
- Ciclos: identificador único, estado, horários e resultado de execução.
- Inspeções: imagem, resultado A/B/C, escore, decisão e eventual revisão humana.
- Eventos: sensores, comandos, confirmações, desconexões e falhas.

Armazenar a previsão original separadamente da decisão corrigida pelo operador. Guardar o caminho da imagem e sua identificação de integridade; nunca sobrescrever uma imagem de outro ciclo. Relacionar cada inspeção à versão exata do modelo e da regra de decisão.

Os contadores devem distinguir inspecionados, decisões aprovadas/rejeitadas, inconclusivos, ciclos executados e ciclos interrompidos. A porcentagem de aprovação visual deve declarar o denominador e tratar lote vazio sem divisão por zero. Totais vêm dos registros, não de incrementos independentes no navegador.

Exportar CSV de inspeções e resumo por lote, com filtros por produto, período e classe. O relatório da feira pode ser impresso pelo navegador. Registrar horários de forma consistente e exibir no fuso America/Manaus; durações devem usar relógio apropriado para medir intervalos.

Definir retenção de imagens, limite de espaço, limpeza controlada e backup com possibilidade de restauração. Como a pasta do projeto está no OneDrive, é preferível que o banco em uso fique em uma pasta local de dados do aplicativo, com backup consistente para sincronização; não depender de sincronização de um banco aberto. Uma falha de gravação deve aparecer e impedir o início de novos ciclos que precisem de rastreabilidade.

## 11. Interface e identidade visual da feira

O painel faz parte da entrega principal. Deve permitir que um visitante entenda rapidamente qual produto está sendo examinado, o resultado da análise e como a máquina age.

### Direção visual

Identidade AmazonVision: verde profundo, superfícies claras, detalhes em verde vivo e tipografia sem serifa. Usar espaçamento amplo, poucos elementos por área e hierarquia de tamanho. Fotografias e resultado devem receber mais destaque que detalhes técnicos. Textos em português, ícones acompanhados de rótulos e números alinhados.

Aprovado usa verde, defeito usa âmbar, refugo/falha usa vermelho, e revisão usa uma identificação própria. Sempre acompanhar cores com texto. Diferenciar um produto rejeitado de uma falha da máquina: rejeição é um resultado normal do processo.

Em modo feira, prever resultado principal de aproximadamente 40–64 px e indicadores com 32–48 px em uma tela Full HD; os tamanhos finais dependem do monitor, da distância e da resolução. Testar presencialmente a leitura a dois ou três metros. Não usar animações que dificultem ler o resultado. Respeitar redução de movimento.

### Telas necessárias

| Tela | Conteúdo e ações |
|---|---|
| Operação | Produto/lote, imagem atual, resultado, confiança, estado da máquina, iniciar/pausar/parar |
| Modo feira | Câmera e classificação ampliadas, totais, fluxo do ciclo e identificação do projeto |
| Histórico | Inspeções reais com foto, classe, decisão, horário, versão e exportação |
| Coleta de imagens | Identificação da amostra, captura, rotulagem e revisão |
| Configuração | Perfil do produto, câmera, região de inspeção e parâmetros validados |
| Diagnóstico | Sensores, comunicação, modelo carregado, eventos e testes manuais controlados |

O modo feira deve esconder edição e manutenção. A troca de produto só será permitida com a máquina parada e sem ciclo ativo. Alterar o seletor deve carregar e verificar o modelo correspondente, sem apenas mudar o título da tela.

### Composição da tela principal

1. Cabeçalho com marca, produto selecionado, lote e acesso ao modo feira.
2. Área maior com imagem de inspeção, identificação da peça e momento da captura.
3. Cartão de resultado: A/B/C, descrição curta, confiança estimada e destino comandado.
4. Indicadores do lote: analisados, aprovados, rejeitados e revisões.
5. Faixa do ciclo: captura, análise, decisão, separação e registro.
6. Histórico recente com miniaturas ou linhas compactas.
7. Estado de conexão e ações do operador, sem competir com a imagem.

Se houver vídeo ao vivo e fotografia analisada, deixar explícito qual é qual. Após a passagem da peça, mostrar a fotografia associada ao resultado, não um frame novo com rótulo antigo. Não desenhar uma caixa de defeito se o modelo só classifica a imagem inteira; o contorno de enquadramento pode indicar apenas a região de inspeção.

### Estados visuais que precisam ser desenhados

- Inicializando e verificando equipamentos.
- Pronto, aguardando produto.
- Capturando, analisando e separando.
- Aprovado, defeito, refugo e inconclusivo.
- Pausado e ciclo interrompido.
- Câmera ausente, frame antigo, modelo indisponível e ESP32 desconectado.
- Histórico vazio, carregando e falha de gravação.

Exibir dados antigos como “última informação recebida”, nunca como status atual conectado. Nenhum gráfico ou total deve ser fabricado para preencher a tela operacional. O sistema real começa vazio e mostra apenas eventos medidos. Dados de ensaio, se necessários ao desenvolvimento, devem ficar em ambiente identificado e separado dos registros de operação.

Desenvolver para Full HD, notebook de 1366 × 768 e dispositivos móveis. O celular pode acompanhar a apresentação em modo de leitura se esse acesso for implementado; não presumir controle remoto habilitado. Gráficos e tabelas devem continuar compreensíveis com teclado e sem depender somente de cores. Evitar bibliotecas, fontes ou imagens carregadas da internet no dia da feira.

## 12. Recursos adicionais previstos no PDF

### Detecção de anomalias

É uma evolução separada do classificador A/B/C. Exige dataset de normalidade, validação com situações distintas e limiar próprio. Guardar escore de anomalia separado da confiança do classificador e definir como combinar os resultados. Só habilitar após validar sua contribuição; não anunciar que qualquer objeto desconhecido será reconhecido.

### Copiloto industrial

Pode responder perguntas sobre quantidades, classes e períodos usando consultas limitadas aos dados reais. Ele deve indicar o período consultado, não inventar causas e informar quando não houver dados. Se o banco só registra B, ele não pode dizer que o defeito mais comum foi “rachadura”.

O copiloto será de consulta, sem autorização para acionar motor, servo, alterar regras ou executar comandos livres. Se usar serviço externo, prever conexão, credencial e eventual custo; se usar modelo local, medir consumo de recursos em paralelo à visão. Falha do copiloto não pode bloquear o ciclo de inspeção. Para a primeira feira, é uma prioridade posterior ao funcionamento integral da máquina.

## 13. Testes e critérios de aceite

| Verificação | Evidência exigida |
|---|---|
| Câmera | Captura atual, enquadramento correto e identificação de frame inválido/desconectado |
| Modelo | Métricas em amostras físicas não usadas no treino; resultados por produto e classe |
| Produto/perfil | Troca apenas em repouso; versão do modelo e parâmetros corretos |
| Serial | Mensagem fragmentada, inválida, atrasada e repetida não causa movimento indevido |
| Sensores | Pulsos repetidos não duplicam ciclos; ausência de S2 provoca falha por prazo |
| Separação | Observação do destino físico em sequência de ensaios; falhas registradas |
| Reinício | Volta sem movimento automático e sem reaplicar decisão antiga |
| Conexão | Remover USB/câmera e fechar serviço produz o comportamento previsto |
| Interface | Atualizar/abrir segunda tela não duplica comandos ou contagens |
| Histórico | Totais conferem com ciclos; imagem e modelo correspondem à inspeção |
| Espaço em disco | Falha de gravação fica visível e novos ciclos são bloqueados |
| Offline | Inicializar e completar lotes sem acesso à internet |
| Visual | Leitura no monitor da feira; Full HD, notebook e celular sem conteúdo cortado |
| Recuperação | Restaurar backup e repetir o procedimento de inicialização documentado |

Proposta de ensaio final: ao menos 100 ciclos distribuídos entre produtos/classes e uma sessão contínua de uma hora, incluindo os cenários de falha. Isso é uma meta de verificação do protótipo, não certificação industrial nem prova estatística de generalização. Repetir a mesma amostra ajuda a testar mecânica, mas não aumenta o número de exemplares independentes na avaliação de IA.

Como ponto inicial de discussão, buscar encaminhamento automático correto para rejeição de pelo menos 90% dos itens reais B/C e falsa aprovação de no máximo 5% desses itens, no conjunto independente. O denominador de ambos é o total de itens realmente B/C; revisões contam à parte e não são tratadas como acerto automático. Reportar também precision/recall/F1 por classe, cobertura automática e rejeição indevida de itens A. Esses números são metas propostas, não resultados obtidos. Antes do teste final, fixar os critérios de acordo com as amostras disponíveis e o objetivo da apresentação. Não ajustar limites olhando o teste reservado.

Avaliar separadamente: acerto da IA, execução da sequência e destino físico observado. Uma classificação correta com servo travado não é um ciclo bem-sucedido de separação.

## 14. Ordem de desenvolvimento e entregas

| Etapa | Trabalho | Condição para encerrar |
|---|---|---|
| 1. Definições | Classes, amostras, duas saídas, interface da esteira e critérios de aceite | Ficha de escopo e exemplos aprovados pela equipe |
| 2. Experiência visual | Projeto das telas, identidade, modo feira e estados de falha | Layout documentado e conferido no monitor previsto |
| 3. Aquisição e dados | Conectar câmera, ferramenta de coleta e rotulagem | Imagens reais organizadas e enquadramento validado |
| 4. Firmware e comunicação | Sensores, atuadores, estados e protocolo | Ciclo físico controlado e falhas testadas |
| 5. IA inicial | Treino, validação e escolha do modelo | Relatório por classe e versão reproduzível |
| 6. Integração | Ligar captura → inferência → ESP32 → registro | Uma peça completa o ciclo real com rastreabilidade |
| 7. Operação completa | Dois produtos, histórico, calibração e modo feira | Troca de lotes e uso pela equipe |
| 8. Estabilização | Testes longos, offline, reinício, backup e documentação | Checklist final executado |
| 9. Extensões | Copiloto e anomalias, conforme tempo disponível | Valor demonstrado sem prejudicar o núcleo |

Visual e coleta podem avançar enquanto a eletrônica é montada. A escolha final de câmera, iluminação e posição precisa acontecer cedo para não invalidar o dataset. A integração com a esteira não deve ser deixada para o último dia.

Não há prazo de feira, disponibilidade da equipe ou experiência informados suficientes para um cronograma confiável em dias. Planejar por essas entregas e reservar uma etapa específica de integração e ensaio; escrever a interface e obter uma IA confiável têm dependências e ritmos diferentes.

### Pacote final a entregar

- Código do aplicativo e interface.
- Firmware, configuração da placa e instruções para gravação.
- Protocolo serial documentado.
- Ferramenta de coleta e manual de rotulagem.
- Dataset organizado e manifesto das partições.
- Rotina de treinamento e avaliação reproduzível.
- Dois modelos de qualidade, metadados e relatórios de teste.
- Banco inicial, exportação e procedimento de backup/restauração.
- Configurações calibradas da bancada e exemplo sem credenciais.
- Inicializador do sistema e verificação de câmera, placa e modelo.
- Manual rápido do operador e roteiro de demonstração.
- Registro de versões das dependências e licença dos componentes distribuídos.
- Evidências dos testes e lista explícita de limitações.

## 15. Decisões pendentes que afetam implementação

1. Confirmar tucumã e castanha como os dois produtos definitivos.
2. Definir castanha com ou sem casca e critérios visuais A/B/C de ambos.
3. Confirmar a proposta de encaminhar B e C à mesma saída.
4. Saber qual esteira será comprada e qual entrada de controle oferece.
5. Identificar câmera/celular, forma de transmissão e computador de execução.
6. Confirmar posição dos sensores, comportamento de parada e geometria da pá.
7. Escolher monitor/resolução para testar a legibilidade presencialmente.
8. Informar prazo, equipe e amostras disponíveis para fechar o cronograma.

Essas pendências não impedem desenhar a interface, especificar o protocolo ou preparar a coleta. Elas precisam ser resolvidas antes de congelar o dataset, os tempos de movimento e a versão final.

## 16. Referências

As características e funções originais vêm do PDF local de apresentação. A escolha de avaliar qualidade foi confirmada pelo usuário. Arquitetura detalhada, tecnologias, políticas de falha, quantitativos de coleta, critérios de teste e direção visual são propostas deste levantamento.

- [Documento original](./AmazonVision_4_0_Apresentacao_do_Projeto_v2.pdf), páginas 3–8 e 10–12.
- [OpenCV: captura](https://docs.opencv.org/4.x/d8/dfe/classcv_1_1VideoCapture.html).
- [PyTorch: transferência de aprendizado](https://docs.pytorch.org/tutorials/beginner/transfer_learning_tutorial.html).
- [Torchvision: modelos e transformações](https://docs.pytorch.org/vision/stable/models.html).
- [FastAPI: WebSockets](https://fastapi.tiangolo.com/advanced/websockets/).
- [pySerial: comunicação serial e timeouts](https://pyserial.readthedocs.io/en/latest/shortintro.html).
- [SQLite: usos apropriados](https://www.sqlite.org/whentouse.html).
- [Espressif: PWM/LEDC](https://docs.espressif.com/projects/arduino-esp32/en/latest/api/ledc.html).
- [scikit-learn: separação por grupos](https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation-iterators-for-grouped-data).

## 17. Estrutura do software e responsabilidades

A implementação deve ser modular, sem colocar toda a lógica em um arquivo. A estrutura abaixo é uma organização proposta, e os nomes podem ser adaptados sem perder as responsabilidades.

| Módulo | Responsabilidade | Regra importante |
|---|---|---|
| Inicialização | Carregar configuração, abrir banco, verificar modelos e dispositivos | Não autorizar movimento automaticamente |
| Câmera | Conectar, manter captura, validar frames e produzir recortes | Só uma instância possui a câmera |
| Inferência | Carregar o modelo, preparar imagem e prever A/B/C | Retornar resultado vinculado à imagem e ao ciclo |
| Política de qualidade | Aplicar limiares e associar classe a destino | Separar previsão de decisão operacional |
| Serial | Abrir porta, validar mensagens, confirmar comandos e reconectar | Não executar decisões antigas após reconexão |
| Coordenação | Organizar lote, ciclo, registros e resposta ao operador | Respeitar o estado físico informado pelo ESP32 |
| Persistência | Guardar eventos, inspeções, imagens e configurações | Evitar duplicatas e preservar previsão original |
| API | Receber solicitações e publicar o estado atual | Validar estado, permissão operacional e parâmetros |
| Interface | Exibir informações e solicitar ações | Não comandar GPIO diretamente nem contar ciclos sozinha |
| Coleta | Capturar e revisar amostras rotuladas | Manter dados de treinamento separados do histórico operacional |
| Treinamento | Produzir e avaliar modelos versionados | Executar fora do ciclo de produção |
| Firmware | Ler sensores e controlar a sequência física | Manter limites de tempo e comportamento de falha locais |

Organização sugerida:

```text
amazonvision/
  app/                 serviço, coordenação e API
  app/camera/          aquisição e preparação das imagens
  app/inference/       carregamento e execução dos modelos
  app/machine/         protocolo e coordenação dos ciclos
  app/storage/         persistência e migrações
  web/                 telas, estilos, módulos JS e recursos locais
  firmware/            programa do ESP32 e configuração da placa
  training/            rotulagem, partições, treinamento e avaliação
  configs/             exemplos e definições dos perfis
  tests/               regras e integrações verificáveis
  docs/                instalação, protocolo, calibração e operação
  scripts/             inicialização, backup e verificação do ambiente
```

Datasets, pesos, banco ativo, imagens e logs ficam em diretórios de dados configuráveis. Não adicionar automaticamente imagens e pesos grandes ao Git. A entrega deve incluir um manifesto das versões e dos arquivos necessários para funcionar offline.

## 18. Contratos da API e comunicação com a interface

O painel e o serviço deverão rodar no mesmo computador, no mesmo endereço de aplicação. Usar HTTP para consultas e solicitações, e WebSocket para eventos de status. O navegador nunca deve enviar código executável, SQL livre ou comandos arbitrários para o ESP32.

### Rotas funcionais propostas

| Método e rota | Finalidade |
|---|---|
| GET /api/health | Verificar se o serviço está ativo |
| GET /api/status | Consultar estado atual, equipamentos, lote e ciclo |
| GET /api/products | Listar perfis de produto disponíveis |
| GET /api/models | Listar modelos, versões e situação de validação |
| GET /api/camera/preview | Obter visualização da câmera, identificando atualização e estado |
| POST /api/lots | Criar lote com produto e perfil definidos |
| GET /api/lots | Consultar lotes anteriores |
| GET /api/lots/{id}/summary | Consultar contadores e resultados do lote |
| POST /api/lots/{id}/close | Encerrar lote sem apagar histórico |
| POST /api/machine/start | Autorizar operação após verificações |
| POST /api/machine/pause | Solicitar pausa conforme a política do ciclo |
| POST /api/machine/stop | Solicitar parada por software |
| POST /api/machine/rearm | Rearmar após resolução de falha, sem movimentar automaticamente |
| GET /api/inspections | Listar inspeções com filtros e paginação |
| GET /api/inspections/{id} | Consultar imagem, previsão, decisão e eventos |
| POST /api/inspections/{id}/review | Registrar revisão humana e motivo |
| GET /api/exports/inspections.csv | Exportar resultados filtrados |
| POST /api/dataset/capture | Capturar amostra para o dataset |
| PATCH /api/dataset/samples/{id}/label | Revisar rótulo da amostra |
| GET /api/config | Consultar parâmetros disponíveis |
| PUT /api/config | Validar e salvar configuração, quando o estado permitir |
| GET /api/diagnostics/events | Consultar eventos e falhas |
| WS /api/events | Receber alterações de estado e resultados |

As rotas são um contrato proposto, não endpoints já existentes. Definir esquemas de entrada e saída para cada uma. Solicitações de movimento precisam de identificador único e estado esperado. Consultas grandes devem ser paginadas. A transmissão de vídeo não deve ocupar o mesmo canal das mensagens críticas de estado.

Publicar eventos como STATE_CHANGED, SENSOR_CHANGED, INSPECTION_READY, DECISION_ACCEPTED, CYCLE_COMPLETED, CONNECTION_LOST e FAULT. Todo evento relevante contém sequência, instante, lote/ciclo quando aplicável e versão do estado. Após uma reconexão, enviar um retrato completo do estado atual antes de voltar aos eventos incrementais.

Padronizar erros com código, mensagem legível, indicação de recuperação e identificador de rastreamento. Exemplos: CAMERA_UNAVAILABLE, STALE_FRAME, MODEL_NOT_READY, SERIAL_DISCONNECTED, INVALID_STATE, SENSOR_TIMEOUT, STORAGE_ERROR e REVIEW_REQUIRED. Mensagens para o operador devem explicar a ação necessária sem expor uma pilha de erros de programação.

Por padrão, disponibilizar o serviço apenas no próprio computador. Se a apresentação precisar de outro aparelho na rede, habilitar uma sessão de leitura e proteger as rotas de controle. A interface deve ter um único operador ativo; visitantes acompanham dados sem mudar configurações. Credenciais futuras, se houver, ficam fora do código e do navegador.

## 19. Dicionário mínimo de dados

Esta seção define informação a armazenar. Não é uma migração de banco já executada.

| Registro | Campos mínimos |
|---|---|
| Perfil do produto | id, nome, apresentação com/sem casca quando aplicável, classes, modelo ativo, parâmetros da imagem, regras de decisão, versão |
| Modelo | id, produto, arquitetura, caminho e hash dos pesos, ordem das classes, pré-processamento, versão do dataset, data e métricas de validação |
| Lote | id, produto, operador, início, fim, status, versão do modelo e cópia da configuração usada |
| Ciclo | id, lote, sessão/boot do ESP32, estado, início, fim, destino comandado, situação da execução e motivo de interrupção |
| Inspeção | id, ciclo, imagem, instante da captura, previsão A/B/C, escores, latência, decisão automática e revisão quando houver |
| Revisão | id, inspeção, responsável, decisão anterior, nova decisão, justificativa e horário |
| Evento | id, origem, sequência, ciclo, tipo, horário, dados e gravidade |
| Amostra de dataset | id, produto, amostra física, sessão de coleta, caminho, rótulo, autor, revisão, partição e versão |

Usar chaves únicas para não registrar o mesmo evento/ciclo duas vezes. Ativar integridade referencial, usar transações e consultas parametrizadas. Serializar gravações e manter transações curtas. Migrações precisam ter versão, preservar dados e ser verificadas em uma cópia antes de atualizar o banco da feira.

Uma revisão manual deve acrescentar um registro de auditoria; não apagar a previsão original. Uma inferência que foi produzida, mas cujo ciclo foi abortado, continua no histórico com esse estado. Não apresentar execução abortada como separação confirmada.

A gravação de imagem e banco precisa tolerar interrupção: salvar arquivo de forma controlada, relacioná-lo ao registro somente quando disponível e reconciliar pendências no próximo início. Um CSV deve preservar acentos, indicar unidades e período, e tratar campos textuais de modo que não sejam interpretados como fórmulas ao abrir em uma planilha.

## 20. Contrato do firmware e parâmetros a calibrar

O protocolo serial deve informar pelo menos:

- protocol_version: versão do contrato.
- boot_id: identificação da inicialização atual do ESP32.
- session_id: conexão operacional negociada com o serviço.
- message_id e command_id: identificação e deduplicação.
- lot_id e cycle_id: vínculo com a peça atual, quando aplicável.
- type: comando, confirmação, evento ou falha.
- state: estado atual do controlador.
- payload: parâmetros validados para aquele tipo.

O fluxo de identificação e negociação precede qualquer autorização de movimento. Para os comandos com efeitos físicos, confirmar recebimento e publicar conclusão separadamente. Ao receber novamente um command_id já processado, responder com a situação conhecida em vez de executar outra vez. Após reinício, uma nova boot_id invalida a sessão anterior; decisões daquela sessão não podem ser reaplicadas.

Calibrar e documentar por perfil: polaridade dos sensores, filtragem de leitura, tempo máximo até S1, estabilização da peça, prazo da análise, tempo máximo até S2, tempo de passagem à saída, posição recolhida do servo, posição de desvio, duração da ação e retorno, prazo de comunicação e limites da interface do motor. A troca de parâmetros físicos só deve ocorrer com máquina parada, sem ciclo ativo.

A configuração de servo deve respeitar os limites reais do conjunto mecânico; um nome comercial “180°” não é motivo para enviar cegamente o máximo de curso. Não configurar velocidades ou tempos como se tivessem sido medidos quando ainda não foram.

A parada de emergência deve prevalecer sobre estados automáticos e manuais. O software pode registrar seu sinal quando houver entrada dedicada ou derivada apropriada; não pode afirmar que o botão está liberado se essa informação não estiver disponível. Status de motor e servo sem realimentação devem ser descritos como comando/estado de controle, não posição/velocidade medida.

## 21. Especificação visual executável como briefing

### Identidade e estilo

Criar um painel de inspeção contemporâneo, com aparência de produto pronto para apresentação pública. Usar a marca AmazonVision 4.0 de forma consistente. O visual deve ser limpo, com poucos gráficos, boa separação entre seções e destaque para fotografia e resultado.

Paleta de referência: verde profundo #102B22, verde principal #197C50, fundo #F4F6F2, superfícies #FFFFFF, texto #172C23, texto secundário #617168 e bordas #DFE6DE. Usar âmbar para classe B, vermelho para classe C/falha, sempre distinguindo os significados com rótulos. Verificar contraste na implementação. Usar Segoe UI ou equivalente do sistema para não depender de baixar fontes.

No desktop, navegação lateral para Operação, Histórico, Modelos, Coleta, Configuração e Diagnóstico. Usar espaçamentos consistentes em múltiplos de 4 ou 8 px, cantos discretamente arredondados e sombras leves somente quando ajudarem a separar superfícies. No celular, reorganizar a navegação e empilhar os blocos. Evitar texto cortado, botões sem rótulo e tabelas que obriguem a rolar a página inteira para os lados.

### Distribuição da operação

```text
Marca | Produto/lote | Estado da estação | Acesso ao modo feira
Totais do lote: inspecionados | aprovados | rejeitados | revisões
Imagem da inspeção, grande    | Classe, confiança e decisão
Etapa atual: captura → análise → decisão → separação → registro
Últimas inspeções             | Câmera, ESP32, modelo e avisos
Ações do operador: iniciar, pausar, parar e encerrar lote
```

Rejeição é um resultado do processo, não deve deixar toda a aplicação com aspecto de falha. Um aviso de perda de câmera precisa ser visualmente diferente de um produto classe C. Exibir “aguardando dados” onde ainda não existe informação.

A imagem usada para a análise deve permanecer associada ao resultado visível. Se houver vídeo ao vivo em paralelo, identificá-lo separadamente. O campo “produto” indica o perfil escolhido pelo operador; não sugerir reconhecimento automático da espécie quando esse recurso não existir.

### Modo feira

Acessível por um botão claro e reversível. Ocultar navegação e parâmetros de manutenção, aumentar fotografia e classificação, manter totais e o fluxo do ciclo. Exibir nome do projeto e vínculo com a feira. Acesso somente de leitura para a tela do público. Tela cheia do navegador pode ser solicitada mediante ação do usuário; a apresentação deve funcionar também sem essa permissão.

Em 1920 × 1080, a composição principal deve caber sem rolagem vertical, ressalvado zoom de acessibilidade. Preservar tamanho de leitura em monitor distante, com título do resultado em torno de 40–64 px. No notebook, adaptar altura e espaçamento mantendo a ação de parada acessível ao operador. No celular, manter a leitura e evitar controles apertados.

### Gráficos e animações

Usar Chart.js para distribuição de classes por lote e, somente quando houver volume de dados suficiente, evolução de aprovação ao longo do tempo. Indicar eixos, período, unidades e quantidade de itens. Não preencher intervalos sem dados como se fossem medições. Disponibilizar os valores também em texto/tabela.

Transições curtas podem ajudar na atualização de resultado, mas não devem reiniciar contagens visualmente nem simular movimento de equipamentos. Não usar percentuais de progresso fictícios para a IA. Mostrar “analisando” até a resposta ou o prazo limite. Respeitar preferência de redução de movimento e navegação por teclado.

### Critérios para considerar o visual entregue

- Todas as telas previstas possuem estado vazio, carregando, pronto e erro aplicável.
- O visitante identifica produto, classe e decisão sem ler detalhes técnicos.
- A leitura funciona no monitor real e no navegador escolhido para a feira.
- Os controles operacionais mostram resultado real da ação, não apenas uma mudança local de cor.
- A interface não usa dados ilustrativos no modo operacional.
- Nenhum recurso essencial depende de imagens, fontes ou bibliotecas externas durante a feira.

## 22. Preparação do ambiente e execução

O desenvolvedor deverá produzir um guia reproduzível com estas etapas:

1. Conferir sistema operacional e hardware do computador de execução.
2. Instalar Python 3.12 e preparar o ambiente virtual do projeto.
3. Instalar as versões compatíveis e fixadas de FastAPI, Uvicorn, Pydantic, OpenCV, pySerial, PyTorch, torchvision e utilitários usados.
4. Preparar as dependências de desenvolvimento: pytest e ferramentas de verificação da interface.
5. Instalar/configurar Arduino IDE 2, suporte à placa ESP32 e driver USB quando necessário.
6. Compilar e gravar o firmware correspondente à versão do protocolo.
7. Configurar a câmera e testar aquisição e reconexão.
8. Importar o modelo treinado, seu manifesto e os perfis calibrados.
9. Criar/verificar o banco e diretórios de imagens, logs e backups.
10. Iniciar o serviço local e abrir o painel pelo endereço informado pelo inicializador.
11. Executar a verificação de prontidão e o ciclo de ensaio.
12. Repetir a inicialização com internet indisponível.

Não executar treinamento pesado enquanto a máquina está em operação. Não baixar pesos, fontes ou dependências automaticamente no início de um lote. Preparar os arquivos antes da feira e incluir uma verificação de integridade no inicializador.

Entregar um atalho ou comando de inicialização que informe erros compreensíveis. Se o ambiente não estiver pronto, indicar o que falta sem acionar a bancada. Ao fechar o serviço, solicitar parada e encerrar recursos de forma controlada; se o serviço morrer abruptamente, o firmware aplica seu prazo de comunicação.

O pacote inicial não exige hospedagem na internet, domínio, banco em nuvem ou assinatura de IA. O funcionamento proposto usa software local. Serviços externos só entram se a evolução do copiloto ou outro requisito posterior justificar.

## 23. Prioridades, dependências e divisão de trabalho

### P0 — obrigatório para chamar de sistema funcional

- Regras visuais A/B/C documentadas.
- Aquisição de imagens reais e dataset revisado.
- Modelo de qualidade por produto, validado em amostras independentes.
- Protocolo e firmware com sequência completa e tratamento de falhas.
- Integração ponta a ponta e histórico persistente.
- Painel de operação e modo feira com dados reais.
- Parada, revisão de inconclusivos, recuperação e ensaio offline.

### P1 — acabamento e operação da equipe

- Ferramenta confortável de coleta/rotulagem.
- Histórico com filtros, exportação e resumo imprimível.
- Diagnóstico legível, calibração documentada e gerenciamento de modelos.
- Backup/restauração, inicializador, manual e roteiro da feira.

### P2 — evoluções do projeto

- Modelo específico de detecção de anomalias.
- Copiloto de consulta aos dados.
- Outros produtos, múltiplas câmeras, localização de defeitos e rastreamento de várias peças.

O sistema deve ser organizado por essas responsabilidades, mesmo se uma pessoa fizer tudo. Para dividir a equipe, usar quatro frentes: dados/IA; firmware/integração; aplicação/dados; interface/apresentação. O responsável pela integração acompanha todas e mantém uma versão que inicia e executa o caminho já disponível. Prazo e esforço em dias dependem de equipe, data da feira, hardware e amostras; não foram definidos nesta especificação.

## 24. Critério final de entrega

A entrega não termina quando a tela fica pronta. Deve ser possível iniciar o sistema, selecionar um produto, processar uma peça real, visualizar sua imagem e classificação, executar a separação, consultar o registro e repetir o procedimento para o outro produto.

Se faltar câmera, modelo, dados ou comunicação, a interface deve dizer isso claramente. O desenvolvedor deve entregar a lista de capacidades implementadas e a evidência dos testes, distinguindo funcionamento verificado, requisito ainda pendente e extensão planejada.

O conjunto completo a entregar é: código-fonte organizado, dependências fixadas, firmware, protocolo, configurações, ferramenta de coleta, dataset e manifesto, rotinas de treinamento, modelos e métricas, banco/migrações, interface, inicializador, backup, documentação e roteiro de apresentação. Parâmetros dependentes de bancada e decisões de qualidade só são considerados concluídos depois da validação correspondente.

### Referências adicionais das tecnologias selecionadas

- [Python: ambiente virtual](https://docs.python.org/3.12/library/venv.html).
- [PyTorch: instalação conforme plataforma](https://pytorch.org/get-started/locally/).
- [Chart.js: gráficos](https://www.chartjs.org/docs/latest/).
- [pytest: testes em Python](https://docs.pytest.org/en/stable/).

As referências descrevem capacidades das ferramentas. O desenho do sistema, os requisitos e os critérios propostos são escolhas para esta bancada; não representam comprovação de desempenho do protótipo.

