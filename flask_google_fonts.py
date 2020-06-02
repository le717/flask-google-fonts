from typing import Optional

from flask import Flask
from jinja2 import Markup


__all__ = ["GoogleFonts"]


class GoogleFonts:
    """Add fast-rendering Google Fonts to your Flask app.

    Uses the techniques outlined in Harry Robert's post.
    https://csswizardry.com/2020/05/the-fastest-google-fonts/
    """

    def __init__(self, app: Optional[Flask] = None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Optional[Flask]):
        if app is None:
            raise TypeError("Parameter 'app' must be a Flask instance")

        @app.context_processor
        def context_processor() -> dict:
            """Register the extension with the app."""
            return {"GoogleFonts": self.render}

    def render(self, url: str) -> str:
        """Render fast-loading Google Fonts markup.

        :param url - A base Google Fonts v1/2 url, without any query params.
        :return str HTML code to go in the <head>.
        """
        # Copied from https://csswizardry.com/2020/05/the-fastest-google-fonts/
        # - 1. Preemptively warm up the fonts’ origin.
        # - 2. Initiate a high-priority, asynchronous fetch for the CSS file.
        # -    Works in most modern browsers.
        # - 3. Initiate a low-priority, asynchronous fetch that gets applied
        # -    to the page only after it’s arrived. Works in all browsers
        # -    with JavaScript enabled.
        # - 4. In the unlikely event that a visitor has intentionally disabled
        # -    JavaScript, fall back to the original method. The good news is
        # -    that, although this is a render-blocking request, it can still
        # -    make use of the preconnect which makes it marginally faster
        # -    than the default.
        html = """<link rel="preconnect" crossorigin href="https://fonts.gstatic.com">
<link rel="preload" as="style" href="{url}&display=swap">
<link rel="stylesheet" media="print" onload="this.media='all'" href="{url}&display=swap">
<noscript>
  <link rel="stylesheet" href="{url}&display=swap">
</noscript>""".format(
            url=url
        )
        return Markup(html)
