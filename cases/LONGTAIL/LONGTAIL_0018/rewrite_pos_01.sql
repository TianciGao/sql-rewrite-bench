SELECT
    ranked.UserId,
    ranked.DisplayName,
    ranked.TotalPosts,
    ranked.TotalQuestions,
    ranked.TotalAnswers,
    ranked.TotalViews,
    ranked.TotalScore,
    ranked.rank_value
FROM (
    SELECT
        stats.UserId,
        stats.DisplayName,
        stats.TotalPosts,
        stats.TotalQuestions,
        stats.TotalAnswers,
        stats.TotalViews,
        stats.TotalScore,
        ROW_NUMBER() OVER (ORDER BY stats.TotalScore DESC) AS rank_value
    FROM (
        SELECT
            U.Id AS UserId,
            U.DisplayName,
            COUNT(P.Id) AS TotalPosts,
            COUNT(DISTINCT CASE WHEN P.PostTypeId = 1 THEN P.Id END) AS TotalQuestions,
            COUNT(DISTINCT CASE WHEN P.PostTypeId = 2 THEN P.Id END) AS TotalAnswers,
            SUM(P.ViewCount) AS TotalViews,
            SUM(P.Score) AS TotalScore
        FROM Users U
        LEFT JOIN Posts P ON U.Id = P.OwnerUserId
        GROUP BY U.Id, U.DisplayName
    ) AS stats
) AS ranked
WHERE ranked.rank_value <= 10;
