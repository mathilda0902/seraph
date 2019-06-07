# seraph

Architectual diagram:
https://docs.google.com/presentation/d/1EXkJ2VNcq-Z6hVikRcESQc6xSBycayqV6yfH9A-MJu4/edit#slide=id.gcb9a0b074_1_0


Data Modelling:

1. LinkedIn for management tenure, number of new hires timeseries, API: Talent Solutions (for new job postings, industry breakdown, etc), API: Consumer Solutions Platform (for tracking new management team, team member tenure and industry background), API: Organization Lookup API (under: `Marketing Developer Platform/Integrations/Community Management/Organizations & Brands`) (metrics: follow stats, share stats, page stats).  https://docs.microsoft.com/en-us/linkedin/marketing/integrations/community-management/organizations/follower-statisticss
2. SEC EDGAR db: https://www.sec.gov/Archives/edgar/Feed/ and rss feeds;
3. Quora crawler (founders + company names); the results are stored at `pure-silicon-196123.seraph_v1.company_quora` under project `My First Project`.
4. Twitter. Features include: Email domains, company type, website url, industries, status, twitter id, employee count range, locations, founded year, end year, number of followers and so on.
5. VC blogs, on new trending industry info.

Dimensional model see slide deck.

