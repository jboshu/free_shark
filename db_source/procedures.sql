DROP PROCEDURE IF EXISTS blockStartStat;
CREATE DEFINER = `root`@`localhost` PROCEDURE `blockStartStat`(IN p DATE, IN q DATE)
BEGIN
	DECLARE
		indexdate DATE;

DROP TABLE
IF EXISTS t;

CREATE TEMPORARY TABLE t (date DATE);


SET indexdate = p;


WHILE indexdate <= q DO
	INSERT INTO t (date)
VALUES
	(indexdate);


SET indexdate = ADDDATE(indexdate, 1);


END
WHILE;

SELECT
	IFNULL(count, 0) AS count,
	date
FROM
	t
LEFT JOIN (
	SELECT
		count(*) AS count,
		DATE(start_time) AS start_time
	FROM
		block
	WHERE
		start_time >= p
	AND start_time <= q
	GROUP BY
		DATE(start_time)
) b ON t.date = b.start_time
ORDER BY
	date ASC;

DROP TABLE t;


END;

DROP PROCEDURE IF EXISTS blockEndStat;
CREATE DEFINER = `root`@`localhost` PROCEDURE `blockEndStat`(IN `p` datetime,IN `q` datetime)
BEGIN
	#Routine body goes here...
	DECLARE
		indexdate DATE;

DROP TABLE
IF EXISTS t;

CREATE TEMPORARY TABLE t (date DATE);


SET indexdate = p;


WHILE indexdate <= q DO
	INSERT INTO t (date)
VALUES
	(indexdate);


SET indexdate = ADDDATE(indexdate, 1);


END
WHILE;

SELECT
	IFNULL(count, 0) AS count,
	date
FROM
	t
LEFT JOIN (
	SELECT
		count(*) AS count,
		DATE(end_time) AS end_time
	FROM
		block
	WHERE
		end_time >= p
	AND end_time <= q
	GROUP BY
		DATE(end_time)
) b ON t.date = b.end_time
ORDER BY
	date ASC;

DROP TABLE t;

END;


DROP PROCEDURE IF EXISTS userRegisterStat;
CREATE DEFINER = `root`@`localhost` PROCEDURE `userRegisterStat`(IN `p` datetime,IN `q` datetime)
BEGIN
	DECLARE
		indexdate DATE;

DROP TABLE
IF EXISTS t;

CREATE TEMPORARY TABLE t (date DATE);


SET indexdate = p;


WHILE indexdate <= q DO
	INSERT INTO t (date)
VALUES
	(indexdate);


SET indexdate = ADDDATE(indexdate, 1);


END
WHILE;

SELECT
	IFNULL(count, 0) AS count,
	date
FROM
	t
LEFT JOIN (
	SELECT
		count(*) AS count,
		DATE(create_time) AS start_time
	FROM
		user
	WHERE
		create_time >= p
	AND create_time <= q
	GROUP BY
		DATE(create_time)
) b ON t.date = b.start_time
ORDER BY
	date ASC;

DROP TABLE t;


END;

