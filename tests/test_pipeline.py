from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import cv2
import numpy as np

from src.correcoes import calcular_metricas, corrigir_automaticamente
from src.main import Configuracao, executar
from src.processamento import processar_imagem
from src.reconhecimento import reconhecer_formas
from src.utils import salvar_imagem


class TestPipeline(unittest.TestCase):
    def setUp(self) -> None:
        self.imagem = np.full((500, 700, 3), 245, dtype=np.uint8)
        cv2.circle(self.imagem, (110, 130), 60, (20, 20, 20), -1)
        cv2.rectangle(self.imagem, (260, 70), (380, 190), (20, 20, 20), -1)
        cv2.fillPoly(
            self.imagem,
            [np.array([[540, 60], [460, 200], [620, 200]], dtype=np.int32)],
            (20, 20, 20),
        )

    def test_reconhece_tres_formas(self) -> None:
        resultado = reconhecer_formas(self.imagem, area_minima=500)
        formas = {objeto.forma for objeto in resultado.objetos}
        self.assertEqual(len(resultado.objetos), 3)
        self.assertTrue({"Circulo", "Quadrado", "Triangulo"}.issubset(formas))

    def test_pipeline_contem_todas_as_etapas(self) -> None:
        resultado = processar_imagem(self.imagem)
        self.assertEqual(len(resultado.etapas), 9)
        self.assertIn("08_bordas_canny", resultado.etapas)

    def test_correcao_clareia_imagem_escura(self) -> None:
        escura = cv2.convertScaleAbs(self.imagem, alpha=0.2)
        antes = calcular_metricas(escura).brilho_medio
        resultado = corrigir_automaticamente(escura)
        self.assertGreater(resultado.metricas_finais.brilho_medio, antes)

    def test_execucao_ponta_a_ponta(self) -> None:
        with tempfile.TemporaryDirectory() as temporario:
            raiz = Path(temporario)
            imagens = raiz / "imagens"
            imagens.mkdir()
            salvar_imagem(imagens / "teste.png", self.imagem)
            codigo = executar(
                Configuracao(imagens, raiz / "resultados", raiz / "relatorio", 500, 50, 150)
            )
            self.assertEqual(codigo, 0)
            self.assertTrue((raiz / "resultados/teste/11_comparacao.png").exists())
            self.assertTrue((raiz / "relatorio/teste.txt").exists())


if __name__ == "__main__":
    unittest.main()

