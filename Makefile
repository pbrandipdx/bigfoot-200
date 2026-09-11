# Bigfoot 200 — rebuild generated pages from tracker/weeks.json
.PHONY: all tracker clean

all: tracker

tracker:
	@cd tracker && python3 build.py && mv bigfoot-tracker.html ../build/
	@echo "-> build/bigfoot-tracker.html"


clean:
	@rm -f build/bigfoot-tracker.html
