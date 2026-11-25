# Checklist do projeto Quantum Transport Quantum Pool

Legenda:

- [x] Tarefa concluída
- [ ] Tarefa em aberto
- [~] Tarefa em andamento

## 1. Configuração do projeto

- [x] Confirmar a estrutura inicial do repositório.
- [x] Criar a pasta `scripts/`.
- [x] Criar a pasta `data/`.
- [x] Criar a pasta `notebooks/`.
- [x] Criar a pasta `figures/`.
- [x] Disponibilizar o ambiente Conda `Tconda`.
- [x] Instalar Kwant no ambiente `Tconda`.
- [x] Configurar o VS Code para usar o Python de `Tconda`.
- [x] Criar `requirements.txt`.

## 2. Documentação teórica

- [x] Criar `DOCS/Problem.md`.
- [x] Escrever o formalismo em `DOCS/Report.md`.
- [x] Definir identificadores estáveis para as equações R1–R33.
- [ ] Completar documentação de parâmetros e convenções numéricas.
- [~] Escrever `DOCS/Results.md` com resultados observados e limitações.

## 3. Geometria da cavidade

- [x] Extrair o contorno da cavidade de `inomeado.svg`.
- [x] Extrair as posições dos três terminais azuis.
- [x] Construir a versão deformada baseada no contorno irregular.
- [x] Construir uma versão regular suavizada.
- [x] Validar visualmente que os contornos preservam a forma esperada.
- [x] Preservar os terminais nas posições relativas normalizadas.
- [x] Converter os contornos em máscaras da lattice quadrada.
- [x] Criar a lattice `120 × 120` em Kwant.
- [x] Salvar contornos e máscaras em `data/geometries.npz`.
- [x] Exportar os contornos em `data/geometries.svg`.
- [ ] Refazer a comparação com uma resolução mais fina.
- [ ] Verificar convergência ao variar o tamanho da lattice.

## 4. Implementação dos terminais

- [x] Definir o lead do terminal 1 como contato semi-infinito.
- [x] Definir o lead do terminal 2 como contato semi-infinito.
- [x] Definir o lead do terminal 3 como contato semi-infinito.
- [x] Usar largura finita igual nos três terminais.
- [x] Acoplar os três terminais às posições compatíveis com `inomeado.svg`.
- [x] Confirmar que os terminais são independentes.
- [x] Verificar o número de modos propagantes por energia.
- [x] Manter os terminais idênticos nas geometrias regular e deformada.
- [x] Projetar os três terminais sobre a fronteira interna das máscaras da lattice.

## 5. Condutância e transporte

- [x] Implementar a matriz de espalhamento de três terminais em Kwant.
- [x] Implementar a transmissão $T_{mn}(E)$ pela Equação R14.
- [x] Implementar a condutância $G_{mn}(E)$ pela Equação R15.
- [x] Calcular a condutância entre os pares 1–2, 1–3 e 2–3.
- [x] Definir uma faixa energética dentro dos modos propagantes.
- [x] Executar a varredura para a cavidade regular.
- [x] Executar a varredura para a cavidade deformada.
- [x] Usar os mesmos parâmetros de lattice e hopping nos dois casos.
- [x] Testar conservação da matriz de espalhamento.
- [x] Salvar os resultados em `data/regular.npz`.
- [x] Salvar os resultados em `data/deformed.npz`.

## 6. Densidade local

- [ ] Implementar a função de onda de espalhamento injetada pelo terminal 1.
- [ ] Implementar a função de onda de espalhamento injetada pelo terminal 2.
- [ ] Implementar a função de onda de espalhamento injetada pelo terminal 3.
- [ ] Calcular $
ho_i(E)=|\psi_i(E)|^2$ pela Equação R17.
- [ ] Definir pelo menos três energias representativas com justificativa física.
- [ ] Gerar mapas da densidade local para a cavidade regular.
- [ ] Gerar mapas da densidade local para a cavidade deformada.
- [ ] Normalizar as densidades para comparação entre geometrias.
- [ ] Calcular a densidade integrada por região pela Equação R18.
- [ ] Calcular o índice de concentração pela Equação R19.

## 7. Corrente local

- [ ] Implementar a corrente de probabilidade em cada link pela Equação R20.
- [ ] Verificar a conservação local pela Equação R21.
- [ ] Calcular a corrente integrada por uma superfície transversal pela Equação R22.
- [ ] Comparar a corrente integrada com as transmissões obtidas pela matriz S.
- [ ] Gerar mapas de fluxo para a cavidade regular.
- [ ] Gerar mapas de fluxo para a cavidade deformada.
- [ ] Registrar a orientação e a convenção de sinal das setas.

## 8. Espectro fechado

