# Report: transporte quântico em bilhares abertos

## 1. Objetivo e organização deste documento

Este relatório estabelece o formalismo teórico, as premissas, os observáveis e o plano metodológico do projeto **Quantum Transport Quantum Pool**. Ele serve como referência estável para os scripts de cálculo e os notebooks de visualização.

A função das equações é dupla: fornecer a definição física de cada quantidade e permitir que resultados numéricos sejam reproduzidos e rastreados. Todas as fórmulas recebem um identificador permanente na forma `(Rk)`. A implementação deve utilizar esses identificadores nas docstrings e na documentação dos resultados.

Este documento não apresenta resultados experimentais ou numéricos ainda não obtidos. Ele delimita o que poderá ser calculado sem confundir hipóteses com conclusões.

## 2. Sistema físico

### 2.1 Cavidade quântica aberta

A cavidade é uma região bidimensional finita contendo elétrons livres efetivamente confinados por contornos duros. A cavidade é conectada a seis terminais semi-infinitos uniformemente distribuídos ao redor de um contorno de floco de neve.

O estudo utilizará exclusivamente uma cavidade deformada com simetria hexagonal de floco de neve. Não haverá comparação ou construção de uma geometria regular no produto principal.

A deformação deve ser introduzida sem alterar significativamente:

- o tamanho efetivo da cavidade;
- as posições relativas dos seis terminais;
- a largura dos terminais;
- o hopping da lattice;
- o intervalo de energia e a discretização.

Essa regra mantém o contorno como principal parâmetro.

### 2.2 Unidades e convenções

Adotaremos unidades numéricas compatíveis com uma lattice tight-binding quadrada:

- $a$: constante da lattice;
- $t$: amplitude positiva de hopping entre primeiros vizinhos;
- $E$: energia da lattice em unidades de $t$;
- $e>0$: módulo da carga elementar;
- $\hbar$: constante de Planck reduzida;
- $G_0=2e^2/h$: quantum de condutância para spin degenerado.

Inicialmente, $a=1$ e $t=1$ podem ser usados internamente. Quando o objetivo for comparar escalas físicas, $a$ e $t$ devem ser tratados como parâmetros documentados no `.npz` correspondente.

Não são considerados nesta etapa:

- campo magnético;
- temperatura finita;
- interações elétron-elétron;
- desordem aleatória;
- spin explícito;
- acoplamentos spin-órbita;
- efeitos de fonte-de-drenagem além da resposta linear;
- perda inelástica dentro da cavidade.

Essas exclusões tornam o modelo coerente com transporte coerente em temperatura zero, mas limitam a interpretação dos resultados.

## 3. Modelo tight-binding

### Equação R1 — Hamiltoniano da cavidade

O sistema é descrito pela rede quadrada através do Hamiltoniano

$$
H=\sum_i \epsilon_i c_i^\dagger c_i
-t\sum_{\langle i,j\rangle}
\left(c_i^\dagger c_j+c_j^\dagger c_i\right),
\tag{R1}
$$

onde:

- $c_i^\dagger$ cria uma partícula no sítio $i$;
- $c_i$ remove uma partícula do sítio $i$;
- $\epsilon_i$ é a energia local do sítio;
- $t>0$ é o hopping entre sítios primeiros vizinhos;
- $\langle i,j\rangle$ indica pares não orientados da lattice;
- $i,j$ são posições discretas em unidades da constante da lattice.

Para uma cavidade não perturbada, tomamos $\epsilon_i=0$ dentro da região fechada. O sinal negativo do hopping implica que o estado de menor energia de uma rede infinita corresponde ao fundo da banda. Alterações locais de $\epsilon_i$ podem representar potenciais ou deformações futuras, mas não são necessárias na primeira implementação.

O formalismo continua de segunda quantização, porém os cálculos numéricos podem usar a matriz de hopping em primeira quantização:

$$
[H_{ij}] =
\begin{cases}
\epsilon_i, & i=j,\\
-t, & i\text{ e }j\text{ são primeiros vizinhos},\\
0, & \text{demais pares}.
\end{cases}
\tag{R2}
$$

Os zeros fora dos pares de vizinhos são responsáveis pela estrutura esparsa da matriz. Essa estrutura permite trabalhar com cavidades maiores sem armazenar integralmente uma matriz densa.

