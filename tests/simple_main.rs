
fn main() {
    let x = 5; // variable no mutable
    let mut y = 7; // variable mutable

    loop {
        y += x;
        if y > 100 {
            break;
        }
    }
}
