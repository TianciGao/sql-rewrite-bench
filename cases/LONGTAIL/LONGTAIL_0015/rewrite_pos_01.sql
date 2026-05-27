SELECT
    ranked.UserId,
    ranked.DisplayName,
    ranked.Reputation,
    ranked.PostCount,
    ranked.QuestionCount,
    ranked.AnswerCount,
    ranked.TotalViews,
    ranked.TotalScore,
    ranked.ScoreRank
FROM (
    SELECT
        stats.UserId,
        stats.DisplayName,
        stats.Reputation,
        stats.PostCount,
        stats.QuestionCount,
        stats.AnswerCount,
        stats.TotalViews,
        stats.TotalScore,
        RANK() OVER (ORDER BY stats.TotalScore DESC) AS ScoreRank
    FROM (
        SELECT
            U.Id AS UserId,
            U.DisplayName,
            U.Reputation,
            COUNT(DISTINCT P.Id) AS PostCount,
            SUM(CASE WHEN P.PostTypeId = 1 THEN 1 ELSE 0 END) AS QuestionCount,
            SUM(CASE WHEN P.PostTypeId = 2 THEN 1 ELSE 0 END) AS AnswerCount,
            SUM(P.ViewCount) AS TotalViews,
            SUM(P.Score) AS TotalScore
        FROM Users U
        LEFT JOIN Posts P ON U.Id = P.OwnerUserId
        GROUP BY U.Id, U.DisplayName, U.Reputation
    ) AS stats
) AS ranked
WHERE ranked.ScoreRank <= 10;
