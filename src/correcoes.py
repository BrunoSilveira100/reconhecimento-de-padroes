"""Diagnostico e correcoes automaticas de problemas visuais."""

from __future__ import annotations

from dataclasses import dataclass

import cv2
import numpy as np

from .utils import Imagem


@dataclass(frozen=True)
class MetricasImagem:
    """Metricas simples usadas pelo diagnostico automatico."""

    brilho_medio: float
    contraste: float
    nivel_ruido: float


@dataclass(frozen=True)
class ResultadoCorrecao:
    """Imagem corrigida, diagnostico inicial e correcoes executadas."""

    imagem: Imagem
    metricas_iniciais: MetricasImagem
    metricas_finais: MetricasImagem
    correcoes_aplicadas: tuple[str, ...]


def _cinza(imagem: Imagem) -> Imagem:
    return cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY) if imagem.ndim == 3 else imagem


def calcular_metricas(imagem: Imagem) -> MetricasImagem:
    """Calcula brilho, desvio-padrao de intensidade e estimativa robusta de ruido."""
    cinza = _cinza(imagem)
    mediana = cv2.medianBlur(cinza, 3)
    residuo = cv2.absdiff(cinza, mediana)
    return MetricasImagem(
        brilho_medio=float(np.mean(cinza)),
        contraste=float(np.std(cinza)),
        nivel_ruido=float(np.std(residuo)),
    )


def _corrigir_gamma(imagem: Imagem, gamma: float) -> Imagem:
    gamma = max(0.1, min(gamma, 5.0))
    tabela = np.array([((i / 255.0) ** gamma) * 255 for i in range(256)], dtype=np.uint8)
    return cv2.LUT(imagem, tabela)


def corrigir_imagem_escura(imagem: Imagem, alvo: float = 135.0) -> Imagem:
    """Clareia tons medios por transformacao gamma."""
    media = max(calcular_metricas(imagem).brilho_medio, 1.0) / 255.0
    gamma = np.log(alvo / 255.0) / np.log(media)
    return _corrigir_gamma(imagem, float(gamma))


def corrigir_excesso_brilho(imagem: Imagem, alvo: float = 145.0) -> Imagem:
    """Escurece uma imagem superexposta por transformacao gamma."""
    media = min(calcular_metricas(imagem).brilho_medio, 254.0) / 255.0
    gamma = np.log(alvo / 255.0) / np.log(max(media, 1e-3))
    return _corrigir_gamma(imagem, float(gamma))


def corrigir_baixo_contraste(imagem: Imagem, limite: float = 2.0) -> Imagem:
    """Aumenta contraste local com CLAHE, preservando cores quando presentes."""
    clahe = cv2.createCLAHE(clipLimit=limite, tileGridSize=(8, 8))
    if imagem.ndim == 2:
        return clahe.apply(imagem)
    lab = cv2.cvtColor(imagem, cv2.COLOR_BGR2LAB)
    luminosidade, canal_a, canal_b = cv2.split(lab)
    luminosidade = clahe.apply(luminosidade)
    return cv2.cvtColor(cv2.merge((luminosidade, canal_a, canal_b)), cv2.COLOR_LAB2BGR)


def reduzir_ruido(imagem: Imagem, intensidade: int = 10) -> Imagem:
    """Reduz ruido mantendo bordas com Non-local Means."""
    if imagem.ndim == 2:
        return cv2.fastNlMeansDenoising(imagem, None, intensidade, 7, 21)
    return cv2.fastNlMeansDenoisingColored(
        imagem, None, intensidade, intensidade, 7, 21
    )


def corrigir_automaticamente(
    imagem: Imagem,
    limiar_escura: float = 80.0,
    limiar_clara: float = 190.0,
    limiar_contraste: float = 42.0,
    limiar_ruido: float = 8.0,
) -> ResultadoCorrecao:
    """Diagnostica e corrige problemas visuais de maneira sequencial."""
    if not 0 <= limiar_escura < limiar_clara <= 255:
        raise ValueError("Os limiares de brilho devem satisfazer 0 <= escura < clara <= 255.")
    if limiar_contraste < 0 or limiar_ruido < 0:
        raise ValueError("Os limiares de contraste e ruido nao podem ser negativos.")

    iniciais = calcular_metricas(imagem)
    corrigida = imagem.copy()
    aplicadas: list[str] = []

    if iniciais.brilho_medio < limiar_escura:
        corrigida = corrigir_imagem_escura(corrigida)
        aplicadas.append("correcao de imagem escura")
    elif iniciais.brilho_medio > limiar_clara:
        corrigida = corrigir_excesso_brilho(corrigida)
        aplicadas.append("correcao de excesso de brilho")

    if calcular_metricas(corrigida).contraste < limiar_contraste:
        corrigida = corrigir_baixo_contraste(corrigida)
        aplicadas.append("correcao de baixo contraste")

    if iniciais.nivel_ruido > limiar_ruido:
        corrigida = reduzir_ruido(corrigida)
        aplicadas.append("reducao automatica de ruido")

    if not aplicadas:
        aplicadas.append("nenhuma correcao automatica necessaria")

    return ResultadoCorrecao(
        imagem=corrigida,
        metricas_iniciais=iniciais,
        metricas_finais=calcular_metricas(corrigida),
        correcoes_aplicadas=tuple(aplicadas),
    )
