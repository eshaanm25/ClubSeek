CREATE TABLE Bars (barName varchar(30), wowFactor int, capacity int, currentTraffic int, address varchar(255), PRIMARY KEY(barName, address));

CREATE TABLE Users (userName varchar(255), userPhoneNumber varchar(15), assignedBarName varchar(30), assignedBarAddress varchar(255), PRIMARY KEY(userName, userPhoneNumber));