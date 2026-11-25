# Checklist do projeto Quantum Transport Quantum Pool

Legenda: [x] concluído, [ ] aberto, [~] em andamento.

## Configuração

- [x] Confirmar a estrutura do repositório.
- [x] Criar scripts, dados, notebooks e figuras.
- [x] Disponibilizar o ambiente Conda `Tconda`.
- [x] Instalar Kwant no ambiente `Tconda`.
- [x] Configurar o VS Code para usar `Tconda`.

## Geometria principal

- [x] Construir o contorno deformado de floco de neve.
- [x] Distribuir seis terminais uniformemente a $60^\circ$.
- [x] Converter o contorno em máscara da lattice $120\times120$.
- [x] Projetar os seis terminais sobre a fronteira interna da máscara.
- [x] Salvar geometria e metadados em `data/geometries.npz`.
- [x] Exportar o contorno em `data/geometries.svg`.
- [x] Gerar a figura Kwant em `figures/geometry_comparison.png`.
- [~] Testar convergência ao refinar a lattice (resoluções 80, 120 e 160 concluídas; diferença ainda significativa).

## Terminais e transporte

- [x] Definir seis leads semi-infinitos.
- [x] Usar largura finita igual nos seis leads.
- [x] Confirmar que os leads são independentes.
- [x] Implementar transmissão $T_{mn}(E)$.
- [x] Implementar condutância $G_{mn}(E)$.
- [x] Varredura energética em $[-1.8,1.8]$ com 37 pontos.
- [x] Salvar transporte em `data/deformed.npz`.
- [x] Criar o notebook `plot_transport.ipynb`.
- [x] Verificar conservação da matriz de espalhamento em toda a faixa disponível (máximo $SS^\dagger-I < 1.2\times10^{-12}$ nas resoluções testadas).
- [x] Concluir a análise integrada dos seis leads.
- [x] Registrar matriz S, modos, transmissões e fluxos por terminal.
- [x] Gerar mapas individuais de densidade e corrente.
- [x] Verificar $SS^\dagger-I$ nas resoluções 80, 120 e 160.
- [~] Concluir convergência espacial das transmissões.

## Densidade e corrente

- [x] Implementar densidade local pela Equação R17.
- [x] Implementar corrente local pela Equação R20.
- [x] Salvar dados locais em `data/local_deformed.npz`.
- [x] Gerar mapas de densidade por cada um dos seis terminais de entrada.
- [x] Gerar mapas de fluxo de corrente por cada terminal de entrada.
- [x] Calcular divergência local em todos os sítios pela Equação R21.
- [~] Verificar conservação local interna separando os sítios de acoplamento dos leads.

## Espectro fechado

- [x] Construir o Hamiltoniano fechado.
- [x] Resolver os autovalores pela Equação R23.
- [x] Salvar o espectro em `data/spectrum_deformed.npz`.
- [ ] Calcular separações consecutivas pela Equação R26.
- [ ] Verificar convergência ao refinar a lattice.
- [ ] Gerar histogramas espectrais no notebook apropriado.

## Validação e documentação

- [x] Registrar scripts responsáveis por cada cálculo.
- [x] Registrar os arquivos `.npz` associados aos resultados.
- [x] Atualizar `DOCS/Problem.md`.
- [x] Atualizar `DOCS/Report.md`.
- [~] Atualizar `DOCS/Results.md` com leitura dos resultados.
- [ ] Confirmar repetibilidade a partir dos scripts.
- [ ] Separar observação numérica de interpretação física.
- [ ] Explicar limites da discretização e do modelo.
- [ ] Confirmar que nenhum notebook realiza cálculo científico principal.

## Hipóteses

- [ ] Testar sensibilidade da densidade a pequenas deformações adicionais.
- [ ] Testar sensibilidade das transmissões entre os seis terminais.
- [ ] Comparar distribuições de tempo de permanência.
- [ ] Confirmar que irregularidade de condutância não é prova isolada de caos.
