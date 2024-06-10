import asyncio
import aiohttp
from fake_useragent import UserAgent
from colorama import Fore, Back, Style

game_id = input("Game ID: ")


print ("\nPerson to win alot/boost in rankings")
winner = input("Winner ID: ") # winner
print ("\n Person to lose alot/tank in rankings\n")
tank = input("Tank ID: ") # Person to lose alot 
print("\n")
amm = int(input("Amount Of Boosts: ")) # amount of boosts
ua = UserAgent()

headers = {
    'User-Agent': ua.random,
    'Content-Type': 'application/json'
}

async def start_game(session, payload):
    async with session.post("https://production-api.uwufufu.com/v1/worldcup/startedGames", headers=headers, json=payload) as response:
        if response.status == 201:
            data = await response.json()
            startedGameId = data.get('startedGameId')
            # print(f"Game ID: {startedGameId}")

            pick = {
                "rounds": 2,
                "startedGameId": startedGameId,
                "selections": [ #64359d3ebf2461aba7f6ff83
                    {"_id": tank, "wins": False},
                    {"_id": winner, "wins": True} 
                ]
            }

            async with session.post("https://production-api.uwufufu.com/v1/worldcup/startedGames/pick", headers=headers, json=pick) as pick_response:
                # print(pick_response.status)
                # print(await pick_response.json())
                print(f"{Fore.BLACK}Succesfully Boosted [{Fore.WHITE+"+1"+Fore.BLACK}]")
        else:
            print("Error starting the game:", await response.json())

async def main():
    tasks = []
    payload = {
        "gameId": game_id,
        "rounds": 2
    }

    async with aiohttp.ClientSession() as session:
        for _ in range(amm):
            task = asyncio.create_task(start_game(session, payload))
            tasks.append(task)

        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
