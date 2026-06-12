"""Segmentacao, classificacao e anotacao de formas geometricas."""

from __future__ import annotations

from dataclasses import dataclass

import cv2
import numpy as np

from .utils import Imagem


@dataclass(frozen=True)
class ObjetoDetectado:
    indice: int
    forma: str
    area: float
    perimetro: float
    circularidade: float
    caixa: tuple[int, int, int, int]


@dataclass(frozen=True)
class ResultadoReconhecimento:
    imagem_anotada: Imagem
    mascara: Imagem
    objetos: tuple[ObjetoDetectado, ...]


def _criar_mascara(imagem: Imagem) -> Imagem:
    cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY) if imagem.ndim == 3 else imagem
    suavizada = cv2.GaussianBlur(cinza, (5, 5), 0)
    _, normal = cv2.threshold(suavizada, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    invertida = cv2.bitwise_not(normal)

    # A polaridade cujo fundo toca menos a borda tende a representar os objetos.
    def ocupacao_borda(mascara: Imagem) -> float:
        borda = np.concatenate((mascara[0], mascara[-1], mascara[:, 0], mascara[:, -1]))
        return float(np.mean(borda > 0))

    mascara = normal if ocupacao_borda(normal) < ocupacao_borda(invertida) else invertida
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mascara = cv2.morphologyEx(mascara, cv2.MORPH_OPEN, kernel, iterations=1)
    return cv2.morphologyEx(mascara, cv2.MORPH_CLOSE, kernel, iterations=2)


def _classificar(contorno: Imagem) -> tuple[str, float, float]:
    perimetro = cv2.arcLength(contorno, True)
    area = cv2.contourArea(contorno)
    circularidade = 4.0 * np.pi * area / (perimetro * perimetro) if perimetro > 0 else 0.0
    aproximacao = cv2.approxPolyDP(contorno, 0.035 * perimetro, True)
    vertices = len(aproximacao)

    if vertices == 3:
        forma = "Triangulo"
    elif vertices == 4:
        x, y, largura, altura = cv2.boundingRect(aproximacao)
        proporcao = largura / max(altura, 1)
        forma = "Quadrado" if 0.80 <= proporcao <= 1.20 else "Quadrilatero"
    elif vertices >= 5 and circularidade >= 0.72:
        forma = "Circulo"
    else:
        forma = "Forma nao identificada"
    return forma, perimetro, float(circularidade)


def reconhecer_formas(
    imagem: Imagem,
    area_minima: float = 250.0,
    area_maxima_relativa: float = 0.90,
) -> ResultadoReconhecimento:
    """Localiza contornos externos, classifica formas e desenha informacoes."""
    if area_minima <= 0:
        raise ValueError("A area minima deve ser positiva.")
    mascara = _criar_mascara(imagem)
    contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    area_imagem = imagem.shape[0] * imagem.shape[1]
    validos = [
        contorno
        for contorno in contornos
        if area_minima <= cv2.contourArea(contorno) <= area_imagem * area_maxima_relativa
    ]
    validos.sort(key=lambda c: (cv2.boundingRect(c)[1], cv2.boundingRect(c)[0]))

    anotada = imagem.copy()
    objetos: list[ObjetoDetectado] = []
    cores = {"Circulo": (0, 255, 0), "Quadrado": (255, 0, 0), "Triangulo": (0, 165, 255)}

    for indice, contorno in enumerate(validos, start=1):
        forma, perimetro, circularidade = _classificar(contorno)
        area = float(cv2.contourArea(contorno))
        x, y, largura, altura = cv2.boundingRect(contorno)
        cor = cores.get(forma, (255, 0, 255))
        cv2.drawContours(anotada, [contorno], -1, cor, 2)
        cv2.rectangle(anotada, (x, y), (x + largura, y + altura), cor, 2)
        texto = f"{indice}: {forma} | A={area:.0f}px2"
        posicao_y = max(20, y - 8)
        cv2.putText(anotada, texto, (x, posicao_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, cor, 2)
        objetos.append(
            ObjetoDetectado(indice, forma, area, perimetro, circularidade, (x, y, largura, altura))
        )

    resumo = f"Objetos encontrados: {len(objetos)}"
    cv2.rectangle(anotada, (5, 5), (310, 35), (0, 0, 0), -1)
    cv2.putText(anotada, resumo, (12, 27), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)
    return ResultadoReconhecimento(anotada, mascara, tuple(objetos))

