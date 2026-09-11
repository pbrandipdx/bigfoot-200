# Bigfoot 200 — rebuild generated pages from tracker/weeks.json
.PHONY: all tracker racebook clean

all: tracker racebook

tracker:
	@cd tracker && python3 build.py && mv bigfoot-tracker.html ../build/
	@echo "-> build/bigfoot-tracker.html"

racebook:
	@cd tracker && python3 build_racebook.py && mv racebook.html ../build/
	@echo "-> build/racebook.html"

clean:
	@rm -f build/bigfoot-tracker.html build/racebook.html
