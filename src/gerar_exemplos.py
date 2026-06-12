"""Gera imagens geometricas controladas para demonstracao e testes manuais."""

from __future__ import annotations

import argparse
from pathlib import Path

import cv2
import numpy as np

from .utils import criar_diretorios, salvar_imagem

RAIZ_PROJETO = Path(__file__).resolve().parent.parent


def _base(valor: int = 245) -> np.ndarray:
    return np.full((600, 800, 3), valor, dtype=np.uint8)


def gerar_imagens(diretorio: Path) -> list[Path]:
    """Cria casos normal, escuro, claro, baixo contraste e ruidoso."""
    criar_diretorios(diretorio)
    rng = np.random.default_rng(42)
    criadas: list[Path] = []

    normal = _base()
    cv2.circle(normal, (150, 170), 80, (20, 20, 190), -1)
    cv2.rectangle(normal, (330, 90), (490, 250), (20, 160, 20), -1)
    cv2.fillPoly(normal, [np.array([[650, 80], [560, 250], [740, 250]])], (190, 30, 30))
    cv2.circle(normal, (250, 440), 65, (100, 20, 170), -1)
    cv2.rectangle(normal, (500, 350), (650, 500), (20, 140, 160), -1)

    casos = {
        "formas_multiplas.png": normal,
        "formas_escuras.png": cv2.convertScaleAbs(normal, alpha=0.30, beta=0),
        "formas_brilho_excessivo.png": cv2.convertScaleAbs(normal, alpha=0.35, beta=165),
        "formas_baixo_contraste.png": cv2.convertScaleAbs(normal, alpha=0.18, beta=175),
    }
    ruido = rng.normal(0, 30, normal.shape).astype(np.int16)
    casos["formas_com_ruido.png"] = np.clip(normal.astype(np.int16) + ruido, 0, 255).astype(np.uint8)

    for nome, imagem in casos.items():
        caminho = diretorio / nome
        salvar_imagem(caminho, imagem)
        criadas.append(caminho)
    return criadas


def main() -> None:
    parser = argparse.ArgumentParser(description="Gera imagens geometricas de exemplo.")
    parser.add_argument("--saida", type=Path, default=RAIZ_PROJETO / "imagens")
    argumentos = parser.parse_args()
    for caminho in gerar_imagens(argumentos.saida):
        print(f"Criada: {caminho}")


if __name__ == "__main__":
    main()

