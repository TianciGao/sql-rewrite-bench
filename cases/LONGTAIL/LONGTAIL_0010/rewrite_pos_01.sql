SELECT
    ranked.UserId,
    ranked.DisplayName,
    ranked.TotalPosts,
    ranked.TotalQuestions,
    ranked.TotalAnswers,
    ranked.TotalScore,
    ranked.TotalViews,
    ranked.AvgScore,
    ranked.AvgViews
FROM (
    SELECT
        stats.UserId,
        stats.DisplayName,
        stats.TotalPosts,
        stats.TotalQuestions,
        stats.TotalAnswers,
        stats.TotalScore,
        stats.TotalViews,
        stats.AvgScore,
        stats.AvgViews,
        ROW_NUMBER() OVER (ORDER BY stats.TotalPosts DESC) AS rank_value
    FROM (
        SELECT
            u.Id AS UserId,
            u.DisplayName,
            COUNT(p.Id) AS TotalPosts,
            COUNT(DISTINCT CASE WHEN p.PostTypeId = 1 THEN p.Id END) AS TotalQuestions,
            COUNT(DISTINCT CASE WHEN p.PostTypeId = 2 THEN p.Id END) AS TotalAnswers,
            SUM(p.Score) AS TotalScore,
            SUM(p.ViewCount) AS TotalViews,
            AVG(p.Score) AS AvgScore,
            AVG(p.ViewCount) AS AvgViews
        FROM Users u
        LEFT JOIN Posts p ON u.Id = p.OwnerUserId
        GROUP BY u.Id, u.DisplayName
    ) AS stats
) AS ranked
WHERE ranked.rank_value <= 10;
