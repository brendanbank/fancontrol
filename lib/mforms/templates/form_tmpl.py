# Autogenerated file
def render(header, form):
    yield """

<form action=\"\" method=\"post\" class=\"needs-validation row justify-content-md-center\" novalidate>

<div class=\"col-md-12\">
        <h2 class=\"text-center\">"""
    yield str(header)
    yield """</h2>
</div>

    <div class=\"row mt-3 col-md-9\">

"""
    for field in form:
        if field.get("type") == "checkbox":
            yield """
                <div class=\""""
            yield str(field.get("css"))
            yield """ position-relative mt-3\">
                    <div class=\"form-check form-switch\">
                      <input class=\"form-check-input\" type=\"checkbox\" name=\""""
            yield str(field.get("name"))
            yield """\" """
            if field.get("value") == "on":
                yield """checked """
            yield """id=\""""
            yield str(field.get("name"))
            yield """\">
                      <label class=\"form-check-label\" for=\""""
            yield str(field.get("name"))
            yield """\"><small>"""
            yield str(field.get("label"))
            yield """</small></label>
                    </div>
                </div>


"""
        elif field.get("type") == "hr":
            yield """
<!--
<div class=\"div-line\">
   <hr class=\"hr-line \">
   <span class=\"text-line\">This is text</span>
</div>
-->
            <div class=\""""
            yield str(field.get("css"))
            yield """ position-relative mt-5 text-center div-line\">
                   <hr class=\"hr-line \">
                   <span class=\"text-line fw-bold fs-6\">"""
            yield str(field.get("value"))
            yield """</span>

            </div>
"""
        else:
            yield """            <div class=\""""
            yield str(field.get("css"))
            yield """ position-relative mt-3\">
                <label for=\""""
            yield str(field.get("name"))
            yield """\" class=\"form-label\"><small>"""
            yield str(field.get("label"))
            yield """</small></label>
                
                <input type=\"text\" class=\"form-control"""
            if field.get("value") != "":
                yield """ """
                yield str(field.get("valid_css"))
            yield """\"
                        id=\""""
            yield str(field.get("name"))
            yield """\" name=\""""
            yield str(field.get("name"))
            yield """\"
                        value=\""""
            yield str(field.get("value"))
            yield """\"
                        aria-describedby=\""""
            yield str(field.get("name"))
            yield """_feedback\" required>
             
                <div id=\""""
            yield str(field.get("name"))
            yield """_feedback\" class=\"invalid-tooltip\">
                  """
            yield str(field.get("label"))
            yield """ """
            yield str(field.get("error"))
            yield """ 
                </div>
              </div>
"""
    yield """</div>


    <div class=\"row mt-3\">
    
        <div class=\"col-md-4 position-relative text-center\">
        </div>

        <div class=\"col-md d-grid gap-2 col-md\">
          <button class=\"btn btn-primary\" type=\"submit\">Submit</button>

        </div>
        <div class=\"col-md-4 position-relative text-center\">
        </div>
    </div>

</form>

<!--
                <div class=\"col-md-sm-2\">
                    &nbsp;
                </div>
                <div class=\"col-md-sm-3\">
                    <div class=\"form-check form-switch\">
                      <input class=\"form-check-input\" type=\"checkbox\" name=\""""
    yield str(field.get("name"))
    yield """\" """
    if field.get("value") == "on":
        yield """checked """
    yield """id=\""""
    yield str(field.get("name"))
    yield """\">
                      <label class=\"form-check-label\" for=\""""
    yield str(field.get("name"))
    yield """\">"""
    yield str(field.get("label"))
    yield """</label>
                    </div>
                </div>
-->

"""