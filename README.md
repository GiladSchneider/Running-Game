# Running-Game

TLDR
I made a game using GitHub CoPilot. CoPilot proved to be very useful.

# Motivation and Setup
To test the strength of GitHub CoPilot, I wanted a task that I was somewhat familiar with but would require heavy brushing-up and take ~16 hours to complete without CoPilot. When I first started programming, I learned PyGame and made some games with it. It has been around four years since I learned PyGame, and I never learned how to work with graphics and sprite sheets. So, making a pretty game was the task. Additionally, I only allowed the Python standard library and PyGame, and could only look something up if CoPilot did not recommend a solution that was functional or I could hack to be functional.

# Results
It took ~10 hours to make this game. The vast, vast, vast majority of that time was spent learning to work with sprite sheets and finding free ones that I liked on itch.io. Creating the infinitely scrolling background also took some time. Additionally, I spent a lot of time making generalizable classes so it would be easy to add additional enemies and upgrades, etcetera; however, I did not take the time to exploit this functionality. If I hadn't focused on using nice-looking sprites, creating a scrolling background, and making things generalizable, this could have taken <4 hrs. Also, my housemate says the game looks good, and the controls feel right, but the only issue is that the gameplay  <strike>sucks</strike> appeals to a niche audience.

Hey, I never claimed to be a game designer :)

# Verdict on CoPilot
GitHub CoPilot was awesome, especially at the beginning of the project. I did much of the code for setting up the screen, creating functions, and organizing classes by writing comments describing what I wanted, and CoPilot handled the rest. CoPilot continually recommended useful code snippets as the project grew and saved me the hassle of googling "How to do X pygame" for every new thing. Overall, it is an incredible tool that I will continue to use. It is worth the $0 it costs students (it is also probably worth the $10 it costs professional devs).

However, there are a few things about CoPilot that... appeal to a niche audience. CoPilot will sometimes recommend syntactically correct code with a logical flaw. These are challenging to catch if you don't immediately test/verify the code that CoPilot gave you. However, logical flaws will be a prevalent problem with code recommender systems as, at its heart, the challenge of programming is with logic, not syntax. CoPilot sometimes gets the syntax wrong by calling a function that doesn't exist or referencing a variable that doesn't exist. Although this is occasionally useful when creating the variable or function is trivial, it is frustrating when you know what CoPilot has to do given your already-written functions and variables, but the code is long and tedious, so you're just trying to get copilot to write the boilerplate for you.

Anyway, the only dependancy for this is PyGame. Enjoy 😊 

# Screenshots
<img width="1587" alt="Screenshot_1" src="https://user-images.githubusercontent.com/73044725/176542614-bd410209-8756-4a69-946c-638b90ce150d.png">

<img width="1588" alt="Screenshot_2" src="https://user-images.githubusercontent.com/73044725/176542640-e96f0f97-a080-404a-9547-1b2612644ea3.png">


