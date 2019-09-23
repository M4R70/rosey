Discord bot built for the Karaoke Lounge with Discord.py and MongoDB (motor).


At the moment the bot is not user friendly and should not be used as is, although the cogs can be used for reference to implement similar features on other bots

I do plan to make it user friendly and let other people add it as is to their servers, but it is not a priority


Current Features:

    Features you should check out: (they are all wip, but they work)

        queues - we use this to manage our karaoke queues, but it can be used to organize user queues for pretty much anuthing
        
        reactionRoles - my super easy to set up and use take on the popular feature. 

        staffPing - it's supposed to work like an @here ping for our staff team (the role we set up is a dummy role no one has and the channel our staff channel)

    
    Features that you probably shouldn't: (they are not well implemented nor innovative atm, but they do work too)

        cicd - a very poor feature that reloads every module when i push to my (private) master branch, it uses a git webhook on a private channel to avoid having to open my home server to the internet (but hey, it works)

        cogManager - loads, realoads and unloads cogs, mostly used for debugging and testing

        eval - self explanatory

        settings and errors are just what they sound like

Planned fetures:

    user info - which invite they used and who joined at roughly the same time (to catch troll groups mostly)

    analytics - i have no idea why there is not a public bot that does this well, I NEED THOSE INSIGHTS
    
    logging - there are some good server logging bots out there, but none do it the way i like it

    and more i'm not remembering rn

    







