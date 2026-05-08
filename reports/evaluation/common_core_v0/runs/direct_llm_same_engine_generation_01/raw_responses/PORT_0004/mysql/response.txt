SELECT CAST( SUM( CASE WHEN `sex` = 'F' THEN 1 ELSE 0 END ) AS DOUBLE ) * 100 / COUNT( `id` ) FROM `patient` WHERE `diagnosis` = 'RA' AND YEAR( `birthday` ) = 1980
