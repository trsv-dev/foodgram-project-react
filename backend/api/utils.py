from datetime import datetime
from io import BytesIO

from django.http import HttpResponse
from django.template.loader import get_template
from weasyprint import HTML

from foodgram.settings import TEMPLATES_DIR


def create_shopping_cart(username, ingredients):
    template_path = f'{TEMPLATES_DIR}/shopping_cart_template.html'
    template = get_template(template_path)

    context = {
        'username': username,
        'ingredients': ingredients,
        'current_date': datetime.today().strftime('%d.%m.%Y'),
    }
    html_string = template.render(context)

    pdf_file = BytesIO()
    HTML(string=html_string).write_pdf(pdf_file)

    response = HttpResponse(
        pdf_file.getvalue(), content_type='application/pdf'
    )
    response['Content-Disposition'] = \
        f'attachment; filename="{username}_download_list.pdf"'
    return response