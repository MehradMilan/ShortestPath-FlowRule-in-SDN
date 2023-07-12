# ShortestPath-FlowRule-in-SDN
## The Computer Networks course extra homework.
### Spring 2023 - Sharif Universuty of Technology
---
- Firstly start running Floodlight using this command:

```sh
java -jar target/floodlight.jar
```

- Then run the mininet with the custom topology (Default remote controller IP is: 127.0.0.1):

```bash
sudo mn --custom testtopo.py --topo mytopo --switch ovsk --controller=remote --link=tc
```

- In the end, run the flow_rule.py script to give weights to the links and find the shortest path and add new rules to the switches:

```sh
python3 flow_rule.py
```

By default, floodlight listens on port 8080 for REST connections and 6633 for OpenFlow connections.

- [Useful Link](https://floodlight.atlassian.net/wiki/spaces/floodlightcontroller/pages/1343539/Floodlight+REST+API)
