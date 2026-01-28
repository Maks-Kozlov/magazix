from django.contrib.messages import get_messages
from django.template.loader import render_to_string

class AlpineMessageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if (
            "X-Alpine-Request" in request.headers
            and 300 > response.status_code >= 200
            and (messages := get_messages(request))
            and hasattr(response, 'content') # Ensure response has content (not FileResponse etc)
            and not response.content.strip().endswith(b"</html>") # Simple check for partial
        ):
            # Note: response.text might not be available on all response types, use content
            # response.text is available on TemplateResponse but we should be careful.
            # The article uses response.text check, but standard Django response is bytes in .content
            # Let's rely on render_to_string and appending to content if it's safe.
            
            # Re-implementing logic safely for Django responses
            try:
                 message_html = render_to_string(
                    "base.html#messages",
                    {"messages": messages},
                    request=request
                )
                 # Append to the response content
                 response.content = response.content + message_html.encode('utf-8')
            except Exception:
                # If rendering fails (e.g. template not found), just ignore
                pass

        return response
