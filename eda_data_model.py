import marimo

__generated_with = "0.25.0"
app = marimo.App(width="full")


@app.cell
def _():
    import hashlib
    import json
    import marimo as mo
    import pandas as pd

    # Carga de la metadata del esquema exportada de DBeaver
    df_schema = pd.read_csv("schema_metadata.csv")

    # Mapeo de subcampos para estructuras JSON complejas (OpenRTB / Tappx Core)
    JSON_SCHEMAS_MAP = {
        "ext": {
            "descripcion": "Objeto de extensión OpenRTB / Tappx con metadatos de subasta, cookies y adaptadores de demanda.",
            "subcampos": [
                {"subcampo": "ext.bidder", "tipo": "Object/JSON", "ejemplo": "{'tappx': {'seat': '101'}}", "descripcion": "Parámetros del adaptador de demanda/DSP."},
                {"subcampo": "ext.prebid", "tipo": "Object/JSON", "ejemplo": "{'storedrequest': {'id': 'adunit_1'}}", "descripcion": "Configuración de Prebid Server."},
                {"subcampo": "ext.gpid", "tipo": "String", "ejemplo": "/12345/app_banner_main", "descripcion": "Global Placement ID (GAM/AdServer)."},
                {"subcampo": "ext.schain", "tipo": "Object/JSON", "ejemplo": "{'ver':'1.0','nodes':[{'asi':'tappx.com'}]}", "descripcion": "SupplyChain validation (ads.txt / sellers.json)."},
                {"subcampo": "ext.consents", "tipo": "Object/JSON", "ejemplo": "{'gdpr': 1, 'consent_string': 'CP123...'}", "descripcion": "Cadenas de consentimiento TCFv2 / CCPA."}
            ]
        },
        "json_data": {
            "descripcion": "Payload crudo con metadatos completos de la solicitud (device, geo, imp).",
            "subcampos": [
                {"subcampo": "json_data.device.ip", "tipo": "String", "ejemplo": "185.12.34.5", "descripcion": "IP de origen del dispositivo."},
                {"subcampo": "json_data.device.ua", "tipo": "String", "ejemplo": "Mozilla/5.0 (iPhone...)", "descripcion": "User-Agent del navegador o app."},
                {"subcampo": "json_data.device.ifa", "tipo": "String", "ejemplo": "EA7583CD-A667-48BC-B806-42ECB2B48D12", "descripcion": "Identificador publicitario (IDFA / GAID)."},
                {"subcampo": "json_data.imp[].banner.w", "tipo": "Int", "ejemplo": "320", "descripcion": "Ancho del banner en píxeles."},
                {"subcampo": "json_data.imp[].banner.h", "tipo": "Int", "ejemplo": "50", "descripcion": "Alto del banner en píxeles."}
            ]
        },
        "json_prices": {
            "descripcion": "Desglose financiero completo de la subasta (Floor prices, net bids, márgenes y comisiones).",
            "subcampos": [
                {"subcampo": "json_prices.price_request_publisher", "tipo": "Decimal", "ejemplo": "0.4500", "descripcion": "Floor price mínimo exigido por el publisher."},
                {"subcampo": "json_prices.price_request_network", "tipo": "Decimal", "ejemplo": "0.6000", "descripcion": "Floor price ajustado enviado al DSP/Red."},
                {"subcampo": "json_prices.price_response_network_net", "tipo": "Decimal", "ejemplo": "1.2000", "descripcion": "Precio neto devuelto por la red ganadora."},
                {"subcampo": "json_prices.price_response_publisher", "tipo": "Decimal", "ejemplo": "0.9500", "descripcion": "Precio final pagado al publisher."},
                {"subcampo": "json_prices.margen_base", "tipo": "Decimal", "ejemplo": "0.1500", "descripcion": "Margen de beneficio retenido por Tappx."}
            ]
        },
        "json_price": {
            "descripcion": "Variante del desglose financiero de subasta (mismas propiedades que json_prices).",
            "subcampos": [
                {"subcampo": "json_price.price_request_publisher", "tipo": "Decimal", "ejemplo": "0.4500", "descripcion": "Floor price mínimo del publisher."},
                {"subcampo": "json_price.price_response_network_net", "tipo": "Decimal", "ejemplo": "1.2000", "descripcion": "Puja neta devuelta por la red."}
            ]
        },
        "json_device": {
            "descripcion": "Atributos técnicos del dispositivo cliente capturados durante la solicitud.",
            "subcampos": [
                {"subcampo": "json_device.ip", "tipo": "String", "ejemplo": "185.12.34.5", "descripcion": "IP pública del usuario."},
                {"subcampo": "json_device.ua", "tipo": "String", "ejemplo": "Mozilla/5.0 (Android...)", "descripcion": "User-Agent completo."},
                {"subcampo": "json_device.ifa", "tipo": "String", "ejemplo": "EA7583CD-A667...", "descripcion": "IDFA / GAID / AAID."},
                {"subcampo": "json_device.os", "tipo": "String", "ejemplo": "android", "descripcion": "Sistema operativo detectado."}
            ]
        }
    }

    # Valores de muestra exhaustivos mapeados para cada campo exacto del catálogo ClickHouse
    SAMPLE_VALUES_MAP = {
        # Campos JSON/Estructurados
        "json_data": "JSON: {'id': 'req_981', 'imp': [{'id': '1', 'banner': {'w': 320, 'h': 50}}]}",
        "json_prices": "JSON: {'price_request_publisher': 0.45, 'price_request_network': 0.60, 'price_response_network_net': 1.20, 'price_response_publisher': 0.95}",
        "json_price": "JSON: {'price_request_publisher': 0.45, 'price_request_network': 0.60, 'price_response_network_net': 1.20, 'price_response_publisher': 0.95}",
        "json_device": "JSON: {'ip': '185.12.34.5', 'ua': 'Mozilla/5.0...', 'ifa': 'EA7583CD-A667-48BC-B806-42ECB2B48D12', 'os': 'android'}",
        "json_extra": "JSON: {'app_version': '2.1.0', 'sdk_version': 'Tappx_4.2', 'schain': {'ver':'1.0'}}",
        "json_qa": "JSON: {'qa_status': 'passed', 'latency_ms': 42, 'fraud_score': 0.01}",
        "json_cache": "JSON: {'cache_id': 'c_98123', 'ttl': 300, 'stored_price': 0.85}",
        "delivery_json_data": "JSON: {'adm': '<script...>','nurl': 'https://tappx.com/win'}",
        "delivery_json_cache": "JSON: {'cached_at': '2026-09-25 12:00:00', 'status': 'valid'}",
        "ext": "JSON: {'bidder': {'tappx': {'seat': '101'}}, 'gpid': '/1234/banner', 'schain': {'ver':'1.0'}}",
        "extra": "JSON: {'internal_tag': 'test_group_a'}",
    
        # Dimensiones del Dominio (Keys / Combos)
        "publisher": "'pub_9812', 'tappx_direct_102', 'app_publisher_55'",
        "ad_unit": "'interstitial_bottom', 'banner_top_300x250', 'rewarded_video_1'",
        "adunit": "'interstitial_bottom', 'banner_top_300x250', 'rewarded_video_1'",
        "bundle": "'com.game.racing3d', 'com.news.portal', 'id123456789'",
        "country": "'ES', 'US', 'DE', 'FR', 'BR', 'MX'",
        "ad_size": "'300x250', '320x50', '728x90', '1920x1080'",
        "network": "'net_pubmatic', 'net_rubicon', 'net_applovin', 'bidder_internal'",
        "device_os": "'android', 'ios', 'windows', 'tizen', 'webos'"
    }

    mo.md("# 📊 Explorador del Modelo de Datos - Tappx")
    return JSON_SCHEMAS_MAP, SAMPLE_VALUES_MAP, df_schema, hashlib, json, mo


