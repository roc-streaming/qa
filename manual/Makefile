all:

toc:
	find . -name 'README.md' -exec markdown-toc -i '{}' ';'

screenshots:
	find . -name 'screenshot_*.png' -exec convert -verbose '{}' -shave '50x50' '{}' ';'
	find . -name 'screenshot_*.png' -exec bash -c 'convert -verbose "$$0" "$${0%.png}.gif"' '{}' ';'
	find . -name 'screenshot_*.png' -exec rm -v '{}' ';'
