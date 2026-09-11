# The phone dashboard

`template.html` + `../plan/schedule.json` → `../../bigfoot200-training/index.html`

    make dashboard

`bigfoot200-training` is a **view**. Never edit its `index.html` — it is overwritten
from here every build. Block dates, vertical targets and the race ladder are written
in `plan/block-targets.md` and `plan/sub100-plan.md`, transcribed into
`plan/schedule.json`, and generated out. One place to change a number.

After building, push the view repo:

    cd ../bigfoot200-training && git add -A && git commit -m "Regenerate" && git push

Still hardcoded in `template.html`: a few dated Block-1 Saturday prescriptions
(Angels Rest, Three Sisters). Those are one-off workout notes, not schedule data.
