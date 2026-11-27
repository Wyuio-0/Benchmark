from markupsafe import Markup


def format_note(text):
    """将备注中的换行转换为 HTML 换行，供页面显示。"""
    return Markup(text.replace('\n', '<br>'))
