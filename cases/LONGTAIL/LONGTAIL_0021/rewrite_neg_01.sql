SELECT 
    ranked.UserId,
    ranked.Reputation,
    ranked.PostCount,
    ranked.QuestionCount,
    ranked.AnswerCount
FROM (
    SELECT 
        stats.UserId,
        stats.Reputation,
        stats.PostCount,
        stats.QuestionCount,
        stats.AnswerCount,
        ROW_NUMBER() OVER (ORDER BY stats.Reputation DESC) AS rank_value
    FROM (
        SELECT 
            u.Id AS UserId,
            u.Reputation,
            COUNT(DISTINCT p.Id) AS PostCount,
            SUM(CASE WHEN p.PostTypeId = 1 THEN 1 ELSE 0 END) AS QuestionCount,
            SUM(CASE WHEN p.PostTypeId = 2 THEN 1 ELSE 0 END) AS AnswerCount
        FROM Users u
        JOIN Posts p ON u.Id = p.OwnerUserId
        GROUP BY u.Id, u.Reputation
    ) stats
) ranked
WHERE ranked.rank_value <= 10;
