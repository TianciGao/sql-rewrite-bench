SELECT
    u.DisplayName,
    u.Reputation,
    u.CreationDate,
    ranked.PostCount,
    ranked.QuestionCount,
    ranked.AnswerCount
FROM (
    SELECT
        counts.UserId,
        counts.PostCount,
        counts.QuestionCount,
        counts.AnswerCount,
        RANK() OVER (ORDER BY counts.PostCount DESC) AS RankByPostCount
    FROM (
        SELECT
            u.Id AS UserId,
            COUNT(DISTINCT p.Id) AS PostCount,
            SUM(CASE WHEN p.PostTypeId = 1 THEN 1 ELSE 0 END) AS QuestionCount,
            SUM(CASE WHEN p.PostTypeId = 2 THEN 1 ELSE 0 END) AS AnswerCount
        FROM Users u
        LEFT JOIN Posts p ON u.Id = p.OwnerUserId
        GROUP BY u.Id
    ) AS counts
) AS ranked
JOIN Users u ON u.Id = ranked.UserId
WHERE ranked.RankByPostCount <= 10
ORDER BY ranked.RankByPostCount;
