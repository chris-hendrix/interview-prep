# Systems Design
https://github.com/donnemartin/system-design-primer

## Scalability

Topics
- **Vertical** scaling: better machines
- **Horizontal scaling**: more machines
- **Caching**: separate key value db
- **Load balancing**: redirects traffic (at global, dns, db, etc.)
- **Database replication**: master/slaves (multiple masters = HA)
- **Database partitioning**: two masters with LB at db layer
- **Clones**: outsource sessions to db and clone server
- **Databases**: scale SQL vertically and horizontally (read from slaves, write to master), or denormalize from start with NoSQL and cache 
- **Caches**: use independent in-memory cache (Redis), object-based caching preferred over query-based (easier to detect changes in data)
- **Asynchronism**: pre-rendering html, heavy jobs done in the background (like amazon compiling your list of transactions to export)

Resources
- [Harvard lecture](https://www.youtube.com/watch?v=-W9F__D3oY4)
- [Scalability for dummies](https://web.archive.org/web/20220530193926/https://www.lecloud.net/tagged/scalability)

## High level trade-offs

Performance vs scalability
- Performance: fast for a single user
- Scalability: fast for a heavy load of users

Latency vs throughput
- Latency: time between request and response
- Throughput: requests per second
- Aim for maximum throughput with acceptable latency

Availability vs consistency (CAP theorem, see below)

## CAP Theorem
### Availability vs consistency
- Request data from one of two servers, choose two of three (C/P or A/P)
  1. **(C)onsitency**: up-to-date data or error
  2. **(A)vailability**: maybe not up-to-date data, no error
  3. **(P)artition tolerance**: continues to function when one server goes down
- Options
  - CP: for atomic reads/writes (operation 2 cannot start until operation 1 finishes)
  - AP: ok for eventual consistency or system needs to continue functioning

### Consistency patterns
- Weak: after a write, reads will eventually catch up (ie cache)
- Eventual: after a write, reads will catchup in milliseconds (ie DNS updating host IP takes a little time)
- Strong: after a write, reads synchronously see it (ie transactions)

### Availability patterns (HA)
- Failover
  - Master-slave: downtime when promoting slave to master
  - Master-master: load split between masters, one takes over if the other fails
  - Disadvantages: more hardware and complexity, writes lost during switching
- Replication (see database section)
  - Master-slave replication
  - Master-master replication
- Calculation
  - Measured in # of 9s (99.9% and 99.99%)
  - Series: `A = A(1) * A(2)`
  - Parallel: `A = (1 - A(1)) * (1 - A(2))`

## Domain name system (DNS)
- Maps domain name to IPv4 address (user goes to google.com -> DNS returns IPv4 > page loads)
- ISP (for example) has cache, on miss, go to root DNS server
- Managed DNS services (CloudFlare) can route traffic via round robin, latency times, and geo-location
- Disadvantages: slight delay, DNS servers are complex and managed by large entities, DDoS attacks

## Content delivery network (CDN)
- Proxy servers that store static content (HTML photos)
- Benefits: content from nearby servers, reduces load on your servers
- Disadvantages: costly, stale data (TTL too long), change URL to point to static content
- Push CDN: 1) updates with server changes, 2) good for small traffic with slow changing content
- Pull CDN: 1) updates when first user requests content, then cached (expires after set time, TTL), 2) can be redundant (expiration but not updated), 3) good for high traffic 


## Load balancer
- Distribute incoming traffic to appropriate servers AND/OR databases
- Benefits
  - Stops traffic from unhealthy/overloaded resources
  - Eliminates single point of failure
  - Can decrypt/encrypt at interface rather than downstream
  - Can keep track of sessions (cookies) if server doesn't
- Methods: random, least loaded, session/cookies, round robin, weighted RR
- Layer 4: middleman that isolates client and server ports, keeps mapping table (client/server) to determine ports, does not read packet data
  - Advantages: Simpler, efficient, NAT (switches client/server to correct port)
  - Disadvantages: not smart, no microservices, no cache (need to know content)
  - Layer 7