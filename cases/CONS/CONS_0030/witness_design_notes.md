# Witness Design Notes

- The salary sum for `deptno=10` exceeds the HAVING threshold, so the EXISTS predicate is live. No department name matches any employee name, which means the source and positive rewrite preserve every employee while the hard negative inner join drops them all.
