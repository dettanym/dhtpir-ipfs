#[allow(non_upper_case_globals)]
const k: usize = 20;

#[derive(Debug, Clone)]
pub struct Record {
    pub cid: String,
    pub multiaddr: String,
}

#[derive(Debug, Clone)]
pub struct Bucket {
    pub records: Vec<Record>,
}

impl Bucket {
    pub fn new(cid: String, multiaddr: String) -> Bucket {
        Bucket {
            records: vec![Record { cid, multiaddr }],
        }
    }
}

#[derive(Debug)]
pub struct RoutingTable {
    pub buckets: Vec<Bucket>,
}

impl RoutingTable {
    pub fn new(key: String, value: String) -> RoutingTable {
        RoutingTable {
            buckets: vec![Bucket::new(key, value)],
        }
    }

    pub fn normalize(self) -> RoutingTable {
        let buckets = self.buckets;

        let mut normalized_buckets: Vec<Bucket> = vec![];
        for (index, bucket) in buckets.iter().enumerate() {
            let mut normalized_records = bucket.records.clone();

            let prev_records: Vec<Record> = if index == 0 {
                vec![]
            } else {
                buckets[0..index - 1]
                    .iter()
                    .flat_map(|bucket| bucket.records.clone())
                    .collect()
            };

            if bucket.records.len() < k {
                if prev_records.len() < k - bucket.records.len() {
                    normalized_records.extend(prev_records);
                    if index < buckets.len() - 1 {
                        let mut l = index + 1;
                        let next_bucket_records = &buckets[l].records;
                        while normalized_records.len() + next_bucket_records.len() < k {
                            normalized_records.extend(next_bucket_records.clone());
                            l += 1;
                        }
                        // TODO: This next while loop seems redundant, if we're just selecting randomly k - normalized_records.len() elements
                        //  from the next bucket.
                        // TODO: Add libraries for random choice.
                    } else {
                        // TODO: nothing for now for last element in buckets vector
                    }
                } else {
                    // TODO: See slide 53 (bucket 3 is empty and buckets 0--2 have a total of 4 elements).
                    //  Don't pick randomly, you'll need to pick closest ones from the entries already in $B'_i$.
                }
            }

            normalized_buckets.push(Bucket {
                records: normalized_records,
            });
        }

        RoutingTable {
            buckets: normalized_buckets,
        }
    }
}

fn main() {
    let rt = RoutingTable::new(String::from("0111"), String::from("12"));
    let new_rt = rt.normalize();
    dbg!("{:?}", new_rt);
}
