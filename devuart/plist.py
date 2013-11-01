class PlistBrowser(object):
    """
    LXML-based navigator for plist-style XML structures.
    """

    def __init__(self, plist):
        self.root = plist

    def parent(self):
        v = self.root.getparent()
        return PlistBrowser(v)

    def find(self, k):
        v = self.root.xpath(".//key[text() = %r]/following-sibling::*[1]" % k)
        if not v:
            raise KeyError
        return PlistBrowser(v[0])

    def get(self, k):
        v = self.root.xpath("./key[text() = %r]/following-sibling::*[1]" % k)
        if not v:
            raise KeyError
        return PlistBrowser(v[0])

    def iterkeys(self):
        assert self.root.tag == "dict"
        return iter(self.root.xpath("./key/text()"))

    def iteritems(self):
        keys = self.root.xpath("./key/text()")
        vals = self.root.xpath("./key/following-sibling::*[1]")
        return zip(
            keys,
            (PlistBrowser(v) for v in vals))

    def value(self):
        tag = self.root.tag
        if tag == "dict":
            return dict(self.iteritems())
        if tag == "array":
            return list(self)
        if tag == "true":
            return True
        if tag == "false":
            return False
        return self.root.text

    def __iter__(self):
        tag = self.root.tag
        if tag == "dict":
            return self.iterkeys()

        if tag == "array":
            vals = (PlistBrowser(v) for v in self.root.iterchildren())
            return vals

        raise ValueError()

    def __getitem__(self, k):
        return self.get(k)

    def __repr__(self):
        return "<PlistBrowser(%r)>" % self.root
