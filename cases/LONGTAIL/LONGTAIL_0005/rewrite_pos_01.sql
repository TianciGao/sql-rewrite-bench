SELECT u.DisplayName,
       COALESCE(stats.TotalPosts, 0) AS TotalPosts,
       COALESCE(stats.TotalQuestions, 0) AS TotalQuestions,
       COALESCE(stats.TotalAnswers, 0) AS TotalAnswers,
       COALESCE(stats.TotalTagWikis, 0) AS TotalTagWikis
FROM Users u
LEFT JOIN (
  SELECT p.OwnerUserId,
         COUNT(p.Id) AS TotalPosts,
         SUM(CASE WHEN p.PostTypeId = 1 THEN 1 ELSE 0 END) AS TotalQuestions,
         SUM(CASE WHEN p.PostTypeId = 2 THEN 1 ELSE 0 END) AS TotalAnswers,
         SUM(CASE WHEN p.PostTypeId IN (4, 5) THEN 1 ELSE 0 END) AS TotalTagWikis
  FROM Posts p
  GROUP BY p.OwnerUserId
) AS stats ON u.Id = stats.OwnerUserId
ORDER BY TotalPosts DESC
LIMIT 10;
