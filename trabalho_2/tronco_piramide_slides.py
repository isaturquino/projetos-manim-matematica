from manim import *
from manim_slides import Slide

# ============================================================
# Dedução da fórmula do volume de um tronco de pirâmide
# Apresentação controlada com Manim Slides
#
# Instalação:
#   pip install manim manim-slides
#
# Renderização:
#   manim-slides render tronco_piramide_slides.py TroncoPiramideSlides
#
# Apresentação:
#   manim-slides present TroncoPiramideSlides
#
# Durante a apresentação, use a seta para a direita para avançar.
# ============================================================

config.background_color = ManimColor("#F8F7F1")

DARK = "#1F1F1F"
PURPLE = "#5E1675"
GREEN = "#79B85A"
GREEN_DARK = "#2F7D32"
BLUE = "#2447B2"
ORANGE = "#E86A17"
RED = "#C62828"
GRAY = "#666666"
WHITE_BG = ManimColor("#F8F7F1")

class TroncoPiramideSlides(Slide):
    def titulo(self, texto: str) -> Text:
        titulo = Text(
            texto,
            font_size=28,
            color=PURPLE,
            weight=BOLD,
        ).to_edge(UP, buff=0.42)

        if titulo.width > 12.0:
            titulo.scale_to_fit_width(12.0)

        return titulo

    def limitar_na_tela(self, objeto, largura=12.0, altura=6.1):
        if objeto.width > largura:
            objeto.scale_to_fit_width(largura)
        if objeto.height > altura:
            objeto.scale_to_fit_height(altura)
        return objeto

    def limpar(self, *objetos, tempo=0.55):
        self.play(*[FadeOut(obj) for obj in objetos], run_time=tempo)

    def criar_piramide(self, escala=1.0):
        """Cria uma representação 2D da pirâmide completa e do tronco."""
        v = np.array([0.0, 2.65, 0.0])
        a = np.array([-2.15, -2.05, 0.0])
        b = np.array([1.05, -2.05, 0.0])
        c = np.array([2.15, -1.25, 0.0])
        d = np.array([-1.05, -1.25, 0.0])

        ap = interpolate(v, a, 0.43)
        bp = interpolate(v, b, 0.43)
        cp = interpolate(v, c, 0.43)
        dp = interpolate(v, d, 0.43)

        tronco_frente = Polygon(
            ap, bp, b, a,
            fill_color=GREEN,
            fill_opacity=0.58,
            stroke_color=GREEN_DARK,
            stroke_width=3,
        )
        tronco_lado = Polygon(
            bp, cp, c, b,
            fill_color=GREEN,
            fill_opacity=0.42,
            stroke_color=GREEN_DARK,
            stroke_width=3,
        )
        base_superior = Polygon(
            ap, bp, cp, dp,
            fill_color="#B9D99F",
            fill_opacity=0.9,
            stroke_color=GREEN_DARK,
            stroke_width=3,
        )

        arestas = VGroup(
            Line(v, a, color=GRAY, stroke_width=2),
            Line(v, b, color=GRAY, stroke_width=2),
            DashedLine(v, c, color=GRAY, stroke_width=2),
            DashedLine(v, d, color=GRAY, stroke_width=2),
            Line(a, b, color=GREEN_DARK, stroke_width=3),
            Line(b, c, color=GREEN_DARK, stroke_width=3),
            DashedLine(c, d, color=GREEN_DARK, stroke_width=2),
            DashedLine(d, a, color=GREEN_DARK, stroke_width=2),
        )

        corte = VGroup(
            Line(ap, bp, color=GREEN_DARK, stroke_width=3),
            Line(bp, cp, color=GREEN_DARK, stroke_width=3),
            DashedLine(cp, dp, color=GREEN_DARK, stroke_width=2),
            DashedLine(dp, ap, color=GREEN_DARK, stroke_width=2),
        )

        centro_base = (a + b + c + d) / 4
        centro_corte = (ap + bp + cp + dp) / 4

        altura_total = DoubleArrow(
            start=centro_base + LEFT * 2.7,
            end=v + LEFT * 2.7,
            buff=0,
            color=DARK,
            stroke_width=2,
            tip_length=0.13,
        )
        altura_d = DoubleArrow(
            start=centro_corte + LEFT * 2.25,
            end=v + LEFT * 2.25,
            buff=0,
            color=BLUE,
            stroke_width=2,
            tip_length=0.13,
        )
        altura_k = DoubleArrow(
            start=centro_base + LEFT * 2.25,
            end=centro_corte + LEFT * 2.25,
            buff=0,
            color=ORANGE,
            stroke_width=2,
            tip_length=0.13,
        )

        labels = VGroup(
            MathTex("V", color=DARK).scale(0.65).next_to(v, UP, buff=0.08),
            MathTex("S_B", color=GREEN_DARK).scale(0.54).move_to(centro_base + DOWN * 0.18),
            MathTex("S_b", color=GREEN_DARK).scale(0.70).move_to(centro_corte + UP * 0.05),
            MathTex("h", color=DARK).scale(0.48).next_to(altura_total, LEFT, buff=0.08),
            MathTex("d", color=BLUE).scale(0.68).next_to(altura_d, RIGHT, buff=0.08),
            MathTex("k", color=ORANGE).scale(0.68).next_to(altura_k, RIGHT, buff=0.08),
        )

        grupo = VGroup(
            tronco_frente,
            tronco_lado,
            base_superior,
            arestas,
            corte,
            altura_total,
            altura_d,
            altura_k,
            labels,
        ).scale(escala)

        return grupo, VGroup(tronco_frente, tronco_lado, base_superior), arestas, corte, labels

    def construct(self):
        self.camera.background_color = WHITE_BG

        self.abertura()
        self.geometria_e_notacao()
        self.diferenca_de_volumes()
        self.semelhanca()
        self.altura_d()
        self.altura_h()
        self.substituicao()
        self.diferenca_de_cubos()
        self.simplificacao_final()
        self.encerramento()

    def abertura(self):
        titulo = Text(
            "Volume de um tronco de pirâmide",
            font_size=44,
            color=PURPLE,
            weight=BOLD,
        )
        subtitulo = Text(
            "Dedução da fórmula",
            font_size=28,
            color=DARK,
        )
        grupo = VGroup(titulo, subtitulo).arrange(DOWN, buff=0.3)

        self.play(FadeIn(grupo, shift=UP), run_time=0.9)
        self.next_slide()
        self.play(FadeOut(grupo), run_time=0.55)

    def geometria_e_notacao(self):
        titulo = self.titulo("1. Geometria e notação")
        piramide, tronco, arestas, corte, labels = self.criar_piramide(0.70)
        piramide.move_to(RIGHT * 3.55 + DOWN * 0.28)

        dados = VGroup(
            MathTex(r"S_B:\ \text{área da base maior}", color=DARK),
            MathTex(r"S_b:\ \text{área da base menor}", color=DARK),
            MathTex(r"h:\ \text{altura da pirâmide maior}", color=DARK),
            MathTex(r"d:\ \text{altura da pirâmide menor}", color=DARK),
            MathTex(r"k:\ \text{altura do tronco}", color=DARK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.30).scale(0.55)
        dados.move_to(LEFT * 3.25 + UP * 0.25)

        relacao = MathTex(r"h=d+k", color=PURPLE).scale(0.78)
        relacao.next_to(dados, DOWN, buff=0.45).align_to(dados, LEFT)

        self.play(Write(titulo))
        self.play(FadeIn(piramide, shift=LEFT), run_time=1.0)
        self.play(LaggedStart(*[Write(item) for item in dados], lag_ratio=0.18))
        self.play(Write(relacao))
        self.next_slide()

        self.piramide = piramide
        self.play(FadeOut(dados), FadeOut(relacao), FadeOut(titulo))

    def diferenca_de_volumes(self):
        titulo = self.titulo("2. O tronco como diferença de duas pirâmides")
        self.play(Write(titulo))

        self.play(self.piramide.animate.scale(0.82).move_to(LEFT * 3.35 + DOWN * 0.30))

        texto = Text(
            "O volume do tronco é o volume da pirâmide maior\nmenos o volume da pirâmide menor.",
            font_size=20,
            color=DARK,
            line_spacing=1.2,
        ).move_to(RIGHT * 3.05 + UP * 1.25)

        eq0 = MathTex(
            r"V_{\text{tronco}}=V_{\text{maior}}-V_{\text{menor}}",
            color=DARK,
        ).scale(0.62)
        eq1 = MathTex(
            r"V_{\text{tronco}}=\frac13S_Bh-\frac13S_bd",
            color=DARK,
        ).scale(0.68)
        eq2 = MathTex(
            r"V_{\text{tronco}}=\frac13\left(S_Bh-S_bd\right)",
            color=PURPLE,
        ).scale(0.72)

        eqs = VGroup(eq0, eq1, eq2).arrange(DOWN, buff=0.45)
        eqs.move_to(RIGHT * 3.05 + DOWN * 0.95)

        self.play(Write(texto))
        self.play(Write(eq0))
        self.next_slide()
        self.play(TransformMatchingTex(eq0.copy(), eq1))
        self.next_slide()
        self.play(Write(eq2))
        destaque = SurroundingRectangle(eq2, color=ORANGE, buff=0.16)
        self.play(Create(destaque))
        self.next_slide()

        self.formula_inicial = eq2.copy()
        self.limpar(titulo, texto, eq0, eq1, eq2, destaque, self.piramide)

    def semelhanca(self):
        titulo = self.titulo("3. Semelhança entre as pirâmides")
        piramide, *_ = self.criar_piramide(0.60)
        piramide.move_to(RIGHT * 3.60 + DOWN * 0.28)

        texto = Text(
            "As duas pirâmides são semelhantes.\nPor isso, a razão entre as áreas das bases\né o quadrado da razão entre as alturas.",
            font_size=19,
            color=DARK,
            line_spacing=1.15,
        ).move_to(LEFT * 3.10 + UP * 1.10)

        eq1 = MathTex(
            r"\frac{S_b}{S_B}=\left(\frac{d}{h}\right)^2",
            color=DARK,
        ).scale(0.78)
        eq2 = MathTex(
            r"\frac{d}{h}=\frac{\sqrt{S_b}}{\sqrt{S_B}}",
            color=PURPLE,
        ).scale(0.78)
        eqs = VGroup(eq1, eq2).arrange(DOWN, buff=0.50)
        eqs.move_to(LEFT * 3.10 + DOWN * 1.10)

        self.play(Write(titulo), FadeIn(piramide))
        self.play(Write(texto))
        self.next_slide()
        self.play(Write(eq1))
        self.next_slide()
        self.play(TransformMatchingTex(eq1.copy(), eq2))
        destaque = SurroundingRectangle(eq2, color=ORANGE, buff=0.16)
        self.play(Create(destaque))
        self.next_slide()

        self.limpar(titulo, texto, eq1, eq2, destaque, piramide)

    def altura_d(self):
        titulo = self.titulo("4. Encontrando a altura da pirâmide menor")
        self.play(Write(titulo))

        eqs = [
            MathTex(r"\frac{d}{h}=\frac{\sqrt{S_b}}{\sqrt{S_B}}", color=DARK),
            MathTex(r"d\sqrt{S_B}=h\sqrt{S_b}", color=DARK),
            MathTex(r"d\sqrt{S_B}=(d+k)\sqrt{S_b}", color=DARK),
            MathTex(r"d\sqrt{S_B}=d\sqrt{S_b}+k\sqrt{S_b}", color=DARK),
            MathTex(r"d\left(\sqrt{S_B}-\sqrt{S_b}\right)=k\sqrt{S_b}", color=DARK),
            MathTex(
                r"d=\frac{k\sqrt{S_b}}{\sqrt{S_B}-\sqrt{S_b}}",
                color=PURPLE,
            ),
        ]
        grupo = VGroup(*eqs).arrange(DOWN, buff=0.27).scale(0.64)
        grupo.move_to(ORIGIN).shift(DOWN * 0.20)
        self.limitar_na_tela(grupo, largura=11.5, altura=5.7)

        observacao = MathTex(r"h=d+k", color=ORANGE).scale(0.58)
        observacao.move_to(RIGHT * 5.25 + UP * 2.55)

        self.play(Write(observacao))
        for i, eq in enumerate(eqs):
            self.play(Write(eq), run_time=0.75)
            if i in (1, 2, 4):
                self.next_slide()

        caixa = SurroundingRectangle(eqs[-1], color=ORANGE, buff=0.17)
        self.play(Create(caixa))
        self.next_slide()

        self.limpar(titulo, grupo, observacao, caixa)

    def altura_h(self):
        titulo = self.titulo("5. Encontrando a altura da pirâmide maior")
        self.play(Write(titulo))

        eqs = [
            MathTex(r"h=d+k", color=DARK),
            MathTex(
                r"h=\frac{k\sqrt{S_b}}{\sqrt{S_B}-\sqrt{S_b}}+k",
                color=DARK,
            ),
            MathTex(
                r"h=\frac{k\sqrt{S_b}+k\sqrt{S_B}-k\sqrt{S_b}}{\sqrt{S_B}-\sqrt{S_b}}",
                color=DARK,
            ),
            MathTex(
                r"h=\frac{k\sqrt{S_B}}{\sqrt{S_B}-\sqrt{S_b}}",
                color=PURPLE,
            ),
        ]
        grupo = VGroup(*eqs).arrange(DOWN, buff=0.43).scale(0.67)
        grupo.move_to(ORIGIN).shift(DOWN * 0.10)
        self.limitar_na_tela(grupo, largura=11.4, altura=5.7)

        for i, eq in enumerate(eqs):
            self.play(Write(eq), run_time=0.85)
            self.next_slide()

        caixa = SurroundingRectangle(eqs[-1], color=ORANGE, buff=0.17)
        self.play(Create(caixa))
        self.next_slide()

        self.limpar(titulo, grupo, caixa)

    def substituicao(self):
        titulo = self.titulo("6. Substituindo as alturas na fórmula do volume")
        self.play(Write(titulo))

        eq1 = MathTex(
            r"V_{\text{tronco}}=\frac13\left(S_Bh-S_bd\right)",
            color=DARK,
        ).scale(0.66)

        eq2 = MathTex(
            r"V_{\text{tronco}}=\frac13\left["
            r"S_B\left(\frac{k\sqrt{S_B}}{\sqrt{S_B}-\sqrt{S_b}}\right)"
            r"-S_b\left(\frac{k\sqrt{S_b}}{\sqrt{S_B}-\sqrt{S_b}}\right)"
            r"\right]",
            color=DARK,
        ).scale(0.72)

        eq3 = MathTex(
            r"V_{\text{tronco}}=\frac{k}{3}"
            r"\left[\frac{(\sqrt{S_B})^3-(\sqrt{S_b})^3}"
            r"{\sqrt{S_B}-\sqrt{S_b}}\right]",
            color=PURPLE,
        ).scale(0.66)

        grupo = VGroup(eq1, eq2, eq3).arrange(DOWN, buff=0.48)
        grupo.move_to(ORIGIN).shift(DOWN * 0.10)
        self.limitar_na_tela(grupo, largura=11.6, altura=5.6)

        self.play(Write(eq1))
        self.next_slide()
        self.play(Write(eq2))
        self.next_slide()
        self.play(Write(eq3))
        caixa = SurroundingRectangle(eq3, color=ORANGE, buff=0.16)
        self.play(Create(caixa))
        self.next_slide()

        self.limpar(titulo, grupo, caixa)

    def diferenca_de_cubos(self):
        titulo = self.titulo("7. Aplicando a diferença de dois cubos")
        self.play(Write(titulo))

        identidade = MathTex(
            r"x^3-y^3=(x-y)(x^2+xy+y^2)",
            color=PURPLE,
        ).scale(0.82)
        caixa_id = SurroundingRectangle(identidade, color=BLUE, buff=0.22)
        grupo_id = VGroup(identidade, caixa_id).shift(UP * 1.65)

        substituicao = MathTex(
            r"x=\sqrt{S_B}\qquad y=\sqrt{S_b}",
            color=DARK,
        ).scale(0.66)

        aplicacao1 = MathTex(
            r"(\sqrt{S_B})^3-(\sqrt{S_b})^3="
            r"(\sqrt{S_B}-\sqrt{S_b})"
            r"\left[(\sqrt{S_B})^2+\sqrt{S_BS_b}+(\sqrt{S_b})^2\right]",
            color=DARK,
        ).scale(0.68)

        aplicacao2 = MathTex(
            r"(\sqrt{S_B})^3-(\sqrt{S_b})^3="
            r"(\sqrt{S_B}-\sqrt{S_b})"
            r"\left(S_B+\sqrt{S_BS_b}+S_b\right)",
            color=PURPLE,
        ).scale(0.56)

        parte_baixa = VGroup(substituicao, aplicacao1, aplicacao2).arrange(DOWN, buff=0.42)
        parte_baixa.shift(DOWN * 0.65)
        self.limitar_na_tela(parte_baixa, largura=11.7, altura=4.5)

        self.play(Write(identidade), Create(caixa_id))
        self.next_slide()
        self.play(Write(substituicao))
        self.next_slide()
        self.play(Write(aplicacao1))
        self.next_slide()
        self.play(Write(aplicacao2))
        self.next_slide()

        self.limpar(titulo, grupo_id, parte_baixa)

    def simplificacao_final(self):
        titulo = self.titulo("8. Simplificação e fórmula final")
        self.play(Write(titulo))

        eq1 = MathTex(
            r"V_{\text{tronco}}=\frac{k}{3}"
            r"\left[\frac{"
            r"(\sqrt{S_B}-\sqrt{S_b})"
            r"(S_B+\sqrt{S_BS_b}+S_b)"
            r"}{\sqrt{S_B}-\sqrt{S_b}}\right]",
            color=DARK,
        ).scale(0.60)

        eq2 = MathTex(
            r"V_{\text{tronco}}=\frac{k}{3}"
            r"\left(S_B+\sqrt{S_BS_b}+S_b\right)",
            color=PURPLE,
        ).scale(0.80)

        eq1.shift(UP * 0.90)
        eq2.shift(DOWN * 0.75)

        self.play(Write(eq1))
        self.next_slide()

        # O cancelamento é indicado por linhas vermelhas desenhadas pelo Manim.
        # Assim, não dependemos do pacote LaTeX \texttt{cancel}.
        linha1 = Line(
            eq1.get_center() + LEFT * 1.55 + UP * 0.27,
            eq1.get_center() + LEFT * 0.10 + UP * 0.02,
            color=RED,
            stroke_width=4,
        )
        linha2 = Line(
            eq1.get_center() + LEFT * 1.35 + DOWN * 0.20,
            eq1.get_center() + LEFT * 0.05 + DOWN * 0.45,
            color=RED,
            stroke_width=4,
        )

        self.play(Create(linha1), Create(linha2))
        self.next_slide()
        self.play(Write(eq2))
        caixa = SurroundingRectangle(eq2, color=ORANGE, buff=0.22, stroke_width=4)
        self.play(Create(caixa))
        self.next_slide()

        self.formula_final = VGroup(eq2, caixa)
        self.limpar(titulo, eq1, linha1, linha2)

    def encerramento(self):
        titulo = Text(
            "Fórmula do volume do tronco de pirâmide",
            font_size=28,
            color=PURPLE,
            weight=BOLD,
        ).to_edge(UP, buff=0.42)

        formula = MathTex(
            r"\boxed{V_{\text{tronco}}=\frac{k}{3}"
            r"\left(S_B+\sqrt{S_BS_b}+S_b\right)}",
            color=DARK,
        ).scale(0.86)

        legenda = VGroup(
            MathTex(r"k=\text{altura do tronco}", color=DARK),
            MathTex(r"S_B=\text{área da base maior}", color=DARK),
            MathTex(r"S_b=\text{área da base menor}", color=DARK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).scale(0.56)
        legenda.next_to(formula, DOWN, buff=0.52)

        self.play(FadeOut(self.formula_final))
        self.play(FadeIn(titulo, shift=UP))
        self.play(Write(formula))
        self.play(LaggedStart(*[Write(item) for item in legenda], lag_ratio=0.20))
        self.next_slide()