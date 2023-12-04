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
        self.location == other.location && self.value == other.value && self.length == other.length
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
                        location: Coord(x, y - length),
                        length: length,
                        value: NodeType::Number(current_number),
                    });
                    current_number = 0;
                    length = 0;
                }
            }
            if current_number != 0 {
                self.numbers.insert(Node {
                    location: Coord(x, self.dimmension_y - length),
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
            let mut li = Coord(x.clone(), y.clone());

            while li.1 > 0 {
                if !self.schema[li.0][li.1 - 1].is_numeric() {
                    break;
                }
                li.1 -= 1;
            }

            let mut ri = Coord(li.0, li.1);
            let mut current_number = 0;
            let mut length = 0;
            // calculate num and len
            while ri.1 < self.dimmension_y {
                if self.schema[ri.0][ri.1].is_numeric() {
                    current_number = current_number * 10
                        + self.schema[ri.0][ri.1].to_digit(10).unwrap() as usize;
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
        if x >= self.dimmension_x || y >= self.dimmension_y {
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
        let Coord(location_x, location_y) = node.location;
        let mut nodes: HashSet<Node> = HashSet::new();

        for x in [location_x as isize - 1, location_x as isize + 1] {
            if x < 0 || x >= self.dimmension_x as isize {
                continue;
            }
            for y in (location_y as isize - 1)..(location_y as isize + node.length as isize + 1) {
                if y < 0 || y >= self.dimmension_y as isize {
                    continue;
                }
                nodes.insert(self.calculate_node(Coord(x.clone() as usize, y.clone() as usize)));
            }
        }
        if location_y != 0 {
            nodes.insert(self.calculate_node(Coord(location_x.clone(), location_y.clone() - 1)));
        }
        if location_y + node.length != self.dimmension_y {
            nodes.insert(
                self.calculate_node(Coord(location_x.clone(), location_y.clone() + node.length)),
            );
        }

        nodes
    }
}

fn main() {
    let mut engine = load_schematic("../../input.txt").unwrap();
    engine.load_numbers();
    engine.load_symbols();

    println!("{:?}", part1(&engine));
    println!("{:?}", part2(&engine));
}

fn part1(engine: &EngineSchema) -> usize {
    let mut count = 0;
    for node in &engine.numbers {
        if let NodeType::Number(node_value) = node.value {
            let neighbors = engine.calculate_neighborhood(node);
            if neighborhood_has_symbol(&neighbors) {
                count += node_value;
            }
        }
    }
    count
}

fn part2(engine: &EngineSchema) -> usize {
    let mut count = 0;
    for node in &engine.symbols {
        if let NodeType::Symbol(_) = node.value {
            let neighbor_values: Vec<usize> = engine
                .calculate_neighborhood(node)
                .iter()
                .filter(|neighbor| {
                    if let NodeType::Number(_) = neighbor.value {
                        return true;
                    }
                    return false;
                })
                .map(|neighbor| {
                    if let NodeType::Number(v) = neighbor.value {
                        return v;
                    }
                    return 0;
                })
                .collect();
            if neighbor_values.len() == 2 {
                count += neighbor_values[0] * neighbor_values[1];
            }
        }
    }
    count
}

fn neighborhood_has_symbol(neighborhood: &HashSet<Node>) -> bool {
    for n in neighborhood {
        if let NodeType::Symbol(_) = n.value {
            return true;
        }
    }
    return false;
}

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

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_part1() {
        let mut engine = load_schematic("../../test.txt").unwrap();
        engine.load_numbers();
        engine.load_symbols();

        assert_eq!(format!("{}", part1(&engine)), "4361");
    }

    #[test]
    fn test_part2() {
        let mut engine = load_schematic("../../test.txt").unwrap();
        engine.load_numbers();
        engine.load_symbols();

        assert_eq!(format!("{}", part2(&engine)), "467835");
    }

    #[test]
    fn test_load_schematic() {
        let mut schematic: EngineSchema = load_schematic("../../test.txt").unwrap();
        let expected: Vec<Vec<char>> = vec![
            //    0    1    2    3    4    5    6    7    8    9
            vec!['4', '6', '7', '.', '.', '1', '1', '4', '.', '.'], // 0
            vec!['.', '.', '.', '*', '.', '.', '.', '.', '.', '.'], // 1
            vec!['.', '.', '3', '5', '.', '.', '6', '3', '3', '.'], // 2
            vec!['.', '.', '.', '.', '.', '.', '#', '.', '.', '.'], // 3
            vec!['6', '1', '7', '*', '.', '.', '.', '.', '.', '.'], // 4
            vec!['.', '.', '.', '.', '.', '+', '.', '5', '8', '1'], // 5
            vec!['.', '.', '5', '9', '2', '.', '.', '.', '.', '.'], // 6
            vec!['.', '.', '.', '.', '.', '.', '7', '5', '5', '.'], // 7
            vec!['.', '.', '.', '$', '.', '*', '.', '.', '.', '.'], // 8
            vec!['.', '6', '6', '4', '.', '5', '9', '8', '.', '.'], // 9
        ];
        assert_eq!(schematic.schema, expected);

        schematic.load_symbols();

        let expected = vec![
            Node {
                location: Coord(1, 3),
                length: 1,
                value: NodeType::Symbol('*'),
            },
            Node {
                location: Coord(3, 6),
                length: 1,
                value: NodeType::Symbol('#'),
            },
            Node {
                location: Coord(4, 3),
                length: 1,
                value: NodeType::Symbol('*'),
            },
            Node {
                location: Coord(5, 5),
                length: 1,
                value: NodeType::Symbol('+'),
            },
            Node {
                location: Coord(8, 3),
                length: 1,
                value: NodeType::Symbol('$'),
            },
            Node {
                location: Coord(8, 5),
                length: 1,
                value: NodeType::Symbol('*'),
            },
        ];
        assert_eq!(schematic.symbols, expected);

        schematic.load_numbers();

        let expected = vec![
            Node {
                location: Coord(0, 0),
                length: 3,
                value: NodeType::Number(467),
            },
            Node {
                location: Coord(0, 5),
                length: 3,
                value: NodeType::Number(114),
            },
            Node {
                location: Coord(2, 2),
                length: 2,
                value: NodeType::Number(35),
            },
            Node {
                location: Coord(2, 6),
                length: 3,
                value: NodeType::Number(633),
            },
            Node {
                location: Coord(4, 0),
                length: 3,
                value: NodeType::Number(617),
            },
            Node {
                location: Coord(5, 7),
                length: 3,
                value: NodeType::Number(581),
            },
            Node {
                location: Coord(6, 2),
                length: 3,
                value: NodeType::Number(592),
            },
            Node {
                location: Coord(7, 6),
                length: 3,
                value: NodeType::Number(755),
            },
            Node {
                location: Coord(9, 1),
                length: 3,
                value: NodeType::Number(664),
            },
            Node {
                location: Coord(9, 5),
                length: 3,
                value: NodeType::Number(598),
            },
        ]
        .into_iter()
        .collect();
        assert_eq!(schematic.numbers, expected);
    }

    #[test]
    fn test_find_calculate_node() {
        let schematic: EngineSchema = load_schematic("../../test.txt").unwrap();
        let node = schematic.calculate_node(Coord(2, 2));

        assert_eq!(
            node,
            Node {
                location: Coord(2, 2),
                length: 2,
                value: NodeType::Number(35)
            }
        );

        let node = schematic.calculate_node(Coord(2, 8));

        assert_eq!(
            node,
            Node {
                location: Coord(2, 6),
                length: 3,
                value: NodeType::Number(633)
            }
        );

        let node = schematic.calculate_node(Coord(5, 9));

        assert_eq!(
            node,
            Node {
                location: Coord(5, 7),
                length: 3,
                value: NodeType::Number(581)
            }
        );
    }

    #[test]
    fn test_find_neighbors() {
        let schematic: EngineSchema = load_schematic("../../test.txt").unwrap();
        let neighborhood = schematic.calculate_neighborhood(&schematic.calculate_node(Coord(2, 2)));
        assert_eq!(neighborhood.len(), 10);

        let neighborhood = schematic.calculate_neighborhood(&schematic.calculate_node(Coord(6, 2)));
        assert_eq!(neighborhood.len(), 12);

        let neighborhood = schematic.calculate_neighborhood(&schematic.calculate_node(Coord(0, 0)));
        assert_eq!(neighborhood.len(), 5);

        let neighborhood = schematic.calculate_neighborhood(&schematic.calculate_node(Coord(4, 0)));
        assert_eq!(neighborhood.len(), 9);

        let neighborhood = schematic.calculate_neighborhood(&schematic.calculate_node(Coord(5, 9)));
        assert_eq!(neighborhood.len(), 9);

        let neighborhood = schematic.calculate_neighborhood(&schematic.calculate_node(Coord(9, 2)));
        assert_eq!(neighborhood.len(), 7);
    }

    #[test]
    fn test_neighborhood_has_symbol() {
        let schematic: EngineSchema = load_schematic("../../test.txt").unwrap();
        let neighborhood = schematic.calculate_neighborhood(&schematic.calculate_node(Coord(2, 6)));
        assert!(neighborhood_has_symbol(&neighborhood));
        let neighborhood = schematic.calculate_neighborhood(&schematic.calculate_node(Coord(5, 9)));
        assert!(!neighborhood_has_symbol(&neighborhood));
        let neighborhood = schematic.calculate_neighborhood(&schematic.calculate_node(Coord(9, 2)));
        assert!(neighborhood_has_symbol(&neighborhood));
    }
}
