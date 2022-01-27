# BankApp

Projektet har gått ut på att ta fram ett fiktivt banksystem. Banken innehåller ett antal kunder som kan skapa och hantera konton och deras information. Den innehåller också funktioner för att kunna hantera kunder samt presentera deras information.
Som bank ska jag kunna skapa, ta bort samt skriva ut alla mina kunders information.

Som kund ska jag kunna skapa ett konto hos banken, lägga in och ta ut pengar på/från mina konton. Kundens ska också kunna skriva ut sin egen information samt information gällande ens konton vilket inkluderar transaktioner på dem.
Kunden ska också kunna byta namn 
De teknologier som använts är Python samt SQL för en databas som skapades med SQLite

Det fanns tre faser under projektets gång, den första var att skapa databasen och fylla den med mockdata. Jag skapade databasen med SQLite och fyllde den med mockdata från Mockaroo. De datatyper jag behövde men inte hade tillgång till via Mockaroo som fyra sista i personnumret, skrev jag en funktion för att slumpa fyra siffror och sedan lägga till dem i slutet av personnumret. 
Den andra fasen var att skapa min DataSource klass så den kunde skicka förfrågningar till databasen och sedan skriva data till min State-fil. 
Sista fasen gick sedan ut på att bygga systemet runt min DataSource och State-filen samt säkerställa att allt fungerade som det skulle. 
Jag planerade inga tasks innan arbetet, då projektet flöt på väldigt snabbt och bra. Något jag kanske hade gjort annorlunda om jag fått göra om arbetet är att tänka mer på hur jag gör felhanteringen. Kändes som att det väldigt överflöd och användning av try-except där det inte borde varit det så det känns som det borde funnits en bättre lösning på det 


















Länkar
Github:
https://github.com/Albinhsn/bank

Class diagram:
https://lucid.app/lucidchart/cd547b12-89f1-46bd-86e4-1b0a0eeb3183/edit?invitationId=inv_4d7af25c-a72f-4e5c-8998-5814b315c951

ER Diagram:
https://whimsical.com/QY4jayzfSBjPVNnDdGHLhq

![bankCLASS](https://user-images.githubusercontent.com/89841505/151412553-1f99d7d4-6e2e-4b2d-b65e-b021e1fde25f.png)
![bankER](https://user-images.githubusercontent.com/89841505/151412576-ecf5baef-afa1-4271-9200-97c0a3d6577e.png)
