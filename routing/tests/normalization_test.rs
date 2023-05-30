use routing::RoutingTable;
// TODO: Configure RT with a randomization seed for last couple test cases.

#[test]
fn test_previous_buckets_upto_k() {
    let new_rt = RoutingTable::new()
        .add_record(0, "0010", "RE")
        .add_record(1, "0001", "RE")
        .add_record(1, "0000", "RE")
        .add_record(2, "0111", "RE")
        .normalize();

    // assert_eq!(new_rt.buckets[0].records[0].cid, "0010");
    // assert_eq!(new_rt.buckets[0].records[1].cid, "0001");
    // assert_eq!(new_rt.buckets[0].records[2].cid, "0000");
    // assert_eq!(new_rt.buckets[1].records[0].cid, "0001");
    // assert_eq!(new_rt.buckets[1].records[1].cid, "0000");
    // assert_eq!(new_rt.buckets[1].records[2].cid, "0010");
    // assert_eq!(new_rt.buckets[1].records[3].cid, "0111");

    assert_eq!(new_rt.buckets[2].records[0].cid, "0111");
    assert_eq!(new_rt.buckets[2].records[1].cid, "0010");
    assert_eq!(new_rt.buckets[2].records[2].cid, "0001");
    assert_eq!(new_rt.buckets[2].records[3].cid, "0000");
}

#[test]
fn test_previous_buckets_less_k_next_buckets_upto_k() {
    let new_rt = RoutingTable::new()
        .add_record(0, "0010", "RE")
        .add_record(1, "0000", "RE")
        .add_record(2, "0111", "RE")
        .add_record(2, "0110", "RE")
        .add_record(3, "1011", "RE")
        .add_record(3, "1001", "RE")
        .normalize();

    assert_eq!(new_rt.buckets[1].records[0].cid, "0000");
    assert_eq!(new_rt.buckets[1].records[1].cid, "0010");
    assert_eq!(new_rt.buckets[1].records[2].cid, "0111");
    assert_eq!(new_rt.buckets[1].records[3].cid, "0110");
}

#[test]
fn test_next_bucket_more_than_k_choose_full_subbuckets() {
    let new_rt = RoutingTable::new()
        .add_record(0, "0010", "RE")
        .add_record(1, "0000", "RE")
        .add_record(2, "0101", "RE")
        .add_record(2, "0100", "RE")
        .add_record(2, "0111", "RE")
        .add_record(3, "1011", "RE")
        .add_record(3, "1001", "RE")
        .normalize();

    assert_eq!(new_rt.buckets[1].records[0].cid, "0000");
    assert_eq!(new_rt.buckets[1].records[1].cid, "0010");
    assert_eq!(new_rt.buckets[1].records[2].cid, "0101");
    assert_eq!(new_rt.buckets[1].records[3].cid, "0100");
}

#[test]
fn test_next_bucket_more_than_k_choose_randomly_from_subbuckets() {
    let new_rt = RoutingTable::new()
        .add_record(0, "0010", "RE")
        .add_record(1, "0000", "RE")
        .add_record(2, "0101", "RE")
        .add_record(2, "0111", "RE")
        .add_record(2, "0110", "RE")
        .add_record(3, "1011", "RE")
        .add_record(3, "1001", "RE")
        .normalize();

    assert_eq!(new_rt.buckets[1].records[0].cid, "0000");
    assert_eq!(new_rt.buckets[1].records[1].cid, "0010");
    assert_eq!(new_rt.buckets[1].records[2].cid, "0101");
    assert_eq!(new_rt.buckets[1].records[3].cid, "0110"); // or 0111 depending on randomness (seed)
}

#[test]
fn test_previous_bucket_more_than_k() {
    let new_rt = RoutingTable::new()
        .add_record(0, "0010", "RE")
        .add_record(1, "0000", "RE")
        .add_record(1, "0001", "RE")
        .add_record(2, "0101", "RE")
        .add_record(2, "0111", "RE")
        .add_record(2, "0110", "RE")
        .add_record(3, "1010", "RE")
        .normalize();

    assert_eq!(new_rt.buckets[3].records[0].cid, "1010");
    // last three nodes can be any nodes out of the other 5 in the RT.
    assert_eq!(new_rt.buckets[3].records[1].cid, "0010");
    assert_eq!(new_rt.buckets[3].records[2].cid, "0101");
    assert_eq!(new_rt.buckets[3].records[3].cid, "0110");
}
