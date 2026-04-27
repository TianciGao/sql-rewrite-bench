SELECT stats.UserId,
       stats.Reputation,
       stats.Views,
       stats.PostCount,
       stats.QuestionCount,
       stats.AnswerCount,
       stats.TotalScore,
       COALESCE(b.BadgeCount, 0) AS BadgeCount
FROM (
  SELECT u.Id AS UserId,
         u.Reputation,
         u.Views,
         COUNT(DISTINCT p.Id) AS PostCount,
         SUM(CASE WHEN p.PostTypeId = 1 THEN 1 ELSE 0 END) AS QuestionCount,
         SUM(CASE WHEN p.PostTypeId = 2 THEN 1 ELSE 0 END) AS AnswerCount,
         SUM(CASE WHEN p.PostTypeId IN (1, 2) THEN p.Score ELSE 0 END) AS TotalScore
  FROM Users u
  LEFT JOIN Posts p ON u.Id = p.OwnerUserId
  GROUP BY u.Id, u.Reputation, u.Views
) AS stats
LEFT JOIN (
  SELECT b.UserId, COUNT(b.Id) AS BadgeCount
  FROM Badges b
  GROUP BY b.UserId
) AS b ON stats.UserId = b.UserId
ORDER BY stats.Reputation DESC, stats.TotalScore DESC
LIMIT 100;
