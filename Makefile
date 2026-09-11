# Bigfoot 200 — rebuild generated pages from tracker/weeks.json
.PHONY: all tracker dashboard clean

all: tracker dashboard

tracker:
	@cd tracker && python3 build.py && mv bigfoot-tracker.html ../build/
	@echo "-> build/bigfoot-tracker.html"


dashboard:
	@python3 dashboard/build.py

clean:
	@rm -f build/bigfoot-tracker.html
