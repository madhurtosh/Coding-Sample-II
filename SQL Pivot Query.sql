CREATE TABLE [dbo].StaffAllocationMatrix (
LaborDate date NOT NULL,
Shift varchar(50) NOT NULL,
Dept varchar(50) NOT NULL,
[21] int, RE25 int, RI25 int, [100] int, [120] int, [302] int,
[552] int, [554] int, [556] int, [561] int, [565] int, [576] int,
[580] int, [585] int, [642] int, [661] int, [670] int, [672] int,
[682] int, [684] int, [685] int, [686] int,
C0310 int, C3336 int, C1440 int, C1927 int, C4451 int, C0450 int, C0709 int,
[8] int, [11] int, [23] int, [24] int, [28] int, [29] int, [37] int, [41] int, [42] int, [45] int)


INSERT [dbo].StaffAllocationMatrix
SELECT LaborDate, Shift, Dept,
       [21],
	   CASE WHEN Dept LIKE 'Retail' THEN [25] END AS [RE25],
	   CASE WHEN Dept LIKE 'Rides' THEN [25] END AS [RI25],
	   [100],[120],[302],[552],[554],[556],[561],[565],[576],
	   [580],[585],[642],[661],[670],[672],[682],[684],[685],[686],
	   [3]+[10] AS [C0310],
	   [33]+[36] AS [C3336],
	   [14]+[40] AS [C1440],
	   [19]+[27] AS [C1927],
	   [44]+[51] AS [C4451],
	   [4]+[50] AS [C0450],
	   [7]+[9] AS [C0709],
	   [8],[11],[23],[24],[28],[29],[37],[41],[42],[45]
FROM dbo.LaborShortFormat
PIVOT
 (SUM(TotEmp)
   FOR LocationId in ([21],[25],[100],[120],[302],[552],[554],[556],[561],
   [565],[576],[580],[585],[642],[661],[670],[672],[682],[684],[685],[686],
   [3],[4],[7],[8],[9],[10],[11],[14],[19],[23],[24],[27],[28],[29],[33],[36],
   [37],[40],[41],[42],[44],[45],[50],[51])) AS P