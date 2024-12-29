import sys
sys.path.append('/Users/brendan/src/fancontrol/lib')


import utemplate

def render_template(template_path, data):
    """
    Renders a uTemplate template with the given data.

    Args:
        template_path (str): Path to the template file.
        data (dict): Data to render in the template.

    Returns:
        str: Rendered HTML content.
    """
    # Load the template from the file
    with open(template_path, "r") as template_file:
        template_content = template_file.read()
    
    # Render the template with the provided data
    rendered_content = utemplate.render(template_content, data)
    return rendered_content

# Dynamic data to populate the template
data = {
    "title": "Leadership Portal",
    "heading": "Welcome to the Leadership Portal",
    "content": "Here is the list of our esteemed leaders:",
    "items": ["Leader 1", "Leader 2", "Leader 3"]
}

# Path to the template file
template_path = "leader_template.tpl"

# Render the template
rendered_html = render_template(template_path, data)

# Output the rendered HTML
print(rendered_html)