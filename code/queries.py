TOP_TEN_CATEGORIES_COUNT = \
"""
SELECT category_name
, COUNT(*) category_count
FROM metadata
GROUP BY category_name
ORDER BY category_count DESC
LIMIT 10;
"""

MOST_OUTDATED_PAGE = \
"""
SELECT max_time_diff.s_page_id page_id
FROM (
  SELECT links.s_page_id
         , MAX(TIMESTAMPDIFF(SECOND, m1.last_modification_date, m2.last_modification_date)) max_time_diff
  FROM `links`
  INNER JOIN `metadata` m1
   ON m1.category_name = '{category}' AND links.s_page_id = m1.page_id
  INNER JOIN `metadata` m2
   ON links.t_page_id = m2.page_id
  WHERE TIMESTAMPDIFF(SECOND, m1.last_modification_date, m2.last_modification_date) > 0
  GROUP BY s_page_id
) max_time_diff
INNER JOIN (
  SELECT links.s_page_id
         , TIMESTAMPDIFF(SECOND, m1.last_modification_date, m2.last_modification_date) time_diff
  FROM `links`
  INNER JOIN `metadata` m1
   ON m1.category_name = '{category}' AND links.s_page_id = m1.page_id
  INNER JOIN `metadata` m2
   ON links.t_page_id = m2.page_id
  WHERE TIMESTAMPDIFF(SECOND, m1.last_modification_date, m2.last_modification_date) > 0
) time_diff
ON max_time_diff.s_page_id = time_diff.s_page_id 
  AND max_time_diff.max_time_diff = time_diff.time_diff
"""