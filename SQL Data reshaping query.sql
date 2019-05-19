-- Checking Access code with average amount mapping access code to previous table


DROP VIEW IF EXISTS [dbo].AccessCodeAvgRates

GO

CREATE VIEW [dbo].AccessCodeAvgRates AS
SELECT AccessCode,
       CASE
	   WHEN RIGHT([PLU],2) = 'PT' THEN 'Points'
	   ELSE RIGHT([PLU],2)
	   END AS TicketType,
	   SUM([QtySold]) As Qty,
	   SUM([AmountSold]) AS TotAmt,
	   SUM([AmountSold])/SUM([QtySold]) AS AvgAmt
FROM [dbo].[TicketSales]
GROUP BY [PLU], AccessCode
HAVING SUM([QtySold]) > 0


-- Revenue EARNED from Points Tickets


GO
DROP VIEW IF EXISTS [dbo].DailyTotalAmountsFromPoints

GO

CREATE VIEW [dbo].DailyTotalAmountsFromPoints AS
SELECT Ridership.[Date],
	   Ridership.[AccessCode],
	   Ridership.Hour,
	   CASE
	   WHEN Ridership.[Hour] < 18 THEN 0
	   ELSE 1
	   END AS Shift,
	   SUM([TotalUses]) as TotUses,
	   TicketType,
	   sum([Ridership].TotalUses*AccessCodeAvgRates.AvgAmt) as TotAmt
FROM [dbo].[Ridership]
JOIN [dbo].AccessCodeAvgRates
ON Ridership.AccessCode = AccessCodeAvgRates.AccessCode
GROUP BY Ridership.[Date], Ridership.Hour, Ridership.[AccessCode], TicketType

GO


-- Download points revenue into excel/output
SELECT [Date],
	   [Hour],
	   SUM(TotAmt) AS TotAmt
FROM [dbo].[DailyTotalAmountsFromPoints]
WHERE TicketType = 'Points'
GROUP BY [Date], [Hour]

GO


-- Wristbands Revenue
DROP VIEW IF EXISTS [dbo].TotalDailyRides

GO

CREATE VIEW [dbo].TotalDailyRides AS
SELECT [Date],
       [Hour],
	   CASE
	   WHEN Ride1.[Hour] < 18 THEN 0
	   ELSE 1
	   END AS Shift,
	   [AccessCode],
	   Ride1.[VisualID],
	   [RideID],
	   [TotalUses],
	   Ride2.DayTotRides
FROM [dbo].[Ridership] AS Ride1

JOIN(SELECT VisualID,
     SUM(TotalUses) AS DayTotRides
	 FROM [dbo].[Ridership]
	 GROUP BY Date, VisualID) AS Ride2

ON Ride1.VisualID = Ride2.VisualID


GO

DROP VIEW IF EXISTS [dbo].WBPricePerShift

GO
-- Divide daily WB revenue into shifts, proportional to usage in each shift

CREATE VIEW [dbo].WBPricePerShift AS
SELECT TDR.[Date],
	   TDR.Hour,
	   TDR.[AccessCode],
	   TDR.VisualID,
	   TicketType,
	   SUM(TDR.TotalUses) AS TotalUses,
	   TDR.DayTotRides,
	   ACR.AvgAmt,
	  (ACR.AvgAmt * SUM(TDR.TotalUses) / TDR.DayTotRides) AS WB_Price_per_shift
FROM [dbo].TotalDailyRides AS TDR
JOIN [dbo].AccessCodeAvgRates AS ACR
ON TDR.AccessCode = ACR.AccessCode
WHERE TicketType = 'WB'
GROUP BY TDR.[Date], TDR.Hour, TDR.[AccessCode], TDR.[VisualID], TDR.DayTotRides, TicketType, ACR.AvgAmt

GO

-- Download WB revenue into excel/output
SELECT [Date],
	   [Hour],
	   SUM(WB_Price_per_shift) AS TotAmt
FROM [dbo].WBPricePerShift
GROUP BY [Date], [Hour]

GO