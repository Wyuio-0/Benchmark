from markupsafe import Markup


def format_note(text):
    """将备注中的换行转换为 HTML 换行；本函数不对输入内容做 HTML 转义。"""
    return Markup(text.replace('\n', '<br>'))
