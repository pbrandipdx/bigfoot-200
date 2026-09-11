# Bigfoot 200 — rebuild generated pages from tracker/weeks.json
.PHONY: all tracker dashboard sync status clean

all: tracker dashboard

tracker:
	@cd tracker && python3 build.py && mv bigfoot-tracker.html ../build/
	@echo "-> build/bigfoot-tracker.html"


dashboard:
	@python3 dashboard/build.py

sync:
	@echo "-- pulling"
	@git pull --rebase --autostash
	@$(MAKE) --no-print-directory all
	@git add -A
	@git diff --cached --quiet || git commit -q -m "Sync $$(date +%Y-%m-%d\ %H:%M)"
	@echo "-- pushing bigfoot-200"
	@git push --quiet
	@if [ -d ../bigfoot200-training/.git ]; then \
		cd ../bigfoot200-training && git pull --rebase --autostash --quiet && git add -A && \
		(git diff --cached --quiet || git commit -q -m "Regenerate from bigfoot-200") && \
		echo "-- pushing bigfoot200-training" && git push --quiet; \
	else echo "-- view repo not cloned here, skipping"; fi
	@echo "-- in sync"

status:
	@printf '%-24s' "bigfoot-200:"; \
	git fetch --quiet 2>/dev/null; \
	printf 'behind %s, ahead %s, %s uncommitted\n' \
	  "$$(git rev-list --count HEAD..@{u} 2>/dev/null || echo ?)" \
	  "$$(git rev-list --count @{u}..HEAD 2>/dev/null || echo ?)" \
	  "$$(git status --porcelain | wc -l | tr -d ' ')"
	@if [ -d ../bigfoot200-training/.git ]; then cd ../bigfoot200-training; \
		printf '%-24s' "bigfoot200-training:"; \
		git fetch --quiet 2>/dev/null; \
		printf 'behind %s, ahead %s, %s uncommitted\n' \
		  "$$(git rev-list --count HEAD..@{u} 2>/dev/null || echo ?)" \
		  "$$(git rev-list --count @{u}..HEAD 2>/dev/null || echo ?)" \
		  "$$(git status --porcelain | wc -l | tr -d ' ')"; \
	else printf '%-24s not cloned here\n' "bigfoot200-training:"; fi

clean:
	@rm -f build/bigfoot-tracker.html
