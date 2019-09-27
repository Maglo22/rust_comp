fn main() {
    let x = 5;
    let mut y = 7;

    if x > y {
        return true;
    } else if x < y {
        while true {
            y -= 1;
            if y <= 0 {
                break;
            }
        }
    }
}