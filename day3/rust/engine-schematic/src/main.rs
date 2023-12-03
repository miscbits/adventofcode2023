use std::collections::HashSet;
use std::fs::File;
use std::hash::{Hash, Hasher};
use std::io::{self, BufRead};
use std::option::Option;
use std::path::Path;

#[derive(Eq, PartialEq, Debug, Hash)]
struct Coord(usize, usize);

#[derive(Eq, Debug, Hash, PartialEq)]
enum NodeType {
    Number(usize),
    Symbol(char),
    Dot,
}

#[derive(Eq, Debug)]
struct Node {
    location: Coord,
    length: usize,
    value: NodeType,
}

impl PartialEq for Node {
    fn eq(&self, other: &Self) -> bool {
        self.location == other.location
    }
}

impl Hash for Node {
    fn hash<H: Hasher>(&self, state: &mut H) {
        self.location.hash(state);
    }
}

#[derive(Debug)]
struct EngineSchema {
    schema: Vec<Vec<char>>,
    numbers: HashSet<Node>,
    symbols: Vec<Node>,
    dimmension_x: usize,
    dimmension_y: usize,
}

impl EngineSchema {
    fn load_numbers(&mut self) {
        for (x, line) in self.schema.clone().into_iter().enumerate() {
            let mut current_number = 0;
            let mut length = 0;
            for (y, c) in line.into_iter().enumerate() {
                if c.is_numeric() {
                    current_number = current_number * 10 + c.to_digit(10).unwrap() as usize;
                    length += 1;
                } else if current_number != 0 {
                    self.numbers.insert(Node {
                        location: Coord(x, y),
                        length: length,
                        value: NodeType::Number(current_number),
                    });
                    current_number = 0;
                    length = 0;
                }
            }
            if current_number != 0 {
                self.numbers.insert(Node {
                    location: Coord(x, self.dimmension_y - 1),
                    length: length,
                    value: NodeType::Number(current_number),
                });
            }
        }
    }

    fn load_symbols(&mut self) {
        for (x, line) in self.schema.clone().into_iter().enumerate() {
            for (y, c) in line.into_iter().enumerate() {
                if !c.is_numeric() && c != '.' {
                    self.symbols.push(Node {
                        location: Coord(x, y),
                        length: 1,
                        value: NodeType::Symbol(c),
                    })
                }
            }
        }
    }

    fn calculate_numeric_node(&self, coord: Coord) -> Option<Node> {
        let Coord(x, y) = coord;
        if let Some(_) = self.schema[x][y].to_digit(10) {
            // find left digit index
            let mut li = Coord(x, y);

            while li.1 > 0 {
                if !self.schema[x][li.1].is_numeric() {
                    break;
                }
                li.1 -= 1;
            }

            let mut ri = Coord(li.0, li.1);
            let mut current_number = 0;
            let mut length = 0;
            // calculate num and len
            while ri.1 < self.dimmension_y {
                if self.schema[x][ri.1].is_numeric() {
                    current_number =
                        current_number * 10 + self.schema[x][ri.1].to_digit(10).unwrap() as usize;
                    length += 1;
                    ri.1 += 1;
                } else {
                    break;
                }
            }

            return Some(Node {
                location: li,
                length: length,
                value: NodeType::Number(current_number),
            });
        }
        None
    }

    fn calculate_node(&self, coord: Coord) -> Node {
        let Coord(x, y) = coord;
        if x > self.dimmension_x || y > self.dimmension_y {
            return Node {
                location: coord,
                length: 1,
                value: NodeType::Dot,
            };
        }
        if !self.schema[x][y].is_numeric() && self.schema[x][y] != '.' {
            return Node {
                location: coord,
                length: 1,
                value: NodeType::Symbol(self.schema[x][y]),
            };
        }
        if self.schema[x][y].is_numeric() {
            return self.calculate_numeric_node(coord).unwrap();
        }

        return Node {
            location: coord,
            length: 1,
            value: NodeType::Dot,
        };
    }

    fn calculate_neighborhood(&self, node: &Node) -> HashSet<Node> {
        let location = &node.location;
        let mut nodes: HashSet<Node> = HashSet::new();
        for x in [location.0 - 1, location.0 + 1] {
            for y in (location.1 - 1)..(location.1 + node.length) {
                nodes.insert(self.calculate_node(Coord(x, y)));
            }
        }
        nodes.insert(self.calculate_node(Coord(location.0, location.1 - 1)));
        nodes.insert(self.calculate_node(Coord(location.0, location.1 + 1)));
        nodes
    }
}

fn main() {
    part1();
}

fn part1() {
    let mut engine = load_schematic("../../input.txt").unwrap();

    engine.load_numbers();
    engine.load_symbols();

    let mut count = 0;
    for node in &engine.numbers {
        if let NodeType::Number(node_value) = node.value {
            let neighbors = engine.calculate_neighborhood(node);
            for neighbor in neighbors {
                if let NodeType::Symbol(_) = neighbor.value {
                    count += node_value;
                    break;
                }
            }
        }
    }
    println!("{:?}", count);
}

fn part2() {}

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

fn load_schematic(schema_path: &str) -> Option<EngineSchema> {
    let mut parsed_schema: Vec<Vec<char>> = Vec::new();
    if let Ok(lines) = read_lines(schema_path) {
        for line in lines {
            if let Ok(line) = line {
                parsed_schema.push(line.chars().collect())
            }
        }
        let dimmension_x = parsed_schema.len();
        let dimmension_y = parsed_schema[parsed_schema.len() - 1].len();
        return Some(EngineSchema {
            schema: parsed_schema,
            numbers: HashSet::new(),
            symbols: Vec::new(),
            dimmension_x: dimmension_x,
            dimmension_y: dimmension_y,
        });
    }

    None
}
