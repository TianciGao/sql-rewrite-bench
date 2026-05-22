set search_path to attr113_sqlglot_sqlglot_transpile_same_dialect_noop_longtail;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
WITH HistoryStats AS (
    SELECT
        ph.PostId,
        COUNT(*) AS revision_count,
        COUNT(DISTINCT ph.UserId) AS distinct_editors,
        MIN(ph.CreationDate) AS first_revision_at,
        MAX(ph.CreationDate) AS last_revision_at
    FROM
        PostHistory ph
    GROUP BY
        ph.PostId
)
SELECT
    p.Id AS PostId,
    p.Title,
    hs.revision_count,
    hs.distinct_editors,
    hs.first_revision_at,
    hs.last_revision_at,
    p.Score,
    p.ViewCount
FROM
    HistoryStats hs
JOIN
    Posts p ON p.Id = hs.PostId
WHERE
    hs.revision_count >= 2
ORDER BY
    hs.revision_count DESC,
    hs.last_revision_at DESC,
    p.Id;
rollback;