### Limite de validade

A lattice quadrada representa apenas aproximadamente uma geometria contínua. Quanto menor $a$ e maior a quantidade de sítios, melhor o contorno deformado é resolvido. O contorno e os seis terminais devem ser verificados visualmente.

## 4. Geometria da cavidade

### 4.1 Contorno principal

A cavidade principal é um floco de neve deformado definido por um contorno fechado.

### Equação R6 — Contorno deformado

A geometria deformada pode ser escrita como

$$
R_d(\theta)=R_0
\left[1+
\alpha_3\cos(3\theta)
+\alpha_5\sin(5\theta)
+\alpha_7\cos(7\theta)
\right].
\tag{R6}
$$

Os coeficientes devem ser pequenos o bastante para que cada curva permaneça simples e fechada. A escolha das harmonias representa visualmente ramificações do floco de neve sem criar auto-interseções.

### 4.2 Conversão para sítios da lattice

Após a definição do contorno, um sítio $i=(m,n)$ pertence à cavidade quando

$$
(m,n)\in\Omega
\quad\Longleftrightarrow\quad
(m,n)\text{ está no interior da região fechada}.
\tag{R7}
$$

Se o contorno estiver definido por uma sequência de vértices $(x_k,y_k)$, o teste de ponto-em-polígono determina quais sítios da lattice estão contidos em $\Omega$.

A discretização deve preservar uma lattice quadrada de tamanho fixo $120\times120$, a mesma resolução espacial e seis terminais acoplados em posições uniformes. O número de sítios da máscara deformada deve ser registrado como metadado no `.npz`.

### 4.3 Posicionamento dos terminais

Os seis terminais azuis permanecem uniformemente distribuídos em ângulos separados por $60^\circ$.

Em coordenadas normalizadas, suas posições podem ser descritas por

$$
{\bf p}_m=(x_m,y_m),\qquad m=1,\ldots,6.
\tag{R8}
$$

Cada terminal é um lead semi-infinito acoplado a uma faixa finita de sítios da cavidade:

$$
L_m={i\in\Omega:\ i\text{ pertence à borda de acoplamento de }m}.
\tag{R9}
$$

Não são confundidos os conceitos de região externa do lead e largura efetiva do acoplamento. A largura define quantos sítios fazem parte da interface. O comprimento do lead é semi-infinito e atua como reservatório ideal.

## 5. Banda do lead e modos propagantes

### Equação R10 — Dispersão da lattice quadrada

Um lead quadrado infinito com hopping $-t$ possui a banda:

$$
E(k_x,k_y)=\epsilon_L
-2t\cos(k_xa)-2t\cos(k_ya).
\tag{R10}
$$

Os valores $k_x,k_y$ são vetores de onda medidos em unidades $1/a$. Para $\epsilon_L=0$, a banda se estende aproximadamente de $-4t$ a $+4t$.

Na presença de confinamento transversal, os modos do lead podem ser obtidos resolvendo

$$
H_L(q)\chi_
u(q)=E\chi_
u(q).
\tag{R11}
$$

Aquantidade $q$ é o vetor de onda longitudinal. O índice $\nu$ identifica o modo transversal. O modo é propagante quando existe uma solução real para $q$. Modos evanescentes possuem $q$ complexo e não contribuem diretamente ao transporte em $T$ no regime aberto.

O intervalo energético usado deverá ser restrito a uma região em que:

- pelo menos um modo esteja propagante;
- o número de modos seja conhecido;
- nenhum terminal esteja fora da faixa de condução;
- a comparação entre geometrias use exatamente a mesma faixa.

Isso pode ser verificado observando o espectro dos leads ou o número de canais propagantes calculado pelo Kwant.

## 6. Matriz de espalhamento

### Equação R12 — Função de Green

A resposta de espalhamento da cavidade é obtida pela matriz de Green retardo-avançado:

$$
G^r(E)=
\left[E-H_c-\sum_m\Sigma_m^r(E)+i0^+\right]^{-1},
\tag{R12}
$$

onde:

- $H_c$ é o Hamiltoniano da cavidade e dos acoplamentos internos;
- $\Sigma_m^r(E)$ é a autocarreira retardo do terminal $m$;
- $i0^+$ representa o limite retardo adequado;
- $G^r(E)$ contém o estado propagado pela excitação em uma dada energia.

