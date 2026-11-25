# Results

Este documento registra os resultados da geometria principal: o floco de neve deformado com seis leads.

## Resultado G1 — Floco deformado

- Equação: [Report.md](./Report.md), equações R3–R9.
- Cálculo: `scripts/build_geometries.py`.
- Dados: `data/geometries.npz`.
- Contorno auxiliar: `data/geometries.svg`.
- Plotagem: `notebooks/plot_comparison.ipynb`.
- Figura: `figures/geometry_comparison.png`.

### Ilustração

![Floco de neve deformado com seis terminais](../figures/geometry_comparison.png)

### Leitura

A lattice possui tamanho efetivo $120\times120$ e o floco deformado contém 2.084 sítios. Seis terminais azuis estão distribuídos uniformemente a $60^\circ$ e acoplados à fronteira interna da máscara.

## Resultado T1 — Transporte dos seis terminais

- Equação: R12--R15.
- Cálculo: `scripts/calculate_transport.py`.
- Dados: `data/deformed.npz`.
- Matriz: transmissões $T_{mn}(E)$ com forma $(37,6,6)$.
- Modos: `mode_counts` com forma $(37,6)$.
- Fluxos: `outgoing_per_source` e `incoming_per_drain` com forma $(37,6)$.
- Plotagem: `notebooks/plot_transport.ipynb`.
- Figura: `figures/transport_deformed.png`.

Há quinze pares distintos entre os seis terminais. Para cada $m<n$, a relação

$$
T_{mn}(E)=\sum_{\alpha\in m}\sum_{\beta\in n}|S_{n\beta,m\alpha}(E)|^2
$$

resume a probabilidade de propagação entre os contatos. A soma por coluna representa o fluxo incidente organizado por terminal de origem, enquanto a soma por linha representa o fluxo recebido por terminal de destino.

## Resultado L1 — Densidade e corrente dos seis terminais

- Equações: R16--R22.
- Cálculo: `scripts/calculate_local.py`.
- Dados: `data/local_deformed.npz`.
- `densities`: forma $(6,N_{sítios})$.
- `iniquities`: concentração espacial por terminal injetor.
- `normalized_centers`: indicador escalar associado ao centro da distribuição.
- `current_links`: correntes somadas por terminal de origem.

Cada linha de `densities` corresponde à função de onda injetada por um lead. Densidade e fluxo devem ser interpretados conjuntamente: densidade indica distribuição espacial; corrente indica direção e conservação; transmissão indica quantificação global entre terminais.

## Resultado L2 — Mapas por terminal de entrada

- Equações: R16--R22.
- Cálculo: `scripts/calculate_local.py`.
- Dados: `data/local_deformed.npz`.
- Energia utilizada: $E/t=0.25$.
- Mapas de densidade: `figures/local_density_deformed.png`.
- Mapas de fluxo: `figures/current_flow_deformed.png`.
- Plotagem: `notebooks/plot_local_density.ipynb`.

Foram gerados seis mapas de densidade, um por cada lead injetor $T_1$ a $T_6$, e seis mapas correspondentes de fluxo nos links da lattice. Os índices de iniquidade mostram a concentração relativa da distribuição para cada entrada. Os vetores azuis e laranja representam a orientação da corrente calculada pelo operador de corrente do Kwant.

## Resultado H1 — Relações dos seis leads

- Equações: R13--R22.
- Cálculo integrado: `scripts/calculate_lead_observables.py`.
- Dados: `data/lead_observables.npz`.
- Figura: `figures/lead_observables.png`.
- Plotagem: `notebooks/plot_transport.ipynb`.

O arquivo contém transmissões $(37,6,6)$, modos $(37,6)$, fluxos emergentes e recebidos $(37,6)$, densidades $(37,6,N_{sítios})$, índices de concentração $(37,6)$ e correntes por link $(37,6,N_{links})$.

Os quinze pares distintos satisfazem

$$
T_{mn}(E)=\sum_{\alpha\in n}\sum_{\beta\in m}|S_{m\beta,n\alpha}(E)|^2.
$$

O número de modos define a disponibilidade dos canais, enquanto a transmissão mede o fluxo efetivo entre origens e destinos. Densidade e corrente devem ser relacionadas a esses fluxos globais pelas Equações R16--R22.

## Resultado S1 — Espectro fechado

- Equações: R23–R27.
- Cálculo: `scripts/calculate_spectrum.py`.
- Dados: `data/spectrum_deformed.npz`.

Estes resultados pertencem apenas ao modelo aberto/fechado do floco deformado. Não há comparação com uma geometria regular neste projeto.

## Resultado C1 — Convergência e conservação da matriz S

- Equações: R13–R15.
- Cálculo: `scripts/validate_convergence.py`.
- Dados: `data/convergence_validation.npz`.
- Resoluções: $80\times80$, $120\times120$ e $160\times160$.
- Faixa: $E/t\in[-1.8,1.8]$, 37 pontos.
- Figura: `figures/convergence_validation.png`.

### Conservação

O valor médio de $\|SS^\dagger-I\|_F$ foi de $1.330\times10^{-13}$ em $80\times80$, $2.884\times10^{-13}$ em $120\times120$ e $4.909\times10^{-13}$ em $160\times160$. Os máximos ficaram abaixo de $1.12\times10^{-12}$. $E=0$ apresentou singularidade MUMPS em todas as resoluções e foi excluído da validação daquela energia.

### Convergência

A diferença média das transmissões foi:

- $80\times80$ contra $120\times120$: $2.484670\times10^{-1}$;
- $120\times120$ contra $160\times160$: $4.244922\times10^{-1}$.

As transmissões ainda não são convergidas entre as resoluções testadas. Portanto, os resultados atuais são específicos da discretização e exigem refinamento adicional antes de interpretação física. A estabilidade da matriz S não garante convergência espacial das transmissões.

## Resultado F1 — Fluxo de corrente e conservação local

- Equação: R20–R21.
- Cálculo: `scripts/calculate_local.py`.
- Dados: `data/local_deformed.npz`.
- Mapas por lead: `figures/current_flow_each_terminal.png`.
- Energia: $E/t=0.25$.

Para cada terminal injetor foram calculados os correntes nos links e a divergência em cada sítio:

$$
D_i=\sum_j J_{ij}.
$$

Os resíduos devem ser analisados separando os sítios internos da cavidade dos sítios acoplados aos leads. Nos sítios internos, $D_i$ deve tender a zero; nos sítios de interface, desvios representam entradas ou saídas de probabilidade entre cavidade e reservatórios. Os valores médios e máximos por terminal estão registrados em `data/local_deformed.npz`.
