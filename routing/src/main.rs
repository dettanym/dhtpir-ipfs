use crate::lib::RoutingTable;

mod lib;

fn main() {
    let new_rt = RoutingTable::new()
        .add_record(0, "0010", "RE 0010")
        .normalize();
    dbg!("{:?}", new_rt);
}
