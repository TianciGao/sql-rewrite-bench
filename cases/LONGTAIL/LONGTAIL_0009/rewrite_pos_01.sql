SELECT
    ustats.DisplayName,
    ustats.Reputation,
    ustats.PostCount,
    ustats.CommentCount,
    ustats.UpVoteCount,
    ustats.DownVoteCount,
    pstats.PostId,
    pstats.Title,
    pstats.CreationDate,
    pstats.ViewCount,
    pstats.Score,
    pstats.AnswerCount,
    pstats.CommentCount,
    pstats.PostType,
    pstats.UpVotes,
    pstats.DownVotes
FROM (
    SELECT
        U.Id AS UserId,
        U.DisplayName,
        U.Reputation,
        COUNT(DISTINCT P.Id) AS PostCount,
        COUNT(DISTINCT C.Id) AS CommentCount,
        SUM(CASE WHEN V.VoteTypeId = 2 THEN 1 ELSE 0 END) AS UpVoteCount,
        SUM(CASE WHEN V.VoteTypeId = 3 THEN 1 ELSE 0 END) AS DownVoteCount
    FROM Users U
    LEFT JOIN Posts P ON U.Id = P.OwnerUserId
    LEFT JOIN Comments C ON P.Id = C.PostId
    LEFT JOIN Votes V ON P.Id = V.PostId
    GROUP BY U.Id, U.DisplayName, U.Reputation
) AS ustats
JOIN (
    SELECT
        P.Id AS PostId,
        P.Title,
        P.CreationDate,
        P.OwnerUserId,
        P.ViewCount,
        P.Score,
        P.AnswerCount,
        P.CommentCount,
        CASE
            WHEN P.PostTypeId = 1 THEN 'Question'
            WHEN P.PostTypeId = 2 THEN 'Answer'
            ELSE 'Other'
        END AS PostType,
        COUNT(CASE WHEN V.VoteTypeId = 2 THEN 1 END) AS UpVotes,
        COUNT(CASE WHEN V.VoteTypeId = 3 THEN 1 END) AS DownVotes
    FROM Posts P
    LEFT JOIN Votes V ON P.Id = V.PostId
    GROUP BY
        P.Id, P.Title, P.CreationDate, P.OwnerUserId, P.ViewCount,
        P.Score, P.AnswerCount, P.CommentCount, P.PostTypeId
) AS pstats
ON ustats.UserId = pstats.OwnerUserId
ORDER BY ustats.Reputation DESC, pstats.ViewCount DESC;
