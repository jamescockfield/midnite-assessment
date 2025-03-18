# Midnite Backend Exercise

## Description

This project implements a backend endpoint `/event` to monitor user activities and trigger alerts based on predefined rules.

## Instructions

1. **Install with Pipenv**: Run `pipenv install` in your terminal.
2. **Run the Server**: Execute `pipenv run dev` to start the server.
3. **Test the Endpoint**: Execute `pipenv run event` to send an example request to the `/event` endpoint
4. **Run unit tests**: Execute `pipenv run test` to run the unit tests


# Midnite Take Home 

At Midnite, we aim to provide safety nets for our users to ensure they are using our platform responsibility, one such system notifies us of any unusual activity. For this reason, you've been tasked with creating an endpoint which will receive a payload representing a user's action. 

This endpoint should be called `/event` and can expect the following payload: 

```json
{ 
    "type": "deposit", 
    "amount": "42.00", 
    "user_id": 1, 
    "t": 10 
} 
```

type is either `deposit` or `withdraw`.

`user_id` represents a unique user. 

`t` denotes the second we receive the payload, this will always be increasing and unique. 

The endpoint should respond as follows: 

```json
{ 
    "alert": true, 
    "alert_codes": [30, 123], 
    "user_id": 1 
} 
```

Given the following set of rules, if the user meets these criteria, add the code to the `alert_codes` . If `alert_codes` is empty, alert should be false , otherwise true . `alert_codes` can be provided in any order. Always provide the `user_id` in the response payload. 

* Code: 1100 : A withdraw amount over 100 
* Code: 30 : 3 consecutive withdraws 
* Code: 300 : 3 consecutive increasing deposits (ignoring withdraws) 
* Code: 123 : Accumulative deposit amount over a window of 30 seconds is over 200 

### Submission 

Please provide a file and README containing instructions on how to run your server. 
You are welcome to include a description of any issues you encounter. 

### Curl Example 

`curl \-XPOST http://127.0.0.1:5000/event \-H 'Content-Type: application/json' \\ \-d '{"type": "deposit", "amount": "42.00", "user\_id": 1, "t": 0}'`