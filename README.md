# timer_programmer
Home Assistant platform with support for a Timer Switch

A Timer Switch is like a clock with dents between the hours, there are two dents per hour so in total, a day has 48 switches; each one of them has a duration of 30 minutes.

This platform is generic, and it is used by Timer Switch in my Diematic Boiler integration. The UI that allows a user to interact with the timer switch shows the clock as an horizontal bar instead.

Internally, the information is stored in a single int value using a bitset. As stated before, every bit corresponds to a period of 30 minutes period at bit 0 goes from 00:00 to 00:30, bit 1 goes from 00:30 to 01:00 and so on.

# Current status

This is working for my integrarion. Set-up instructions will come later. Actually, the code was once in my home assistant development environment and it got lost due to the use of git stage, git rebase and git stage apply. I don't know why but I don't trust git anymore! neither the developer documentation of Home Assistant that is really frustrating experience!

# Note

I'm trying to add this code as an integration in HACS