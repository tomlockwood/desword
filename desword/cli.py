import sys
import site_generator

input = sys.argv[1]
output = sys.argv[2]
href_base = sys.argv[3]

site_generator.SiteGenerator(input, output, href_base)
