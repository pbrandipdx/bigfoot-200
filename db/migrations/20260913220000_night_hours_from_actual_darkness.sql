-- 20260913_night_hours_from_actual_darkness
--
-- Night hours used to be a fixed clock window: on foot, 45+ min, starting
-- before 06:00 or at/after 20:00. That is wrong in both directions and worst
-- exactly when it matters. Portland's earliest sunset is 16:28 (Dec 10) and
-- its latest is 21:05 (Jun 26), so in December three and a half hours of real
-- darkness each evening went uncounted, while a June evening session in broad
-- daylight scored full marks. Block 1's night sessions start in November.
--
-- sun_times() is the NOAA approximation, checked against five published times
-- for Portland (Sep 13 06:46/19:27, Dec 10 sunset 16:28, Jun 26 sunset 21:05,
-- Jan 1 sunrise 07:49, Jun 15 sunrise 05:19) and matching all five within two
-- minutes. Local time comes from `at time zone 'America/Los_Angeles'`, so DST
-- is handled by Postgres rather than by hand.
--
-- NOTE the date re-anchoring at the end: the Julian-day basis put the correct
-- clock times on the previous calendar day for a west-longitude site, and
-- because least()/greatest() silently ignore NULLs and mismatched days, that
-- bug made dark_seconds() return the FULL duration of a midday hike. Sunrise
-- and sunset on date d are by definition on date d in local time.

create or replace function sun_times(d date)
returns table(sunrise timestamp, sunset timestamp)
language plpgsql immutable as $$
declare
  phi constant double precision := radians(45.5152);   -- Portland, OR
  lw  constant double precision := 122.6784;           -- west longitude, positive
  jd double precision; n double precision; jstar double precision;
  m double precision; c double precision; lam double precision;
  jtr double precision; dec_ double precision; cosw double precision; w double precision;
  r timestamp; s2 timestamp;
begin
  jd := (d - date '2000-01-01')::double precision + 2451544.5;
  n  := floor(jd - 2451545.0 + 0.0008);
  jstar := n + lw/360.0;
  m := (357.5291 + 0.98560028*jstar) - 360.0*floor((357.5291 + 0.98560028*jstar)/360.0);
  c := 1.9148*sin(radians(m)) + 0.0200*sin(radians(2*m)) + 0.0003*sin(radians(3*m));
  lam := (m + c + 180 + 102.9372) - 360.0*floor((m + c + 180 + 102.9372)/360.0);
  jtr := 2451545.0 + jstar + 0.0053*sin(radians(m)) - 0.0069*sin(radians(2*lam));
  dec_ := asin( sin(radians(lam)) * sin(radians(23.44)) );
  cosw := ( sin(radians(-0.833)) - sin(phi)*sin(dec_) ) / ( cos(phi)*cos(dec_) );
  cosw := greatest(-1.0, least(1.0, cosw));
  w := degrees(acos(cosw));
  r  := ((timestamptz '2000-01-01 12:00:00+00' + make_interval(secs => ((jtr - w/360.0) - 2451545.0)*86400))
          at time zone 'America/Los_Angeles')::timestamp;
  s2 := ((timestamptz '2000-01-01 12:00:00+00' + make_interval(secs => ((jtr + w/360.0) - 2451545.0)*86400))
          at time zone 'America/Los_Angeles')::timestamp;
  return query select (d + r::time)::timestamp, (d + s2::time)::timestamp;
end $$;

-- Seconds of an activity that fall between sunset and sunrise. Walks d-1, d and
-- d+1 so an effort crossing midnight, or a 20-hour day crossing two nights, is
-- counted correctly rather than clipped.
create or replace function dark_seconds(t0 timestamp, dur_s numeric)
returns numeric language plpgsql immutable as $$
declare
  t1 timestamp; total numeric := 0; d date; sr timestamp; ss timestamp;
begin
  if dur_s is null or dur_s <= 0 then return 0; end if;
  t1 := t0 + make_interval(secs => dur_s);
  for d in select generate_series(t0::date - 1, t1::date + 1, interval '1 day')::date loop
    select s.sunrise, s.sunset into sr, ss from sun_times(d) s;
    total := total + greatest(0, extract(epoch from (least(t1, sr) - greatest(t0, d::timestamp))));
    total := total + greatest(0, extract(epoch from (least(t1, (d+1)::timestamp) - greatest(t0, ss))));
  end loop;
  return total;
end $$;

-- weekly_progress gains two columns:
--   night_hours          every minute on foot that falls in darkness
--   night_session_hours  the same, but only runs and hikes of 45+ minutes -
--                        the deliberate sessions the plan asks for, rather than
--                        a pre-dawn dog walk in December
-- The finish-odds night gate reads night_session_hours.
