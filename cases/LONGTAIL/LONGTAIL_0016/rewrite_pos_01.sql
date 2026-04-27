SELECT
    ranked.UserId,
    ranked.Reputation,
    ranked.PostCount,
    ranked.TotalPostScore,
    ranked.QuestionCount,
    ranked.AnswerCount,
    ranked.WikiCount,
    ranked.rank_value
FROM (
    SELECT
        stats.UserId,
        stats.Reputation,
        stats.PostCount,
        stats.TotalPostScore,
        stats.QuestionCount,
        stats.AnswerCount,
        stats.WikiCount,
        ROW_NUMBER() OVER (ORDER BY stats.TotalPostScore DESC) AS rank_value
    FROM (
        SELECT
            U.Id AS UserId,
            U.Reputation,
            COUNT(DISTINCT P.Id) AS PostCount,
            SUM(COALESCE(P.Score, 0)) AS TotalPostScore,
            SUM(COALESCE(CASE WHEN P.PostTypeId = 1 THEN 1 ELSE 0 END, 0)) AS QuestionCount,
            SUM(COALESCE(CASE WHEN P.PostTypeId = 2 THEN 1 ELSE 0 END, 0)) AS AnswerCount,
            SUM(COALESCE(CASE WHEN P.PostTypeId IN (3, 4, 5) THEN 1 ELSE 0 END, 0)) AS WikiCount
        FROM Users U
        LEFT JOIN Posts P ON U.Id = P.OwnerUserId
        GROUP BY U.Id, U.Reputation
    ) AS stats
) AS ranked
WHERE ranked.rank_value <= 10
ORDER BY ranked.TotalPostScore DESC;
