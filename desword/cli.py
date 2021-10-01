import sys
from .site_generator import SiteGenerator

input = sys.argv[1]
output = sys.argv[2]
href_base = sys.argv[3]

SiteGenerator(input, output, href_base)
