SELECT MIN(`title`.`title`) `movie_title`
FROM `keyword`
CROSS JOIN `movie_info`
CROSS JOIN `movie_keyword`
CROSS JOIN `title`
WHERE `keyword`.`keyword` LIKE '%sequel%' AND ((`movie_info`.`info` = 'Sweden' OR `movie_info`.`info` = 'Norway' OR (`movie_info`.`info` = 'Germany' OR `movie_info`.`info` = 'Denmark') OR (`movie_info`.`info` = 'Swedish' OR `movie_info`.`info` = 'Denish' OR (`movie_info`.`info` = 'Norwegian' OR `movie_info`.`info` = 'German'))) AND `title`.`production_year` > 2005) AND (`title`.`id` = `movie_info`.`movie_id` AND `title`.`id` = `movie_keyword`.`movie_id` AND (`movie_keyword`.`movie_id` = `movie_info`.`movie_id` AND `keyword`.`id` = `movie_keyword`.`keyword_id`))
