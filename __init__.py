from aqt import mw
from aqt.editor import Editor
from aqt.qt import *
from aqt.utils import showInfo
from aqt.gui_hooks import editor_did_init_buttons
import re

def change_font_size(editor: Editor, direction: str):
    """Vergrößert oder verkleinert den markierten Text im aktuell bearbeiteten Feld."""
    # Sicherstellen, dass ein Feld aktiv ist
    if editor.currentField is None:
        showInfo("Bitte klicke zuerst in ein Feld.")
        return

    # Markierten Text aus dem Editor holen
    selected = editor.web.selectedText()
    if not selected:
        showInfo("Bitte Text markieren.")
        return
    
    if '\n' in selected:
        zeilen = selected.split('\n')
    else:
        zeilen = [selected]
    
    # Feldindex bestimmen und aktuellen HTML-Inhalt lesen
    field_index = editor.currentField
    html = editor.note.fields[field_index]

    for zeile in zeilen:
    
        if not zeile:
            continue
            
        # Regex vorbereiten (markierten Text sicher escapen)
        escaped = re.escape(zeile)
        pattern = re.compile(
            rf"<span[^>]*font-size:\s*(\d+)%[^>]*>({escaped})</span>",
            re.IGNORECASE
        )
    
        match = pattern.search(html)
        if match:
            # Wenn der markierte Text schon in einem span mit Font-Size ist → anpassen
            old_size = int(match.group(1))
            new_size = old_size + 10 if direction == "bigger" else old_size - 10
            new_size = max(50, min(400, new_size))  # Begrenzen auf 50–400 %
            replacement = f'<span style="font-size:{new_size}%">{match.group(2)}</span>'
            html = pattern.sub(replacement, html, count=1)
        else:
            # Neuen <span> um den markierten Text setzen
            new_size = 110 if direction == "bigger" else 90
            html = html.replace(
                zeile,
                f'<span style="font-size:{new_size}%">{zeile}</span>',
                1
            )
    
        # Aktualisieren des Feldes und Redraw im Editor
        editor.note.fields[field_index] = html
        editor.loadNoteKeepingFocus()


def remove_all_spans(editor: Editor):
    """Entfernt alle <span>-Tags im aktuellen Feld, behält aber den Text."""
    if editor.currentField is None:
        showInfo("Bitte zuerst ein Feld aktivieren.")
        return

    field_index = editor.currentField
    html_content = editor.note.fields[field_index]

    # Alle <span ...>...</span> entfernen, Text behalten
    html_content = re.sub(r'<span[^>]*>(.*?)</span>', r'\1', html_content, flags=re.DOTALL | re.IGNORECASE)

    editor.note.fields[field_index] = html_content
    editor.loadNoteKeepingFocus()


def on_setup_buttons(buttons, editor: Editor):
    """Fügt die Buttons A+ und A− hinzu."""
    btn_bigger = editor.addButton(
        icon=None,
        cmd="makeTextBigger",
        func=lambda e=editor: change_font_size(e, "bigger"),
        tip="Markierten Text vergrößern (STRG + Plus)",
        label="A+",
        keys="Ctrl++"
    )
    buttons.append(btn_bigger)

    btn_smaller = editor.addButton(
        icon=None,
        cmd="makeTextSmaller",
        func=lambda e=editor: change_font_size(e, "smaller"),
        tip="Markierten Text verkleinern (STRG + Minus)",
        label="A−",
        keys="Ctrl+-"
    )
    buttons.append(btn_smaller)
    
    btn_remove = editor.addButton(
        icon=None,
        cmd="removeAllSpans",
        func=lambda e=editor: remove_all_spans(e),
        tip="Setzt alle Vergrößerungen/Verkleinerungen zurück",
        label="A (reset)"
    )
    buttons.append(btn_remove)

editor_did_init_buttons.append(on_setup_buttons)
