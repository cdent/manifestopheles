

def test_compile():
    try:
        import tiddlywebplugins.manifestopheles
        assert True
    except ImportError, exc:
        assert False, exc
