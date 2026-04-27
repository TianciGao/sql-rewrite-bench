SELECT
    ranked.UserId,
    ranked.DisplayName,
    ranked.Reputation,
    ranked.TotalPosts,
    ranked.TotalQuestions,
    ranked.TotalAnswers,
    ranked.TotalViews,
    ranked.NetVotes,
    ranked.ReputationRank,
    ranked.PostRank,
    ranked.ViewRank
FROM (
    SELECT
        stats.UserId,
        stats.DisplayName,
        stats.Reputation,
        stats.TotalPosts,
        stats.TotalQuestions,
        stats.TotalAnswers,
        stats.TotalViews,
        stats.NetVotes,
        RANK() OVER (ORDER BY stats.Reputation DESC) AS ReputationRank,
        RANK() OVER (ORDER BY stats.TotalPosts DESC) AS PostRank,
        RANK() OVER (ORDER BY stats.TotalViews DESC) AS ViewRank
    FROM (
        SELECT
            Users.Id AS UserId,
            Users.DisplayName,
            Users.Reputation,
            Users.UpVotes,
            Users.DownVotes,
            (Users.UpVotes - Users.DownVotes) AS NetVotes,
            COUNT(DISTINCT Posts.Id) AS TotalPosts,
            COUNT(DISTINCT CASE WHEN Posts.PostTypeId = 1 THEN Posts.Id END) AS TotalQuestions,
            COUNT(DISTINCT CASE WHEN Posts.PostTypeId = 2 THEN Posts.Id END) AS TotalAnswers,
            SUM(COALESCE(Posts.ViewCount, 0)) AS TotalViews
        FROM Users
        LEFT JOIN Posts ON Users.Id = Posts.OwnerUserId
        GROUP BY Users.Id, Users.DisplayName, Users.Reputation, Users.UpVotes, Users.DownVotes
    ) AS stats
) AS ranked
WHERE ranked.TotalPosts > 0
ORDER BY ranked.Reputation DESC, ranked.TotalPosts DESC, ranked.TotalViews DESC
LIMIT 10;
