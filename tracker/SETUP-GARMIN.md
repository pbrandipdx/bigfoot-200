# Garmin sync — one-time setup

The system Python on this Mac is 3.9 (Xcode Command Line Tools). `garminconnect`
resolves to 0.2.8 there, which predates hill score, endurance score, running
tolerance and training readiness. You need Python 3.10+ to get the current
library.

## 1. A newer Python

    brew --version

If that errors, install Homebrew first from https://brew.sh — then:

    brew install python@3.12

## 2. Rebuild the venv

    cd ~/Developer/bigfoot-200
    rm -rf .venv
    /opt/homebrew/bin/python3.12 -m venv .venv
    .venv/bin/pip install -U pip garminconnect requests
    .venv/bin/pip show garminconnect | head -2

You want version 0.2.2x or newer, not 0.2.8.

## 3. Credentials

    cp tracker/.env.example tracker/.env
    open -e tracker/.env

Four values. `tracker/.env` is gitignored — it never gets committed and never
passes through Claude.

- `GARMIN_EMAIL`, `GARMIN_PASSWORD` — password only for the first run; a token
  caches to `~/.garminconnect` and you can blank it afterwards
- `SUPABASE_URL` — already filled in
- `SUPABASE_SERVICE_KEY` — Supabase dashboard → bigfoot-200-training →
  Project Settings → API → **service_role** (not `anon`; RLS is on)

## 4. Check what your version can reach

    .venv/bin/python tracker/sync_garmin.py discover

Prints every `get_*` method and marks the ones this script wants OK or MISS.

## 5. Backfill, then keep it current

    .venv/bin/python tracker/sync_garmin.py backfill 2024-09-01 2026-09-11
    .venv/bin/python tracker/sync_garmin.py daily

The backfill takes a while — it sleeps 1s per day, so about two years is ~12
minutes. Metrics only exist from when Garmin started computing them on a device
you owned, so early dates will return nothing for the newer scores.

## Weekly

Run `daily` after each Sunday's Strava refresh:

    cd ~/Developer/bigfoot-200 && .venv/bin/python tracker/sync_garmin.py daily && make sync

## What it fills

- `garmin_daily` — resting HR, HRV, sleep stages, body battery, stress, SpO2,
  respiration, steps, intensity minutes
- `garmin_training` — hill score, endurance score, running tolerance, VO2 max,
  training status, race predictions
- `garmin_raw` — every payload verbatim, so a mapping bug loses nothing

These are what the monitors in `plan/block-targets.md` read.
