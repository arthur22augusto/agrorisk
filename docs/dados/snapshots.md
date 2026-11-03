# Snapshots mensais do CAR e da IDE-Sisema

Motivo (`docs/decisoes/escopo-mvp.md` §4): o CAR público e a IDE-Sisema só expõem o estado **vigente**; sem snapshot próprio não há
como saber o que se sabia em t₀. Cada snapshot é congelado com hash; o teste limpo do modelo é prospectivo sobre eles.

## Rodar (todo mês, ~15 min na vitrine; ~1 h no treino)
```bash
pip install -e ".[pipeline]"
python -m agrorisk.fontes.snapshot --recorte vitrine      # grava data/raw/snapshots/<AAAA-MM-DD>/vitrine/
# exemplo de agendamento local (dia 1, 03h): 0 3 1 * * cd /caminho/agrorisk && python -m agrorisk.fontes.snapshot --recorte treino
```
- Conteúdo: CAR (`sicar:sicar_imoveis_mg`, por município) e 6 camadas IDE-Sisema (supressão autorizada IEF e FEAM, embargos estaduais, UCs est./fed./mun.).
- Saída: `manifest.json` com sha256 por arquivo e `hash_snapshot` (sha256 da concatenação dos hashes por ordem de arquivo).
- **Fora do git:** os dados (`data/`). **No git:** só `docs/dados/snapshots_registro.csv` (data, recorte, nº de CARs, hash). Guardar cópia dos dados em armazenamento do fundador (os snapshots não são recuperáveis depois).
- LGPD: removidas as colunas `autorizado` (IEF), `fiscalizad` e `doc_fiscal` (embargos Sisema). O hash vale para o arquivo **já sem** dados pessoais.
- Idempotente: se o diretório do dia já tem `manifest.json`, não baixa de novo.

## Limitações
- Snapshots só existem a partir de 2026-11-03: o retrospectivo 2021–24 continua sendo **exploratório** (geometria atual do CAR).
- A nuvem baixa o CAR sem problema (SICAR WFS via `curl`). Se o SICAR bloquear, o fundador roda o mesmo comando localmente e copia `data/raw/snapshots/` para o ambiente.