A autocarreira incorpora o fato de que o lead é semi-infinito. Ela tem parte imaginária associada ao escape da cavidade para os contatos.

### Equação R13 — Matriz de espalhamento

A matriz de espalhamento combina todos os canais dos seis terminais:

$$
S(E)=\left[S_{mn}(E)\right],\qquad m,n\in\{1,\ldots,6\},
\tag{R13}
$$

simplificada como uma matriz por contatos. Para canais individuais, o elemento $S_{mn}^{\beta\alpha}(E)$ representa a amplitude de um estado injetado no canal $\alpha$ do terminal $n$ que emerge no canal $\beta$ do terminal $m$.

As propriedades fundamentais são:

- $SS^\dagger=I$ em ausência de perda;
- $S$ é unitária;
- os fluxos totais incidentes e emergentes satisfazem conservação;
- $S$ contém tanto a fase quanto o módulo das amplitudes.

### Equação R14 — Condutância de Landauer

A transmissão do terminal $n$ para o terminal $m$ é

$$
T_{mn}(E)=
\sum_{\alpha\in n}
\sum_{\beta\in m}
\left|S_{m\beta,n\alpha}(E)\right|^2,
\tag{R14}
$$

com $m\neq n$ para a transmissão entre contatos distintos.

A condutância em temperatura zero é

$$
G_{mn}(E)=G_0T_{mn}(E),
\qquad G_0=\frac{2e^2}{h}
\tag{R15}
$$

para um sistema com spin degenerado. Na implementação sem spin explícito, $G_0$ pode ser usado como fator teórico. Alternativamente, os gráficos podem apresentar $T_{mn}$ ou $G_{mn}/G_0$.

É necessário declarar o tipo de gráfico usado, pois:

- $T$ é adimensional;
- $G/G_0$ coincide numericamente com $T$ quando o modelo ignora degenerescências;
- $G$ possui unidade de condutância quando se inclui $G_0$.

Para os seis terminais, os pares relevantes são todas as combinações distintas $m<n$, com $m,n=1,\ldots,6$.

## 7. Densidade local e distribuição espacial

### Equação R16 — Densidade local

A densidade local associada à função de onda $\psi(E)$ é

$$
\rho({\bf r},E)=|\psi({\bf r},E)|^2.
\tag{R16}
$$

Em uma rede discreta,

$$
\rho_i(E)=|\psi_i(E)|^2.
\tag{R17}
$$

A função $\psi$ deve ser obtida pela solução de espalhamento injetada por um terminal específico. Em Kwant, uma função de onda do lead pode ser usada para construir o estado incidentes. Não se deve comparar mapas gerados por fluxos de entrada diferentes sem declarar o terminal de origem.

A densidade representa probabilidade relativa; para fluxo unitário normalizado, ela pode ser comparada entre energias. Seu máximo não identifica isoladamente um estado próprio fechado, pois o sistema aberto possui autoestados quasinormais com largura finita.

### Equação R18 — Densidade integrada por região

Para analisar ergodicidade espacial, a cavidade pode ser dividida em regiões $A_k$. A densidade integrada é

$$
P_k(E)=\frac{\sum_{i\in A_k}\rho_i(E)}
{\sum_{i\in\Omega}\rho_i(E)}.
\tag{R18}
$$

Se a distribuição fosse uniformemente ergódica em uma região estável, as frações $P_k$ tenderiam a acompanhar a área relativa da região. Desvios podem indicar concentração, canais preferenciais ou estados quase localizados. Porém, a escolha das regiões afeta o resultado e deve ser registrada.

### Equação R19 — Índice de iniquidade espacial

Uma medida simples de concentração é

$$
I(E)=\frac{\sum_i \rho_i(E)^2}
{\left(\sum_i\rho_i(E)\right)^2}.
\tag{R19}
$$

Uma distribuição concentrada em poucos sítios pode produzir $I$ maior. Uma distribuição distribuída em mais sítios tende a diminuir $I$.

Como na rede existem fronteiras, discretização e normalização, a interpretação deve ser comparativa entre geometrias com o mesmo $N$ efetivo e sem alterações arbitrárias da escala.

## 8. Corrente local

### Equação R20 — Operador de corrente em um link

