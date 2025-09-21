def build_table(
    columns,
    rows,
    form_action="#",
    editable_fields=None,
    row_click_url=None,
    actions=None,
    widgets=None,
    generate_ids=False
):
    """
    columns: dict di colonne. Es: {"name": {"label": "Nome", "type": "text", "editable": True}}
    rows: lista di dict. Ogni dict è una riga, con almeno una chiave "id"
    form_action: url di submit per modifica riga
    editable_fields: lista di campi modificabili (sovrascrive quelli definiti in columns)
    row_click_url: stringa tipo "/user/{id}"
    actions: lista di dict con {label, url, class}
    widgets: dict di widget Jinja richiamabili tramite `attribute(widgets, nome)(row)`
    """
    table = {
        "columns": [],
        "rows": [],
        "form_action": form_action,
        "row_click_url": row_click_url,
        "actions": actions or [],
        "widgets": widgets or {},
    }

    editable_fields = set(editable_fields or [])

    for key, info in columns.items():
        col = {
            "key": key,
            "label": info.get("label", key),
            "type": info.get("type", "text"),
            "editable": info.get("editable", key in editable_fields),
            "extra": info.get("extra", None),
        }
        table["columns"].append(col)
    cur_id=0
    for row in rows:
        processed = {
            "id":  row["id"] if row['id'] else cur_id if generate_ids else None,
            "click_url": row_click_url.format(**row) if row_click_url else None,
            "fields": [],
        }
        cur_id+=1
        for col in table["columns"]:
            if col['type'] == 'prerender-widgets':
                value = table['widgets'][col['extra']](row)
            else:
                value = row.get(col["key"], "")
            processed["fields"].append({
                "key": col["key"],
                "value": value,
                "type": col["type"],
                "editable": col["editable"],
                "extra": col["extra"],
            })
        processed["raw"] = row  # utile per i widget o le azioni
        table["rows"].append(processed)

    return table