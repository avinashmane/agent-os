# Resource Plan

Resource plan needs following inputs:
⦁	Project type: CS or AMS (CS is default)
⦁	total efforts and
⦁	duration (this can be calculated)

## Format

Resource plan is a tabular dataframe with each line representing role with title, skill, skill level, location, start month, duration.
⦁	Use separate line for different person


## Duration

### CS: Implementation or design build

User may provide duration, normally in months.
Duration can be assumed as rounded square root of person months of efforts divided by factor of 1.2

### AMS : Maintenance or support

Default is 3 years. Each year we should achieve productivity to reduce the headcount.
Target productivity for 3 years: 30% total
Target productivity for 4 years: 40% total
Target productivity for 5+ years: 50% total

## Roles

⦁	location can be onsite, onshore, nearshore, offshore
 	- Offshore can be India China Philippines
 	- for Arabic countries Egypt can be chosen
⦁	Month can be depicted as M1, M2, M3 as column headers
 	- Please fill resource allocation underneath 100% as 1, and 50% allocation as 0.5
⦁	Skill level can be:
  - delivery resources
  - Leadership roles
⦁	Band is the precise skill level
  - delivery resources:
 	- very low: band B
 	- Low: band GH,
 	- medium: band 6b,
 	- high: band 7a
 	- very high: band 7b
  - Leadership roles: low 7b, med 8 and high 9

## Staffing Guidance
⦁	Bandmix can be calculated as weighted average of all roles on the basis of total hours
  - weightages for bands are:
 	Band B: 5,
 	band GH: 5.5,
 	band 6a: 6,
 	band 6b: 6.5,
 	band 7a: 7,
 	band 7b: 7.5,
 	and for band 8 and above same number as band