# Reproduce Internal (In)consistency

Background: https://www.scattered-thoughts.net/writing/internal-consistency-in-streaming-systems/

1. Generate test data:

```bash
python3 datagen.py large
```

Optional, verify that data has been written:
```bash
❯ cat transactions_large.json | wc -l
10000000
```

2. Launch redpanda, create input topic and fill it with `transaction_large.json`

```bash
docker run --name redpanda -p 9092:9092 --rm -itd docker.redpanda.com/vectorized/redpanda:v23.2.3 redpanda start --smp 4
rpk topic delete input
rpk topic create input -c retention.ms=-1 -c retention.bytes=-1
cat transactions_large.json | rpk topic produce input
```

3. Install and start Rising Wave

```
curl https://risingwave.com/sh | sh
export ENABLE_TELEMETRY=false
rm -rf ~/.risingwave && ./risingwave
```

4. In a new shell, monitor the output topic 

```bash
rpk topic delete output
rpk topic create output -c retention.ms=-1 -c retention.bytes=-1
rpk topic consume output --brokers localhost:9092 > output.json
```

4. In a new shell, create the pipeline

```bash
psql -h 0.0.0.0 -p 4566 -d dev -U root < program.sql
```

5. Monitor the system, wait until processing is done
```
psql -h localhost -p 4566 -d dev -U root
```

Run the following query in the shell, stop when you see it display 1000000 as the count
(you may have to execute the query multiple times):

```
dev=> select count(*) from transactions;
  count   
----------
 10000000
(1 row)
```

6. Plot results

Hit Ctrl+c on the shell that monitors the output topic.
Then run `python plot.py` script.
The balances are displayed in `inconsistent.png`.


