from manim import *

# ============================================================
# Exercício 37 - Bandeira do Brasil
#
# Para rodar:
# python -m manim -pql exercicio37.py Exercicio37
#
# Qualidade alta:
# python -m manim -pqh exercicio37.py Exercicio37
#
# Observação:
# Usa MathTex, então precisa do MiKTeX/LaTeX funcionando.
# ============================================================

config.background_color = "#F8F7F1"

DARK = "#1F1F1F"
GREEN = "#148B3D"
YELLOW = "#F7D84A"
BLUE = "#2447B2"
PURPLE = "#5E1675"
ORANGE = "#E86A17"
GRAY = "#616161"
RED = "#C62828"
WHITE_BG = "#F8F7F1"


class Exercicio37(Scene):
    def titulo(self, texto):
        return Text(
            texto,
            font_size=30,
            color=PURPLE,
            weight=BOLD
        ).to_edge(UP, buff=0.35)

    def limpar(self, *objs):
        self.play(*[FadeOut(obj) for obj in objs], run_time=0.6)

    def criar_bandeira_com_medidas(self, escala=1):
        ret = Rectangle(
            width=5.6 * escala,
            height=3.92 * escala,
            color=GREEN,
            fill_color=GREEN,
            fill_opacity=1,
            stroke_width=3
        )

        margem = 0.48 * escala

        topo = ret.get_top() + DOWN * margem
        direita = ret.get_right() + LEFT * margem
        baixo = ret.get_bottom() + UP * margem
        esquerda = ret.get_left() + RIGHT * margem

        losango = Polygon(
            topo,
            direita,
            baixo,
            esquerda,
            color=YELLOW,
            fill_color=YELLOW,
            fill_opacity=1,
            stroke_width=3
        )

        circulo = Circle(
            radius=0.95 * escala,
            color=BLUE,
            fill_color=BLUE,
            fill_opacity=1,
            stroke_width=3
        )

        medida_comprimento = MathTex(r"200\,cm", color=DARK).scale(0.58 * escala / 0.82)
        medida_comprimento.next_to(ret, DOWN, buff=0.12)

        medida_largura = MathTex(r"140\,cm", color=DARK).scale(0.58 * escala / 0.82)
        medida_largura.next_to(ret, RIGHT, buff=0.12)

        medida_raio = MathTex(r"r=35\,cm", color=WHITE).scale(0.52 * escala / 0.82)
        medida_raio.move_to(circulo.get_center())

        dist_topo = MathTex(r"17\,cm", color=RED).scale(0.46 * escala / 0.82)
        dist_topo.move_to(ret.get_top() + DOWN * (0.33 * escala / 0.82) + RIGHT * (1.05 * escala / 0.82))

        dist_lado = MathTex(r"17\,cm", color=RED).scale(0.46 * escala / 0.82)
        dist_lado.move_to(ret.get_right() + LEFT * (0.34 * escala / 0.82) + DOWN * (0.65 * escala / 0.82))

        medidas = VGroup(
            medida_comprimento,
            medida_largura,
            medida_raio,
            dist_topo,
            dist_lado
        )

        bandeira = VGroup(ret, losango, circulo)
        bandeira_com_medidas = VGroup(bandeira, medidas)

        return bandeira_com_medidas, bandeira, ret, losango, circulo, medidas

    def construct(self):
        self.camera.background_color = WHITE_BG

        self.abertura()
        self.parte_1_enunciado()
        self.parte_2_area_total()
        self.parte_3_losango()
        self.parte_4_verde()
        self.parte_5_circulo()
        self.parte_6_amarelo()
        self.parte_7_porcentagem()
        self.resposta_final()

    def abertura(self):
        titulo = Text(
            "Exercício 37",
            font_size=46,
            color=PURPLE,
            weight=BOLD
        )

        subtitulo = Text(
            "Áreas na Bandeira do Brasil",
            font_size=28,
            color=DARK
        )

        grupo = VGroup(titulo, subtitulo).arrange(DOWN, buff=0.3)

        self.play(FadeIn(grupo, shift=UP))
        self.wait(2)
        self.play(FadeOut(grupo))

    def parte_1_enunciado(self):
        titulo = self.titulo("1. Interpretando o enunciado")
        self.play(Write(titulo))

        bandeira_com_medidas, bandeira, ret, losango, circulo, medidas = self.criar_bandeira_com_medidas(0.82)
        bandeira_com_medidas.to_edge(RIGHT, buff=0.65).shift(DOWN * 0.12)

        dados = VGroup(
            Text("Retângulo: 2 m por 1,40 m", font_size=23, color=DARK),
            Text("Vértices do losango: 17 cm dos lados", font_size=23, color=DARK),
            Text("Raio do círculo: 35 cm", font_size=23, color=DARK),
            Text("Usar π = 22/7", font_size=23, color=DARK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        dados.to_edge(LEFT, buff=0.7).shift(UP * 0.85)

        conversao = VGroup(
            MathTex(r"2\,m=200\,cm", color=PURPLE),
            MathTex(r"1{,}40\,m=140\,cm", color=PURPLE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).scale(0.75)
        conversao.next_to(dados, DOWN, buff=0.45).align_to(dados, LEFT)

        self.play(Write(dados))
        self.play(Write(conversao))
        self.play(FadeIn(bandeira_com_medidas))
        self.wait(3)

        self.bandeira_data = (bandeira_com_medidas, bandeira, ret, losango, circulo, medidas)

        self.limpar(titulo, dados, conversao)

    def parte_2_area_total(self):
        bandeira_com_medidas, bandeira, ret, losango, circulo, medidas = self.bandeira_data

        titulo = self.titulo("2. Calculando a área total da bandeira")
        self.play(Write(titulo))

        self.play(
            bandeira_com_medidas.animate.scale(0.82).to_edge(LEFT, buff=0.55).shift(DOWN * 0.1),
            run_time=1.0
        )

        explicacao = Text(
            "A área total é a área do retângulo.",
            font_size=23,
            color=DARK
        ).next_to(titulo, DOWN, buff=0.35)

        eq1 = MathTex(r"A_{\text{total}}=base\cdot altura", color=DARK).scale(0.78)
        eq2 = MathTex(r"A_{\text{total}}=200\cdot140", color=DARK).scale(0.78)
        eq3 = MathTex(r"A_{\text{total}}=28000\,cm^2", color=PURPLE).scale(0.82)

        eqs = VGroup(eq1, eq2, eq3).arrange(DOWN, aligned_edge=LEFT, buff=0.42)
        eqs.to_edge(RIGHT, buff=1.0).shift(UP * 0.1)

        contorno = SurroundingRectangle(ret, color=GREEN, buff=0.03, stroke_width=5)

        self.play(Write(explicacao))
        self.wait(1)
        self.play(FadeOut(explicacao))
        self.play(Create(contorno))

        for eq in eqs:
            self.play(Write(eq), run_time=0.8)

        destaque = SurroundingRectangle(eq3, color=ORANGE, buff=0.18)
        self.play(Create(destaque))
        self.wait(2)

        self.limpar(titulo, contorno, eqs, destaque)

    def parte_3_losango(self):
        bandeira_com_medidas, bandeira, ret, losango, circulo, medidas = self.bandeira_data

        titulo = self.titulo("3. Calculando a área do losango")
        self.play(Write(titulo))

        vertices = losango.get_vertices()
        topo, direita, baixo, esquerda = vertices[0], vertices[1], vertices[2], vertices[3]

        diagonal_maior = DashedLine(esquerda, direita, color=PURPLE, stroke_width=4)
        diagonal_menor = DashedLine(topo, baixo, color=PURPLE, stroke_width=4)

        texto = Text(
            "Como o losango fica a 17 cm dos lados, subtraímos duas margens.",
            font_size=21,
            color=DARK
        ).next_to(titulo, DOWN, buff=0.35)

        self.play(Write(texto))
        self.wait(1.3)
        self.play(FadeOut(texto))

        self.play(Create(diagonal_maior), Create(diagonal_menor))

        d1 = MathTex(r"D=200-2\cdot17", color=DARK).scale(0.72)
        d2 = MathTex(r"D=166\,cm", color=PURPLE).scale(0.76)
        d3 = MathTex(r"d=140-2\cdot17", color=DARK).scale(0.72)
        d4 = MathTex(r"d=106\,cm", color=PURPLE).scale(0.76)

        diagonais = VGroup(d1, d2, d3, d4).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        diagonais.to_edge(RIGHT, buff=1.0).shift(UP * 0.35)

        for item in diagonais:
            self.play(Write(item), run_time=0.7)

        self.wait(1)
        self.play(FadeOut(diagonais))

        a1 = MathTex(r"A_{\text{losango}}=\frac{D\cdot d}{2}", color=DARK).scale(0.78)
        a2 = MathTex(r"A_{\text{losango}}=\frac{166\cdot106}{2}", color=DARK).scale(0.76)
        a3 = MathTex(r"A_{\text{losango}}=8798\,cm^2", color=PURPLE).scale(0.82)

        area_losango = VGroup(a1, a2, a3).arrange(DOWN, aligned_edge=LEFT, buff=0.38)
        area_losango.to_edge(RIGHT, buff=0.85).shift(UP * 0.15)

        for item in area_losango:
            self.play(Write(item), run_time=0.8)

        destaque = SurroundingRectangle(a3, color=ORANGE, buff=0.18)
        self.play(Create(destaque))
        self.wait(2)

        self.limpar(titulo, diagonal_maior, diagonal_menor, area_losango, destaque)

    def parte_4_verde(self):
        bandeira_com_medidas, bandeira, ret, losango, circulo, medidas = self.bandeira_data

        titulo = self.titulo("4. Área da região verde")
        self.play(Write(titulo))

        texto = Text(
            "A parte verde é o retângulo menos o losango.",
            font_size=23,
            color=DARK
        ).next_to(titulo, DOWN, buff=0.35)

        contorno_ret = SurroundingRectangle(ret, color=GREEN, buff=0.03, stroke_width=5)

        contorno_los = Polygon(
            *losango.get_vertices(),
            color=ORANGE,
            fill_opacity=0,
            stroke_width=5
        )

        self.play(Write(texto))
        self.wait(1.2)
        self.play(FadeOut(texto))

        self.play(Create(contorno_ret))
        self.play(Create(contorno_los))

        eq1 = MathTex(
            r"A_{\text{verde}}=A_{\text{total}}-A_{\text{losango}}",
            color=DARK
        ).scale(0.72)

        eq2 = MathTex(
            r"A_{\text{verde}}=28000-8798",
            color=DARK
        ).scale(0.76)

        eq3 = MathTex(
            r"A_{\text{verde}}=19202\,cm^2",
            color=PURPLE
        ).scale(0.82)

        eq4 = MathTex(
            r"A_{\text{verde}}=1{,}9202\,m^2",
            color=PURPLE
        ).scale(0.78)

        eqs = VGroup(eq1, eq2, eq3, eq4).arrange(DOWN, aligned_edge=LEFT, buff=0.34)
        eqs.to_edge(RIGHT, buff=0.75).shift(UP * 0.15)

        for eq in eqs:
            self.play(Write(eq), run_time=0.75)

        destaque = SurroundingRectangle(eq3, color=ORANGE, buff=0.18)
        self.play(Create(destaque))
        self.wait(2.5)

        self.limpar(titulo, contorno_ret, contorno_los, eqs, destaque)

    def parte_5_circulo(self):
        bandeira_com_medidas, bandeira, ret, losango, circulo, medidas = self.bandeira_data

        titulo = self.titulo("5. Área do círculo azul")
        self.play(Write(titulo))

        texto = Text(
            "Agora calculamos a área do círculo usando π = 22/7.",
            font_size=23,
            color=DARK
        ).next_to(titulo, DOWN, buff=0.35)

        contorno_circ = Circle(
            radius=circulo.radius,
            color=BLUE,
            stroke_width=6
        ).move_to(circulo.get_center())

        self.play(Write(texto))
        self.wait(1.2)
        self.play(FadeOut(texto))
        self.play(Create(contorno_circ))

        eq1 = MathTex(r"A_{\text{círculo}}=\pi r^2", color=DARK).scale(0.78)
        eq2 = MathTex(r"A_{\text{círculo}}=\frac{22}{7}\cdot35^2", color=DARK).scale(0.74)
        eq3 = MathTex(r"A_{\text{círculo}}=\frac{22}{7}\cdot1225", color=DARK).scale(0.74)
        eq4 = MathTex(r"A_{\text{círculo}}=3850\,cm^2", color=PURPLE).scale(0.82)

        eqs = VGroup(eq1, eq2, eq3, eq4).arrange(DOWN, aligned_edge=LEFT, buff=0.34)
        eqs.to_edge(RIGHT, buff=0.9).shift(UP * 0.15)

        for eq in eqs:
            self.play(Write(eq), run_time=0.75)

        destaque = SurroundingRectangle(eq4, color=ORANGE, buff=0.18)
        self.play(Create(destaque))
        self.wait(2.2)

        self.limpar(titulo, contorno_circ, eqs, destaque)

    def parte_6_amarelo(self):
        bandeira_com_medidas, bandeira, ret, losango, circulo, medidas = self.bandeira_data

        titulo = self.titulo("6. Área da região amarela")
        self.play(Write(titulo))

        texto = Text(
            "A região amarela é a área do losango menos a área do círculo.",
            font_size=22,
            color=DARK
        ).next_to(titulo, DOWN, buff=0.35)

        contorno_los = Polygon(
            *losango.get_vertices(),
            color=YELLOW,
            fill_opacity=0,
            stroke_width=6
        )

        contorno_circ = Circle(
            radius=circulo.radius,
            color=BLUE,
            stroke_width=6
        ).move_to(circulo.get_center())

        self.play(Write(texto))
        self.wait(1.2)
        self.play(FadeOut(texto))

        self.play(Create(contorno_los))
        self.play(Create(contorno_circ))

        eq1 = MathTex(
            r"A_{\text{amarela}}=A_{\text{losango}}-A_{\text{círculo}}",
            color=DARK
        ).scale(0.66)

        eq2 = MathTex(
            r"A_{\text{amarela}}=8798-3850",
            color=DARK
        ).scale(0.76)

        eq3 = MathTex(
            r"A_{\text{amarela}}=4948\,cm^2",
            color=PURPLE
        ).scale(0.82)

        eqs = VGroup(eq1, eq2, eq3).arrange(DOWN, aligned_edge=LEFT, buff=0.38)
        eqs.to_edge(RIGHT, buff=0.65).shift(UP * 0.15)

        for eq in eqs:
            self.play(Write(eq), run_time=0.8)

        destaque = SurroundingRectangle(eq3, color=ORANGE, buff=0.18)
        self.play(Create(destaque))
        self.wait(2.3)

        self.limpar(titulo, contorno_los, contorno_circ, eqs, destaque)

    def parte_7_porcentagem(self):
        bandeira_com_medidas, bandeira, ret, losango, circulo, medidas = self.bandeira_data

        self.play(FadeOut(bandeira_com_medidas), run_time=0.7)

        titulo = self.titulo("7. Porcentagem da região amarela")
        self.play(Write(titulo))

        texto = Text(
            "Comparamos a área amarela com a área total da bandeira.",
            font_size=23,
            color=DARK
        ).next_to(titulo, DOWN, buff=0.35)

        self.play(Write(texto))
        self.wait(1.2)
        self.play(FadeOut(texto))

        eq1 = MathTex(
            r"\%=\frac{A_{\text{amarela}}}{A_{\text{total}}}\cdot100",
            color=DARK
        ).scale(0.78)

        eq2 = MathTex(
            r"\%=\frac{4948}{28000}\cdot100",
            color=DARK
        ).scale(0.82)

        eq3 = MathTex(
            r"\%=17{,}671428\ldots",
            color=DARK
        ).scale(0.82)

        eq4 = MathTex(
            r"\%=17{,}67\%",
            color=PURPLE
        ).scale(1.0)

        eqs = VGroup(eq1, eq2, eq3, eq4).arrange(DOWN, buff=0.42)
        eqs.move_to(ORIGIN).shift(UP * 0.15)

        for eq in eqs:
            self.play(Write(eq), run_time=0.8)

        destaque = SurroundingRectangle(eq4, color=ORANGE, buff=0.22)
        self.play(Create(destaque))
        self.wait(2.5)

        self.limpar(titulo, eqs, destaque)

    def resposta_final(self):
        titulo = Text(
            "Resposta final",
            font_size=42,
            color=PURPLE,
            weight=BOLD
        )

        resposta_a = MathTex(
            r"\text{a) Área verde}=19202\,cm^2",
            color=DARK
        ).scale(0.85)

        resposta_a_m = MathTex(
            r"\text{ou }1{,}9202\,m^2",
            color=DARK
        ).scale(0.82)

        resposta_b = MathTex(
            r"\text{b) Área amarela}=17{,}67\%\text{ da bandeira}",
            color=DARK
        ).scale(0.82)

        grupo = VGroup(
            titulo,
            resposta_a,
            resposta_a_m,
            resposta_b
        ).arrange(DOWN, buff=0.4)

        caixa_a = SurroundingRectangle(
            VGroup(resposta_a, resposta_a_m),
            color=GREEN,
            buff=0.2
        )

        caixa_b = SurroundingRectangle(
            resposta_b,
            color=YELLOW,
            buff=0.2
        )

        self.play(FadeIn(titulo, shift=UP))
        self.play(Write(resposta_a), Write(resposta_a_m), Create(caixa_a))
        self.play(Write(resposta_b), Create(caixa_b))
        self.wait(4)

        self.play(
            FadeOut(titulo),
            FadeOut(resposta_a),
            FadeOut(resposta_a_m),
            FadeOut(resposta_b),
            FadeOut(caixa_a),
            FadeOut(caixa_b)
        )
