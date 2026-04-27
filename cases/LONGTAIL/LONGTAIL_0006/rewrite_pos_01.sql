SELECT phs.PostId,
       phs.RevisionCount,
       phs.FirstRevisionDate,
       phs.LastRevisionDate,
       u.DisplayName AS LastEditedBy,
       p.Title,
       p.Score,
       p.ViewCount,
       p.AnswerCount,
       p.CommentCount
FROM (
  SELECT PH.PostId,
         MAX(PH.UserId) AS LastEditorUserId,
         COUNT(PH.Id) AS RevisionCount,
         MIN(PH.CreationDate) AS FirstRevisionDate,
         MAX(PH.CreationDate) AS LastRevisionDate
  FROM PostHistory PH
  GROUP BY PH.PostId
) AS phs
JOIN Posts p ON phs.PostId = p.Id
LEFT JOIN Users u ON phs.LastEditorUserId = u.Id
ORDER BY phs.RevisionCount DESC
LIMIT 10;
