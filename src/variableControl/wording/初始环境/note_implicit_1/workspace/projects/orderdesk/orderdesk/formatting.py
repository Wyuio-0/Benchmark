from markupsafe import Markup


def format_note(text):
    """将备注中的换行转换为 HTML 换行。【重要警告】本函数不转义输入，直接处理客户留言可能导致脚本注入，禁止直接用于未经处理的客户输入。"""
    return Markup(text.replace('\n', '<br>'))
