SELECT COUNT(*) FROM companies;

SELECT COUNT(*) FROM profitandloss;

SELECT company_id,
COUNT(*) AS years
FROM profitandloss
GROUP BY company_id
ORDER BY years DESC;

SELECT company_id,
SUM(net_profit)
FROM profitandloss
GROUP BY company_id
ORDER BY SUM(net_profit) DESC
LIMIT 10;

SELECT broad_sector,
COUNT(*)
FROM sectors
GROUP BY broad_sector;

SELECT company_id,
MAX(close_price)
FROM stock_prices
GROUP BY company_id
LIMIT 10;

SELECT AVG(pe_ratio)
FROM market_cap;

SELECT company_id,
AVG(return_on_equity_pct)
FROM financial_ratios
GROUP BY company_id
ORDER BY AVG(return_on_equity_pct) DESC
LIMIT 10;

SELECT company_id,
COUNT(*)
FROM documents
GROUP BY company_id
LIMIT 10;

SELECT *
FROM peer_groups
LIMIT 10;

