# Lightning

Lightning is the software that runs on every Raspberry Pi that is responsible
for two things:

1. Monitor power consumption
2. Report to the Main Frame



## Initialize

Before one can properly use Lightning, it needs to be initialized to link to the main server (a.k.a. Main Frame), receive its unique ID, etc. Run following commands to initialize.

```bash
chmod +x init # if init is not marked as executable
./init
```

Lightning works in sync with the other houses that are connected to the network. You will need to specify IDs of those houses you are connected to.

```
Input lightning_ids of connected houses: 69 420
Sending b'{"mac": "175961238223", "cons": [1, 2, 3], "geo": [50.94110870361328, -1.373610019683838]}'.
Awaiting response.
Settings file received.
```



## Monitor Power Consumption

something



## Report to the Main Frame

something
