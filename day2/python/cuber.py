import polars as pl

# game_id, round_num, red, green, blue
game_table = pl.read_parquet("input.parquet")


def get_max_cubes_by_game(games: pl.DataFrame):
    return games.group_by("game_id").agg(
        pl.max("red").alias("max_red"),
        pl.max("green").alias("max_green"),
        pl.max("blue").alias("max_blue"),
    )


def filter_possible_games(
    games: pl.DataFrame, red: int, green: int, blue: int
) -> pl.DataFrame:
    return (
        get_max_cubes_by_game(games)
        .filter(
            pl.col("max_red").le(red)
            & pl.col("max_green").le(green)
            & pl.col("max_blue").le(blue)
        )
        .select("game_id")
    )


def part1():
    possible_games = filter_possible_games(game_table, 12, 13, 14)

    id_sum = possible_games.select(pl.sum("game_id"))

    print(id_sum)


def part2():
    max_cubes_by_games = get_max_cubes_by_game(game_table)

    powers = max_cubes_by_games.select(
        pl.col("game_id"),
        (pl.col("max_red") * pl.col("max_green") * pl.col("max_blue")).alias("power"),
    )

    power_sum = powers.select(pl.sum("power"))

    print(power_sum)
