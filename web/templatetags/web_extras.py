import os
import textwrap
from typing import Text

from django import template
from django.urls.base import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

from accounts.forms import StudyListSearchForm
from accounts.queries import get_child_eligibility
from project.settings import DEBUG

register = template.Library()

GOOGLE_TAG_MANAGER_ID = os.environ.get("GOOGLE_TAG_MANAGER_ID", "")


def format(text: Text) -> Text:
    if not DEBUG and GOOGLE_TAG_MANAGER_ID:
        return mark_safe(textwrap.dedent(text))
    else:
        return ""


@register.simple_tag
def child_is_valid_for_study_criteria_expression(child, study):
    return get_child_eligibility(child, study.criteria_expression)


@register.simple_tag
def google_tag_manager() -> Text:
    return format(
        f"""
    <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
    new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
    j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
    'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
    }})(window,document,'script','dataLayer','{GOOGLE_TAG_MANAGER_ID}');</script>
    """
    )


@register.simple_tag
def nav_item(request, url_name, text):
    li_class = ""
    url = reverse(url_name)

    if request.path == url:
        li_class = "active"

    return mark_safe(f'<li class="{li_class}"><a href="{url}">{_(text)}</a></li>')


@register.simple_tag
def studies_tab_text(tabs):
    for tab in tabs:
        if tab.data["selected"]:
            value = tab.data["value"]
            if value == StudyListSearchForm.Tabs.all_studies.value[0]:
                return _(
                    "Please note you'll need a laptop or desktop computer (not a mobile device) running Chrome or Firefox to participate, unless a specific study says otherwise."
                )
            elif value == StudyListSearchForm.Tabs.synchronous_studies.value[0]:
                return _(
                    'You and your child can participate in these studies right now by choosing a study and then clicking "Participate." Please note you\'ll need a laptop or desktop computer (not a mobile device) running Chrome or Firefox to participate, unless a specific study says otherwise.'
                )
            elif value == StudyListSearchForm.Tabs.asynchronous_studies.value[0]:
                return _(
                    'You and your child can participate in these studies by scheduling a time to meet with a researcher (usually over video conferencing). Choose a study and then click "Participate" to sign up for a study session in the future.'
                )
