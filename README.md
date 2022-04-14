# timer_programmer
Home Assistant platform with support for a timer programmer

A Timer Programmer is like a clock with dents between the hours, there are two dents per hour so in total, a day has 48 steps.

The UI that is currently using this platform shows the clock as an horizontal bar instead.

Internally, the information is stored in a single int value using a bitset. Every bit corresponds to a period of 30 minutes period at bit 0 goes from 00:00 to 00:30, bit 1 goes from 00:30 to 01:00 and so on.

# Current status

This is working for my integrarion. Set-up instructions will come later. Actually, the code was once in my home assistant development environment and it got lost due to the use of git stage, git rebase and git stage apply. I don't know why but I don't trust git anymore! neither the developer documentation of Home Assistant that is really frustrating experience!

# Note

The is under development!