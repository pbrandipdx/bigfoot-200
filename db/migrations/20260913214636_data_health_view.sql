-- 20260913214636_data_health_view
--
-- One row you can read at a glance to answer "are the numbers trustworthy?"
-- without taking anyone's word for it. The daily check-in ends every readout
-- with a line built from this, so silence is never mistaken for health.

create or replace view data_health as
with a as (
  select (start_local at time zone 'UTC')::date d,
         distance_m, elevation_gain_m, raw,
         case when coalesce(distance_m,0) > 800 and coalesce(elevation_gain_m,0) > 0
              then 5280.0 * elevation_gain_m / distance_m end as ft_per_mile
  from activities
)
select
  (select max(d) from a)                                         as activities_through,
  (select max(day) from garmin_daily)                            as garmin_through,
  (current_date - (select max(d) from a))                        as activities_days_stale,
  (current_date - (select max(day) from garmin_daily))           as garmin_days_stale,
  (select count(*) from a)                                       as activity_rows,
  (select count(*) from a where raw is not null and raw ? 'total_elevation_gain')
                                                                 as rows_with_strava_payload,
  (select round(avg(ft_per_mile)) from a where ft_per_mile is not null)  as avg_ft_per_mile,
  (select round(max(ft_per_mile)) from a where ft_per_mile is not null)  as max_ft_per_mile,
  (select count(*) from a where ft_per_mile > 1800)              as unit_guard_violations,
  (select count(*) from pg_trigger
     where tgrelid = 'activities'::regclass
       and tgname = 'activities_units_guard_trg'
       and not tgisinternal)                                     as unit_guard_installed;
