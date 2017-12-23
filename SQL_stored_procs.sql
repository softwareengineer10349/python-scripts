DELIMITER //
CREATE PROCEDURE sp_get_all_skills ()
BEGIN
SELECT DISTINCT `job_skill` FROM `master_table`;
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE sp_get_info_for_whole_chart(city_in VARCHAR(100), skill_type VARCHAR(200))
BEGIN
SELECT COUNT(*) as TOTALCOUNT, j.job_skill FROM `job_table` as j, `master_table` as m
WHERE j.city = city_in
AND j.job_skill = m.job_skill
AND m.type_of_skill = skill_type
GROUP BY j.job_skill;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE sp_get_all_cities()
BEGIN
SELECT DISTINCT city FROM `job_table`;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE sp_get_all_types_of_skills()
BEGIN
SELECT DISTINCT type_of_skill FROM `master_table`;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE sp_get_all_skills_of_type_and_not_specific_skill(skill_dont_want_to_include VARCHAR(200), skill_type VARCHAR(200))
BEGIN
SELECT DISTINCT job_skill FROM `master_table` WHERE job_skill <> skill_dont_want_to_include AND type_of_skill = skill_type;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE sp_count_overlap_of_skill(skill1 VARCHAR(200), skill2 VARCHAR(200), city_in VARCHAR(100))
BEGIN
SELECT COUNT(*) as TOTALCOUNT FROM `job_table` t1 INNER JOIN `job_table` t2 ON t1.url = t2.url AND t1.job_skill = skill1 AND t2.job_skill = skill2 AND t1.city = city_in;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE sp_count_overlap_of_skill_with_all_other_skills(skill1 VARCHAR(200), skill_type VARCHAR(200), city_in VARCHAR(100))
BEGIN
SELECT COUNT(*) as TOTALCOUNT, t2.job_skill AS skill FROM `job_table` t1 INNER JOIN `job_table` t2 ON t1.url = t2.url AND t1.job_skill = skill1 AND t2.job_skill <> t1.job_skill AND t1.city = city_in
AND t2.job_skill IN (SELECT job_skill FROM `master_table` WHERE type_of_skill = skill_type)
GROUP BY t2.job_skill;
END //
DELIMITER ;