@app.cell
def _(df_schema, mo):
    todos_los_campos = sorted(df_schema["column_name"].dropna().unique().tolist())

    # Multiselección de campos
    filtro_campo = mo.ui.multiselect(
        options=todos_los_campos,
        value=["json_prices", "json_data"] if "json_prices" in todos_los_campos and "json_data" in todos_los_campos else [todos_los_campos[0]],
        label="🔎 Selecciona los campos a inspeccionar:"
    )

    mo.vstack([
        mo.md("## 1️⃣ Bloque de Inspección de Campos"),
        filtro_campo
    ])
    return (filtro_campo,)


@app.cell
def _(JSON_SCHEMAS_MAP, SAMPLE_VALUES_MAP, df_schema, filtro_campo, mo):
    campos_seleccionados = filtro_campo.value

    if not campos_seleccionados:
        bloque_1_output = mo.md("⚠️ Selecciona al menos un campo arriba para inspeccionar.")
    else:
        # 1. Filtrar la presencia de los campos en las tablas
        df_presencia = df_schema[df_schema["column_name"].isin(campos_seleccionados)][
            ["column_name", "database_name", "table_name", "data_type", "column_key"]
        ].drop_duplicates().sort_values(by=["column_name", "database_name", "table_name"])

        # 2. Asignar los valores de muestra exactos
        df_presencia["Valores de Muestra"] = df_presencia["column_name"].apply(
            lambda col: SAMPLE_VALUES_MAP.get(
                str(col).lower(), 
                f"Valores alfanuméricos / numéricos estándar de '{col}'"
            )
        )

        df_presencia.columns = ["Campo", "Capa (Database)", "Tabla", "Tipo de Dato", "Key", "Valores de Muestra"]

        # 3. Construir la vista expandida para los objetos JSON presentes
        json_html_list = []
        for c_sel in campos_seleccionados:
            json_info = JSON_SCHEMAS_MAP.get(str(c_sel).lower(), None)
            if json_info:
                filas = ""
                for s in json_info["subcampos"]:
                    filas += f"""
                    <tr style="border-bottom: 1px solid #E2E8F0;">
                        <td style="padding: 6px 10px; font-weight: bold; color: #1E293B;">{s['subcampo']}</td>
                        <td style="padding: 6px 10px; color: #0284C7; font-family: monospace;">{s['tipo']}</td>
                        <td style="padding: 6px 10px; color: #475569; font-family: monospace; font-size: 11px;">{s['ejemplo']}</td>
                        <td style="padding: 6px 10px; color: #334155;">{s['descripcion']}</td>
                    </tr>
                    """
                json_card = f"""
                <div style="background-color: #F0F9FF; border: 1px solid #BAE6FD; border-radius: 8px; padding: 12px; margin-top: 15px;">
                    <h4 style="color: #0369A1; margin-bottom: 6px;">📦 Estructura Interna del Campo JSON: <code>{c_sel}</code></h4>
                    <p style="font-size: 12px; color: #0C4A6E; margin-bottom: 10px;">{json_info['descripcion']}</p>
                    <table style="width: 100%; border-collapse: collapse; font-size: 12px; background: white; border-radius: 6px; overflow: hidden;">
                        <thead>
                            <tr style="background-color: #E0F2FE; text-align: left; color: #0369A1;">
                                <th style="padding: 8px 10px;">Subcampo</th>
                                <th style="padding: 8px 10px;">Tipo</th>
                                <th style="padding: 8px 10px;">Ejemplo</th>
                                <th style="padding: 8px 10px;">Descripción</th>
                            </tr>
                        </thead>
                        <tbody>{filas}</tbody>
                    </table>
                </div>
                """
                json_html_list.append(mo.Html(json_card))

        bloque_1_output = mo.vstack([
            mo.md(f"### 🎯 Presencia y Muestras para: `{', '.join(campos_seleccionados)}` ({len(df_presencia)} coincidencias)"),
            mo.ui.table(df_presencia),
            *json_html_list,
            mo.md("---")
        ])

    bloque_1_output
    return