Para um hopping do sítio $j$ para o sítio $i$, a corrente de probabilidade é

$$
J_{ij}
=
\frac{2}{\hbar}\operatorname{Im}
\left(\psi_i^*t_{ij}\psi_j\right).
\tag{R20}
$$

Na lattice quadrada, o valor de $t_{ij}$ é $-t$ para links reais. Como o sinal global pode depender da convenção adotada pelo Kwant, o plano inicial de visualização deve usar setas normalizadas ou vetores projetados pela média dos links.

A continuidade local é expressa por

$$
\sum_j J_{ij}=0
\tag{R21}
$$

para um sítio interno na ausência de fontes, dissipação ou acoplamentos não unitários. Esse balanço permite verificar se o cálculo apresenta fluxo conservado.

### Equação R22 — Corrente integrada

A corrente que atravessa uma superfície transversal $C$ é

$$
I_C(E)=\sum_{i\in C^-}\sum_{j\in C^+}J_{ij}(E).
\tag{R22}
$$

As interfaces $C^-$ e $C^+$ são definidas à esquerda e à direita da superfície. A corrente integrada deve ser comparada à transmissão calculada pela matriz $S$, permitindo uma verificação cruzada de que a densidade e o fluxo correspondem ao mesmo estado incidente.

## 9. Estados fechados e espectro auxiliar

### Equação R23 — Problema de autovalores fechado

Para uma cavidade sem leads, o espectro satisfaz

$$
H_c\phi_n=E_n\phi_n.
\tag{R23}
$$

Os vetores $\phi_n$ representam estados normados da cavidade fechada:

$$
\sum_i|\phi_n(i)|^2=1.
\tag{R24}
$$

Os espectros fechado e aberto não são idênticos. Os leads deslocam os níveis por meio da autocarreia e acrescentam largura de escape:

$$
E_n^{\rm aberto}
\sim E_n^{\rm fechado}
+\Delta E_n
-i\frac{\Gamma_n}{2}.
\tag{R25}
$$

Assim, o espectro fechado é apenas uma referência auxiliar para compreender a densidade de estados. A ressonância aberta aparece como pico ou oscilações finitas em observáveis de espalhamento.

### Equação R26 — Separação de níveis

As separações consecutivas são

$$
s_n=E_{n+1}-E_n.
\tag{R26}
$$

Para comparar geometrias com diferentes densidades médias de estados, pode-se usar separação não normalizada ou energia normalizada por

$$
r_n=
\frac{
\min(s_n,s_{n+1})
}{
\max(s_n,s_{n+1})
},
\tag{R27}
$$

conhecida como razão de separações consecutivas.

Uma amostra isolada de $s_n$ ou $r_n$ não prova integração ou regularidade clássica. Para um estudo estatístico adequado, devem ser respeitados:

- janela espectral suficiente;
- desenrolamento da densidade média de estados;
- separação de simetrias;
- convergência com a discretização;
- identificação clara da classe de espectro utilizada.

## 10. Tempo de permanência

### Equação R28 — Matriz de Smith

O tempo de permanência pode ser definido pela matriz de Smith:

$$
Q(E)
=-i\hbar S^\dagger(E)
\frac{dS(E)}{dE},
\tag{R28}
$$

cuja parte dos Wigner associados ao atraso é

$$
\tau_W(E)
=\frac{1}{N_{\rm ch}}
\operatorname{Tr}Q(E),
\tag{R29}
$$

onde $N_{\rm ch}$ é o número total de canais abertos.

A matriz $Q$ é hermitiana em condições adequadas, e seus autovalores representam tempos de permanência associados aos modos próprios de delay. Uma aproximação numérica exige derivada de $S$ em uma malha suficientemente fina:

$$
\frac{dS}{dE}
\approx
\frac{S(E+\Delta E)-S(E-\Delta E)}{2\Delta E}.
\tag{R30}
$$

Os resultados dependem do tamanho de $\Delta E$ e da suavidade dos dados. O valor do passo deverá ser registrado no `.npz` e comparado com uma variação menor como teste de convergência.

## 11. Suscetibilidade à deformação

### Equação R31 — Variação da condutância

Uma pequena mudança geométrica $\delta\Omega$ pode ser caracterizada por

$$
\Delta G_{mn}(E)
=
G_{mn}^{\rm def}(E)-G_{mn}^{\rm reg}(E).
\tag{R31}
$$

