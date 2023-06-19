use itertools::FoldWhile::{Continue, Done};
use itertools::Itertools;
use rand::distributions::{Distribution, Uniform};
use rand_xoshiro::SplitMix64;
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

    pub fn dist(&self) -> usize {
        usize::from_str_radix(self.cid.as_str(), 2).unwrap()
            ^ usize::from_str_radix(OWN_NODE_ID, 2).unwrap()
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

#[derive(Debug, Clone)]
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

    fn pick_at_random_from_records(
        rand: &mut SplitMix64,
        n: usize,
        records: Vec<Record>,
    ) -> Vec<Record> {
        Uniform::from(0..records.len())
            .sample_iter(rand)
            .take(n)
            .map(|i| records[i].clone())
            .collect()
    }

    fn get_records_from_previous_buckets(
        rand: &mut SplitMix64,
        n: usize,
        previous_buckets: &[Bucket],
    ) -> Vec<Record> {
        if n == 0 {
            return vec![];
        }

        let prev_records: Vec<Record> = previous_buckets
            .iter()
            .flat_map(|bucket| bucket.records.clone())
            // .take(n)
            .collect();

        if prev_records.len() <= n {
            return prev_records;
        }

        RoutingTable::pick_at_random_from_records(rand, n, prev_records)
    }

    fn get_records_from_next_buckets(
        rand: &mut SplitMix64,
        n: usize,
        next_buckets: &[Bucket],
        own_bucket_max_size: usize,
    ) -> Vec<Record> {
        next_buckets
            .iter()
            .fold_while(vec![], |mut acc_outer, bucket| {
                if acc_outer.len() == n {
                    return Done(acc_outer);
                }
                if bucket.records.len() + acc_outer.len() <= n {
                    acc_outer.extend(bucket.records.clone());
                } else {
                    let mut next_records = bucket.records.clone();
                    next_records.sort_by_key(|record| record.dist());
                    let vec_sub_buckets: Vec<Vec<Record>> = next_records
                        .chunks(own_bucket_max_size)
                        .map(|s| s.into())
                        .collect();
                    let max_len = n - acc_outer.len();
                    let elements_from_sub_buckets = vec_sub_buckets
                        .iter()
                        .fold_while(vec![], |mut acc_inner, sub_bucket| {
                            if acc_inner.len() == max_len {
                                return Done(acc_inner);
                            }
                            if sub_bucket.len() + acc_inner.len() <= max_len {
                                acc_inner.extend(sub_bucket.clone());
                            } else {
                                acc_inner.extend(RoutingTable::pick_at_random_from_records(
                                    rand,
                                    max_len - acc_inner.len(),
                                    sub_bucket.to_vec(),
                                ));
                            }
                            Continue(acc_inner)
                        })
                        .into_inner();
                    acc_outer.extend(elements_from_sub_buckets);
                }
                Continue(acc_outer)
            })
            .into_inner()
    }

    pub fn normalize2(self, rand: &mut SplitMix64) -> RoutingTable {
        let normalized_buckets: Vec<Bucket> = self
            .buckets
            .iter()
            .enumerate()
            .map(|(index, bucket)| {
                let normalized_records_size = bucket.records.len();

                let records_from_prev_buckets = RoutingTable::get_records_from_previous_buckets(
                    rand,
                    K - normalized_records_size,
                    &self.buckets[0..index],
                );

                let records_from_next_buckets = RoutingTable::get_records_from_next_buckets(
                    rand,
                    K - normalized_records_size - records_from_prev_buckets.len(),
                    &self.buckets[index + 1..self.buckets.len()],
                    2u32.pow(index as u32).try_into().unwrap(),
                );

                let mut normalized_records = bucket.records.clone();
                normalized_records.extend(records_from_prev_buckets);
                normalized_records.extend(records_from_next_buckets);

                Bucket {
                    records: normalized_records,
                }
            })
            .collect();

        RoutingTable {
            buckets: normalized_buckets,
        }
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

#[cfg(test)]
mod test {
    use super::*;
    use rand_core::SeedableRng;
    use std::borrow::BorrowMut;

    #[test]
    fn test_empty_prev_buckets() {
        assert!(RoutingTable::get_records_from_previous_buckets(
            SplitMix64::seed_from_u64(0).borrow_mut(),
            0,
            &[Bucket::new()]
        )
        .is_empty());
    }

    #[test]
    fn test_empty_next_buckets() {
        assert!(RoutingTable::get_records_from_next_buckets(
            SplitMix64::seed_from_u64(0).borrow_mut(),
            0,
            &[Bucket::new()],
            2
        )
        .is_empty());
    }
}
