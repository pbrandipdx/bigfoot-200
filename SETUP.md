# Setting up the other devices

## 1. Mac mini — push this repo up (do this first)

The repo is already built, committed, and pointed at the right remote.
Create the empty repo on GitHub, then push. In **Terminal**:

    gh repo create pbrandipdx/bigfoot-200 --private --source=. --remote=origin --push

If you don't have `gh` installed, create it at
https://github.com/new (name: `bigfoot-200`, **Private**, no README/.gitignore),
then:

    cd ~/Developer/bigfoot-200
    git push -u origin main

## 2. MacBook

    cd ~/Developer            # NOT ~/Desktop, NOT ~/Documents — those are iCloud
    git clone https://github.com/pbrandipdx/bigfoot-200.git
    cd bigfoot-200
    make                      # confirm it builds

Then find whatever Bigfoot files already exist on the MacBook and move them
somewhere out of the way — `~/Desktop/BIGFOOT-old/`. Do not merge them by hand.
If you think something on the MacBook is newer than what's in the repo, say so
and I'll diff it properly against the clone.

## 3. iPhone

Nothing to install. The phone reads the published racebook:

**https://claude.ai/code/artifact/1b073ecd-aa0c-44d3-8549-f4416989a436**

Add it to your home screen. It updates when the racebook is republished after a
weekly refresh — you never sync a file to the phone.

## 4. Stop iCloud from recreating the problem

System Settings → Apple Account → iCloud → Drive → **Desktop & Documents Folders**.

You don't have to switch it off. You do have to keep this repo out of it — which
is why it lives in `~/Developer`. If you ever see a folder ending in ` 2` or a file
ending in `_1`, that's iCloud, and it means something got saved in a synced folder.

## The daily habit

Both Macs, every time:

    git pull      # before you start
    git push      # when you stop

That's the whole system. Git tells you when two machines disagree, instead of
iCloud silently guessing and leaving you a `BIGFOOT 2` folder.
