SELECT 
    ranked.UserId,
    ranked.DisplayName,
    ranked.Reputation,
    ranked.PostCount,
    ranked.QuestionsCount,
    ranked.AnswersCount,
    ranked.TotalScore,
    ranked.TotalViewCount,
    ranked.UserRank
FROM (
    SELECT 
        stats.UserId,
        stats.DisplayName,
        stats.Reputation,
        stats.PostCount,
        stats.QuestionsCount,
        stats.AnswersCount,
        stats.TotalScore,
        stats.TotalViewCount,
        RANK() OVER (ORDER BY stats.Reputation DESC) AS UserRank
    FROM (
        SELECT 
            U.Id AS UserId,
            U.DisplayName,
            U.Reputation,
            COUNT(DISTINCT P.Id) AS PostCount,
            SUM(CASE WHEN P.PostTypeId = 1 THEN 1 ELSE 0 END) AS QuestionsCount,
            SUM(CASE WHEN P.PostTypeId = 2 THEN 1 ELSE 0 END) AS AnswersCount,
            SUM(COALESCE(P.Score, 0)) AS TotalScore,
            SUM(COALESCE(P.ViewCount, 0)) AS TotalViewCount
        FROM Users U
        JOIN Posts P ON U.Id = P.OwnerUserId
        WHERE U.Reputation > 0
        GROUP BY U.Id, U.DisplayName, U.Reputation
    ) stats
) ranked
WHERE ranked.UserRank <= 10
ORDER BY ranked.UserRank;
