# cabrtapi
An API for simulating the real-time locations of drivers.

Available at: [cabrtapi.wckd.pk](https://cabrtapi.wckd.pk)

## How to use
In order to use this API, you need to provide 3 values.

#### sKey
The `sKey` is the sessionKey. Initialise this with a random value. Whatever value you choose, it is important to keep the same value for conseqent requests. This value helps keep track of the current location of a driver. If you need to represent a different driver, then use a unique `sKey` for each driver.

#### uLoc
The location of the user (ie. where the driver is headed). This needs to be provided with coordinates such as `33.615039, 73.010180`. The comma is necessary.

#### dLoc
The initial location of the driver. This needs to be provided with coordinates such as `33.615039, 73.010180`. The comma is necessary.

#### zLvl (optional)
The zoom level of the map. Default is 14. Higher values zoom more.

## Example
The user is at Comsats. The driver is at Faizabad. The driver is heading to the User.
```
https://cabrtapi.wckd.pk/?dLoc=33.66333451355563,73.08406293089536&uLoc=33.652462898044405,73.15694979804003&zLvl=13&sKey=0
```
Refresh the page to see this in action. The driver's location updates each time and moves closer and closer to the user.