Para quantificar o tamanho relativo da resposta, pode-se usar

$$
\chi_G(E)
=
\frac{|G^{\rm def}(E)-G^{\rm reg}(E)|}
{|G^{\rm reg}(E)|+\epsilon},
\tag{R32}
$$

sendo $\epsilon>0$ uma constante pequena usada para evitar divisão por zero.

### Equação R33 — Variação da densidade

Em diferentes geometrias, o mapa na rede não deve ser comparado diretamente por índice $i$ sem remover diferenças de contorno. Uma medida possível é

$$
D(E)
=
\frac{
\sum_{i\in\Omega_{\rm comp}}
\left|\rho_i^{\rm def}(E)-\rho_i^{\rm reg}(E)
\right|
}
{
\sum_{i\in\Omega_{\rm comp}}
\left(
\rho_i^{\rm def}(E)+\rho_i^{\rm reg}(E)
\right)
},
\tag{R33}
$$

onde $\Omega_{\rm comp}$ é a região interna comum ou uma região normalizada definida antes da comparação.

O mapa pode ser interpolado em coordenadas normalizadas para uma resolução comum. Todas as normalizações devem ser descritas no notebook ou no arquivo `.npz`.

## 12. Indicadores de caos quântico

A deformação de um bilhar pode transformar trajetórias clássicas estáveis em trajetórias caóticas. Em sistemas quânticos abertos, não existe uma trajetória única que demonstre caos. Os indicadores abaixo devem ser interpretados como evidências complementares.

### 12.1 Sensibilidade à energia e à geometria

Oscilações rápidas e complexas de $G(E)$ podem indicar interferência entre muitos caminhos quânticos. Uma resposta geométrica mais sensível pode surgir da geometria deformada, mas irregularidade na condutância não prova caos.

### 12.2 Ergocidade espacial

A densidade local pode se distribuir de modo semelhante ao comportamento ergódico na região permitida. Em contrapartida, padrões organizados podem sugerir órbitas periódicas ou estados escarceadores. Essas interpretações dependem da resolução e da escolha do estado.

### 12.3 Distribuição espectral

A estatística de separações e razões pode indicar:

- acumulação próxima de Poisson em casos integráveis ou regularidade forte;
- repulsão de níveis em modelos quânticos caóticos compatíveis com ensembles adequados;
- efeitos de simetria ou lacunas de partícula que devem ser removidos antes da análise.

O projeto não deve substituir um cálculo estatístico completo por um único histograma.

### 12.4 Tempo de permanência

Uma distribuição ampla de tempos pode refletir variabilidade de trajetórias e armazenamento parcial das ondas. A distribuição não pode ser usada isoladamente para concluir sobre caos clássico, pois o acoplamento dos terminais e o número de modos afetam fortemente o escape.

### 12.5 Trajetórias clássicas auxiliares

Quando houver geometria correspondente e bola clássica definida, trajetórias no contorno podem auxiliar a interpretação. Elas não serão consideradas uma exigência da etapa inicial se não puderem ser construídas com correspondência direta à lattice.

## 13. Metodologia numérica

### 13.1 Fluxo de cálculo

O fluxo recomendado é:

1. extrair ou representar o contorno em coordenadas normalizadas;
2. construir uma lattice quadrada em Kwant;
3. selecionar os sítios da cavidade;
4. adicionar hopping e potencial local;
5. acoplar os três leads semi-infinitos;
6. verificar o número de canais propagantes;
7. varrer uma faixa limitada de energia;
8. calcular a matriz de espalhamento;
9. calcular $T_{mn}$, $G_{mn}$ e os observáveis locais;
10. resolver o problema fechado para referência;
11. salvar os dados em arquivos `.npz`;
12. realizar toda a plotagem em notebooks Jupyter.

O cálculo numérico não deve ser realizado nos notebooks principais. Os notebooks devem apenas abrir arquivos `.npz`, validar metadados e produzir gráficos.

### 13.2 Metadados mínimos dos `.npz`

Cada arquivo de dados deve conter, sempre que aplicável:

