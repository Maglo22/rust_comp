// NOMBRE: tipo '=' valor
// i8 -> int de 8 bits (signed)
const Z: i8 = 1;

fn main() {
    let x = 5; // variable no mutable
    let mut y = 7; // variable mutable
    let b: bool = true;

    if x > y {
        if x > Z {
            if b {
                return true;
            }
        }
    } else if x < y {
        while x < y {
            y -= 1;
        }
        println!("y era mayor");
        
        return false;
    }
}
