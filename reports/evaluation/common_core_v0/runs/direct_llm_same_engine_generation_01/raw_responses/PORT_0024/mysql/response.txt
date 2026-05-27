SELECT SUM( CASE WHEN `istextless` = 0 AND `isstoryspotlight` = 1 THEN 1 ELSE 0 END ) * 100 / COUNT( `id` ) AS percentage FROM `cards`
