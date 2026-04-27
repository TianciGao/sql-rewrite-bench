SELECT ranked.DisplayName,
       ranked.TotalPosts,
       ranked.TotalQuestions,
       ranked.TotalAnswers,
       ranked.PositivePosts,
       ranked.NegativePosts,
       ranked.TotalViews,
       CASE
         WHEN ranked.RankByPosts <= 10 THEN 'Top Contributor'
         WHEN ranked.RankByViews <= 10 THEN 'Popular User'
         ELSE 'Regular User'
       END AS UserCategory
FROM (
  SELECT stats.UserId,
         stats.DisplayName,
         stats.TotalPosts,
         stats.TotalQuestions,
         stats.TotalAnswers,
         stats.PositivePosts,
         stats.NegativePosts,
         stats.TotalViews,
         RANK() OVER (ORDER BY stats.TotalPosts DESC) AS RankByPosts,
         RANK() OVER (ORDER BY stats.TotalViews DESC) AS RankByViews
  FROM (
    SELECT u.Id AS UserId,
           u.DisplayName,
           COUNT(p.Id) AS TotalPosts,
           SUM(CASE WHEN p.PostTypeId = 1 THEN 1 ELSE 0 END) AS TotalQuestions,
           SUM(CASE WHEN p.PostTypeId = 2 THEN 1 ELSE 0 END) AS TotalAnswers,
           SUM(CASE WHEN p.Score > 0 THEN 1 ELSE 0 END) AS PositivePosts,
           SUM(CASE WHEN p.Score < 0 THEN 1 ELSE 0 END) AS NegativePosts,
           SUM(p.ViewCount) AS TotalViews
    FROM Users u
    LEFT JOIN Posts p ON u.Id = p.OwnerUserId
    GROUP BY u.Id, u.DisplayName
  ) AS stats
) AS ranked
WHERE ranked.TotalPosts > 50 OR ranked.TotalViews > 1000
ORDER BY ranked.TotalPosts DESC, ranked.TotalViews DESC;
