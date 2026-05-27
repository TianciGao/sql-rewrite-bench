SELECT CAST( COUNT( t1.id ) AS DOUBLE ) / 12 FROM postlinks AS t1 INNER JOIN posts AS t2 ON t1.postid = t2.id WHERE t2.answercount <= 2 AND TO_CHAR( t1.creationdate, 'YYYY' ) = '2010'
