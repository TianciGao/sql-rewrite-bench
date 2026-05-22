WITH RankedPosts AS (
  SELECT
    p.Id AS PostId,
    p.Title,
    p.OwnerUserId,
    p.CreationDate,
    p.Score,
    ROW_NUMBER() OVER (PARTITION BY p.OwnerUserId ORDER BY p.Score DESC) AS rank_value
  FROM Posts AS p
  WHERE
    p.PostTypeId = 1
), UserStats AS (
  SELECT
    u.Id AS UserId,
    u.DisplayName,
    COALESCE(SUM(v.BountyAmount), 0) AS TotalBounty,
    SUM(CASE WHEN b.Class = 1 THEN 1 ELSE 0 END) AS GoldBadges,
    COUNT(DISTINCT p.Id) AS QuestionCount
  FROM Users AS u
  LEFT JOIN Votes AS v
    ON u.Id = v.UserId AND v.VoteTypeId IN (8, 9)
  LEFT JOIN Badges AS b
    ON u.Id = b.UserId
  LEFT JOIN Posts AS p
    ON u.Id = p.OwnerUserId AND p.PostTypeId = 1
  GROUP BY
    u.Id,
    u.DisplayName
)
SELECT
  u.DisplayName,
  COUNT(DISTINCT p.Id) AS AnsweredQuestions,
  COALESCE(AVG(p.Score), 0) AS AvgScore,
  us.TotalBounty,
  us.GoldBadges,
  us.QuestionCount,
  bp.Body AS BestPostContent
FROM Users AS u
LEFT JOIN Posts AS p
  ON u.Id = p.OwnerUserId AND p.PostTypeId = 2
LEFT JOIN RankedPosts AS rp
  ON u.Id = rp.OwnerUserId AND rp.rank_value = 1
LEFT JOIN Posts AS bp
  ON rp.PostId = bp.Id
LEFT JOIN UserStats AS us
  ON u.Id = us.UserId
WHERE
  u.Reputation > 1000
GROUP BY
  u.DisplayName,
  us.TotalBounty,
  us.GoldBadges,
  us.QuestionCount,
  bp.Body
HAVING
  COUNT(DISTINCT p.Id) > 0
ORDER BY
  AvgScore DESC,
  TotalBounty DESC
