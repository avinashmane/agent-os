# Estimation Guidelines

## Inputs

* Project type:  
	* CS: Implementation
	* AMS: Support or maintenance
* Scope Boundary Parameters:
	* CS: Need scope boundary parameters defined in specific offering 
	* AMS: 
		* Number of years: Always needed, can be defaulted to 3 years
		* when combined with CS can use DCUT efforts
		* when standalone AMS estimation need 
			
			* number of users / tickets

## Common Guidance

Please overall estimate includes deliver efforts + 10% additional for governance


### BA-SAP

#### Deliver effort

following are scope boundary parameters

* Hours per Program : 80 hrs
* Hours per Interface : 100 hrs
* Hours per Report : 40 hrs
* Hours per Workflow : 100 hours
* Hours per Enhancement : 60 hours

### AO-SAP

#### Deliver effort

##### DCUT based model

Can be used only in conjunction with BA-SAP

* Hours per Year as percentage of BA-SAP hours:

  * High Complexity: 30%
  * Default Medium Complexity: 25%
  * Low Complexity: 20%

##### User/Ticket based model

If started from users
* Number of tickets per user per year: 1
* % of tickets L1.5 incident : 20%
* % of tickets L2 incident : 50%
* % of tickets L3 incident : 15%
* % of service request : 15%

 

* Hours per L1.5 incident : 1 hrs
* Hours per L2 incident : 4 hrs
* Hours per L3 incident : 12 hrs
* Hours per service request : 2 hours
* Hours per Enhancement : 60 hours

### AO-Oracle

Same as AO-SAP