from __future__ import annotations

from html import escape

W, H = 1600, 1000


def _sheet(title: str, code: str, body: str, note: str = "PRANCHA DIDÁTICA · DADOS SINTÉTICOS · NÃO FABRICAR") -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(title)}">
<style>text{{font-family:Arial,Helvetica,sans-serif;fill:#182330}}.mono{{font-family:Consolas,monospace}}.muted{{fill:#667788}}.thin{{stroke:#354452;stroke-width:1.4;fill:none}}.wire{{stroke:#263d51;stroke-width:2.2;fill:none}}.signal{{stroke:#338a79;stroke-width:2;stroke-dasharray:8 5;fill:none}}.symbol{{stroke:#203140;stroke-width:2;fill:#fff}}.shade{{fill:#e9eef1;stroke:#263b4e;stroke-width:1.5}}.teal{{fill:#e3f2ef;stroke:#28695f;stroke-width:1.6}}.blue{{fill:#e8eff9;stroke:#315780;stroke-width:1.6}}.amber{{fill:#fbf2de;stroke:#86652a;stroke-width:1.6}}</style>
<rect width="1600" height="1000" fill="#fff"/><rect x="26" y="24" width="1548" height="952" fill="none" stroke="#1e2c38" stroke-width="2"/>
<text x="58" y="66" font-size="25" font-weight="700">{escape(title)}</text><text x="58" y="94" class="muted" font-size="13">PAINEL LAB · CONJUNTO DIDÁTICO PARA DEMONSTRAÇÃO DE GERAÇÃO ASSISTIDA POR IA</text>
<text x="1515" y="58" text-anchor="end" class="mono" font-size="14" font-weight="700">{escape(code)}</text><text x="1515" y="82" text-anchor="end" class="mono muted" font-size="12">REV. A · SEM ESCALA</text>
<line x1="48" y1="112" x2="1552" y2="112" stroke="#273744" stroke-width="1.5"/>
{body}
<line x1="48" y1="916" x2="1552" y2="916" stroke="#263744" stroke-width="1.5"/>
<text x="58" y="941" font-size="12" font-weight="700">{escape(note)}</text><text x="58" y="963" class="muted" font-size="10">Todos os identificadores, blocos e arranjos desta prancha foram criados para o laboratório público.</text>
<text x="1517" y="941" text-anchor="end" class="mono" font-size="12">PAINEL LAB / {escape(code)}</text><text x="1517" y="963" text-anchor="end" class="mono muted" font-size="10">FOLHA 1 / 1</text></svg>'''


def _box(x, y, w, h, label, sub="", klass="symbol", radius=5):
    subline = f'<text x="{x+w/2}" y="{y+h-12}" text-anchor="middle" font-size="11" class="muted">{escape(sub)}</text>' if sub else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" class="{klass}"/><text x="{x+w/2}" y="{y+25}" text-anchor="middle" font-size="14" font-weight="700">{escape(label)}</text>{subline}'


def _line(x1, y1, x2, y2, klass="wire"):
    return f'<path d="M{x1} {y1} L{x2} {y2}" class="{klass}"/>'


def _label(x, y, value, size=13, anchor="middle", bold=False, klass=""):
    weight = "700" if bold else "400"
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" font-weight="{weight}" class="{klass}">{escape(value)}</text>'


def single_line(layout):
    b=[]
    b.append(_label(800,150,"ALIMENTAÇÃO DE DEMONSTRAÇÃO",17,bold=True))
    b.append(_line(800,166,800,208)); b.append(_box(710,208,180,76,"QS-01","Seccionamento didático","shade"))
    b.append(_line(800,284,800,331)); b.append('<rect x="350" y="331" width="900" height="14" rx="3" fill="#d8e0e5" stroke="#253b4d" stroke-width="2"/>')
    b.append(_label(800,321,"BARRAMENTO PRINCIPAL · EXEMPLO",12,bold=True))
    branches=[(520,"QF-01","DRV-01","M-01"),(800,"QF-02","DRV-02","M-02"),(1080,"QF-03","RESERVA","—")]
    for x,qf,drv,motor in branches:
        b.append(_line(x,345,x,405)); b.append(f'<circle cx="{x}" cy="345" r="6" fill="#263d51"/>')
        b.append(_box(x-74,405,148,64,qf,"Proteção · símbolo","amber")); b.append(_line(x,469,x,514))
        b.append(_box(x-82,514,164,82,drv,"Módulo funcional","blue")); b.append(_line(x,596,x,651))
        if motor != "—":
            b.append(f'<circle cx="{x}" cy="700" r="43" class="symbol"/>'); b.append(_label(x,696,"M",22,bold=True)); b.append(_label(x,760,motor,13,bold=True)); b.append(_line(x,651,x,657))
        else:
            b.append(_box(x-65,666,130,68,"RESERVA","Posição sem carga","teal"))
        b.append(_label(x,790,"RAMAL DIDÁTICO",10,klass="muted"))
    b.append(_label(800,860,"Fluxo funcional: alimentação → seccionamento → distribuição → ramais de demonstração",14,klass="muted"))
    return _sheet("DIAGRAMA UNIFILAR · PAINEL DIDÁTICO", "PL-EL-001", "".join(b))


def control_diagram(layout):
    b=[]
    b.append(_label(250,164,"CAMPO · SINAIS FICTÍCIOS",15,bold=True)); b.append(_label(800,164,"CONTROLADOR",15,bold=True)); b.append(_label(1350,164,"ATUADORES / CARGAS",15,bold=True))
    b.append(_box(110,220,270,92,"S-01 · SENSOR A","Entrada digital · exemplo","teal"))
    b.append(_box(110,390,270,92,"S-02 · SENSOR B","Entrada analógica · exemplo","teal"))
    b.append(_box(610,245,380,275,"PLC-01","Controlador genérico","blue"))
    b.append(_box(660,326,128,70,"DI-01","Entrada","shade")); b.append(_box(812,326,128,70,"AI-01","Entrada","shade"))
    b.append(_box(660,420,128,70,"DO-01","Saída","shade")); b.append(_box(812,420,128,70,"AO-01","Saída","shade"))
    b.append(_box(1210,220,270,92,"Y-01 · ATUADOR A","Saída digital · exemplo","amber"))
    b.append(_box(1210,390,270,92,"DRV-01 · REFERÊNCIA","Comando demonstrativo","amber"))
    b.append('<path d="M380 266 H422 V300 H432 M518 300 H590 V361 H660" class="signal"/>')
    b.append('<path d="M380 436 H422 V405 H432 M518 405 H740 V361 H812" class="signal"/>')
    b.append('<path d="M788 455 H1010 V300 H1042 M1128 300 H1175 V266 H1210" class="signal"/>')
    b.append('<path d="M940 455 H1020 V405 H1042 M1128 405 H1170 V436 H1210" class="signal"/>')
    # terminal strips placed over each connection to make the I/O path explicit
    for x,y,tag in [(475,300,"X1:01"),(475,405,"X1:02"),(1085,300,"X2:01"),(1085,405,"X2:02")]:
        b.append(f'<rect x="{x-43}" y="{y-21}" width="86" height="42" rx="4" fill="#fff" stroke="#527064" stroke-width="1.5"/><text x="{x}" y="{y+5}" text-anchor="middle" font-size="11" class="mono">{tag}</text>')
    b.append(_label(800,620,"DI / DO / AI / AO: siglas didáticas para organizar a prancha, sem especificação de campo",13,klass="muted"))
    b.append(_box(495,690,610,95,"LEGENDA","Linha contínua = potência | Linha tracejada = sinal de controle","shade"))
    return _sheet("DIAGRAMA FUNCIONAL · CONTROLE E INTERFACES", "PL-AU-001", "".join(b))


def terminal_diagram(layout):
    n=min(24,max(8,layout["counts"]["terminal_positions"]))
    b=[]; x0=140; y0=300; tw=53; th=78; gap=5
    b.append(_label(800,160,"RÉGUA X1 · AGRUPAMENTO ILUSTRATIVO",17,bold=True))
    b.append(_label(800,189,"Identificação genérica para demonstrar referências cruzadas entre desenho e lista",12,klass="muted"))
    for i in range(n):
        x=x0+i*(tw+gap); group="SINAIS" if i< n*.65 else "RESERVA"
        b.append(f'<rect x="{x}" y="{y0}" width="{tw}" height="{th}" rx="3" class="{"teal" if group=="SINAIS" else "shade"}"/>')
        b.append(_label(x+tw/2,y0+25,f"{i+1:02d}",13,bold=True,klass="mono")); b.append(_label(x+tw/2,y0+53,"X1",10,klass="mono muted"))
        b.append(_line(x+tw/2,y0-44,x+tw/2,y0)); b.append(_line(x+tw/2,y0+th,x+tw/2,y0+th+42))
        b.append(_label(x+tw/2,y0-55,f"C{i+1:02d}",9,klass="mono muted"))
    b.append(_line(x0-15,y0+th+58,x0+n*(tw+gap)-gap+15,y0+th+58,"thin"))
    b.append(_label(800,475,"BLOCO TERMINAL · VISTA FRONTAL",12,klass="muted"))
    # schedule table
    tx,ty=180,545; cols=[110,220,410,390,250]; headers=["BORNE","GRUPO","ORIGEM","DESTINO","OBSERVAÇÃO"]
    xx=tx
    for cw,hd in zip(cols,headers):
        b.append(f'<rect x="{xx}" y="{ty}" width="{cw}" height="40" fill="#e8edf1" stroke="#526170"/>'); b.append(_label(xx+12,ty+26,hd,11,"start",True)); xx+=cw
    rows=[("X1:01","ENTRADA","S-01 / SINAL A","PLC-01 / DI-01","EXEMPLO"),("X1:02","ENTRADA","S-02 / SINAL B","PLC-01 / AI-01","EXEMPLO"),("X1:03","SAÍDA","PLC-01 / DO-01","Y-01 / ATUADOR","EXEMPLO"),("X1:04","SAÍDA","PLC-01 / AO-01","DRV-01 / REF.","EXEMPLO")]
    for ri,row in enumerate(rows):
        xx=tx; yy=ty+40+ri*42
        for cw,val in zip(cols,row):
            b.append(f'<rect x="{xx}" y="{yy}" width="{cw}" height="42" fill="#fff" stroke="#9aa7b0"/>'); b.append(_label(xx+12,yy+26,val,11,"start",False,"mono")); xx+=cw
    b.append(_label(800,790,f"POSIÇÕES EXIBIDAS: {n} · QUANTIDADE CONFIGURÁVEL · CONTEÚDO TOTALMENTE FICTÍCIO",12,klass="muted"))
    return _sheet("DIAGRAMA DE BORNES · LISTA DE CONEXÕES", "PL-TE-001", "".join(b))


def external_view(layout):
    b=[]; x,y,w,h=520,185,540,630
    b.append(_label(800,155,"VISTA FRONTAL · PORTA FECHADA",16,bold=True))
    b.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="#e8edf0" stroke="#24394b" stroke-width="3"/>')
    b.append(f'<rect x="{x+26}" y="{y+25}" width="{w-52}" height="{h-50}" rx="8" fill="#f8fafb" stroke="#7b8b98" stroke-width="1.5"/>')
    b.append(_box(x+170,y+88,200,104,"HMI-01","Interface demonstrativa","blue"))
    b.append(f'<rect x="{x+188}" y="{y+104}" width="164" height="56" rx="3" fill="#d4e5e9" stroke="#456171"/><text x="{x+270}" y="{y+138}" text-anchor="middle" font-size="13" class="mono">STATUS · DEMO</text>')
    for i,(lab,col) in enumerate([("PRONTO","#4c9b76"),("ATENÇÃO","#c89436"),("FALHA","#b65353")]):
        cx=x+150+i*120; cy=y+284
        b.append(f'<circle cx="{cx}" cy="{cy}" r="22" fill="{col}" stroke="#344657" stroke-width="2"/><circle cx="{cx}" cy="{cy}" r="8" fill="#f4f7f9"/>'); b.append(_label(cx,cy+50,lab,10,klass="muted"))
    for i,(lab,cx) in enumerate([("SELETOR",x+180),("CONFIRMAR",x+360)]):
        cy=y+430;b.append(f'<circle cx="{cx}" cy="{cy}" r="32" fill="#dce3e7" stroke="#405364" stroke-width="2"/><circle cx="{cx}" cy="{cy}" r="12" fill="#718390"/>');b.append(_label(cx,cy+58,lab,10,klass="muted"))
    b.append(f'<rect x="{x+w-48}" y="{y+315}" width="18" height="112" rx="5" fill="#c6d0d6" stroke="#526271"/><circle cx="{x+w-39}" cy="{y+370}" r="11" fill="#738797"/>')
    b.append(_label(800,850,"Dispositivos e rótulos são ilustrativos; não definem função de segurança ou operação real.",12,klass="muted"))
    return _sheet("VISTA EXTERNA · INTERFACE DO OPERADOR", "PL-ME-001", "".join(b))


def internal_layout(layout):
    b=[]; e=layout["enclosure"]; x,y,w,h=420,145,760,690; scale=min((w-70)/e["width_mm"],(h-70)/e["height_mm"]); pw=e["width_mm"]*scale; ph=e["height_mm"]*scale; px=x+(w-pw)/2; py=y+(h-ph)/2
    b.append(_label(800,137,f"PLACA DE MONTAGEM · ENVELOPE DEMONSTRATIVO {e['width_mm']} × {e['height_mm']} mm",14,bold=True))
    b.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" fill="#f4f6f7" stroke="#243b4d" stroke-width="2.5"/>')
    for ry in layout["rails_y"]:
        yy=py+ry*scale;b.append(f'<rect x="{px+18}" y="{yy}" width="{pw-36}" height="5" fill="#98a6ae" stroke="#4d5e6a"/>')
    colors={"protection":"amber","control":"blue","drive":"blue","terminals":"teal"}
    for c in layout["components"]:
        cx,cy,cw,ch=px+c["x"]*scale,py+c["y"]*scale,c["w"]*scale,c["h"]*scale
        b.append(f'<rect x="{cx:.1f}" y="{cy:.1f}" width="{cw:.1f}" height="{ch:.1f}" rx="3" class="{colors[c["kind"]]}"/>')
        b.append(_label(cx+cw/2,cy+18,c["id"],11,bold=True,klass="mono"))
        kind_label={"protection":"PROTE\u00c7\u00c3O","control":"CONTROLE","drive":"ACIONAMENTO","terminals":"R\u00c9GUA X1"}[c["kind"]]
        b.append(_label(cx+cw/2,cy+ch*.68,kind_label,7,klass="muted"))
    b.append(_line(px,py+ph+22,px+pw,py+ph+22,"thin"));b.append(_label(px+pw/2,py+ph+42,f"{e['width_mm']} mm",11,klass="mono"))
    b.append(_line(px-25,py,px-25,py+ph,"thin"));b.append(_label(px-40,py+ph/2,f"{e['height_mm']} mm",11,klass="mono"))
    b.append(_label(800,877,"Folgas, cabos, dissipação e acessibilidade não são calculados nesta demonstração.",12,klass="muted"))
    return _sheet("ARRANJO INTERNO · PLACA E COMPONENTES", "PL-LY-001", "".join(b))


def model_3d(layout):
    b=[];x0,y0=560,245;ew,eh=layout["enclosure"]["width_mm"],layout["enclosure"]["height_mm"];sc=min(420/ew,520/eh);fw,fh=ew*sc,eh*sc;dx,dy=120,-68;fx=x0;fy=y0
    b.append(_label(800,145,"MODELO VOLUMÉTRICO ESQUEMÁTICO · GABINETE E COMPONENTES",14,bold=True))
    b.append(f'<path d="M{fx} {fy} l{dx} {dy} h{fw} l{-dx} {-dy}z" fill="#dbe3e8" stroke="#20384b" stroke-width="2"/>')
    b.append(f'<path d="M{fx+fw} {fy} l{dx} {dy} v{fh} l{-dx} {-dy}z" fill="#d4dde2" stroke="#20384b" stroke-width="2"/>')
    b.append(f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" fill="#f2f5f6" stroke="#20384b" stroke-width="2.5"/>')
    b.append(f'<rect x="{fx+15}" y="{fy+15}" width="{fw-30}" height="{fh-30}" fill="#fff" stroke="#82929c" stroke-width="1.5"/>')
    palette={"protection":"#d5b76d","control":"#84b9c8","drive":"#86a8d4","terminals":"#80baa5"}
    for c in layout["components"]:
        x=fx+c["x"]*sc;y=fy+c["y"]*sc;cw=c["w"]*sc;ch=c["h"]*sc;d=12
        b.append(f'<path d="M{x} {y} l{d} {-d} h{cw} l{-d} {d}z" fill="#dce4e8" stroke="#42576a"/>')
        b.append(f'<path d="M{x+cw} {y} l{d} {-d} v{ch} l{-d} {d}z" fill="#d2dbe0" stroke="#42576a"/>')
        b.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="3" fill="{palette[c["kind"]]}" stroke="#31495d" stroke-width="1.5"/>')
        b.append(_label(x+cw/2,y+18,c["id"],10,bold=True,klass="mono"))
    b.append(_label(800,850,f"LARGURA {ew} mm · ALTURA {eh} mm · PROFUNDIDADE ILUSTRATIVA",12,klass="mono muted"))
    b.append(_label(800,875,"Perspectiva conceitual; não comprova dimensões, interferências nem fabricação.",11,klass="muted"))
    return _sheet("MODELO 3D · VISTA ISOMÉTRICA", "PL-3D-001", "".join(b))


def workflow():
    b=[];items=[(110,"REQUISITOS","Contexto, fontes e limites"),(400,"IA ASSISTIDA","Geração e iteração do código"),(690,"MODELO DE DADOS","Componentes e coordenadas"),(980,"GERADOR CAD","Desenhos vetoriais"),(1270,"PRANCHAS + 3D","Saídas e conferência")]
    for i,(x,title,sub) in enumerate(items):
        b.append(_box(x,340,220,130,title,sub,"teal" if i in (1,2) else "shade"))
        if i<len(items)-1:b.append(f'<path d="M{x+220} 405h54l-12 -9m12 9l-12 9" fill="none" stroke="#326d63" stroke-width="2.5"/>')
    b.append(_box(430,570,740,100,"REVISÃO HUMANA","Premissas · coerência · conferência visual · aprovação técnica","amber"))
    b.append(_line(800,470,800,570,"signal"));b.append(_label(800,280,"FLUXO DE DESENVOLVIMENTO · PAPÉIS SEPARADOS",16,bold=True))
    b.append(_label(800,740,"A IA apoia a criação das ferramentas; o código produz geometrias; pessoas qualificadas verificam e aprovam.",13,klass="muted"))
    return _sheet("FLUXO DE GERAÇÃO · IA, CÓDIGO, CAD E 3D", "PL-FL-001", "".join(b))


def build_drawings(layout):
    return {
        "01_unifilar.svg": single_line(layout),
        "02_controle.svg": control_diagram(layout),
        "03_bornes.svg": terminal_diagram(layout),
        "04_arranjo_interno.svg": internal_layout(layout),
        "05_vista_externa.svg": external_view(layout),
        "06_modelo_3d.svg": model_3d(layout),
        "07_fluxo_ia_cad.svg": workflow(),
    }
