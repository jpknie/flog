# Utility functions for flog application

def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]


from jinja2 import Markup

class MomentJS(object):
	""" Helper class for rendering moment.js datetime
	"""

	def __init__(self, timestamp):
		self.timestamp = timestamp

	def render(self, format):
		return Markup("<script>\ndocument.write(moment(\"%s\").%s);\n</script>" % (self.timestamp.strftime("%Y-%m-%dT%H:%M:%S Z"), format))

	def format(self, fmt):
		return self.render("format(\"%s\")" % fmt)