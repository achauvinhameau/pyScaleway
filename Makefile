all:
	@echo make all
	@echo make lint or bandit or pep or flake
	@echo make quality
	@echo make clean

PYSRCS = *py C*/*py
IGNORE = --ignore=E501

quality: pep flake bandit lint

lint:
	@python3 -m pylint -d C0330 ${PYSRCS}

bandit:
	@bandit ${PYSRCS}

pep:
	@python3 -m pycodestyle --statistics ${IGNORE} ${PYSRCS}

flake:
	@flake8 ${IGNORE} ${PYSRCS}

clean:
	@rm -f *~ .*~ C*/*~
	@rm -rf __pycache__ C*/__pycache__ 
