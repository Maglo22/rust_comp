fn main() {
    let x = 5;
    let mut y = 7;

    if x > y {
        return true;
    } else if x < y {
        while x < y {
            y -= 1;
        }
        return false;
    }
}