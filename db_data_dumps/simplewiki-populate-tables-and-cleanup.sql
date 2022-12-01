-- populate tables in DB
USE newdb;

DROP TABLE IF EXISTS `metadata`;

CREATE TABLE `metadata` (
  SELECT page.page_id
    , page.page_title
    , cl.cl_to `category_name`
    , page.page_touched `last_modification_date`
  FROM `page` 
  INNER JOIN `categorylinks` `cl`
    ON page.page_id = cl.cl_from
);

DROP TABLE IF EXISTS `links`;

CREATE TABLE `links` (
  SELECT pl.pl_from `s_page_id`
    , page.page_id `t_page_id`
  FROM `pagelinks` `pl`
  INNER JOIN `page`
    ON pl.pl_title = page.page_title AND pl.pl_namespace = page.page_namespace
);

-- clean up
DROP TABLE IF EXISTS `page`;
DROP TABLE IF EXISTS `pagelinks`;
DROP TABLE IF EXISTS `categorylinks`;
