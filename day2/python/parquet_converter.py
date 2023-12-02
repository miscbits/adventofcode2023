import polars as pl

game_ids, round_nums, reds, greens, blues = [], [], [], [], []
with open("../input.txt", "r") as game_data:
    for line in game_data:
        game_id, rounds = line.split(":")
        game_id = int(game_id.split(" ")[1])
        rounds = rounds.split(";")
        for round_num in range(len(rounds)):
            red, green, blue = 0, 0, 0
            for color_info in rounds[round_num].split(","):
                print(color_info)
                if "red" in color_info:
                    red = int("".join([x for x in color_info if x.isdigit()]))
                if "green" in color_info:
                    green = int("".join([x for x in color_info if x.isdigit()]))
                if "blue" in color_info:
                    blue = int("".join([x for x in color_info if x.isdigit()]))
            game_ids.append(game_id)
            round_nums.append(round_num)
            reds.append(red)
            greens.append(green)
            blues.append(blue)

df = pl.DataFrame(
    {
        "game_id": game_ids,
        "round_num": round_nums,
        "red": reds,
        "green": greens,
        "blue": blues,
    }
)

df.write_parquet("input.parquet", compression="lz4")
