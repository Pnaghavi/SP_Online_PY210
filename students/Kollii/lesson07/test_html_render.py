"""
test code for html_render.py

This is just a start -- you will need more tests!
"""

import io
import pytest

# import * is often bad form, but makes it easier to test everything in a module.
from html_render import *


def render_result(element, ind=""):
    outfile = io.StringIO()
    if ind:
        element.render(outfile, ind)
    else:
        element.render(outfile)
    return outfile.getvalue()

########
# Step 1
########

def test_init():
    e = Element()

    e = Element("this is some text")


def test_append():
 
    e = Element("this is some text")
    e.append("some more text")


def test_render_element():

    e = Element("this is some text")
    e.append("and this is some more text")

    file_contents = render_result(e).strip()
    print(file_contents)
   
    assert("this is some text") in file_contents
    assert("and this is some more text") in file_contents

   
    assert file_contents.index("this is") < file_contents.index("and this")

    assert file_contents.startswith("<html>")
    assert file_contents.endswith("</html>")

def test_render_element2():
   
    e = Element()
    e.append("this is some text")
    e.append("and this is some more text")

    file_contents = render_result(e).strip()

  
    assert("this is some text") in file_contents
    assert("and this is some more text") in file_contents

    # make sure it's in the right order
    assert file_contents.index("this is") < file_contents.index("and this")

   
    assert file_contents.startswith("<html>")
    assert file_contents.endswith("</html>")



# # ########
# # # Step 2
# # ########


# tests for the new tags
def test_html():
    e = Html("this is some text")
    e.append("and this is some more text")

    file_contents = render_result(e).strip()

    assert("this is some text") in file_contents
    assert("and this is some more text") in file_contents
    print(file_contents)
    assert file_contents.endswith("</html>")


def test_body():
    e = Body("this is some text")
    e.append("and this is some more text")

    file_contents = render_result(e).strip()

    assert("this is some text") in file_contents
    assert("and this is some more text") in file_contents

    assert file_contents.startswith("<body>")
    assert file_contents.endswith("</body>")


def test_p():
    e = P("this is some text")
    e.append("and this is some more text")

    file_contents = render_result(e).strip()

    assert("this is some text") in file_contents
    assert("and this is some more text") in file_contents

    assert file_contents.startswith("<p>")
    assert file_contents.endswith("</p>")


def test_sub_element():
    """
    tests that you can add another element and still render properly
    """
    page = Html()
    page.append("some plain text.")
    page.append(P("A simple paragraph of text"))
    page.append("Some more plain text.")

    file_contents = render_result(page)
    print(file_contents) # so we can see it if the test fails

    # note: The previous tests should make sure that the tags are getting
    #       properly rendered, so we don't need to test that here.
    assert "some plain text" in file_contents
    assert "A simple paragraph of text" in file_contents
    assert "Some more plain text." in file_contents
    assert "some plain text" in file_contents
    # but make sure the embedded element's tags get rendered!
    assert "<p>" in file_contents
    assert "</p>" in file_contents




#######
#Step 3
#######

def test_head():
    e = Head("This is a Header")

    file_contents = render_result(e).strip()

    assert("This is a Header") in file_contents

    assert file_contents.startswith("<head>")
    assert file_contents.endswith("</head>")
 
def test_title():
    """
    Test whether a one line tag is created for the title class
    """

    e = Title("This is a Title")

    file_contents = render_result(e).strip()

    assert("This is a Title") in file_contents
    print(file_contenets)
    assert '\n' not in file_contents
    assert file_contents.startswith("<title>")
    assert file_contents.endswith("</title>")

def test_title_append():
    """Test that a Title element can't append content"""
    with pytest.raises(NotImplementedError):
        t = Title("This is a Title")
        t.append("some content")


def test_attributes():
    e = P("A paragraph of text", style="text-align: center", id="intro")

    file_contents = render_result(e).strip()
    print(file_contents)

    assert "A paragraph of text" in file_contents
    assert file_contents.endswith("</p>")
    assert file_contents.startswith("<p ")
    assert 'style="text-align: center"' in file_contents
    assert 'id="intro"' in file_contents
    assert file_contents[:-1].index(">") > file_contents.index('id="intro"')
    assert file_contents[:file_contents.index(">")].count(" ") == 3

def test_hr():
    """
    A simple horizontal rule with no attributes
    """
    hr = Hr()
    file_contents= render_result(hr)
    print(file_contents)
    assert file_contents == '<hr />\n'

def test_hr_attr():
    """
    A horizontal rule with an attribute
    """
    hr = Hr(width=400)
    file_contents = render_result(hr)
    print(file_contents)
    assert file_contents == '<hr width="400" />\n'

def test_br():
    br = Br()
    file_contents = render_result(br)
    print(file_contents)
    assert file_contents == '<br />\n'

def test_content_in_br():
    with pytest.raises(TypeError):
        br = Br('some content')

def test_append_content_in_br():
    with pytest.raises(TypeError):
        br = Br()
        br.append('some content')

def test_anchor():
    a = A('http://google.com', 'link to google')
    file_contents = render_result(a)
    print(file_contents)
    assert file_contents == '<a href="http://google.com">link to google</a>'
    assert 'link to google' in file_contents

def test_header():
    h2 = H(2, "The text of a header")
    file_contents = render_result(h2).strip()
    print(file_contents)
    assert file_contents == '<h2>The text of a header</h2>'

#####################
# indentation testing
#  Uncomment for Step 9 -- adding indentation
#####################


def test_indent():
    """
    Tests that the indentation gets passed through to the renderer
    """
    html = Html("some content")
    file_contents = render_result(html, ind="").rstrip()  #remove the end newline

    print(file_contents)
    lines = file_contents.split("\n")
    assert lines[1].startswith("<")
    print(repr(lines[-1]))
    assert lines[-1].startswith("<")


def test_indent_contents():
    """
    The contents in a element should be indented more than the tag
    by the amount in the indent class attribute
    """
    html = Element("some content")
    file_contents = render_result(html, ind="")
    print(file_contents)
    lines = file_contents.split("\n")
    assert lines[1].startswith(Element.indent)


def test_multiple_indent():
    """
    make sure multiple levels get indented fully
    """
    body = Body()
    body.append(P("some text"))
    html = Html(body)

    file_contents = render_result(html)

    print(file_contents)
    lines = file_contents.split("\n")
    for i in range(3):  # this needed to be adapted to the <DOCTYPE> tag
        assert lines[i + 1].startswith(i * Element.indent + "<")

    assert lines[4].startswith(3 * Element.indent + "some")


def test_element_indent1():
    """
    Tests whether the Element indents at least simple content

    we are expecting to to look like this:

    <html>
        this is some text
    </html>

    More complex indentation should be tested later.
    """
    e = Element("this is some text")

    # This uses the render_results utility above
    file_contents = render_result(e).strip()

    # making sure the content got in there.
    assert("this is some text") in file_contents

    # break into lines to check indentation
    lines = file_contents.split('\n')
    # making sure the opening and closing tags are right.
    assert lines[0] == "<html>"
    # this line should be indented by the amount specified
    # by the class attribute: "indent"
    assert lines[1].startswith(Element.indent + "thi")
    assert lines[2] == "</html>"
    assert file_contents.endswith("</html>")
