SELECT u.Id AS UserId,
       u.DisplayName,
       u.Reputation,
       p.Id AS PostId,
       p.Title,
       p.CreationDate AS PostCreationDate,
       p.Score AS PostScore,
       p.ViewCount,
       COALESCE(vc.UpVotes, 0) AS UpVotes,
       COALESCE(vc.DownVotes, 0) AS DownVotes,
       COALESCE(vc.TotalVotes, 0) AS TotalVotes
FROM Users u
LEFT JOIN Posts p ON u.Id = p.OwnerUserId
LEFT JOIN (
  SELECT PostId,
         SUM(CASE WHEN VoteTypeId = 2 THEN 1 ELSE 0 END) AS UpVotes,
         SUM(CASE WHEN VoteTypeId = 3 THEN 1 ELSE 0 END) AS DownVotes,
         COUNT(*) AS TotalVotes
  FROM Votes
  GROUP BY PostId
) AS vc ON p.Id = vc.PostId
WHERE p.Id IS NOT NULL
ORDER BY u.Reputation DESC, p.CreationDate DESC;
