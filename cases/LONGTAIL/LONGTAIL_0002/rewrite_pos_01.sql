SELECT
    u.DisplayName,
    ups.TotalPosts,
    ups.TotalQuestions,
    ups.TotalAnswers,
    ups.TotalScore,
    ups.AvgViewCount,
    bs.TotalBadges,
    bs.TotalGoldBadges,
    bs.TotalSilverBadges,
    bs.TotalBronzeBadges
FROM
    Users u
LEFT JOIN (
    SELECT
        p.OwnerUserId AS UserId,
        COUNT(p.Id) AS TotalPosts,
        SUM(CASE WHEN p.PostTypeId = 1 THEN 1 ELSE 0 END) AS TotalQuestions,
        SUM(CASE WHEN p.PostTypeId = 2 THEN 1 ELSE 0 END) AS TotalAnswers,
        SUM(p.Score) AS TotalScore,
        AVG(p.ViewCount) AS AvgViewCount
    FROM
        Posts p
    GROUP BY
        p.OwnerUserId
) ups ON u.Id = ups.UserId
LEFT JOIN (
    SELECT
        b.UserId,
        COUNT(b.Id) AS TotalBadges,
        SUM(CASE WHEN b.Class = 1 THEN 1 ELSE 0 END) AS TotalGoldBadges,
        SUM(CASE WHEN b.Class = 2 THEN 1 ELSE 0 END) AS TotalSilverBadges,
        SUM(CASE WHEN b.Class = 3 THEN 1 ELSE 0 END) AS TotalBronzeBadges
    FROM
        Badges b
    GROUP BY
        b.UserId
) bs ON u.Id = bs.UserId
ORDER BY
    ups.TotalScore DESC,
    ups.TotalPosts DESC;
