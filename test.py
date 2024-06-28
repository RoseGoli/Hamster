import asyncio

from aioclock import AioClock, Every, Once, OnShutDown, OnStartUp
from aioclock.group import Group

# groups.py
group = Group()
app = AioClock()
app.include_group(group)

@group.task(trigger=Every(seconds=10))
async def every():
    print("Every 10 seconds, I make a quantum leap. Where will I land next?")



@group.task(trigger=Once())
async def once():
    print("Just once, I get to say something. Here it goes... I love lamp.")


# app.py



@app.task(trigger=OnStartUp())
async def startup():
    print(
        "Welcome to the Async Chronicles! Did you know a group of unicorns is called a blessing? Well, now you do!"
    )


@app.task(trigger=OnShutDown())
async def shutdown():
    print("Going offline. Remember, if your code is running, you better go catch it!")


# main.py
if __name__ == "__main__":
    asyncio.run(app.serve())