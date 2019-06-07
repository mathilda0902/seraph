SELECT *
FROM `pure-silicon-196123.seraph_v1.company_quora` 
WHERE company_name IS NOT NULL
AND company_name NOT IN ('founder', 'Founder', 'CEO', 'Founder & CEO', 'Founder and CEO')