- `geometry` ou nome da geometria;
- `size` ou $L_x,L_y$ da lattice;
- `hopping` ou $t$;
- `onsite` ou $\epsilon_i$;
- `energies`;
- `lead_width`;
- `number_of_modes`;
- arrays de transmissões ou condutâncias;
- arrays de densidades locais;
- arrays de correntes locais;
- posições dos sítios;
- metadados de normalização;
- passos de discretização espectral ou geométrica.

A ausência desses parâmetros impede uma comparação reprodutível entre cavidades.

### 13.3 Estratégia de verificação

A implementação mínima deve incluir:

- visualização do floco deformado com seis terminais;
- teste de conservação da matriz de espalhamento;
- comparação da corrente integrada com a transmissão;
- pelo menos três energias representativas;
- comparação da condutância entre os pares de terminais;
- mapas de densidade e fluxo para cada terminal injetor;
- refinamento qualitativo da lattice;
- análise cautelosa do espectro fechado.

Uma energia representativa pode ser selecionada por um dos seguintes critérios:

- pico identificado em $T_{mn}(E)$;
- mínimo de transmissão;
- mudança rápida da densidade;
- regime com número fixo de modos;
- afinidade com uma ressonância do espectro fechado;
- varredura sistemática indicada por pontos de interesse definidos antes da visualização.

Não é suficiente escolher três valores arbitrários sem declarar o procedimento.

## 14. Produtos visuais mínimos

A entrega didática deverá incluir:

1. figura do floco deformado com seis terminais destacados;
2. matriz e curvas das transmissões dos quinze pares;
3. número de modos propagantes por lead;
4. seis mapas de densidade por terminal injetor;
5. seis mapas de fluxo por terminal injetor;
6. divergência local $D_i$ e conservação da corrente;
7. resíduos de unitividade da matriz S;
8. espectro fechado e histogramas de separação.

Todos os notebooks devem citar a equação utilizada. Por exemplo:

```python
def density_from_wavefunction(wavefunction):
    """Calcula a densidade local pela Eq. R16 do DOCS/Report.md."""
```

## 15. Limitações da interpretação

Os seguintes pontos devem ser evitados:

- assumir que condutância irregular implica caos clássico;
- comparar mapas sem normalização e sem terminal de entrada explícito;
- confundir espectro fechado com espectro de decaimento aberto;
- usar estatísticas espectrais com amostra pequena;
- alterar simultaneamente geometria, lattice, hoppings e terminal;
- interpretar concentração local como prova de órbita clássica;
- considerar apenas um par de terminais em um sistema de três;
- usar energia arbitrária fora da faixa propagante.

Os resultados são evidências sobre o modelo calculado. Uma declaração sobre caos quântico exige convergência, observáveis complementares e leitura cuidadosa das limitações.

## 16. Critérios de rastreabilidade

Para cada resultado futuro, o registro deve indicar:

- equação correspondente em `DOCS/Report.md`;
- script que realizou o cálculo;
- arquivo `.npz` produzido;
- notebook que realizou a plotagem;
- parâmetros e intervalo de energia;
- geometria regular ou deformada;
- terminal injetor e terminal coletor;
- normalização usada;
- limitações da interpretação.

A estrutura recomendada é:

```text
notebooks/plot_transport.ipynb
  -> lê data/deformed.npz
  -> aplica equações R14 e R15

scripts/calculate_transport.py
  -> calcula matriz S, transmissão e observáveis locais
  -> salva os arquivos .npz

scripts/calculate_spectrum.py
  -> calcula o espectro fechado pela Eq. R23
  -> salva os dados espectrais

scripts/calculate_lead_observables.py
  -> integra transmissões, modos e observáveis locais dos seis leads

scripts/validate_convergence.py
  -> refina a lattice e verifica $SS^\dagger-I$ em toda a faixa
```

## 17. Síntese conceitual

O transporte quântico na cavidade é determinado pela interferência coerente entre todos os caminhos permitidos pelos terminais. A mudança de geometria modifica os caminhos de espalhamento, os estados quasinormais e os padrões espaciais. A condutância revela a resposta global, a densidade mostra a distribuição interna da onda, o fluxo verifica a conservação da probabilidade e o espectro fechado fornece uma referência auxiliar.

Nenhum desses observáveis isoladamente demonstra caos. A conclusão deve ser construída por convergência numérica, unitividade da matriz S, conservação local da corrente e análise consistente entre terminais, energias e indicadores complementares.
