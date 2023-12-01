const std = @import("std");

const FoundNumTuple = struct { []const u8, []const u8 };

fn mapStringToInt(inputString: []const u8) u8 {
    const stringDict = [_][]const u8{
        "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
        "1",   "2",   "3",     "4",    "5",    "6",   "7",     "8",     "9",
    };
    const numberDict = [_]u8{
        1, 2, 3, 4, 5, 6, 7, 8, 9,
        1, 2, 3, 4, 5, 6, 7, 8, 9,
    };

    var i: u8 = 0;
    while (i < stringDict.len) : (i += 1) {
        if (std.mem.eql(u8, inputString, stringDict[i])) {
            return numberDict[i];
        }
    }
    return 0;
}

fn findSpelledOutNumbers(inputString: []const u8) !FoundNumTuple {
    var foundMin: []const u8 = "not found";
    var foundMax: []const u8 = "not found";
    const stringDict = [_][]const u8{
        "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
        "1",   "2",   "3",     "4",    "5",    "6",   "7",     "8",     "9",
    };

    // forward access
    var i: usize = 0;
    var foundMatch = false;
    while (i < inputString.len) : (i += 1) {
        for (stringDict) |number| {
            const subStr = inputString[i..];
            if (subStr.len >= number.len and std.mem.eql(u8, subStr[0..number.len], number)) {
                if (foundMatch == false) {
                    foundMin = number;
                }
                foundMax = number;
                foundMatch = true;
                break;
            }
        }
    }
    return .{ foundMin, foundMax };
}

pub fn main() anyerror!void {
    var file = try std.fs.cwd().openFile("../input.txt", .{});
    defer file.close();

    var buf_reader = std.io.bufferedReader(file.reader());
    var in_stream = buf_reader.reader();

    var buf: [1024]u8 = undefined;
    var total: usize = 0;
    while (try in_stream.readUntilDelimiterOrEof(&buf, '\n')) |line| {
        const result = try findSpelledOutNumbers(line);
        total += (mapStringToInt(result[0]) * 10) + mapStringToInt(result[1]);
    }

    std.debug.print("{d}\n", .{total});
}
