from app.main import HeaderGrammar

def test_no_eoh():
    raw = """
# Titre

Content
"""
    
    hg = HeaderGrammar(raw)
    hg.parse()

    assert getattr(hg, "content", None) == raw
    assert getattr(hg, "raw", None) == raw

def test_eoh():
    raw = """
----------

# Titre

Content
"""

    content = """
# Titre

Content
"""
    
    hg = HeaderGrammar(raw)
    hg.parse()

    assert getattr(hg, "content", None) == content
    assert getattr(hg, "raw", None) == raw

def test_attribute():
    raw = """
attribute : value
----------

# Titre

Content
"""

    content = """
# Titre

Content
"""
    
    hg = HeaderGrammar(raw)
    hg.parse()

    assert getattr(hg, "attribute", None) == "value"
    assert getattr(hg, "content", None) == content


def test_comments():
    raw = """
attribute : value //comment : foo
----------

# Titre

Content
"""
    
    hg = HeaderGrammar(raw)
    hg.parse()

    assert getattr(hg, "attribute", None) == "value"
