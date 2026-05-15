from manim import *

# ============================================================
# Dedução da Fórmula de Heron 
# Para rodar:
# python -m manim -pql heron.py TrabalhoHeron
# Qualidade alta:
# python -m manim -pqh heron.py TrabalhoHeron
#
# Observação:
# Este código usa MathTex, então precisa do MiKTeX/LaTeX funcionando.
# ============================================================

config.background_color = "#FAF7F0"

DARK = "#1F1F1F"
PURPLE = "#6A1B9A"
PINK = "#C2185B"
BLUE = "#1565C0"
GREEN = "#2E7D32"
ORANGE = "#EF6C00"
GRAY = "#616161"


class TrabalhoHeron(Scene):
    def titulo(self, texto):
        return Text(
            texto,
            font_size=32,
            color=PURPLE,
            weight=BOLD
        ).to_edge(UP, buff=0.35)

    def limpar(self, *objetos):
        self.play(*[FadeOut(obj) for obj in objetos], run_time=0.7)

    def construct(self):
        self.camera.background_color = "#FAF7F0"

        self.abertura()
        self.parte_1_triangulo()
        self.parte_2_encontrando_x()
        self.parte_3_encontrando_h()
        self.parte_4_area()
        self.parte_5_fatoracao()
        self.parte_6_semiperimetro()
        self.fechamento()

    def abertura(self):
        titulo = Text(
            "Dedução da Fórmula de Heron",
            font_size=42,
            color=PURPLE,
            weight=BOLD
        )

        subtitulo = Text(
            "Área de um triângulo conhecendo apenas os três lados",
            font_size=24,
            color=DARK
        )

        grupo = VGroup(titulo, subtitulo).arrange(DOWN, buff=0.35)

        self.play(FadeIn(grupo, shift=UP))
        self.wait(2)
        self.play(FadeOut(grupo))

    def parte_1_triangulo(self):
        titulo = self.titulo("1. Começamos com um triângulo qualquer")
        self.play(Write(titulo))

        A = np.array([0, 2.0, 0])
        B = np.array([-2.8, -1.4, 0])
        C = np.array([2.8, -1.4, 0])
        H = np.array([0, -1.4, 0])

        triangulo = Polygon(A, B, C, color=PURPLE, stroke_width=5)
        altura = DashedLine(A, H, color=PINK, stroke_width=4)

        pontos = VGroup(
            Dot(A, color=PURPLE),
            Dot(B, color=PURPLE),
            Dot(C, color=PURPLE),
            Dot(H, color=PINK)
        )

        labels = VGroup(
            MathTex("A", color=DARK).next_to(A, UP),
            MathTex("B", color=DARK).next_to(B, LEFT),
            MathTex("C", color=DARK).next_to(C, RIGHT),
            MathTex("H", color=DARK).next_to(H, DOWN),
            MathTex("c", color=BLUE).move_to((A+B)/2 + LEFT*0.25),
            MathTex("b", color=GREEN).move_to((A+C)/2 + RIGHT*0.25),
            MathTex("a", color=ORANGE).move_to((B+C)/2 + DOWN*0.35),
            MathTex("h", color=PINK).next_to(altura, RIGHT, buff=0.1)
        )

        explicacao = Text(
            "Traçamos a altura h, formando dois triângulos retângulos.",
            font_size=24,
            color=DARK
        ).to_edge(DOWN, buff=0.55)

        self.play(Create(triangulo), FadeIn(pontos))
        self.play(Create(altura), FadeIn(labels))
        self.play(Write(explicacao))
        self.wait(2)

        self.triangulo_data = (A, B, C, H, triangulo, altura, pontos, labels)
        self.limpar(titulo, explicacao)

    def parte_2_encontrando_x(self):
        A, B, C, H, triangulo, altura, pontos, labels = self.triangulo_data

        titulo = self.titulo("2. Dividimos a base e aplicamos Pitágoras")
        self.play(Write(titulo))

        self.play(FadeOut(labels[-2]))

        novos_labels = VGroup(
            MathTex("x", color=ORANGE).move_to((B+H)/2 + DOWN*0.35),
            MathTex("a-x", color=ORANGE).move_to((H+C)/2 + DOWN*0.35)
        )
        self.play(FadeIn(novos_labels))

        eqs = VGroup(
            MathTex(r"c^2=h^2+x^2", color=BLUE),
            MathTex(r"b^2=h^2+(a-x)^2", color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).scale(0.82)

        eqs.to_edge(RIGHT, buff=0.8).shift(UP*0.45)

        obs = Text(
            "Usamos Pitágoras nos dois triângulos menores.",
            font_size=23,
            color=DARK
        ).to_edge(DOWN, buff=0.55)

        self.play(Write(obs))
        self.play(Write(eqs[0]))
        self.play(Write(eqs[1]))
        self.wait(1)

        passo = VGroup(
            MathTex(r"h^2=c^2-x^2", color=DARK),
            MathTex(r"b^2=c^2-x^2+(a-x)^2", color=DARK),
            MathTex(r"b^2=c^2-x^2+a^2-2ax+x^2", color=DARK),
            MathTex(r"x=\frac{a^2-b^2+c^2}{2a}", color=PURPLE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).scale(0.70)

        passo.next_to(eqs, DOWN, buff=0.35)

        for item in passo:
            self.play(Write(item), run_time=0.75)

        destaque = SurroundingRectangle(passo[-1], color=PURPLE, buff=0.15)
        self.play(Create(destaque))
        self.wait(2)

        self.play(
            FadeOut(triangulo),
            FadeOut(altura),
            FadeOut(pontos),
            FadeOut(labels),
            FadeOut(novos_labels)
        )

        self.limpar(titulo, obs, eqs, passo, destaque)

    def parte_3_encontrando_h(self):
        titulo = self.titulo("3. Substituímos x para encontrar h²")
        self.play(Write(titulo))

        eq1 = MathTex(r"h^2=c^2-x^2", color=DARK).scale(0.85)
        eq2 = MathTex(r"x=\frac{a^2-b^2+c^2}{2a}", color=PURPLE).scale(0.85)
        eq3 = MathTex(
            r"h^2=c^2-\left(\frac{a^2-b^2+c^2}{2a}\right)^2",
            color=DARK
        ).scale(0.72)
        eq4 = MathTex(
            r"h^2=\frac{4a^2c^2-(a^2-b^2+c^2)^2}{4a^2}",
            color=PURPLE
        ).scale(0.72)

        eqs = VGroup(eq1, eq2, eq3, eq4).arrange(DOWN, buff=0.42)
        eqs.shift(UP*0.15)

        for item in eqs:
            self.play(Write(item), run_time=0.9)

        self.wait(2)
        self.limpar(titulo, eqs)

    def parte_4_area(self):
        titulo = self.titulo("4. Usamos a fórmula da área")
        self.play(Write(titulo))

        explicacao = Text(
            "Substituímos o valor de h² na fórmula da área.",
            font_size=23,
            color=GRAY
        ).next_to(titulo, DOWN, buff=0.35)

        eq1 = MathTex(
            r"A=\frac{a\cdot h}{2}",
            color=DARK
        ).scale(0.85)

        eq2 = MathTex(
            r"A^2=\frac{a^2h^2}{4}",
            color=DARK
        ).scale(0.85)

        eq3 = MathTex(
            r"A^2=",
            r"\frac{a^2}{4}",
            r"\cdot",
            r"\frac{4a^2c^2-(a^2-b^2+c^2)^2}{4a^2}",
            color=DARK
        ).scale(0.56)

        eq4 = MathTex(
            r"A^2=",
            r"\frac{(2ac)^2-(a^2-b^2+c^2)^2}{16}",
            color=PURPLE
        ).scale(0.66)

        grupo = VGroup(eq1, eq2, eq3, eq4)
        grupo.arrange(DOWN, buff=0.42)
        grupo.next_to(explicacao, DOWN, buff=0.45)

        self.play(Write(explicacao))
        self.play(Write(eq1))
        self.play(Write(eq2))
        self.play(Write(eq3), run_time=1.1)
        self.play(Write(eq4))

        destaque = SurroundingRectangle(eq4, color=ORANGE, buff=0.18)
        self.play(Create(destaque))

        self.wait(2)
        self.limpar(titulo, explicacao, grupo, destaque)

    def parte_5_fatoracao(self):
        titulo = self.titulo("5. Fatoramos usando diferença de quadrados")
        self.play(Write(titulo))

        dica = Text(
            "Diferença de quadrados:",
            font_size=23,
            color=GRAY
        )

        dica2 = MathTex(
            r"m^2-n^2=(m+n)(m-n)",
            color=ORANGE
        ).scale(0.78)

        topo = VGroup(dica, dica2).arrange(DOWN, buff=0.18)
        topo.next_to(titulo, DOWN, buff=0.25)

        self.play(Write(dica))
        self.play(Write(dica2))

        eq1 = MathTex(
            r"A^2=",
            r"\frac{(2ac)^2-(a^2-b^2+c^2)^2}{16}",
            color=DARK
        ).scale(0.62)

        eq2 = MathTex(
            r"A^2=",
            r"\frac{[2ac+(a^2-b^2+c^2)]}{16}",
            r"\cdot",
            r"[2ac-(a^2-b^2+c^2)]",
            color=DARK
        ).scale(0.52)

        eq3 = MathTex(
            r"A^2=",
            r"\frac{[(a+c)^2-b^2]}{16}",
            r"\cdot",
            r"[b^2-(a-c)^2]",
            color=DARK
        ).scale(0.56)

        eq4 = MathTex(
            r"A^2=",
            r"\frac{(a+c+b)(a+c-b)}{16}",
            r"\cdot",
            r"(b+a-c)(b-a+c)",
            color=PURPLE
        ).scale(0.52)

        grupo = VGroup(eq1, eq2, eq3, eq4)
        grupo.arrange(DOWN, buff=0.38)
        grupo.next_to(topo, DOWN, buff=0.3)

        self.play(Write(eq1), run_time=1)
        self.play(Write(eq2), run_time=1.1)
        self.play(Write(eq3), run_time=1.1)
        self.play(Write(eq4), run_time=1.1)

        destaque = SurroundingRectangle(eq4, color=ORANGE, buff=0.18)
        self.play(Create(destaque))

        self.wait(2.5)
        self.limpar(titulo, topo, grupo, destaque)

    def parte_6_semiperimetro(self):
        titulo = self.titulo("6. Substituímos pelo semiperímetro")
        self.play(Write(titulo))

        intro = Text(
            "Chamamos de p a metade do perímetro do triângulo.",
            font_size=23,
            color=DARK
        ).next_to(titulo, DOWN, buff=0.35)

        eqs = VGroup(
            MathTex(r"p=\frac{a+b+c}{2}", color=PURPLE),
            MathTex(r"\frac{a+b+c}{2}=p", color=DARK),
            MathTex(r"\frac{-a+b+c}{2}=p-a", color=DARK),
            MathTex(r"\frac{a-b+c}{2}=p-b", color=DARK),
            MathTex(r"\frac{a+b-c}{2}=p-c", color=DARK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).scale(0.68)

        eqs.next_to(intro, DOWN, buff=0.32).to_edge(LEFT, buff=1.05)

        formula_quadrada = MathTex(
            r"A^2=p(p-a)(p-b)(p-c)",
            color=DARK
        ).scale(0.80).to_edge(RIGHT, buff=0.8).shift(UP*0.1)

        formula_final = MathTex(
            r"A=\sqrt{p(p-a)(p-b)(p-c)}",
            color=PURPLE
        ).scale(0.82).next_to(formula_quadrada, DOWN, buff=0.65)

        caixa = SurroundingRectangle(formula_final, color=ORANGE, buff=0.22)

        self.play(Write(intro))

        for item in eqs:
            self.play(Write(item), run_time=0.5)

        self.play(Write(formula_quadrada))
        self.play(Write(formula_final), Create(caixa))
        self.wait(3)

        self.limpar(titulo, intro, eqs, formula_quadrada, formula_final, caixa)

    def fechamento(self):
        titulo = Text(
            "Conclusão",
            font_size=40,
            color=PURPLE,
            weight=BOLD
        )

        texto = Text(
            "A Fórmula de Heron permite calcular a área usando apenas os três lados.",
            font_size=24,
            color=DARK
        )

        formula = MathTex(
            r"A=\sqrt{p(p-a)(p-b)(p-c)}",
            color=PURPLE
        ).scale(0.95)

        grupo = VGroup(titulo, texto, formula).arrange(DOWN, buff=0.42)

        self.play(FadeIn(grupo, shift=UP))
        self.wait(3)
        self.play(FadeOut(grupo))
