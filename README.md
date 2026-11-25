# Quantum Transport Quantum Pool

## Estado atual

O projeto utiliza exclusivamente um floco de neve deformado em lattice quadrada, acoplado a seis leads Kwant semi-infinitos. Foram implementados:

- Transmissão e condutância entre os quinze pares de terminais.
- Número de modos propagantes por terminal e energia.
- Densidade local para cada terminal injetor.
- Corrente nos links e divergência local pela Equação R21.
- Espectro fechado auxiliar.
- Validação da unidade da matriz S e convergência em três resoluções.

## Dados

- `data/geometries.npz`
- `data/deformed.npz`
- `data/lead_observables.npz`
- `data/local_deformed.npz`
- `data/spectrum_deformed.npz`
- `data/convergence_validation.npz`

## Documentação

- [Report.md](./DOCS/Report.md): teoria, premissas e equações.
- [Results.md](./DOCS/Results.md): resultados, limitações e rastreabilidade.
- [Problem.md](./DOCS/Problem.md): enunciado, objetivos e metodologia.
- [checklist.md](./checklist.md): estado das tarefas implementadas.