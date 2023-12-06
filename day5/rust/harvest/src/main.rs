use polars::prelude::*;
use std::fs;

fn main() {
    println!("{:?}", part_1("../../input.txt"));
    println!("{:?}", part_2("../../input.txt"));
}

fn part_2(file_name: &str) -> Option<i64> {
    let binding = fs::read_to_string(file_name).unwrap();
    let table_data: Vec<_> = binding.split("\n\n").collect();

    let seeds: Vec<(i64, i64)> = table_data[0]
        .replace("seeds: ", "")
        .split(" ")
        .map(|str_n| str_n.parse::<i64>().unwrap())
        .collect::<Vec<_>>()
        .chunks_exact(2)
        .map(|c| (c[0], c[1]))
        .collect();

    let seed_soil = parse_table_data_to_vec(table_data[1]);
    let soil_fertilizer = parse_table_data_to_vec(table_data[2]);
    let fertilizer_water = parse_table_data_to_vec(table_data[3]);
    let water_light = parse_table_data_to_vec(table_data[4]);
    let light_temperature = parse_table_data_to_vec(table_data[5]);
    let temperature_humidity = parse_table_data_to_vec(table_data[6]);
    let humidity_location = parse_table_data_to_vec(table_data[7]);

    // Calculate the minimum location number for each range
    seeds
        .iter()
        .map(|&(start, length)| {
            let end = start + length;
            let soil_start = convert_number(start, seed_soil.clone());
            let soil_end = convert_number(end, seed_soil.clone());
            let fertilizer_start = convert_number(soil_start, soil_fertilizer.clone());
            let fertilizer_end = convert_number(soil_end, soil_fertilizer.clone());
            let water_start = convert_number(fertilizer_start, fertilizer_water.clone());
            let water_end = convert_number(fertilizer_end, fertilizer_water.clone());
            let light_start = convert_number(water_start, water_light.clone());
            let light_end = convert_number(water_end, water_light.clone());
            let temperature_start = convert_number(light_start, light_temperature.clone());
            let temperature_end = convert_number(light_end, light_temperature.clone());
            let humidity_start = convert_number(temperature_start, temperature_humidity.clone());
            let humidity_end = convert_number(temperature_end, temperature_humidity.clone());
            let location_start = convert_number(humidity_start, humidity_location.clone());
            let location_end = convert_number(humidity_end, humidity_location.clone());

            // Return the minimum location number for the range
            location_start.min(location_end)
        })
        .min()
}

fn part_1(file_name: &str) -> Option<i64> {
    let binding = fs::read_to_string(file_name).unwrap();
    let table_data: Vec<_> = binding.split("\n\n").collect();

    let seeds: Vec<_> = table_data[0]
        .replace("seeds: ", "")
        .split(" ")
        .map(|str_n| str_n.parse::<i64>().unwrap())
        .collect();

    let seed_soil = parse_table_data_to_dataframe(table_data[1]);
    let soil_fertilizer = parse_table_data_to_dataframe(table_data[2]);
    let fertilizer_water = parse_table_data_to_dataframe(table_data[3]);
    let water_light = parse_table_data_to_dataframe(table_data[4]);
    let light_temperature = parse_table_data_to_dataframe(table_data[5]);
    let temperature_humidity = parse_table_data_to_dataframe(table_data[6]);
    let humidity_location = parse_table_data_to_dataframe(table_data[7]);

    let location_num: i64 = seeds
        .iter()
        .map(|seed_num| {
            let soil_num: i64 = map_value(*seed_num, &seed_soil);
            let fertilizer_num: i64 = map_value(soil_num, &soil_fertilizer);
            let watern_num: i64 = map_value(fertilizer_num, &fertilizer_water);
            let light_num: i64 = map_value(watern_num, &water_light);
            let temperature_num: i64 = map_value(light_num, &light_temperature);
            let humid_num: i64 = map_value(temperature_num, &temperature_humidity);
            let location_num: i64 = map_value(humid_num, &humidity_location);
            return location_num;
        })
        .min()
        .unwrap();

    Some(location_num)
}

fn map_value(id: i64, dataframe: &DataFrame) -> i64 {
    return match dataframe
        .clone()
        .lazy()
        .select([
            (col("destination") + (lit(id) - col("source"))).alias("destination"),
            col("source"),
            col("range"),
        ])
        .filter(
            (lit(id) - col("source"))
                .lt(col("range"))
                .and(lit(id).gt_eq(col("source"))),
        )
        .collect()
        .unwrap()
        .get_columns()[0]
        .sum()
    {
        Some(0) => id,
        None => id,
        Some(n) => n,
    };
}

fn parse_table_data_to_dataframe(table_data: &str) -> DataFrame {
    let mut destination: Vec<i64> = Vec::new();
    let mut source: Vec<i64> = Vec::new();
    let mut range: Vec<i64> = Vec::new();

    for row in &mut table_data.lines().collect::<Vec<_>>()[1..] {
        let vals: Vec<i64> = row
            .split(" ")
            .map(|str_n| str_n.parse::<i64>().unwrap())
            .collect();
        destination.push(vals[0]);
        source.push(vals[1]);
        range.push(vals[2])
    }
    return df!(
        "destination" => destination,
        "source" => source,
        "range" => range
    )
    .unwrap();
}

fn parse_table_data_to_vec(table_data: &str) -> Vec<(i64, i64, i64)> {
    let mut source_dest_map: Vec<(i64, i64, i64)> = Vec::new();

    for row in &mut table_data.lines().collect::<Vec<_>>()[1..] {
        let vals: Vec<i64> = row
            .split(" ")
            .map(|str_n| str_n.parse::<i64>().unwrap())
            .collect();
        source_dest_map.push((vals[0], vals[1], vals[2]));
    }
    source_dest_map
}

fn find_overlap(range1: (i64, i64), range2: (i64, i64)) -> Option<(i64, i64)> {
    let start1 = range1.0;
    let end1 = range1.0 + range1.1;

    let start2 = range2.0;
    let end2 = range2.0 + range2.1;

    let start = start1.max(start2);
    let end = end1.min(end2);

    if start <= end {
        Some((start, end - start))
    } else {
        None
    }
}

fn convert_number(input_number: i64, conversion_map: Vec<(i64, i64, i64)>) -> i64 {
    for (dest_start, src_start, length) in conversion_map {
        if input_number >= src_start && input_number < src_start + length {
            return dest_start + (input_number - src_start);
        }
    }
    input_number
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_table_data_to_datafrmae() {
        let actual = parse_table_data_to_dataframe("test map:\n25 32 8\n0 1 2");

        let expected = df!(
            "destination" => vec![25, 0],
            "source" => vec![32, 1],
            "range" => vec![8, 2]
        )
        .unwrap();

        assert_eq!(expected, actual);
    }

    #[test]
    fn test_map_value() {
        let binding = fs::read_to_string("../../test.txt").unwrap();
        let table_data: Vec<_> = binding.split("\n\n").collect();

        let seed_soil = parse_table_data_to_dataframe(table_data[1]);

        let expected = 52;
        let actual = map_value(50, &seed_soil);
        assert_eq!(expected, actual);
    }

    #[test]
    fn test_part_1() {
        let actual = part_1("../../test.txt").unwrap();
        let expected = 35;

        assert_eq!(expected, actual);
    }

    #[test]
    fn test_part_2() {
        let actual = part_2("../../test.txt").unwrap();
        let expected = 46;

        assert_eq!(expected, actual);
    }
}
