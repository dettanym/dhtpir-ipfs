use crate::lib::RoutingTable;
use rand_core::SeedableRng;
use rand_xoshiro::SplitMix64;
use std::borrow::BorrowMut;

mod lib;

fn main() {
    let new_rt = RoutingTable::new()
        .add_record(0, "0010", "RE 0010")
        .normalize(SplitMix64::seed_from_u64(0).borrow_mut());
    dbg!("{:?}", new_rt);
}
