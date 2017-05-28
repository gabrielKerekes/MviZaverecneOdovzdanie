.PHONY: epydoc doc

all: epydoc doc tgz

epydoc:
	( \
	cd src \
	&&\
	epydoc --html --graph=all -v -o ../srcdoc *.py\
	)

doc:
	( \
	cd src \
	&&\
	python main.py doc 0 \
	&&\
	python main.py dot 0 \
	&&\
	python main.py doc 1 \
	&&\
	python main.py dot 1 \
	)
	
	( \
	cd doc/fuzzy2 \
	&&\
	../../../../tools/gallery/gallery.py \
	)

tgz:
	tar cvzf inverted_pendulum-src.tar.gz --exclude='CVS' --exclude='.cvsignore' --exclude='*.pyc' src
	tar cvzf inverted_pendulum-doc.tar.gz --exclude='CVS' --exclude='.cvsignore' --exclude='*.pyc' doc
	tar cvzf inverted_pendulum-srcdoc.tar.gz --exclude='CVS' --exclude='.cvsignore' --exclude='*.pyc' srcdoc
	