@app.cell
def _(df_schema, mo):
    mo.md("## 2️⃣ Bloque de Diagrama de Capas y Relaciones")

    capas_unicas = sorted(df_schema["database_name"].dropna().unique().tolist())

    filtro_capas_diagrama = mo.ui.multiselect(
        options=capas_unicas,
        value=capas_unicas,
        label="🔍 Selecciona Capas (raw, normalized, consolidated):"
    )

    filtro_capas_diagrama
    return (filtro_capas_diagrama,)


@app.cell
def _(df_schema, filtro_capas_diagrama, mo):
    df_capas_diagrama = df_schema[
        df_schema["database_name"].isin(filtro_capas_diagrama.value)
    ].copy()

    tablas_unicas_diagrama = sorted(df_capas_diagrama["table_name"].unique().tolist())

    filtro_tablas_diagrama = mo.ui.multiselect(
        options=tablas_unicas_diagrama,
        value=tablas_unicas_diagrama[:6] if len(tablas_unicas_diagrama) >= 6 else tablas_unicas_diagrama,
        label="📌 Selecciona Tablas para graficar en el Canvas:"
    )

    filtro_tablas_diagrama
    return (filtro_tablas_diagrama,)


@app.cell
def _(
    df_schema,
    filtro_capas_diagrama,
    filtro_tablas_diagrama,
    hashlib,
    json,
    mo,
):
    if not filtro_tablas_diagrama.value:
        bloque_2_output = mo.md("⚠️ Selecciona al menos una tabla para renderizar el diagrama.")
    else:
        df_canvas = df_schema[
            (df_schema["database_name"].isin(filtro_capas_diagrama.value))
            & (df_schema["table_name"].isin(filtro_tablas_diagrama.value))
        ].copy()

        conteo_cols = df_canvas["column_name"].value_counts()
        cols_compartidas = conteo_cols[conteo_cols > 1].index.tolist()

        PALETA = [
            {"bg": "#FEF08A", "text": "#854D0E", "border": "#FACC15"},
            {"bg": "#BFDBFE", "text": "#1E40AF", "border": "#60A5FA"},
            {"bg": "#BBF7D0", "text": "#166534", "border": "#4ADE80"},
            {"bg": "#FBCFE8", "text": "#9D174D", "border": "#F472B6"},
            {"bg": "#DDD6FE", "text": "#5B21B6", "border": "#A78BFA"},
            {"bg": "#FED7AA", "text": "#9A3412", "border": "#FB923C"},
            {"bg": "#CCFBF1", "text": "#115E59", "border": "#2DD4BF"},
            {"bg": "#E2E8F0", "text": "#334155", "border": "#94A3B8"},
        ]

        def obtener_color(col):
            if col not in cols_compartidas:
                return {"bg": "#FFFFFF", "text": "#1F2937", "border": "transparent"}
            idx = int(hashlib.md5(col.encode("utf-8")).hexdigest(), 16) % len(PALETA)
            return PALETA[idx]

        tables_payload = []
        grid_cols = 3
        spacing_x = 340
        spacing_y = 380

        for idx, ((capa, tabla), grp) in enumerate(df_canvas.groupby(["database_name", "table_name"])):
            t_id = f"{capa}__{tabla}"
            pos_x = 40 + (idx % grid_cols) * spacing_x
            pos_y = 40 + (idx // grid_cols) * spacing_y

            cols_data = []
            for _, row in grp.iterrows():
                c_name = str(row["column_name"])
                c_type = (
                    str(row["data_type"])
                    .replace("LowCardinality(", "")
                    .replace("Nullable(", "")
                    .replace(")", "")
                )
                is_pk = str(row.get("column_key", "")).upper() == "PRI"
                c_style = obtener_color(c_name)

                cols_data.append({
                    "name": c_name,
                    "type": c_type,
                    "is_pk": is_pk,
                    "is_shared": c_name in cols_compartidas,
                    "bg": c_style["bg"],
                    "text": c_style["text"],
                    "border": c_style["border"],
                })

            tables_payload.append({
                "id": t_id,
                "layer": capa.lower(),
                "name": tabla,
                "x": pos_x,
                "y": pos_y,
                "columns": cols_data,
            })

        connections = []
        drawn_pairs = set()
        for i in range(len(tables_payload)):
            t1 = tables_payload[i]
            c1 = {c["name"]: c for c in t1["columns"]}

            for j in range(i + 1, len(tables_payload)):
                t2 = tables_payload[j]
                c2 = {c["name"]: c for c in t2["columns"]}

                comunes = set(c1.keys()).intersection(set(c2.keys())).intersection(cols_compartidas)
                claves_prioritarias = [
                    "publisher", "ad_unit", "adunit", "bundle", "country", "size",
                    "network", "app", "id", "user"
                ]
                comunes_ordenados = sorted(
                    list(comunes),
                    key=lambda x: any(k in x.lower() for k in claves_prioritarias),
                    reverse=True,
                )

                for campo in comunes_ordenados[:5]:
                    pair_key = tuple(sorted([f"{t1['id']}:{campo}", f"{t2['id']}:{campo}"]))
                    if pair_key not in drawn_pairs:
                        drawn_pairs.add(pair_key)
                        style = obtener_color(campo)
                        connections.append({
                            "from_table": t1["id"],
                            "to_table": t2["id"],
                            "field": campo,
                            "color": style["border"],
                        })

        html_canvas = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                * {{ box-sizing: border-box; margin: 0; padding: 0; user-select: none; }}
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                    background-color: #F8FAFC;
                    overflow: auto;
                    height: 100vh;
                    position: relative;
                }}
                #board {{
                    position: relative;
                    min-width: 1600px;
                    min-height: 1000px;
                    padding: 20px;
                }}
                svg#connections {{
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    pointer-events: none;
                    z-index: 1;
                }}
                .table-card {{
                    position: absolute;
                    width: 300px;
                    min-width: 200px;
                    min-height: 120px;
                    background: #FFFFFF;
                    border-radius: 8px;
                    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -2px rgba(0,0,0,0.1);
                    border: 1px solid #E2E8F0;
                    z-index: 2;
                    cursor: grab;
                    resize: both;
                    overflow: hidden;
                    display: flex;
                    flex-direction: column;
                }}
                .table-card:active {{ cursor: grabbing; z-index: 10; }}
                .card-header {{
                    padding: 10px 12px;
                    color: #FFFFFF;
                    font-weight: 700;
                    font-size: 13px;
                    border-top-left-radius: 7px;
                    border-top-right-radius: 7px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    flex-shrink: 0;
                }}
                .layer-raw {{ background: #C2410C; }}
                .layer-normalized {{ background: #047857; }}
                .layer-consolidated {{ background: #1D4ED8; }}
            
                .layer-tag {{
                    font-size: 9px;
                    padding: 2px 6px;
                    border-radius: 4px;
                    background: rgba(255,255,255,0.25);
                    letter-spacing: 0.5px;
                }}
                .col-list {{
                    flex-grow: 1;
                    overflow-y: auto;
                    font-size: 11px;
                }}
                .col-row {{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding: 5px 10px;
                    border-bottom: 1px solid #F1F5F9;
                    transition: background 0.15s;
                }}
                .col-name {{
                    font-weight: 500;
                    display: flex;
                    align-items: center;
                    gap: 4px;
                }}
                .pk-pill {{
                    font-size: 8px;
                    background: #FEF08A;
                    color: #854D0E;
                    border: 1px solid #EAB308;
                    border-radius: 3px;
                    padding: 1px 4px;
                    font-weight: 800;
                }}
                .col-type {{
                    font-size: 10px;
                    color: #64748B;
                    font-family: monospace;
                }}
                path.rel-line {{
                    stroke-width: 2.5;
                    fill: none;
                    stroke-dasharray: 4, 3;
                    opacity: 0.75;
                    transition: stroke-width 0.2s, opacity 0.2s;
                }}
                path.rel-line:hover {{
                    stroke-width: 4.5;
                    opacity: 1;
                }}
            </style>
        </head>
        <body>
            <div id="board">
                <svg id="connections"></svg>
                <div id="cards-container"></div>
            </div>

            <script>
                const tables = {json.dumps(tables_payload)};
                const connections = {json.dumps(connections)};
                const board = document.getElementById('board');
                const svg = document.getElementById('connections');
                const container = document.getElementById('cards-container');

                tables.forEach(t => {{
                    const card = document.createElement('div');
                    card.className = 'table-card';
                    card.id = t.id;
                    card.style.left = t.x + 'px';
                    card.style.top = t.y + 'px';

                    let colsHtml = '';
                    t.columns.forEach(c => {{
                        const pkBadge = c.is_pk ? '<span class="pk-pill">🔑 PK</span>' : '';
                        const borderStyle = c.is_shared ? `border-left: 4px solid ${{c.border}}; background-color: ${{c.bg}}; color: ${{c.text}};` : '';
                        colsHtml += `
                            <div class="col-row" id="${{t.id}}__${{c.name}}" style="${{borderStyle}}">
                                <span class="col-name">${{pkBadge}} ${{c.name}}</span>
                                <span class="col-type">${{c.type}}</span>
                            </div>
                        `;
                    }});

                    card.innerHTML = `
                        <div class="card-header layer-${{t.layer}}">
                            <span>${{t.name}}</span>
                            <span class="layer-tag">${{t.layer.toUpperCase()}}</span>
                        </div>
                        <div class="col-list">${{colsHtml}}</div>
                    `;

                    container.appendChild(card);
                    makeDraggableAndResizable(card);
                }});

                function drawLines() {{
                 svg.innerHTML = '';
                        const boardRect = board.getBoundingClientRect();

                        connections.forEach(conn => {{
                            const el1 = document.getElementById(`${{conn.from_table}}__${{conn.field}}`);
                            const el2 = document.getElementById(`${{conn.to_table}}__${{conn.field}}`);

                            if (el1 && el2) {{
                                const card1 = el1.closest('.table-card');
                                const card2 = el2.closest('.table-card');

                                const r1 = el1.getBoundingClientRect();
                                const r2 = el2.getBoundingClientRect();
                                const c1Rect = card1.getBoundingClientRect();
                                const c2Rect = card2.getBoundingClientRect();

                                // Verificar que el campo sea visible dentro del área de scroll de la tarjeta
                                const isVisible1 = (r1.top >= c1Rect.top) && (r1.bottom <= c1Rect.bottom);
                                const isVisible2 = (r2.top >= c2Rect.top) && (r2.bottom <= c2Rect.bottom);

                                if (isVisible1 && isVisible2) {{
                                    const isCard1Left = c1Rect.left < c2Rect.left;

                                    // Enganchar la línea a los bordes laterales exteriores de las tarjetas
                                    const x1 = isCard1Left ? (c1Rect.right - boardRect.left) : (c1Rect.left - boardRect.left);
                                    const y1 = (r1.top + r1.bottom) / 2 - boardRect.top;

                                    const x2 = isCard1Left ? (c2Rect.left - boardRect.left) : (c2Rect.right - boardRect.left);
                                    const y2 = (r2.top + r2.bottom) / 2 - boardRect.top;

                                    const dx = Math.min(Math.abs(x2 - x1) * 0.5, 150);
                                    const d = `M ${{x1}} ${{y1}} C ${{x1 + (isCard1Left ? dx : -dx)}} ${{y1}}, ${{x2 + (isCard1Left ? -dx : dx)}} ${{y2}}, ${{x2}} ${{y2}}`;

                                    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
                                    path.setAttribute('d', d);
                                    path.setAttribute('class', 'rel-line');
                                    path.setAttribute('stroke', conn.color);
                                    svg.appendChild(path);
                                }}
                        }}
                    }});
                }}

                function makeDraggableAndResizable(el) {{
                    let isDragging = false;
                    let startX, startY, initX, initY;

                    const resizeObserver = new ResizeObserver(() => {{
                        drawLines();
                    }});
                    resizeObserver.observe(el);

                    el.addEventListener('mousedown', e => {{
                        const rect = el.getBoundingClientRect();
                        const isResizeHandle = (e.clientX > rect.right - 16) && (e.clientY > rect.bottom - 16);
                    
                        if (e.target.closest('.col-list') || isResizeHandle) return;
                    
                        isDragging = true;
                        startX = e.clientX;
                        startY = e.clientY;
                        initX = el.offsetLeft;
                        initY = el.offsetTop;
                        document.addEventListener('mousemove', onMouseMove);
                        document.addEventListener('mouseup', onMouseUp);
                    }});

                    function onMouseMove(e) {{
                        if (!isDragging) return;
                        el.style.left = (initX + e.clientX - startX) + 'px';
                        el.style.top = (initY + e.clientY - startY) + 'px';
                        drawLines();
                    }}

                    function onMouseUp() {{
                        isDragging = false;
                        document.removeEventListener('mousemove', onMouseMove);
                        document.removeEventListener('mouseup', onMouseUp);
                    }}
                }}

                setTimeout(drawLines, 100);
                window.addEventListener('resize', drawLines);
            </script>
        </body>
        </html>
        """

        bloque_2_output = mo.vstack([
            mo.iframe(html=html_canvas, width="100%", height="750px")
        ])

    bloque_2_output
    return


if __name__ == "__main__":
    app.run()
