"""Pipeline de processamento digital de imagens."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import cv2
import matplotlib
import numpy as np

matplotlib.use("Agg")
from matplotlib import pyplot as plt

from .correcoes import ResultadoCorrecao, corrigir_automaticamente, reduzir_ruido
from .utils import Imagem, salvar_imagem


@dataclass(frozen=True)
class ResultadoProcessamento:
    """Resultados em memoria e lista dos processamentos executados."""

    etapas: dict[str, Imagem]
    correcao: ResultadoCorrecao
    processamentos_aplicados: tuple[str, ...]


def converter_escala_cinza(imagem: Imagem) -> Imagem:
    return cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY) if imagem.ndim == 3 else imagem.copy()


def ajustar_brilho(imagem: Imagem, alvo: float = 128.0) -> Imagem:
    """Desloca intensidades para aproximar o brilho medio do alvo."""
    beta = alvo - float(np.mean(imagem))
    ajustada = imagem.astype(np.float32) + beta
    return np.clip(ajustada, 0, 255).astype(np.uint8)


def ajustar_contraste(imagem: Imagem, contraste_alvo: float = 64.0) -> Imagem:
    """Escala intensidades ao redor da media para melhorar o contraste global."""
    desvio = float(np.std(imagem))
    alpha = min(3.0, contraste_alvo / max(desvio, 1.0))
    media = float(np.mean(imagem))
    ajustada = (imagem.astype(np.float32) - media) * alpha + media
    return np.clip(ajustada, 0, 255).astype(np.uint8)


def aplicar_filtro_gaussiano(imagem: Imagem, tamanho: int = 5) -> Imagem:
    if tamanho < 3 or tamanho % 2 == 0:
        raise ValueError("O tamanho do filtro Gaussiano deve ser impar e >= 3.")
    return cv2.GaussianBlur(imagem, (tamanho, tamanho), 0)


def equalizar_histograma(imagem: Imagem) -> Imagem:
    return cv2.equalizeHist(converter_escala_cinza(imagem))


def detectar_bordas(imagem: Imagem, limiar_baixo: int = 50, limiar_alto: int = 150) -> Imagem:
    if not 0 <= limiar_baixo < limiar_alto <= 255:
        raise ValueError("Os limiares de Canny devem satisfazer 0 <= baixo < alto <= 255.")
    return cv2.Canny(converter_escala_cinza(imagem), limiar_baixo, limiar_alto)


def processar_imagem(
    imagem: Imagem,
    tamanho_gaussiano: int = 5,
    canny_baixo: int = 50,
    canny_alto: int = 150,
    limiar_escura: float = 80.0,
    limiar_clara: float = 190.0,
    limiar_contraste: float = 42.0,
    limiar_ruido: float = 8.0,
) -> ResultadoProcessamento:
    """Executa as correcoes e todas as transformacoes obrigatorias."""
    correcao = corrigir_automaticamente(
        imagem,
        limiar_escura=limiar_escura,
        limiar_clara=limiar_clara,
        limiar_contraste=limiar_contraste,
        limiar_ruido=limiar_ruido,
    )
    cinza = converter_escala_cinza(correcao.imagem)
    brilho = ajustar_brilho(cinza)
    contraste = ajustar_contraste(brilho)
    gaussiano = aplicar_filtro_gaussiano(contraste, tamanho_gaussiano)
    equalizada = equalizar_histograma(gaussiano)
    sem_ruido = reduzir_ruido(equalizada)
    bordas = detectar_bordas(sem_ruido, canny_baixo, canny_alto)

    etapas = {
        "00_original": imagem,
        "01_correcao_automatica": correcao.imagem,
        "02_escala_cinza": cinza,
        "03_ajuste_brilho": brilho,
        "04_ajuste_contraste": contraste,
        "05_filtro_gaussiano": gaussiano,
        "06_equalizacao_histograma": equalizada,
        "07_reducao_ruido": sem_ruido,
        "08_bordas_canny": bordas,
    }
    obrigatorios = (
        "conversao para escala de cinza",
        "ajuste de brilho",
        "ajuste de contraste",
        "filtro Gaussiano",
        "equalizacao de histograma",
        "reducao de ruido",
        "deteccao de bordas Canny",
    )
    return ResultadoProcessamento(
        etapas=etapas,
        correcao=correcao,
        processamentos_aplicados=correcao.correcoes_aplicadas + obrigatorios,
    )


def salvar_etapas(resultado: ResultadoProcessamento, diretorio: Path) -> None:
    for nome, imagem in resultado.etapas.items():
        salvar_imagem(diretorio / f"{nome}.png", imagem)


def salvar_comparacao(original: Imagem, processada: Imagem, caminho: Path) -> None:
    """Cria comparacao lado a lado pronta para documentacao academica."""
    caminho.parent.mkdir(parents=True, exist_ok=True)
    figura, eixos = plt.subplots(1, 2, figsize=(12, 6))
    eixos[0].imshow(cv2.cvtColor(original, cv2.COLOR_BGR2RGB))
    eixos[0].set_title("Imagem original")
    eixos[1].imshow(cv2.cvtColor(processada, cv2.COLOR_BGR2RGB))
    eixos[1].set_title("Imagem processada e reconhecida")
    for eixo in eixos:
        eixo.axis("off")
    figura.tight_layout()
    figura.savefig(caminho, dpi=160, bbox_inches="tight")
    plt.close(figura)
