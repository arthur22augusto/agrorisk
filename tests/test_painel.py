"""Testes do pipeline piloto (sessão 07).
Unitários com geometrias sintéticas (sempre rodam) + verificações sobre data/processed/painel_car_t0.parquet (rodam se existir)."""
from pathlib import Path

import pandas as pd
import pytest

gpd = pytest.importorskip("geopandas")
from shapely.geometry import box  # noqa: E402

from agrorisk import gate, painel  # noqa: E402

PAINEL = Path("data/processed/painel_car_t0.parquet")


def test_eventos_contiguidade_minima_1ha():
    # CAR 20 ha; dois polígonos PRODES de 0,6 ha separados (soma 1,2 ha, mas nenhum contíguo >= 1 ha) e um de 1,5 ha em outro ano
    car = gpd.GeoDataFrame({"cod_imovel": ["A"]}, geometry=[box(0, 0, 400, 500)], crs=gate.UTM)
    p = gpd.GeoDataFrame({"year": [2022, 2022, 2023]},
                         geometry=[box(10, 10, 110, 70), box(200, 200, 300, 260), box(10, 100, 150, 207)], crs=gate.UTM)
    ev = gate.eventos(car, p).set_index("year")
    assert round(ev.loc[2022, "ha_total"], 2) == 1.2 and ev.loc[2022, "ha_contiguo"] < 1.0
    assert ev.loc[2023, "ha_contiguo"] >= 1.0


def test_autorizacao_so_conta_com_fracao_minima_e_janela():
    ev = gpd.GeoDataFrame({"year": [2023]}, geometry=[box(0, 0, 100, 100)], crs=gate.UTM)
    ief = gpd.GeoDataFrame({"data_publi": ["10/01/2023", "10/01/2018"]},
                           geometry=[box(0, 0, 100, 50), box(0, 0, 100, 100)], crs=gate.UTM)
    feam = gpd.GeoDataFrame(geometry=[box(95, 0, 200, 100)], crs=gate.UTM)  # só 5% do evento: abaixo de MIN_FRAC_AUT
    a = gate.autorizacao(ev, ief, feam)
    assert bool(a.aut_ief_janela.iloc[0]) and not bool(a.aut_feam_sem_data.iloc[0])


@pytest.mark.skipif(not PAINEL.exists(), reason="painel não construído (python -m agrorisk.pipeline --etapa todas)")
class TestPainel:
    @pytest.fixture(scope="class")
    def p(self):
        return pd.read_parquet(PAINEL)

    def test_unicidade_car_t0(self, p):
        assert not p.duplicated(["cod_imovel", "data_corte"]).any()

    def test_sem_fonte_posterior_a_t0(self, p):
        # PRODES: ano usado + 4 meses de defasagem (fim do ciclo 31/jul) <= t0
        fim = pd.to_datetime(p.prodes_ano_max_usado.astype(str) + "-07-31") + pd.DateOffset(months=4)
        assert (fim <= p.data_corte).all()
        # embargo: data do ato <= t0
        assert (p.embargo_data_min.dropna() <= p.loc[p.embargo_data_min.notna(), "data_corte"]).all()
        # elegibilidade: inscrito há >= 6 meses
        assert (p.idade_car_meses >= 5.9).all()

    def test_colunas_datadas_nao_incluem_vigentes_nem_diagnosticas(self, p):
        assert set(painel.PREDITORES_DATADOS) <= set(p.columns)
        assert not any(c.startswith(("vig_", "diag_", "Y_")) for c in painel.PREDITORES_DATADOS)

    def test_eventos_por_ano_batem_com_o_gate(self, p):
        res = Path("reports/07-gate/eventos_por_ano_vitrine.csv")
        if not res.exists():
            pytest.skip("relatório do gate ausente")
        g = pd.read_csv(res).set_index("year").imoveis_ge_1ha
        pos = p.groupby("ano_prodes").Y_total.sum()
        assert (pos <= g.reindex(pos.index)).all()          # painel é subconjunto (só elegíveis em t0)
        assert (pos > 0).all()

    def test_derivados_respeitam_hierarquia(self, p):
        assert (p.Y_agro <= p.Y_total).all() and (p.Y_ilegal <= p.Y_total).all()
