-- 20260913214549_activities_units_guard
--
-- Unit guard for activities.
--
-- Strava sends BOTH `distance` and `total_elevation_gain` in METRES, and the
-- columns store metres; weekly_progress is the single place that converts gain
-- to feet. On 2026-09-13 a Claude reading the Strava API in chat treated
-- total_elevation_gain as feet and under-reported climbing by 3.28x. The
-- database survived that only because nothing wrote to it. Now that the daily
-- check-in writes here, the rule needs to live in Postgres, where no prompt can
-- ignore it.
--
-- The check is exact where it can be: if the row carries its own raw Strava
-- payload, the stored columns must MATCH that payload. A converted number
-- cannot match its own source. Rows with no payload fall back to a loose
-- plausibility ceiling.
--
-- Catches BOTH directions. A steepness ceiling alone would miss the dangerous
-- one: dividing by 3.28 makes gain too SMALL, which looks perfectly plausible.

create or replace function activities_units_guard() returns trigger
language plpgsql as $$
declare
  raw_gain numeric;
  raw_dist numeric;
  ft_per_mile numeric;
begin
  if new.raw is not null and new.raw ? 'total_elevation_gain' then
    raw_gain := (new.raw->>'total_elevation_gain')::numeric;
    if new.elevation_gain_m is null
       or abs(new.elevation_gain_m - raw_gain) > greatest(1.0, raw_gain * 0.01) then
      raise exception
        'elevation_gain_m=% does not match raw.total_elevation_gain=% for activity %. '
        'Strava sends METRES; store it unconverted (x3.28084 happens once, in weekly_progress).',
        new.elevation_gain_m, raw_gain, new.id;
    end if;
  end if;

  if new.raw is not null and new.raw ? 'distance' then
    raw_dist := (new.raw->>'distance')::numeric;
    if new.distance_m is null
       or abs(new.distance_m - raw_dist) > greatest(1.0, raw_dist * 0.01) then
      raise exception
        'distance_m=% does not match raw.distance=% for activity %. '
        'Strava sends METRES; store it unconverted.',
        new.distance_m, raw_dist, new.id;
    end if;
  end if;

  -- No payload to check against: fall back to physical plausibility.
  -- 5280 * gain_m / dist_m is exactly feet per mile. Patrick's 122 measured
  -- activities average 62 ft/mile and peak at 322. 1,800 is a ~34% average
  -- grade over the whole outing - beyond any real session, including steep
  -- repeats, and comfortably tripped by a x3.28 inflation of a hard day.
  if coalesce(new.distance_m, 0) > 800 and coalesce(new.elevation_gain_m, 0) > 0 then
    ft_per_mile := 5280.0 * new.elevation_gain_m / new.distance_m;
    if ft_per_mile > 1800 then
      raise exception
        'activity % is % ft/mile (% m gain over % m) - implausible. '
        'Likely a metres/feet conversion applied to elevation_gain_m, which must be METRES.',
        new.id, round(ft_per_mile), new.elevation_gain_m, new.distance_m;
    end if;
  end if;

  return new;
end $$;

drop trigger if exists activities_units_guard_trg on activities;
create trigger activities_units_guard_trg
  before insert or update on activities
  for each row execute function activities_units_guard();
