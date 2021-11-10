<%!
    from pdoc.html_helpers import minify_css
    colors = [
        ("--bg-highlight-color", "#FFEE99", "#3E4951"),
        ("--bg-default", "#FFFFFF", "#22282D"),
        ## ...
    ]

    default = [f"{color[0]}: {color[1]};" for color in colors]
    dark = [f"{color[0]}: {color[2]};" for color in colors]

    root_light = f":root[data-theme='theme-light'] {{{''.join(default)}}}"
    root_dark = f":root[data-theme='theme-dark'] {{{''.join(dark)}}}"
    root_light_auto = f"@media (prefers-color-scheme: light) {{ :root[data-theme='theme-light'] {{{''.join(default)}}} }}"
    root_dark_auto = f"@media (prefers-color-scheme: dark) {{ :root[data-theme='theme-dark'] {{{''.join(dark)}}} }}"

    color_variables = f"{root_light}{root_dark}{root_light_auto}{root_dark_auto}"
%>

<%def name="style()" filter="minify_css">
    ${color_variables}
</%def>
