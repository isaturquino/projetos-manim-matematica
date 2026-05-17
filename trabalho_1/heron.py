from manim import *

# ============================================================
# Dedução da Fórmula de Heron — versão melhorada
#1
# Para rodar (qualidade baixa, preview rápido):
#   python -m manim -pql heron.py TrabalhoHeron
# Qualidade alta:
#   python -m manim -pqh heron.py TrabalhoHeron
# ============================================================

config.background_color = "#FAF7F0"

DARK   = "#1F1F1F"
PURPLE = "#6A1B9A"
PINK   = "#C2185B"
BLUE   = "#1565C0"
GREEN  = "#2E7D32"
ORANGE = "#EF6C00"
GRAY   = "#616161"
GOLD   = "#F9A825"

TOTAL_PARTES = 6


class TrabalhoHeron(Scene):
    """
    Cena principal que apresenta a dedução da Fórmula de Heron para cálculo
    da área de um triângulo usando apenas os três lados.
    """

    # ------------------------------------------------------------------
    # Helpers reutilizáveis
    # ------------------------------------------------------------------

    # Cria título com indicador opcional de progresso.
    def titulo(self, texto, parte=None):
        """Cria título com indicador opcional de progresso."""
        t = Text(texto, font_size=30, color=PURPLE, weight=BOLD).to_edge(UP, buff=0.3)
        if parte is not None:
            prog = Text(
                f"Parte {parte} de {TOTAL_PARTES}",
                font_size=16, color=GRAY
            ).to_corner(UR, buff=0.25)
            return VGroup(t, prog)
        return t

    # Anima a saída (FadeOut) de um ou mais objetos com tempo configurável.
    def limpar(self, *objetos, tempo=0.6):
        self.play(*[FadeOut(obj) for obj in objetos], run_time=tempo)

    # Escreve uma sequência de equações uma por vez com animação Write.
    def escrever_sequencia(self, *equacoes, run_time=0.75):
        for eq in equacoes:
            self.play(Write(eq), run_time=run_time)

    # Destaca um objeto criando uma caixa ao redor com animação Create.
    def destaque(self, obj, cor=ORANGE):
        box = SurroundingRectangle(obj, color=cor, buff=0.18, corner_radius=0.08)
        self.play(Create(box))
        return box

    # Cria um quadrado de ângulo reto (marcador) em um ponto específico.
    def marcador_angulo_reto(self, ponto, tam=0.18):
        """Quadrado de ângulo reto centrado no canto superior-direito de H.
        Cresce para cima (direção da altura) e para a direita (direção de HC),
        sem sobrepor o label H que fica abaixo-esquerda."""
        q = Square(side_length=tam, color=GRAY, stroke_width=1.8, fill_opacity=0)
        # Posiciona o canto inferior-esquerdo do quadrado exatamente em H
        q.move_to(ponto + np.array([tam/2, tam/2, 0]))
        return q

    # ------------------------------------------------------------------
    # Estrutura principal
    # ------------------------------------------------------------------

    # Método principal que coordena todas as partes da cena.
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

    # ------------------------------------------------------------------
    # Abertura
    # ------------------------------------------------------------------

    # Cena de abertura com título, subtítulo e preview da fórmula.
    def abertura(self):
        titulo = Text(
            "Dedução da Fórmula de Heron",
            font_size=44, color=PURPLE, weight=BOLD
        )
        subtitulo = Text(
            "Área de um triângulo usando apenas os três lados",
            font_size=22, color=DARK
        )
        formula_preview = MathTex(
            r"A = \sqrt{p(p-a)(p-b)(p-c)}",
            color=GRAY
        ).scale(0.85)
        formula_preview.set_opacity(0.5)

        grupo = VGroup(titulo, subtitulo, formula_preview).arrange(DOWN, buff=0.4)

        # Animação FadeIn: aparece com deslocamento para cima
        self.play(FadeIn(titulo, shift=UP * 0.3), run_time=0.8)
        # Animação FadeIn: aparece normalmente
        self.play(FadeIn(subtitulo), run_time=0.6)
        # Animação FadeIn: aparece normalmente
        self.play(FadeIn(formula_preview), run_time=0.6)
        self.wait(2)
        # Animação FadeOut: desaparece ao final da abertura
        self.play(FadeOut(grupo))

    # ------------------------------------------------------------------
    # Parte 1 — Triângulo e altura
    # ------------------------------------------------------------------

    # Apresenta o triângulo inicial com vértices A, B, C e ponto H na base.
    def parte_1_triangulo(self):
        cabecalho = self.titulo("Começamos com um triângulo qualquer", parte=1)
        # Animação Write: escreve o texto do cabeçalho
        self.play(Write(cabecalho))

        # Triângulo menor e centralizado na área útil (abaixo do título,
        # acima da explicação). A fica claramente acima da base.
        A = np.array([ 0.0,  1.2, 0])
        B = np.array([-2.5, -1.0, 0])
        C = np.array([ 2.5, -1.0, 0])
        H = np.array([ 0.0, -1.0, 0])

        triangulo = Polygon(A, B, C, color=PURPLE, stroke_width=4)
        altura    = DashedLine(A, H, color=PINK, stroke_width=3)
        ang_reto  = self.marcador_angulo_reto(H)

        # Pontos do triângulo com animação Create
        pontos = VGroup(
            Dot(A, color=PURPLE, radius=0.07),
            Dot(B, color=PURPLE, radius=0.07),
            Dot(C, color=PURPLE, radius=0.07),
            Dot(H, color=PINK,   radius=0.06),
        )

        # Criação dos pontos com animação Create
        self.play(Create(pontos))

        # Labels do triângulo
        labels = VGroup(
            MathTex("A", color=DARK).next_to(A, UP,    buff=0.15),
            MathTex("B", color=DARK).next_to(B, LEFT,  buff=0.12),
            MathTex("C", color=DARK).next_to(C, RIGHT, buff=0.12),
            # H deslocado para baixo-esquerda para não sobrepor o marcador
            # de ângulo reto (que ocupa o canto superior direito de H)
            MathTex("H", color=PINK).move_to(H + DOWN*0.28 + LEFT*0.22),
            MathTex("c", color=BLUE ).move_to((A+B)/2 + LEFT*0.30),
            MathTex("b", color=GREEN).move_to((A+C)/2 + RIGHT*0.30),
            MathTex("a", color=ORANGE).move_to((B+C)/2 + DOWN*0.32),
            MathTex("h", color=PINK).next_to(altura, RIGHT, buff=0.12),
        )

        explicacao = Text(
            "A altura h divide a base a em dois segmentos,\n"
            "formando dois triângulos retângulos.",
            font_size=22, color=DARK, line_spacing=1.3
        ).to_edge(DOWN, buff=0.45)

        self.play(Create(triangulo), FadeIn(pontos), run_time=1.0)
        self.play(Create(altura), FadeIn(ang_reto), FadeIn(labels), run_time=0.9)
        self.play(Write(explicacao))
        self.wait(2.5)

        self.triangulo_data = (A, B, C, H, triangulo, altura, ang_reto, pontos, labels)
        self.limpar(cabecalho, explicacao)

    # ------------------------------------------------------------------
    # Parte 2 — Encontrando x via Pitágoras
    # ------------------------------------------------------------------

    # Deriva o valor de x usando o teorema de Pitágoras no triângulo.
    def parte_2_encontrando_x(self):
        A, B, C, H, triangulo, altura, ang_reto, pontos, labels = self.triangulo_data

        cabecalho = self.titulo("Pitágoras nos dois triângulos menores", parte=2)
        self.play(Write(cabecalho))

        # --- Passo 1: encolher e deslocar o triângulo para a esquerda ---
        # Agrupa tudo que pertence ao triângulo numa escala menor e o empurra
        # para a metade esquerda da tela, liberando o lado direito para as equações.
        tri_group = VGroup(triangulo, altura, ang_reto, pontos, labels)
        self.play(
            tri_group.animate
                .scale(0.72)
                .to_edge(LEFT, buff=0.3)
                .shift(DOWN * 0.3),
            run_time=0.9
        )

        # Recalcula posições dos pontos após a transformação para usarmos
        # nos novos labels de x e a-x.
        # (os Dot objects já se moveram junto com o grupo, basta referenciar)
        dot_B = pontos[1]
        dot_H = pontos[3]
        dot_C = pontos[2]

        # Substitui o rótulo "a" pelos segmentos x e a-x
        self.play(FadeOut(labels[6]))
        novos_labels = VGroup(
            MathTex("x",   color=ORANGE, font_size=26).next_to(
                dot_B.get_center() * 0 + (dot_B.get_center() + dot_H.get_center()) / 2,
                DOWN, buff=0.15),
            MathTex("a-x", color=ORANGE, font_size=26).next_to(
                (dot_H.get_center() + dot_C.get_center()) / 2,
                DOWN, buff=0.15),
        )
        self.play(FadeIn(novos_labels))
        self.wait(0.4)

        # --- Passo 2: equações de Pitágoras na coluna direita ---
        # Âncora: x=0.05 (centro) → coluna direita começa em x≈0.1 (unidades Manim)
        eqs_pit = VGroup(
            MathTex(r"c^2 = h^2 + x^2",     color=BLUE),
            MathTex(r"b^2 = h^2 + (a-x)^2", color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).scale(0.84)
        # Posiciona no terço superior direito, sem tocar o triângulo
        eqs_pit.to_edge(RIGHT, buff=0.5).align_to(cabecalho, UP).shift(DOWN * 0.85)

        obs = Text(
            "Pitágoras em cada triângulo retângulo.",
            font_size=20, color=GRAY
        ).to_edge(DOWN, buff=0.45)

        self.play(Write(obs))
        self.escrever_sequencia(*eqs_pit)
        self.wait(0.4)

        # --- Passo 3: desenvolvimento algébrico abaixo das equações de Pitágoras ---
        passos = VGroup(
            MathTex(r"h^2 = c^2 - x^2",                   color=DARK),
            MathTex(r"b^2 = c^2 - x^2 + (a-x)^2",         color=DARK),
            MathTex(r"b^2 = c^2 + a^2 - 2ax",             color=DARK),
            MathTex(r"b^2 - c^2 - a^2 = -2ax",            color=DARK),
            MathTex(r"x = \frac{a^2 - b^2 + c^2}{2a}",    color=PURPLE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.20).scale(0.66)
        passos.next_to(eqs_pit, DOWN, buff=0.28).align_to(eqs_pit, LEFT)

        self.escrever_sequencia(*passos, run_time=0.62)

        box_x = self.destaque(passos[-1])
        self.wait(2.5)

        # Limpar tudo
        self.play(
            FadeOut(tri_group), FadeOut(novos_labels),
        )
        self.limpar(cabecalho, obs, eqs_pit, passos, box_x)

    # ------------------------------------------------------------------
    # Parte 3 — Encontrando h²
    # ------------------------------------------------------------------

    def parte_3_encontrando_h(self):
        cabecalho = self.titulo("Substituímos x para obter h²", parte=3)
        self.play(Write(cabecalho))

        eqs = VGroup(
            MathTex(r"h^2 = c^2 - x^2",    color=DARK).scale(0.84),
            MathTex(r"x = \frac{a^2 - b^2 + c^2}{2a}", color=PURPLE).scale(0.84),
            MathTex(
                r"h^2 = c^2 - \left(\frac{a^2 - b^2 + c^2}{2a}\right)^2",
                color=DARK
            ).scale(0.70),
            MathTex(
                r"h^2 = \frac{(2ac)^2 - (a^2 - b^2 + c^2)^2}{4a^2}",
                color=PURPLE
            ).scale(0.70),
        ).arrange(DOWN, buff=0.45)
        eqs.shift(UP*0.1)

        seta1 = Arrow(
            eqs[0].get_bottom(), eqs[2].get_top(),
            buff=0.08, color=GRAY, stroke_width=1.5, tip_length=0.18
        )
        seta2 = Arrow(
            eqs[1].get_bottom(), eqs[2].get_top(),
            buff=0.08, color=GRAY, stroke_width=1.5, tip_length=0.18
        )

        self.escrever_sequencia(eqs[0], eqs[1])
        self.play(Create(seta1), Create(seta2), run_time=0.5)
        self.escrever_sequencia(eqs[2], eqs[3])

        box_h2 = self.destaque(eqs[3])
        self.wait(2.5)
        self.limpar(cabecalho, eqs, seta1, seta2, box_h2)

    # ------------------------------------------------------------------
    # Parte 4 — Área em função de h²
    # ------------------------------------------------------------------

    def parte_4_area(self):
        cabecalho = self.titulo("Área em função dos lados", parte=4)
        self.play(Write(cabecalho))

        intro = Text(
            "Partimos de A = ah/2 e elevamos ao quadrado para eliminar a raiz.",
            font_size=21, color=GRAY
        ).next_to(cabecalho, DOWN, buff=0.3)

        eqs = VGroup(
            MathTex(r"A = \frac{a \cdot h}{2}",          color=DARK).scale(0.86),
            MathTex(r"A^2 = \frac{a^2 h^2}{4}",          color=DARK).scale(0.86),
            MathTex(
                r"A^2 = \frac{a^2}{4} \cdot \frac{(2ac)^2 - (a^2-b^2+c^2)^2}{4a^2}",
                color=DARK
            ).scale(0.60),
            MathTex(
                r"A^2 = \frac{(2ac)^2 - (a^2 - b^2 + c^2)^2}{16}",
                color=PURPLE
            ).scale(0.68),
        ).arrange(DOWN, buff=0.4)
        eqs.next_to(intro, DOWN, buff=0.4)

        self.play(Write(intro))
        self.escrever_sequencia(*eqs)

        box_a2 = self.destaque(eqs[-1])
        self.wait(2.5)
        self.limpar(cabecalho, intro, eqs, box_a2)

    # ------------------------------------------------------------------
    # Parte 5 — Fatoração por diferença de quadrados
    # ------------------------------------------------------------------

    def parte_5_fatoracao(self):
        cabecalho = self.titulo("Fatoramos com diferença de quadrados", parte=5)
        self.play(Write(cabecalho))

        regra = VGroup(
            Text("Identidade utilizada:", font_size=20, color=GRAY),
            MathTex(r"m^2 - n^2 = (m+n)(m-n)", color=ORANGE).scale(0.80),
        ).arrange(DOWN, buff=0.15)
        regra.next_to(cabecalho, DOWN, buff=0.3)
        box_regra = SurroundingRectangle(regra[1], color=ORANGE, buff=0.12, corner_radius=0.06)

        self.play(Write(regra), Create(box_regra))
        self.wait(0.5)

        eqs = VGroup(
            MathTex(
                r"A^2 = \frac{(2ac)^2 - (a^2-b^2+c^2)^2}{16}",
                color=DARK
            ).scale(0.62),
            MathTex(
                r"A^2 = \frac{\bigl[2ac + (a^2-b^2+c^2)\bigr]\bigl[2ac - (a^2-b^2+c^2)\bigr]}{16}",
                color=DARK
            ).scale(0.52),
            MathTex(
                r"A^2 = \frac{\bigl[(a+c)^2 - b^2\bigr]\bigl[b^2 - (a-c)^2\bigr]}{16}",
                color=DARK
            ).scale(0.56),
            MathTex(
                r"A^2 = \frac{(a+c+b)(a+c-b)(b+a-c)(b-a+c)}{16}",
                color=PURPLE
            ).scale(0.54),
        ).arrange(DOWN, buff=0.32)
        eqs.next_to(regra, DOWN, buff=0.35)

        self.escrever_sequencia(*eqs, run_time=0.9)

        box_fat = self.destaque(eqs[-1])
        self.wait(2.5)
        self.limpar(cabecalho, regra, box_regra, eqs, box_fat)

    # ------------------------------------------------------------------
    # Parte 6 — Semiperímetro e fórmula final
    # ------------------------------------------------------------------

    def parte_6_semiperimetro(self):
        cabecalho = self.titulo("Introduzimos o semiperímetro p", parte=6)
        self.play(Write(cabecalho))

        intro = Text(
            "Chamamos de p a metade do perímetro do triângulo.",
            font_size=21, color=DARK
        ).next_to(cabecalho, DOWN, buff=0.3)

        # Coluna esquerda: substituições
        subs = VGroup(
            MathTex(r"p = \frac{a+b+c}{2}",      color=PURPLE),
            MathTex(r"p - a = \frac{-a+b+c}{2}", color=DARK),
            MathTex(r"p - b = \frac{a-b+c}{2}",  color=DARK),
            MathTex(r"p - c = \frac{a+b-c}{2}",  color=DARK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).scale(0.68)
        subs.next_to(intro, DOWN, buff=0.35).to_edge(LEFT, buff=0.9)

        # Coluna direita: resultado
        formula_q = MathTex(
            r"A^2 = p\,(p-a)(p-b)(p-c)",
            color=DARK
        ).scale(0.78).to_edge(RIGHT, buff=0.8).shift(UP*0.5)

        formula_f = MathTex(
            r"A = \sqrt{p\,(p-a)(p-b)(p-c)}",
            color=PURPLE
        ).scale(0.84).next_to(formula_q, DOWN, buff=0.6)

        caixa = SurroundingRectangle(formula_f, color=GOLD, buff=0.22, corner_radius=0.1)
        caixa.set_stroke(width=2.5)

        self.play(Write(intro))
        for item in subs:
            self.play(Write(item), run_time=0.5)

        self.play(Write(formula_q))
        self.play(Write(formula_f), Create(caixa))
        self.wait(3)

        self.limpar(cabecalho, intro, subs, formula_q, formula_f, caixa)

    # ------------------------------------------------------------------
    # Fechamento com exemplo numérico
    # ------------------------------------------------------------------

    def fechamento(self):
        # ── Tela 1: fórmula em destaque, centralizada ──────────────────
        titulo = Text("Fórmula de Heron", font_size=42, color=PURPLE, weight=BOLD)
        formula = MathTex(
            r"A = \sqrt{p\,(p-a)(p-b)(p-c)}",
            color=PURPLE
        ).scale(1.05)

        # Agrupa título + fórmula antes de criar a caixa,
        # assim ela envolve os dois com espaçamento uniforme.
        tela1 = VGroup(titulo, formula).arrange(DOWN, buff=0.45)
        tela1.move_to(ORIGIN)

        caixa = SurroundingRectangle(
            tela1, color=GOLD, buff=0.35, corner_radius=0.14
        ).set_stroke(width=2.5)

        self.play(FadeIn(titulo, shift=UP * 0.25), run_time=0.7)
        self.play(Write(formula), run_time=0.9)
        self.play(Create(caixa))
        self.wait(2)
        self.play(FadeOut(VGroup(titulo, formula, caixa)))

        # ── Tela 2: exemplo numérico em duas colunas ───────────────────
        # Cabeçalho
        ex_titulo = Text(
            "Exemplo: triângulo com lados 5, 12 e 13",
            font_size=26, color=DARK, weight=BOLD
        ).to_edge(UP, buff=0.45)

        separador = Line(
            ex_titulo.get_left() + DOWN * 0.1,
            ex_titulo.get_right() + DOWN * 0.1,
            color=GRAY, stroke_width=0.8
        ).next_to(ex_titulo, DOWN, buff=0.18)

        self.play(Write(ex_titulo), Create(separador))

        # Coluna esquerda — cálculo do semiperímetro e fatores
        col_esq = VGroup(
            MathTex(r"p = \frac{5+12+13}{2} = 15", color=DARK),
            MathTex(r"p - a = 15 - 5 = 10",        color=DARK),
            MathTex(r"p - b = 15 - 12 = 3",        color=DARK),
            MathTex(r"p - c = 15 - 13 = 2",        color=DARK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.30).scale(0.76)
        col_esq.next_to(separador, DOWN, buff=0.4).to_edge(LEFT, buff=0.7)

        # Coluna direita — aplicação na fórmula
        col_dir = VGroup(
            MathTex(r"A = \sqrt{p(p-a)(p-b)(p-c)}", color=PURPLE),
            MathTex(r"A = \sqrt{15 \cdot 10 \cdot 3 \cdot 2}", color=DARK),
            MathTex(r"A = \sqrt{900}", color=DARK),
            MathTex(r"A = 30", color=PURPLE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.30).scale(0.76)
        col_dir.next_to(separador, DOWN, buff=0.4).to_edge(RIGHT, buff=0.7)

        # Linha vertical separando as colunas
        linha_v = DashedLine(
            separador.get_center() + DOWN * 0.1,
            separador.get_center() + DOWN * 3.6,
            color=GRAY, stroke_width=0.8, dash_length=0.12
        )

        self.play(Create(linha_v))
        # Anima as duas colunas em paralelo, linha por linha
        for esq, dir_ in zip(col_esq, col_dir):
            self.play(Write(esq), Write(dir_), run_time=0.55)

        # Destaque no resultado final
        box_res = SurroundingRectangle(
            col_dir[-1], color=GOLD, buff=0.18, corner_radius=0.08
        ).set_stroke(width=2)
        self.play(Create(box_res))

        # Verificação embaixo, centralizada
        verificacao = Text(
            "Verificação: triângulo retângulo (5² + 12² = 13²)  →  A = ½ · 5 · 12 = 30  ✓",
            font_size=17, color=GRAY
        ).to_edge(DOWN, buff=0.45)
        self.play(FadeIn(verificacao))
        self.wait(3.5)

        self.play(FadeOut(VGroup(
            ex_titulo, separador, linha_v,
            col_esq, col_dir, box_res, verificacao
        )))