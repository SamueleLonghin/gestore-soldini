from datetime import date, datetime
import json
from markupsafe import Markup, escape

from tools.mapper import deserialize_options


def init_template_filters(app):
    @app.template_filter("date_display")
    def date_display(value):
        if isinstance(value, str) and value != "":
            value = datetime.strptime(value, app.config["DB_DATE_FORMAT"])

        if isinstance(value, datetime) or isinstance(value, date):
            return value.strftime(app.config["DISPLAY_DATE_FORMAT"])

        return value

    @app.template_filter("date_form")
    def date_form(value):
        if isinstance(value, str):
            value = datetime.strptime(value, app.config["DB_DATE_FORMAT"])

        if isinstance(value, datetime) or isinstance(value, date):
            return value.strftime(app.config["FORM_DATE_FORMAT"])
        return value
    
    @app.template_filter("json_deserialize")
    def json_deserialize(string):
        return json.loads(string)

    @app.template_filter("pk_to_text")
    def pk_to_text(pk, dictionary ):
        return dictionary.get(pk,'-')

    @app.template_filter("render_category_options")
    def render_category_options(categorie, *, selected: int | None = None):
            """
            Rende <optgroup><option> da un dict tipo:
            {'Casa': {1:'...', 2:'...'}, 'Trasporti': {...}, ...}

            Parametri:
            - selected: id già selezionato (es. 6) -> aggiunge selected sull'option
            - sort_groups: ordina alfabeticamente i gruppi
            - sort_items: ordina alfabeticamente le voci interne
            """
            
            # categorie = deserialize_options(categorie)
            if not categorie:
                return Markup("")

            html_parts: list[str] = []
            for tipo, sotto in categorie.items():
                if type(sotto) == str:
                    sel = ' selected' if selected is not None and tipo == selected else ''
                    html_parts.append(f'<option value="{tipo}"{sel}>{escape(sotto)}</option>')
                else:
                    html_parts.append(f'<optgroup label="{escape(tipo)}">')
                    items = sotto.items()
                    for k, label in items:
                        sel = ' selected' if selected is not None and k == selected else ''
                        html_parts.append(f'<option value="{k}"{sel}>{escape(label)}</option>')
                    html_parts.append("</optgroup>")
            return Markup("".join(html_parts))