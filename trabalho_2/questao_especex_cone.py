from manim import *
from manim_slides import Slide

BG = ManimColor('#F8F7F1')
DARK = ManimColor('#1F1F1F')
PURPLE = ManimColor('#5E1675')
GREEN = ManimColor('#2F7D32')
BLUE = ManimColor('#2F67C7')
LIGHT_BLUE = ManimColor('#8EC5FF')
ORANGE = ManimColor('#E86A17')
YELLOW = ManimColor('#E4B83A')
GRAY = ManimColor('#666666')

config.background_color = BG


class QuestaoEsPCExCone(Slide):
    def titulo(self, texto: str, tamanho=29) -> Text:
        titulo = Text(texto, font_size=tamanho, color=PURPLE, weight=BOLD).to_edge(UP, buff=0.42)
        if titulo.width > 12:
            titulo.scale_to_fit_width(12)
        return titulo

    def limpar(self, *objetos, tempo=0.45):
        objetos = [obj for obj in objetos if obj is not None]
        if objetos:
            self.play(*[FadeOut(obj) for obj in objetos], run_time=tempo)

    def criar_cone_inicial(self, escala=1.0):
        topo_esq = np.array([-2.1, 2.0, 0])
        topo_dir = np.array([2.1, 2.0, 0])
        vertice = np.array([0, -2.3, 0])
        y_interface = -0.15
        t = (y_interface - vertice[1]) / (topo_esq[1] - vertice[1])
        int_esq = interpolate(vertice, topo_esq, t)
        int_dir = interpolate(vertice, topo_dir, t)

        contorno = VGroup(
            Line(topo_esq, vertice, color=DARK, stroke_width=3),
            Line(topo_dir, vertice, color=DARK, stroke_width=3),
            Ellipse(width=4.2, height=0.52, color=DARK, stroke_width=3).move_to([0, 2.0, 0]),
        )
        agua = Polygon(vertice, int_dir, int_esq, fill_color=LIGHT_BLUE, fill_opacity=0.85,
                       stroke_color=BLUE, stroke_width=2)
        oleo = Polygon(int_esq, int_dir, topo_dir, topo_esq, fill_color=YELLOW,
                       fill_opacity=0.55, stroke_opacity=0)
        linha_interface = DashedLine(int_esq, int_dir, color=GRAY, stroke_width=2)
        altura = DoubleArrow(vertice + LEFT * 2.75, np.array([0, 2.0, 0]) + LEFT * 2.75,
                             buff=0, color=DARK, stroke_width=2, tip_length=0.12)
        metade = DoubleArrow(vertice + RIGHT * 2.55, np.array([0, y_interface, 0]) + RIGHT * 2.55,
                             buff=0, color=BLUE, stroke_width=2, tip_length=0.12)
        rotulos = VGroup(
            MathTex('h', color=DARK).scale(0.64).next_to(altura, LEFT, buff=0.08),
            MathTex(r'\frac{h}{2}', color=BLUE).scale(0.62).next_to(metade, RIGHT, buff=0.08),
            Text('óleo', font_size=25, color=ORANGE).move_to([0, 0.95, 0]),
            Text('água', font_size=25, color=BLUE).move_to([0, -0.95, 0]),
            MathTex('R', color=DARK).scale(0.58).move_to([0, 2.23, 0]),
        )
        return VGroup(oleo, agua, contorno, linha_interface, altura, metade, rotulos).scale(escala)

    def criar_cone_final(self, escala=1.0):
        topo_esq = np.array([-2.1, 2.0, 0])
        topo_dir = np.array([2.1, 2.0, 0])
        vertice = np.array([0, -2.3, 0])
        altura_relativa = (7 ** (1 / 3)) / 2
        y_oleo = vertice[1] + altura_relativa * (2.0 - vertice[1])
        t = (y_oleo - vertice[1]) / (topo_esq[1] - vertice[1])
        nivel_esq = interpolate(vertice, topo_esq, t)
        nivel_dir = interpolate(vertice, topo_dir, t)

        contorno = VGroup(
            Line(topo_esq, vertice, color=DARK, stroke_width=3),
            Line(topo_dir, vertice, color=DARK, stroke_width=3),
            Ellipse(width=4.2, height=0.52, color=DARK, stroke_width=3).move_to([0, 2.0, 0]),
        )
        oleo = Polygon(vertice, nivel_dir, nivel_esq, fill_color=YELLOW, fill_opacity=0.68,
                       stroke_color=ORANGE, stroke_width=2)
        linha_nivel = DashedLine(nivel_esq, nivel_dir, color=ORANGE, stroke_width=2)
        altura_final = DoubleArrow(vertice + RIGHT * 2.55, np.array([0, y_oleo, 0]) + RIGHT * 2.55,
                                   buff=0, color=ORANGE, stroke_width=2, tip_length=0.12)
        rotulos = VGroup(
            MathTex('H', color=ORANGE).scale(0.68).next_to(altura_final, RIGHT, buff=0.08),
            Text('óleo', font_size=25, color=ORANGE).move_to([0, (vertice[1] + y_oleo) / 2, 0]),
        )
        return VGroup(oleo, contorno, linha_nivel, altura_final, rotulos).scale(escala)

    def construct(self):
        self.camera.background_color = BG
        self.abertura(); self.interpretacao(); self.semelhanca_inicial(); self.razao_dos_volumes()
        self.volume_do_oleo(); self.situacao_final(); self.nova_semelhanca(); self.resposta_final()

    def abertura(self):
        titulo = Text('Questão EsPCEx', font_size=44, color=PURPLE, weight=BOLD)
        subtitulo = Text('Cone com água e óleo', font_size=28, color=DARK)
        grupo = VGroup(titulo, subtitulo).arrange(DOWN, buff=0.28)
        self.play(FadeIn(grupo, shift=UP), run_time=0.8); self.next_slide(); self.play(FadeOut(grupo), run_time=0.45)

    def interpretacao(self):
        titulo = self.titulo('1. Interpretando o enunciado')
        cone = self.criar_cone_inicial(0.72).move_to(RIGHT * 3.5 + DOWN * 0.25)
        texto = VGroup(
            Text('O recipiente é um cone invertido,', font_size=21, color=DARK),
            Text('com altura total h e raio R.', font_size=21, color=DARK),
            Text('A água ocupa inicialmente a metade', font_size=21, color=DARK),
            Text('inferior da altura do cone.', font_size=21, color=DARK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.20).move_to(LEFT * 3.25 + UP * 1.10)
        objetivo = VGroup(
            Text('Objetivo:', font_size=22, color=PURPLE, weight=BOLD),
            Text('determinar a altura final do óleo', font_size=21, color=DARK),
            Text('medida a partir do vértice.', font_size=21, color=DARK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to(LEFT * 3.25 + DOWN * 1.25)
        self.play(Write(titulo)); self.play(FadeIn(cone, shift=LEFT))
        self.play(LaggedStart(*[Write(i) for i in texto], lag_ratio=0.15))
        self.play(LaggedStart(*[Write(i) for i in objetivo], lag_ratio=0.15)); self.next_slide()
        self.limpar(titulo, texto, objetivo, cone)

    def semelhanca_inicial(self):
        titulo = self.titulo('2. Semelhança entre o cone total e o cone de água')
        cone = self.criar_cone_inicial(0.67).move_to(LEFT * 3.55 + DOWN * 0.25)
        explicacao = Text('Como o nível da água está na metade da altura,\no cone de água é semelhante ao cone total.',
                          font_size=21, color=DARK, line_spacing=1.05).move_to(RIGHT * 3.05 + UP * 1.25)
        eq1 = MathTex(r'\frac{h}{h/2}=2', color=DARK).scale(0.86)
        eq2 = MathTex(r'\text{razão linear}=2:1', color=PURPLE).scale(0.74)
        eqs = VGroup(eq1, eq2).arrange(DOWN, buff=0.48).move_to(RIGHT * 3.05 + DOWN * 0.70)
        self.play(Write(titulo), FadeIn(cone)); self.play(Write(explicacao)); self.next_slide()
        self.play(Write(eq1)); self.next_slide(); self.play(Write(eq2))
        caixa = SurroundingRectangle(eq2, color=ORANGE, buff=0.15); self.play(Create(caixa)); self.next_slide()
        self.limpar(titulo, cone, explicacao, eq1, eq2, caixa)

    def razao_dos_volumes(self):
        titulo = self.titulo('3. Razão entre os volumes')
        texto = Text('Em sólidos semelhantes, a razão dos volumes\né o cubo da razão entre as medidas lineares.',
                     font_size=22, color=DARK, line_spacing=1.05).move_to(UP * 1.65)
        eq1 = MathTex(r'\frac{V_{\text{total}}}{V_{\text{água}}}=2^3', color=DARK).scale(0.90)
        eq2 = MathTex(r'\frac{V_{\text{total}}}{V_{\text{água}}}=8', color=PURPLE).scale(0.95)
        eq3 = MathTex(r'V_{\text{total}}=8V_{\text{água}}', color=PURPLE).scale(0.90)
        grupo = VGroup(eq1, eq2, eq3).arrange(DOWN, buff=0.42).move_to(DOWN * 0.55)
        self.play(Write(titulo), Write(texto)); self.next_slide(); self.play(Write(eq1)); self.next_slide()
        self.play(Write(eq2)); self.next_slide(); self.play(Write(eq3))
        caixa = SurroundingRectangle(eq3, color=ORANGE, buff=0.16); self.play(Create(caixa)); self.next_slide()
        self.limpar(titulo, texto, grupo, caixa)

    def volume_do_oleo(self):
        titulo = self.titulo('4. Determinando o volume do óleo')
        eq1 = MathTex(r'V_{\text{total}}=V_{\text{água}}+V_{\text{óleo}}', color=DARK).scale(0.83)
        eq2 = MathTex(r'8V_{\text{água}}=V_{\text{água}}+V_{\text{óleo}}', color=DARK).scale(0.80)
        eq3 = MathTex(r'V_{\text{óleo}}=7V_{\text{água}}', color=PURPLE).scale(0.92)
        eq4 = MathTex(r'\frac{V_{\text{óleo}}}{V_{\text{água}}}=7', color=PURPLE).scale(0.88)
        grupo = VGroup(eq1, eq2, eq3, eq4).arrange(DOWN, buff=0.43).move_to(DOWN * 0.10)
        self.play(Write(titulo))
        for eq in grupo:
            self.play(Write(eq), run_time=0.7); self.next_slide()
        caixa = SurroundingRectangle(eq4, color=ORANGE, buff=0.16); self.play(Create(caixa)); self.next_slide()
        self.limpar(titulo, grupo, caixa)

    def situacao_final(self):
        titulo = self.titulo('5. Situação após toda a água escoar')
        inicial = self.criar_cone_inicial(0.57).move_to(LEFT * 3.55 + DOWN * 0.20)
        final = self.criar_cone_final(0.57).move_to(RIGHT * 3.55 + DOWN * 0.20)
        rotulo1 = Text('Situação inicial', font_size=22, color=BLUE).next_to(inicial, DOWN, buff=0.20)
        rotulo2 = Text('Situação final', font_size=22, color=ORANGE).next_to(final, DOWN, buff=0.20)
        seta = Arrow(LEFT * 0.95, RIGHT * 0.95, color=PURPLE, stroke_width=4, buff=0.05)
        texto = Text('A água sai completamente,\nmas nenhum óleo é perdido.', font_size=21,
                     color=DARK, line_spacing=1.05).move_to(UP * 1.95)
        self.play(Write(titulo)); self.play(FadeIn(inicial), Write(rotulo1)); self.play(GrowArrow(seta))
        self.play(FadeIn(final), Write(rotulo2)); self.play(Write(texto)); self.next_slide()
        self.limpar(titulo, inicial, final, rotulo1, rotulo2, seta, texto)

    def nova_semelhanca(self):
        titulo = self.titulo(
            "6. Nova semelhança para calcular a altura final",
            tamanho=27,
        )

        cone = self.criar_cone_final(0.61)
        cone.move_to(LEFT * 3.70 + DOWN * 0.25)

        texto = Text(
            "O volume final do óleo é 7 vezes\n"
            "o volume do cone de água inicial.\n"
            "Logo, a razão linear é a\n"
            "raiz cúbica de 7.",
            font_size=16,
            color=DARK,
            line_spacing=1.05,
        )
        texto.move_to(RIGHT * 3.15 + UP * 1.72)

        if texto.width > 5.45:
            texto.scale_to_fit_width(5.45)

        eq1 = MathTex(
            r"\frac{V_{\text{óleo}}}{V_{\text{água}}}=7",
            color=DARK,
        ).scale(0.52)

        eq2 = MathTex(
            r"\frac{H}{h/2}=\sqrt[3]{7}",
            color=DARK,
        ).scale(0.58)

        eq3 = MathTex(
            r"H=\sqrt[3]{7}\cdot\frac{h}{2}",
            color=PURPLE,
        ).scale(0.61)

        eq4 = MathTex(
            r"H=\frac{\sqrt[3]{7}}{2}h",
            color=PURPLE,
        ).scale(0.68)

        equacoes = VGroup(eq1, eq2, eq3, eq4).arrange(
            DOWN,
            buff=0.42,
        )

        equacoes.next_to(texto, DOWN, buff=0.34)
        equacoes.align_to(texto, RIGHT)

        if equacoes.height > 3.75:
            equacoes.scale_to_fit_height(3.75)

        self.play(Write(titulo), FadeIn(cone))
        self.play(Write(texto))
        self.next_slide()

        for equacao in equacoes:
            self.play(Write(equacao), run_time=0.70)
            self.next_slide()

        caixa = SurroundingRectangle(
            eq4,
            color=ORANGE,
            buff=0.16,
            stroke_width=4,
        )

        self.play(Create(caixa))
        self.next_slide()

        self.limpar(
            titulo,
            cone,
            texto,
            equacoes,
            caixa,
        )

    def resposta_final(self):
        titulo = self.titulo("Resposta final")

        formula = MathTex(
            r"\boxed{H=\frac{\sqrt[3]{7}}{2}h}",
            color=DARK,
        ).scale(1.10)

        alternativa = Text(
            "Alternativa A",
            font_size=28,
            color=GREEN,
            weight=BOLD,
        )

        explicacao = Text(
            "Portanto, a altura do nível do óleo,\n"
            "medida a partir do vértice, é:",
            font_size=21,
            color=DARK,
            line_spacing=1.05,
        )

        grupo = VGroup(
            explicacao,
            formula,
            alternativa,
        ).arrange(
            DOWN,
            buff=0.44,
        ).move_to(DOWN * 0.10)

        self.play(Write(titulo))
        self.play(Write(explicacao))
        self.play(Write(formula))

        caixa = SurroundingRectangle(
            formula,
            color=ORANGE,
            buff=0.20,
            stroke_width=4,
        )

        self.play(Create(caixa))
        self.play(FadeIn(alternativa, shift=UP))
        self.next_slide()