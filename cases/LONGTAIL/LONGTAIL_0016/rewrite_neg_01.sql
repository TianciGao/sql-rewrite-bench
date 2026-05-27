WITH UserStats AS (
    SELECT
        U.Id AS UserId,
        U.Reputation,
        COUNT(DISTINCT P.Id) AS PostCount,
        SUM(COALESCE(P.Score, 0)) AS TotalPostScore,
        SUM(COALESCE(CASE WHEN P.PostTypeId = 1 THEN 1 ELSE 0 END, 0)) AS QuestionCount,
        SUM(COALESCE(CASE WHEN P.PostTypeId = 2 THEN 1 ELSE 0 END, 0)) AS AnswerCount,
        SUM(COALESCE(CASE WHEN P.PostTypeId IN (3, 4, 5) THEN 1 ELSE 0 END, 0)) AS WikiCount
    FROM Users U
    JOIN Posts P ON U.Id = P.OwnerUserId
    GROUP BY U.Id, U.Reputation
),
TopUsers AS (
    SELECT
        UserId,
        Reputation,
        PostCount,
        TotalPostScore,
        QuestionCount,
        AnswerCount,
        WikiCount,
        ROW_NUMBER() OVER (ORDER BY TotalPostScore DESC) AS rank_value
    FROM UserStats
)
SELECT
    UserId,
    Reputation,
    PostCount,
    TotalPostScore,
    QuestionCount,
    AnswerCount,
    WikiCount,
    rank_value
FROM TopUsers
WHERE rank_value <= 10
ORDER BY TotalPostScore DESC;
