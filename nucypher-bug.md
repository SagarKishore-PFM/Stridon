## Info about the nucypher bug:
---

When policy grant method's m and n are set to 1 and 1, the retrieve function returns a key not found error as it is trying to find more nodes.
[error log](https://pastebin.com/UhpyBgnj)

For quick access to the fours scripts that access nucypher click [here](https://gist.github.com/SagarKishore-PFM/13c17c0f7b1bdbc6c1cbe148e09d8810)

When policy grant method's m and n are not set to 1 and 1, the script goes into a loop to learn nodes.
[error log](https://pastebin.com/9E4VPxKv)

    Note: this is with run_local_fleet.sh ursualas running.