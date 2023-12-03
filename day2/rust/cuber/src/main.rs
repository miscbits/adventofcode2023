use polars::prelude::*;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

// The output is wrapped in a Result to allow matching on errors
// Returns an Iterator to the Reader of the lines of the file.
fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

fn get_max_cubes_by_game(games: DataFrame) -> Result<DataFrame, PolarsError> {
    return games
        .lazy()
        .group_by(["game_id"])
        .agg([
            max("red").alias("max_red"),
            max("green").alias("max_green"),
            max("blue").alias("max_blue"),
        ])
        .collect();
}

fn filter_possible_games(
    games: DataFrame,
    red: u32,
    green: u32,
    blue: u32,
) -> Result<DataFrame, PolarsError> {
    return get_max_cubes_by_game(games)?
        .lazy()
        .filter(
            col("max_red")
                .lt_eq(red)
                .and(col("max_green").lt_eq(green))
                .and(col("max_blue").lt_eq(blue)),
        )
        .select([col("game_id")])
        .collect();
}

fn part1() {
    let possible_games =
        filter_possible_games(create_df(), 12, 13, 14).expect("could not filter possible games");

    let id_sum = possible_games
        .lazy()
        .select([col("game_id").sum()])
        .collect()
        .unwrap();

    println!("{:?}", id_sum);
}

fn part2() {
    let max_cubes_by_games =
        get_max_cubes_by_game(create_df()).expect("could not get max cubes by game");

    let powers = max_cubes_by_games.lazy().select([
        col("game_id"),
        (col("max_red") * col("max_green") * col("max_blue")).alias("power"),
    ]);

    let power_sum = powers.select([col("power").sum()]).collect().unwrap();

    println!("{:?}", power_sum);
}

fn main() {
    part1();
    part2();
}

fn create_df() -> DataFrame {
    let mut game_ids: Vec<u32> = Vec::new();
    let mut round_nums: Vec<u32> = Vec::new();
    let mut reds: Vec<u32> = Vec::new();
    let mut greens: Vec<u32> = Vec::new();
    let mut blues: Vec<u32> = Vec::new();
    // File hosts.txt must exist in the current path
    if let Ok(lines) = read_lines("../../input.txt") {
        // Consumes the iterator, returns an (Optional) String
        for line in lines {
            if let Ok(game) = line {
                let mut game_parts = game.split(":");

                let game_id = game_parts
                    .next()
                    .unwrap()
                    .replace("Game", "")
                    .trim()
                    .parse::<u32>()
                    .expect("could not parse game id");

                let rounds: Vec<&str> = game_parts.next().unwrap().split(";").collect();
                let mut round_num = 0u32;
                for round in rounds {
                    let (mut r, mut g, mut b) = (0u32, 0u32, 0u32);
                    round_num += 1;
                    let round_data: Vec<&str> = round.split(",").collect();
                    for color_data in round_data {
                        if color_data.contains("red") {
                            r = parse_num_from_color_data("red");
                        } else if color_data.contains("green") {
                            g = parse_num_from_color_data("green");
                        } else if color_data.contains("blue") {
                            b = parse_num_from_color_data("blue");
                        }
                    }
                    game_ids.push(game_id);
                    round_nums.push(round_num);
                    reds.push(r);
                    greens.push(g);
                    blues.push(b);
                }
            }
        }
    }
    return df!(
        "game_id" => &game_ids,
        "round_num" => &round_nums,
        "red" => &reds,
        "green" => &greens,
        "blue" => &blues,
    )
    .unwrap();
}

fn parse_num_from_color_data(color: &str) -> u32 {
    color
        .replace(" ", "")
        .replace("red", "")
        .parse::<u32>()
        .unwrap()
}
