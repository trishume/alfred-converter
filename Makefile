
FILES=converter icons icon.png info.plist poscUnits22.xml README.rst
ARGS=--recurse-paths --verbose
OUTFILE=unit_converter.alfredworkflow

all:
	rm -vf ${OUTFILE}
	zip ${ARGS} ${OUTFILE} ${FILES}

