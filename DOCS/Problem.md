# Problem

## 1. Enunciado

Investigar o transporte quântico em uma cavidade bidimensional deformada com formato de floco de neve e seis terminais elétricos uniformemente distribuídos.

O sistema é modelado em uma lattice tight-binding quadrada com o pacote Kwant. Cada terminal é um lead semi-infínito ideal acoplado à fronteira da cavidade. A geometria principal é exclusivamente o floco de neve deformado; não existe uma geometria regular comparativa neste projeto.

A temperatura será considerada zero e não haverá campo magnético externo.

A pergunta central é:

> Como a geometria deformada do floco de neve modifica o transporte quântico, a distribuição espacial das ondas, o espectro fechado e os observáveis característicos de um bilhar quântico aberto com seis terminais?

## 2. Objetivos

### 2.1 Objetivo geral

Construir uma implementação mínima e reproduzível em Kwant para estudar o floco de neve deformado em temperatura zero.

### 2.2 Objetivos específicos

1. Representar o contorno deformado e exportar sua máscara e contorno.
2. Converter o contorno em uma lattice tight-binding $120\times120$.
3. Acoplar seis leads semi-infinitos uniformemente separados por $60^\circ$.
4. Calcular transmissões e condutâncias entre os pares de terminais.
5. Calcular densidade local e corrente injetada por cada terminal.
6. Calcular o espectro fechado da cavidade.
7. Visualizar geometria, transporte, densidade e fluxo em notebooks Jupyter.
8. Associar os padrões observados a indicadores quânticos de caos, sem confundir irregularidade numérica com causalidade física.

## 3. Modelo físico

O sistema segue o Hamiltoniano tight-binding

$$
H = \sum_i \epsilon_i c_i^\dagger c_i
-t\sum_{\langle i,j\rangle}
\left(c_i^\dagger c_j+c_j^\dagger c_i\right).
$$

Adota-se $a=1$, $t=1$, $\epsilon_i=0$ dentro da cavidade e hopping unitário entre primeiros vizinhos. Os seis terminais são azuis no modelo visual e semi-infinitos no cálculo Kwant.

Não são considerados: campo magnético, temperatura finita, interação elétron-elétron, desordem, spin explícito e acoplamento spin-órbita.

## 4. Geometria principal

A geometria é um contorno fechado obtido por uma modulação polar hexagonal:

$$
R(\theta)=R_0\left[1+0.55\cos(6\theta)+0.22\cos(18\theta)+0.12\cos(24\theta)\right],
$$

com $R_0=0.20$ em coordenadas normalizadas. Os seis terminais são centrados em posições angulares uniformes.

## 5. Observáveis

1. Condutância $G_{mn}(E)=G_0T_{mn}(E)$.
2. Densidade local $\rho_i(E)=|\psi_i(E)|^2$.
3. Corrente local em cada link da lattice.
4. Autovalores da cavidade fechada.
5. Separação de níveis e distribuição estatística.
6. Tempo de permanência pela matriz de Smith.
7. Ergódicidade espacial da densidade.
8. Sensibilidade a pequenas perturbações adicionais do contorno.

## 6. Metodologia

1. Construir a máscara deformada em `scripts/build_geometries.py`.
2. Projetar os seis terminais sobre a fronteira da máscara.
3. Calcular transporte em `scripts/calculate_transport.py`.
4. Calcular espectro em `scripts/calculate_spectrum.py`.
5. Calcular densidade e corrente em `scripts/calculate_local.py`.
6. Salvar os resultados em arquivos `.npz`.
7. Ler apenas os `.npz` nos notebooks Jupyter para plotagem.

## 7. Produtos visuais

- Figura Kwant do floco deformado com seis leads azuis.
- Matriz $6\times6$ de transmissões médias.
- Transmissão emergente e modos propagantes por lead.
- Seis mapas de densidade, um por terminal injetor.
- Seis mapas individuais de corrente nos links.
- Mapa da divergência local e conservação por terminal.
- Curva de resíduos unitários da matriz S em três resoluções.
- Curvas espectrais e histogramas de separação de níveis.

## 8. Produtos de dados

- `data/geometries.npz`: contorno, máscara, lattice e terminais.
- `data/deformed.npz`: transmissões e modos dos seis leads.
- `data/lead_observables.npz`: matriz S, transmissões, modos, densidades por lead e correntes por link.
- `data/local_deformed.npz`: densidades, correntes e divergência local.
- `data/spectrum_deformed.npz`: espectro fechado.
- `data/convergence_validation.npz`: convergência espacial e resíduos unitários.

## 9. Critérios de sucesso

- O floco deformado está reproduzido e verificado visualmente.
- Os seis leads são independentes e semi-infinitos.
- Condutância, densidade, corrente e espectro usam os mesmos parâmetros físicos.
- A matriz de espalhamento é unitária dentro da precisão numérica disponível.
- A conservação local é calculada separando sítios internos dos sítios de acoplamento.
- Os resultados de convergência são registrados em resoluções distintas.
- Cada cálculo está separado da plotagem.
- Os resultados são rastreáveis às equações de `DOCS/Report.md`.