const K: usize = 4;
const NO_OF_BUCKETS: usize = 4;
const OWN_NODE_ID: &'static str = "0011";

#[derive(Debug, Clone)]
pub struct Record {
    pub cid: String,
    pub multiaddr: String,
}

impl Record {
    pub fn new(cid: &str, multiaddr: &str) -> Record {
        Record {
            cid: String::from(cid),
            multiaddr: String::from(multiaddr),
        }
    }
}

#[derive(Debug, Clone)]
pub struct Bucket {
    pub records: Vec<Record>,
}

impl Bucket {
    pub fn new() -> Bucket {
        Bucket { records: vec![] }
    }

    pub fn add(mut self, cid: &str, multiaddr: &str) -> Self {
        self.records.push(Record::new(cid, multiaddr));
        self
    }
}

#[derive(Debug)]
pub struct RoutingTable {
    pub buckets: Vec<Bucket>,
}

impl RoutingTable {
    pub fn new() -> RoutingTable {
        RoutingTable { buckets: vec![] }
    }

    pub fn add_record(mut self, bucket_id: usize, cid: &str, multiaddr: &str) -> Self {
        if bucket_id < self.buckets.len() {
            self.buckets[bucket_id]
                .records
                .push(Record::new(cid, multiaddr));
        } else if bucket_id == self.buckets.len() {
            self.buckets.push(Bucket::new().add(cid, multiaddr))
        } else {
            panic!("bucket_id is out of bucket bounds")
        }
        self
    }

    pub fn normalize(self) -> RoutingTable {
        let buckets = self.buckets;

        let mut normalized_buckets: Vec<Bucket> = vec![];
        for (index, bucket) in buckets.iter().enumerate() {
            let mut normalized_records = bucket.records.clone();

            let prev_records: Vec<Record> = buckets[0..index]
                .iter()
                .flat_map(|bucket| bucket.records.clone())
                .collect();

            if bucket.records.len() < K {
                if prev_records.len() <= K - bucket.records.len() {
                    normalized_records.extend(prev_records);
                    if index < buckets.len() - 1 {
                        let mut l = index + 1;
                        while l < buckets.len()
                            && normalized_records.len() + &buckets[l].records.len() <= K
                        {
                            normalized_records.extend(buckets[l].records.clone());
                            l += 1;
                        }
                        if l < buckets.len() {
                            let next_bucket_records = &buckets[l].records;
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