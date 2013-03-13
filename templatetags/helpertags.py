from google.appengine.ext.webapp import template
register = template.Library()

print "I got loaded"

@register.inclusion_tag('input.html')
def input(key, pretty, note=''):
	return {'key':key, 'pretty':pretty, 'note':note}
