-- case_id: PORT_0007
-- draft source id: PORT_PARROT_DRAFT_0001
-- draft-only / not validated
-- target dialect: mysql_like_positive
SELECT `text` FROM `comments` WHERE `postid` IN ( SELECT `id` FROM `posts` WHERE `viewcount` BETWEEN 100 AND 150 ) ORDER BY `score` DESC LIMIT 1
