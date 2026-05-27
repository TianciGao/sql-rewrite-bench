SELECT pt.Name AS PostType,
       stats.PostCount,
       stats.AverageScore,
       stats.AverageViewCount,
       stats.ActiveUsers
FROM PostTypes pt
JOIN (
  SELECT p.PostTypeId,
         COUNT(p.Id) AS PostCount,
         AVG(p.Score) AS AverageScore,
         AVG(p.ViewCount) AS AverageViewCount,
         COUNT(DISTINCT p.OwnerUserId) AS ActiveUsers
  FROM Posts p
  GROUP BY p.PostTypeId
) AS stats ON pt.Id = stats.PostTypeId
ORDER BY stats.PostCount DESC;
