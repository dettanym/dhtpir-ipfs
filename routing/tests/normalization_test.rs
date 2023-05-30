use routing::RoutingTable;

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
