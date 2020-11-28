import asyncio, aiohttp, json # main
import arrow, calendar # dates

headers = {
    "Accept":"application/vnd.github.v3+json",
    "Authorization": "token " + input("Personal Access Token\n\t> ")
}
arg_error = IndexError("Failed to construct request url. Did you provide proper arguments?")

ending = lambda day : "th" if 3 < day < 21 or 23 < day < 31 else ["st", "nd", "rd"][day % 10 - 1]

def parse(time: str):
    parsed = arrow.get(time).datetime

    day = str(parsed.day) + ending(parsed.day)
    time = f"{parsed.hour}:{parsed.minute}:{parsed.second}"
    return f"{time} on {calendar.month_name[parsed.month]} {day}, {parsed.year}"

async def main(args):
    async with aiohttp.ClientSession(headers=headers) as session:
        # 955c1fdda5609ef9660d3d6bcd48527c88edbd55

        try:
            url = f"https://api.github.com/repos/{args[1]}/{args[2]}/commits?path={args[3]}"

            async with session.get(url) as response:
                results = await response.json()
                print("\nCOMMIT HISTORY:\n")

                for result in results:
                    commit = result["commit"]
                    author = commit["author"]

                    print(f"\t{commit['message']} [ {result['sha']} ]")
                    print(f"\t    author: {author['name']} ({author['email']})")
                    print(f"\t    url: {result['html_url']}\n\t    date: {parse(author['date'])}\n")

                # DEBUG: print(f"{len(results)} results\n\n{json.dumps(results, indent=4)}")
        except IndexError as err:
            raise arg_error from err

if __name__ == "__main__":
    import sys # command-line arguments: user, repo, file

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(sys.argv))