- [ ] Implementar o Hamiltoniano fechado da cavidade regular.
- [ ] Implementar o Hamiltoniano fechado da cavidade deformada.
- [ ] Resolver os autovalores pela Equação R23.
- [ ] Normalizar os autovetores pela Equação R24.
- [ ] Calcular separações consecutivas pela Equação R26.
- [ ] Calcular razões de separações pela Equação R27.
- [ ] Verificar a estabilidade do espectro ao refinar a lattice.
- [ ] Salvar os resultados em `data/spectrum_regular.npz`.
- [ ] Salvar os resultados em `data/spectrum_deformed.npz`.

## 9. Tempo de permanência

- [ ] Implementar a derivada numérica da matriz S pela Equação R30.
- [ ] Construir a matriz de Smith pela Equação R28.
- [ ] Calcular o tempo médio de Wigner pela Equação R29.
- [ ] Extrair os tempos próprios associados aos autovalores de Q.
- [ ] Comparar distribuições entre as duas geometrias.
- [ ] Testar convergência ao variar o passo energético.
- [ ] Salvar os resultados em arquivos `.npz`.

## 10. Suscetibilidade à deformação

- [ ] Implementar a diferença absoluta de condutância pela Equação R31.
- [ ] Calcular a resposta relativa pela Equação R32.
- [ ] Comparar densidades em uma região comum pela Equação R33.
- [ ] Aplicar normalização consistente às geometrias regular e deformada.
- [ ] Identificar regiões com maior sensibilidade geométrica.
- [ ] Comparar pequenas variações da cavidade entre si.

## 11. Índices de caos quântico e clássico

- [ ] Calcular estatística espacial da densidade.
- [ ] Comparar ergodicidade espacial nas duas geometrias.
- [ ] Analisar histogramas de separação de níveis.
- [ ] Comparar os níveis com uma janela estatística apropriada.
- [ ] Remover ou controlar simetrias da lattice antes da análise.
- [ ] Analisar a distribuição dos tempos de permanência.
- [ ] Implementar o bilhar clássico correspondente quando possível.
- [ ] Calcular trajetórias clássicas no contorno correspondente.
- [ ] Calcular expoentes de Lyapunov positivos ou negativos.
- [ ] Construir mapa de Poincaré, quando a geometria permitir.
- [ ] Relacionar os indicadores clássicos aos indicadores quânticos.
- [ ] Evitar afirmar caos sem convergência e evidências complementares.

## 12. Plotagem em notebooks

- [ ] Implementar `notebooks/plot_transport.ipynb` usando apenas dados `.npz`.
- [ ] Implementar `notebooks/plot_local_density.ipynb` usando apenas dados `.npz`.
- [x] Implementar `notebooks/plot_comparison.ipynb` usando apenas dados `.npz`.
- [x] Gerar figura das duas geometrias com os três terminais.
- [ ] Gerar gráfico da condutância por pares em função da energia.
- [ ] Gerar mapas de densidade para pelo menos três energias representativas.
- [ ] Gerar mapas de fluxo em cada geometria.
- [ ] Gerar histogramas ou curvas comparativas dos observáveis.
- [x] Exportar as figuras para `figures/`.
- [ ] Garantir que nenhum notebook realiza cálculo científico principal.

## 13. Validação numérica

- [ ] Confirmar repetibilidade a partir dos scripts.
- [ ] Registrar parâmetros, lattice, hopping e energias em cada `.npz`.
- [ ] Testar pelo menos três resoluções da lattice.
- [ ] Testar pelo menos três tamanhos de passo energético.
- [ ] Verificar conservação de probabilidade.
- [ ] Comparar os três terminais físicos como leads independentes.
- [ ] Confirmar que os resultados usam o mesmo intervalo energético.
- [ ] Comparar regularização e deformação sem alterar outros parâmetros.

## 14. Consolidação dos resultados

- [~] Atualizar `DOCS/Results.md` com tabelas de parâmetros.
- [x] Registrar equações usadas em cada resultado.
- [x] Registrar os scripts responsáveis por cada cálculo.
- [x] Registrar os arquivos `.npz` associados a cada figura.
- [x] Registrar os notebooks usados em cada plotagem.
- [ ] Documentar as hipóteses testadas.
- [ ] Separar observação numérica de interpretação física.
- [ ] Explicar limites do modelo e da discretização.
- [ ] Descrever cautelosamente as diferenças entre cavidade regular e deformada.

## 15. Hipóteses iniciais

- [ ] Testar padrões mais organizados na cavidade regular.
- [ ] Testar maior espalhamento da densidade na cavidade deformada.
- [ ] Testar maior sensibilidade geométrica da densidade e condutância.
- [ ] Comparar distribuições de tempo de permanência.
- [ ] Confirmar que irregularidade de condutância não é prova isolada de caos.
