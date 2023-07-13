# Checklist for Performance Efficiency

This checklist presents a set of recommendations for your system to scale its ability to grow to meet workload usage demand. The goal of performance is that every valid interaction to a healthy system continues to be efficient even as demand increases. This must be designed and implemented with focus on efficiency and effectiveness in cost, complexity, supporting new requirements, technical debt, reporting, and toil factored in.

Every system has a limit on how much it can be scaled without redesigning, introducing a workaround, or having human involvement.**** If you haven’t checked the boxes and considered the tradeoffs, the design could be at risk. Careful consideration of all the points covered in the checklist will give you confidence in success.

Code

Recommendation

PE: 01

Define performance targets. Performance targets should exist for all workload flows.

See more at [Best practices for establishing and exposing performance targets](https://microsoft.sharepoint.com/teams/WAF2.0DevelopmentTeam/Shared%20Documents/Pillar%20development/Content/Performance%20Efficiency/PE%2001%20-%20Define%20performance%20targets.docx).

*One-liner: Define and report the numeric key performance indicators for the application and user flows.*

**Define the performance targets, visualization, and signaling** to drive actions that** measure workload flows** that are in-scope for performance calibration.

PE: 02

Collect performance data on workload components and flows. The data collection should be automatic, continuous, and meaningful.

Guide:

See more at [Best practices for capturing performance metrics and logs](https://microsoft.sharepoint.com/teams/WAF2.0DevelopmentTeam/Shared%20Documents/Pillar%20development/Content/Performance%20Efficiency/PE%2002%20-%20Capture%20performance%20data.docx).

*One-liner: Automatically and continuously capture complete & accurate data across the workload to power established KPIs.*

**Capture complete performance data** from workload components and flows,** automatically and continuously**. This data is used exclusively to create the alerts, dashboards, and reports that track progress on the defined targets.

Monitor all application endpoints to detect performance issues. Endpoint performance issues include slow response, inaccurate data, or malformed data.

*Needs to be from resources and custom code deployed. When we talk about code, use the term “instrumentation.” Guide should talk about performance data of both resources and and flows. This was “Instrument the solution.”*

*The data needs to be across individual components and also across flows.*

*A cultural habit. Make sure the metrics are “at load”*

*Performant for you.*

*“Just enough” (need health signal-to-noise)*

PE: 03

**Test performance targets against a baseline.** Performance target testing should be regular and performed in an environment that matches the production environment.

**Related guide/assessment content:**

**Perform benchmark testing** against a baseline. Regularly test in an environment that closely matches production *and* in actual production, measuring the impact against performance targets.

(Part of guide ?) Fine-tune the system until you achieve a consistent and acceptable level of performance relative to the baseline.

*Establish performance baselines; measure and test all candidate & deployed changes against them.*

Performance baseline measurements are established and maintained over time. All proposed application code or infrastructure changes are tested (measured) in a production-like environment against the current baseline to detect and block untenable deviation. This happens as an integrated part of the SDLC for the workload, using techniques like synthetic transitions & load. Impact that can only be measured, practically, after release is measured as a “test in production” action, such that identified issues can have a remediation plan built.

Non-functional requirements such as performance (CPU utilization / max RPS) should be a part of quality checks as much as functional requirements are. If a new build fails these requirements your should not proceed with deployment to production and go back to development.

Any pre-production testing should have production-like data (both in shape, quantity, and rate of change). Resetting test data to a “known state” before tests. Test data scrubbing/masking. These reasons bolster the “test in production” ideal. Maintaining testing data is part of SDLC.

QA: get notified of perf issues early in the SDLC, never early enough to start testing.

. How much perf degradation can I tolerate between releases? E.g. consider setting a percentage threshold against baseline (0% in extreme cases). Without these defined numeric thresholds, you cannot alert on performance drift.

People “plan to do performance testing” but they do it at the end. But pressure to ship or hit a deadline. Don’t skip this. It must be started from the very beginning\! “Shift left” both in terms of SDLC and in terms of project timelines.

Test per flow.

Predictive performance alerts.

Five buckets: Frequency, Vital, Risky, Data intensive, architecturally intensive

To generate sufficient and various load, consider load testing techniques such as traffic mirroring. Special events, daily fluxuation, variable, acquiring a new tenant/customer. Load models.

Lab enviornments may not reflect production sufficently for certain workloads. IoT specifically wants a production mirror and load.

Automation of execution and alerting.

To aide in remediation of found issues, you’ll benefit from having instrumented code so that you can see hot paths, new significant memory allocations, new late-generation garbage collection, etc. Learn your performance monitoring tooling, such as [ETW](/azure/windows/win32/etw/about-event-tracing), [BenchmarkDotNet](https://github.com/dotnet/BenchmarkDotNet), and [PerfView](https://github.com/microsoft/perfview).

Always consider the end user perspective (client resources, location, mobility) on performance. Meet the users where they are, measuring & testing from that perspective. Measuring requests per second, or server processing time doesn’t account for the end user experience. Onboard users into the Microsoft network sooner by selecting regions that are geographically close to them or using edge resources, like Azure Front Door. The users experience the full stack of your workload, and you should influence what you can control.

PE: 04

**Implement a scaling and partitioning strategy**. The strategy should be reliable and controlled, and it should be based on the workload’s scale-unit design.

**Related guide/assessment content:**

The goal is to have enough resources to meet valid usage demands.

*Make enough resources available to meet legitimate usage demands by implementing a reliable and bounded scaling strategy.*

See more at [Best practices for scaling and partitioning](https://microsoft.sharepoint.com/:w:/t/WAF2.0DevelopmentTeam/IQDwGZLxEeDUQ6OQr7vsy7gqAdmUoNVYNhBxzSceXzDVFLA?e=vHonHs).

All components subject to expected & potential usage fluctuations that impact their utilization limits are proven to be independently scalable, in a timely and responsible manner, to account for workload demand. Components that are expected to be scaled together are documented as part of your scale unit design.

Constrain autoscaling to mitigate the effects of runaway automation.

Limits are in place to prevent runaway automated scaling or alerts are established to detect the same. Scaling in and out happens with a defined end user or business metric disruption threshold, in most cases “no disruption” is desired.

Scale impact on downstream & external dependencies, per infrastructure component, are understood and documented.

Should talk about data partitioning (vertical and horizontal [sharding])

Test and prove this stratregy out.

Perfer services that support out-of-the-box scaling. Configure and go. Be aware of services that “scale up/out” only; some don’t support scale “down/in” once done with that burst need. Scale down in these cases can be very process/time intensive.

When in doubt, POC\! Test scaling behavior (delay, cost, in/out features, troubleshooting). Decide base on data. The scaling methods per component are optimized for the use case and capabilities of that component:

- *scale-out (horizontal)* by adding additional replicas of the resource.
- *logical and physical partitioning around functional boundaries*, mirroring a single responsibility principle per process. Such as microservices deployed to separate infrastructure.
- *logical and physical partitioning around data boundaries*, using discoverable data to define segmentation boundaries. Such as geography, tenant, date, organizational unit.

Be aware of scale limits for each of the component

Be aware of the scaling time involved for each Azure resources. Based on this, the scaling event/threshold needs to be decided.

Ideally the Azure resource scaling should have direct correlation with the business “unit of work" scaling.

Evaluate on scale limits of vertical scale (scale-up) for data stores and if this is sufficient in long term growth, invest in scale-out approach. Don’t invest too much when not required. Sometimes it involves application re-write and hence tradeoff’s should be factored in.

Scaling in multi-tenants should be looked different from just Azure resource scaling perspective. Ideally it should scale the billing or work units in the architecture. Noisy neignhour consideration should be factored in for shared systems which result in scaling of Azure resources not result in scaling the system capacity.

PE: 05

Choose the right infrastructure, resources, and SKUs to support your performance targets. The selections should weigh the benefits of using platform features or building a custom implementation.

**Related guide/assessment content:** 

**Select Azure resources, their SKUs, regions & zones, and features that support your performance requirements in an optimized way. Compare the performance impact of custom implementation versus offloading functionality to the platform.**

**See more at** [**Best practices for selecting the right services**](https://microsoft.sharepoint.com/:w:/t/WAF2.0DevelopmentTeam/IQBI7WOL-VEORoB4SzXs17k8AbkNJB9OmurhS3UmLply8zg?e=4Ee7xm)**.**

*With the whole workload usage & lifecycle in mind, select right-sized, right-featured Azure services.*

All infrastructure components provisioned for the workload are Azure resources, their SKUs, their quantities, and their instance that:

- Offload functionality to platform features where they meet your performance requirements, develop custom code when platform features don’t suffice.
- support scaling in [PE: 03](#PE3), including your partitioning strategy,
- supports your data sharding strategy,
- and can achieve your established [performance KPIs](#PE01) and can [emit the data](#PE02) to prove it.

Be sure to talk about sku limits/boundaries. There is a central URL that links to all per-service limits. Predict future data and usage volume growing over the next *n* years. Plan for reasonable growth. Also understand the cliffs in the design – once you hit a cliff, it’s a re-architecture and migration exercise.

Some organizations have an “allow list” of services (or features of services). That’s a constraint that might limit the ability to have complete freedom.

Pay attention to all migration or cross-premises scenarios. “Like-for-like” isn’t always going to give you same performance characteristics. Must test at load.

Understand performance guarantees for the right services and SKUs

Various levels of skus,

Skill of team might impact SKU selection. K8s vs app service vs spring. Team expertise. Choice of the database is a huge one. We are a “SQL” or “mySQL” shop or whatever…

When your solution spans availability zones across subscriptions, ensure you’ve considered the zone mapping between the regions that comprise your solution. Zone 1 in a subscription’s region might not be Zone 1 in the same region in another subscription.

PE: 06

Design components to distribute load. The load distribution should be across multiple resources or resource instances to enable load balancing and scale-out operations.

**Related guide/assessment content:**

*Components are designed to distribute and redistribute load across multiple resources or resource instances, avoiding reliance on pinning or singletons.*

Where possible, avoid solutions that require client affinity, data locking, or state affinity to a single instance to ensure that a client or process can always be directed to a resource that has capacity. This enables simplified load balancing & scale operations.

These are “bottlenecks” in your design.

PE: 07

Measure the effects of operations on performance. The performance effects of software development lifecycle and other routine operations should be known and minimal.

**Related guide/assessment content:**

**Respect your performance targets while performing SDLC and routine operations.** 

as guide examples:** such as deploying a new version, performing periodic or one-off backups, or performing audits.** 

** Deploying a new version into production should be done “at scale” of the current run state of the system. Do not deploy to a “minimum/default” and force the system to immediately perform a scale operation.**

*Build & execute lifecycle operation processes that respect your performance targets.*

Ensure the *actions/operations* of lifecycle concerns, such as the deploying a new version of the workload, has understood, and ideally negligible, impact on the established performance KPIs. Your operations tasks are not of concern to your end users nor your business metrics.

Service features such as deployment slots. AKS doing side-by-side (B/G) deployments and do traffic shifting. Database point-in-time.

Database changes should be carefully planned and announced. Can we learn anything from M365 teams for SharePoint Online?

Timing and methods of deployment.

Take advantage of offhours if there is such a concept. Reindexing/scanning off hours. Data compacting, data teiring, etc.

Administrative operations take away from limited resources on any instances.

Be aware of IaC-based deployments not respecting current scaling. For example, your IaC may set an instance count of “2” and support scaling to “10” and the current deployed environment is running at “8.” If instance count of “2” is set at deployment time, you’ll negatively impact the run-state of that service.

Pre-warm instances during fresh deployment so that it is ready to serve users immediately and have minimum impact to users.

PE: 08

Design all data stores, partitions, and indexes for their intended use in the workload.

**Related guide/assessment content:**

*Design all data stores, partitions, & indexes explicitly for their intended usage in the workload.*

**Where your workload controls its own data, design all data stores, partitions, and indexes for their intended use in the workload.** 

**(guide?) Tune data shape and indexes based on coded CRUD usage patterns. Use eventual consistency where practical to facilitate data caching, shard replication, and deferred data capture.**

Implement a sustainable data sharding model to segment data across performance boundaries that avoids data and query hotspots. Index and shape data based on expected usage (CRUD) patterns. Use eventual consistency where possible to facilitate sharding and data caching.

Maintenance jobs for indexes and statistics. PSQL, MySQL, etc insights for long-running queries, missed indexes. “Databases are never done.”

Separating OLTP and OLAP use cases

If CAP theorem is evaluated for your workload’s data, remember that it does not have any provisions for performance. If data latency is a critical factor in your workload, consider using an alternative such as PACELC which puts latency measured against consistency.

PE: 09

Optimize use of workload resources. Code and infrastructure should only be used for their core purpose and only when necessary.

**Related guide/assessment content:** 

**Keep all resource utilization limited to its core purpose and only use the resource when necessary by using architectural techniques like data caching, gateway processing, and utilizing available client resources. Also reduce resource utilization (such as CPU cores and memory) by optimizing code to avoid memory leaks, unnecessary large object heap allocations, seeking O(1) solutions, and taking advantage of the processor architectures and their threading models.**

*Optimize code and application vs optimize with brute force. Need to have skilled engineering team. This is an efficiency point. Investing where you’ll get ROI with minimum I.*

Reduce resource utilization to avoid memory leaks, unnecessary large object heap allocations, seeking 0(1) solutions. Take advantage of the processor architecture and threading models.

*Keep resource utilization limited to its core purpose and only use the resource when necessary.*

Use techniques that ultimately minimize the need for usage of your system’s resources. For example:

- Instill an expectation of reasonably up-to-date data in the workload so that you can offload/externalize responsibility and resource utilization to clients or intermediaries, such as search indexes and caches.
- Offload security checks, such as web application firewalls, to gateway resources, and not within your code or your individual compute instances.

Optimize all on-wire communication and the processing of it. Use techniques as appropriate to the situation such as minimizing data retrieved, using optimized protocols, using compression, or even avoiding communication altogether if redundant.

Keeping code tight. Easier to manage, less complex, optimize resource utilization. Single responsibly principle

Does data compression go here? How about connection pooling?

Code that is optimized & defect free from the perspective of performance goes a long way in reducing your resource consumption. Avoiding bugs such as memory leaks is one thing, but optimizing your code to use less resources or to make better use of the resources you have available. Some examples would be looking for opportunities to replace O(N) operations with O(1) equivalents, reducing large object heap memory allocations, ensuring your code takes advantage of the CPU architecture of your compute, removing unnecessary busy-waiting conditions, using object and connection pooling, etc.

Add resource usage limits wherever possible. Eg: AKS resource limits or JVM memory limits. Avoid increasing resources as a way to fix the performance issues which originate from the application code.

PE: 10

**Conduct formal capacity planning and drilling activities at key points in the lifecycle of the workload.** Capacity planning should occur before predicted changes in usage patterns.

**Related guide/assessment content:**

(initial business requirements, significant business model changes, marketing pushes, seasonal drift).

*Formal capacity planning activities are performed at key points in the lifecycle of the workload.*

This includes initial workload design based on initial business requirements, business model changes, seasonal drift, 8am sign-on rush, etc.

The drilling part maybe should be put into PE:05 (testing)? Simulate the future (3 years). How do we know “how much capacity we need?” Buy until you get there?

Can we tie in capacity model into the formal capacity planning aspect here?

Formal capacity modeling is a prediction exercise, months, years? Planning is the exercise to implement/resource the model. Is this actually a distinction with a difference?

Current capacity vs projected capacity. Application will need to meet the performance goals eventually.

Maybe we talk about “cliffs” in here as well?

PE: 11

Perform a root cause analysis (RCA) on performance and scaling issues. The RCA should determine how to return to normal operations faster and incorporate preventive measures into the workload.

**Related guide/assessment content:** 

Learn from the issue and incorporate. How to get back to healthy faster and mitigate.

ways to introduce self-preservation and self-healing.

*The workload operations team can efficiently perform live-site activities related to potential performance or scaling malfunction.*

Your workload operations team has enough data, insights, & access to perform live-site triage and troubleshooting activities that are related to performance or scaling malfunction. This access needs to be across the whole stack: code, networking, compute, security, etc.

Do you have the proper monitoring? Did you contact support? Was the issue on data side? Networking? App? Etc. Be equiped to find issues as quick as possible, and improve upon them.

**5xWhy**

**How was the problem mitigated?**

**How are we preventing it from happening again?**

- Root Cause Analysis: Performance monitoring data is invaluable when investigating and resolving performance-related incidents or outages. When issues occur, monitoring data provides a historical record of performance metrics, allowing you to analyze the root cause and identify contributing factors. This facilitates efficient troubleshooting, accelerates incident resolution, and reduces downtime, resulting in cost savings and improved service reliability.

PE: 12

**Prioritize the performance of critical flows and critical users. Prioritization should focus on where to invest limited resources.** 

**Related guide/assessment content:** 

**Where practical, yield lower & non-priority usage to higher priority usage. This might align with your workload’s business or tenant model.**

*Prioritize the performance of critical flows and users.*

Prioritize critical user, data, and workflows along with critical user access. This could align with workload business models, for example or tied back to business outcomes like revenue. Where practical yield lower & non-priority usage to higher priority usage. Use techniques such as rate limiting, priority queue processing, etc.

Isolate critical workflows, maybe even to the enviornment levelThis optimizes performance such that the service level provided for critical path interactions does not need to be extraneously extended to all components or all flows in the system.

PE: 13

Continuously optimize performance. The focus should be on components whose performance deteriorates over time, such as databases and networking features.

**Related guide/assessment content:**

Re-index relational databases

Institute continuous effort to optimize performance of solution components that may deteriorate over time (growth/usage), like databases and networking components. Consider developing or taking advantage of existing specialized resources across workloads.

*Continuous optimization of solution components*

*Teams with specialized skills, potentially dedicated to that. Automate where practical. Reduce manual effort/toil.*

Enable automated tuning of database resources provided by cloud service vendors such as automatic creating missing indexes, dropping unused indexes, and plan correction.

As my ten most widely used top 10 sql statements, optimized? Montior top flows, widly used pages, databases. Look for ways to optimize these critical flows.

Use the automated tuning features that cloud service vendors provide. These features include automatic creating missing indexes, dropping unused indexes, and plan correction.

Automatic tuning options can be independently enabled or disabled for each database, or they can be configured at the server-level and applied on every database that inherits settings from the server.

Try to reduce technical debt of the overall system. Allowing technical debt to grow continuously over time will result in inefficiencies and performance impact over time.

- Performance monitoring allows you to identify performance issues, bottlenecks, or anomalies in real-time or near real-time
- By continuously monitoring performance metrics, you can detect problems as soon as they arise, enabling you to take immediate action before they escalate into larger issues. Early detection helps minimize the impact on users, mitigate potential downtime, and reduce the cost and effort required to resolve performance-related problems.
- Proactive Performance Optimization: Monitoring performance metrics over time provides insights into trends and patterns.
- By tracking performance metrics, you can identify periods of peak demand, forecast future resource needs, and plan capacity accordingly.
- By monitoring key performance indicators (KPIs) and comparing them against SLA requirements, you can ensure that your application or service is meeting the agreed-upon performance targets.

PE: 14

**[Recommendation text]**

**Related guide/assessment content:**

*[Pithy one sentence summary]*

*Formal capacity planning vs deploy and be ready to instantly adapt*

*Have the knowledge and skills team to be able to react. They need to understand the tooling, the architecture, and the impact profile of failure. Especially cross-team (team boundaries). DB team vs app team. CROSS-TEAM Drilling can help sort out bottlenecks in people/process.*

*DevOps team culture and adoption *

*LEARN FROM PRODUCTION – that’s a key point*

*[Free-form guide “seed” content.]*

PE: 15

**Related guide/assessment content:**

*[Pithy one sentence summary]*

*[Free-form guide “seed” content.]*

PE: 16

**Related guide/assessment content:**

*[Pithy one sentence summary]*

*[Free-form guide “seed” content.]*

Automatic tuning options can be independently enabled or disabled for each database, or they can be configured at the server-level and applied on every database that inherits settings from the server.

## Tradeoffs

*[This section covers the tradeoffs mentioned in the checklist items. The tradeoffs are tied back to the pillar. Combined tradeoff messaging can be considered.]*

- *[Tradeoff 1] [Workaround, if applicable]*
- *Sustainability? Should this surface above in a checklist as part of the defined system’s constraints?*
- *Cost is mostly trade-off while adding additional capacity*
- *Critical vs non-critical business flows in the architecture which needs to prioritized in case of performance constraints*

The list

- Visualize.

# Appendix

![A screenshot of a computer

Description automatically generated with low confidence]

[ADD IMAGE HERE][ADD IMAGE HERE]![A picture containing text, screenshot, font, design

Description automatically generated]

[ADD IMAGE HERE]

| Code  | Recommendation                                                                                                                                                                                                                                                                                                  |
|:-------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| PE: 01 | Define performance targets. Performance targets should exist for all workload flows.                                                                                                                                                                                                                                                               |
|    |                                                                                                                                                                                                                                                                                                         |
|    | See more at .                                                                                                                                                                                                                                                                                                  |
|    | One-liner: Define and report the numeric key performance indicators for the application and user flows.                                                                                                                                                                                                                                                     |
|    | Define the performance targets, visualization, and signaling to drive actions that measure workload flows that are in-scope for performance calibration.                                                                                                                                                                                                                             |
| PE: 02 | Collect performance data on workload components and flows. The data collection should be automatic, continuous, and meaningful.                                                                                                                                                                                                                                         |
|    |                                                                                                                                                                                                                                                                                                         |
|    | Guide:                                                                                                                                                                                                                                                                                                      |
|    | See more at .                                                                                                                                                                                                                                                                                                  |
|    | One-liner: Automatically and continuously capture complete & accurate data across the workload to power established KPIs.                                                                                                                                                                                                                                            |
|    |                                                                                                                                                                                                                                                                                                         |
|    | Capture complete performance data from workload components and flows, automatically and continuously. This data is used exclusively to create the alerts, dashboards, and reports that track progress on the defined targets.                                                                                                                                                                                          |
|    |                                                                                                                                                                                                                                                                                                         |
|    | Monitor all application endpoints to detect performance issues. Endpoint performance issues include slow response, inaccurate data, or malformed data.                                                                                                                                                                                                                              |
|    | Needs to be from resources and custom code deployed. When we talk about code, use the term “instrumentation.” Guide should talk about performance data of both resources and and flows. This was “Instrument the solution.”                                                                                                                                                                                          |
|    | The data needs to be across individual components and also across flows.                                                                                                                                                                                                                                                                     |
|    |                                                                                                                                                                                                                                                                                                         |
|    |                                                                                                                                                                                                                                                                                                         |
|    | “Just enough” (need health signal-to-noise)                                                                                                                                                                                                                                                                                   |
| PE: 03 | Test performance targets against a baseline. Performance target testing should be regular and performed in an environment that matches the production environment.                                                                                                                                                                                                                        |
|    |                                                                                                                                                                                                                                                                                                         |
|    | Related guide/assessment content:                                                                                                                                                                                                                                                                                        |
|    | Perform benchmark testing against a baseline. Regularly test in an environment that closely matches production and in actual production, measuring the impact against performance targets.                                                                                                                                                                                                            |
|    |                                                                                                                                                                                                                                                                                                         |
|    | (Part of guide ?) Fine-tune the system until you achieve a consistent and acceptable level of performance relative to the baseline.                                                                                                                                                                                                                                       |
|    | Establish performance baselines; measure and test all candidate & deployed changes against them.                                                                                                                                                                                                                                                         |
|    | Performance baseline measurements are established and maintained over time. All proposed application code or infrastructure changes are tested (measured) in a production-like environment against the current baseline to detect and block untenable deviation. This happens as an integrated part of the SDLC for the workload, using techniques like synthetic transitions & load. Impact that can only be measured, practically, after release is measured as a “test in production” action, such that identified issues can have a remediation plan built.                         |
|    | Non-functional requirements such as performance (CPU utilization / max RPS) should be a part of quality checks as much as functional requirements are. If a new build fails these requirements your should not proceed with deployment to production and go back to development.                                                                                                                                                                 |
|    | Any pre-production testing should have production-like data (both in shape, quantity, and rate of change). Resetting test data to a “known state” before tests. Test data scrubbing/masking. These reasons bolster the “test in production” ideal. Maintaining testing data is part of SDLC.                                                                                                                                                          |
|    |                                                                                                                                                                                                                                                                                                         |
|    | QA: get notified of perf issues early in the SDLC                                                                                                                                                                                                                                                                                |
|    | . How much perf degradation can I tolerate between releases? E.g. consider setting a percentage threshold against baseline (0% in extreme cases). Without these defined numeric thresholds, you cannot alert on performance drift.                                                                                                                                                                                       |
|    | People “plan to do performance testing” but they do it at the end. But pressure to ship or hit a deadline. Don’t skip this. It must be started from the very beginning! “Shift left” both in terms of SDLC and in terms of project timelines.                                                                                                                                                                                  |
|    | Test per flow.                                                                                                                                                                                                                                                                                                  |
|    | Predictive performance alerts.                                                                                                                                                                                                                                                                                          |
|    | Five buckets: Frequency, Vital, Risky, Data intensive, architecturally intensive                                                                                                                                                                                                                                                                 |
|    | To generate sufficient and various load, consider load testing techniques such as traffic mirroring. Special events, daily fluxuation, acquiring a new tenant/customer. Load models.                                                                                                                                                                                                               |
|    |                                                                                                                                                                                                                                                                                                         |
|    | Automation of execution and alerting.                                                                                                                                                                                                                                                                                      |
|    | To aide in remediation of found issues, you’ll benefit from having instrumented code so that you can see hot paths, new significant memory allocations, new late-generation garbage collection, etc. Learn your performance monitoring tooling, such as , , and .                                                                                                                                                                        |
|    | Always consider the end user perspective (client resources, location, mobility) on performance. Meet the users where they are, measuring & testing from that perspective. Measuring requests per second, or server processing time doesn’t account for the end user experience. Onboard users into the Microsoft network sooner by selecting regions that are geographically close to them or using edge resources, like Azure Front Door. The users experience the full stack of your workload, and you should influence what you can control.                                 |
| PE: 04 | Implement a scaling and partitioning strategy. The strategy should be reliable and controlled, and it should be based on the workload’s scale-unit design.                                                                                                 Related guide/assessment content:                                                                                             The goal is to have enough resources to meet valid usage demands.                                                                                                                                                                                                                                                                       Make enough resources available to meet legitimate usage demands by implementing a reliable and bounded scaling strategy.                                                                                                                                                                                                                                            |
|    | See more at .                                                                                                                                                                                                                                                                                                  |
|    | All components subject to expected & potential usage fluctuations that impact their utilization limits are proven to be independently scalable, in a timely and responsible manner, to account for workload demand. Components that are expected to be scaled together are documented as part of your scale unit design.                                                                                                                                             |
|    |                                                                                                                                                                                                                                                                                                         |
|    | Constrain autoscaling to mitigate the effects of runaway automation.                                                                                                                                                                                                                                                                       |
|    | Limits are in place to prevent runaway automated scaling or alerts are established to detect the same. Scaling in and out happens with a defined end user or business metric disruption threshold, in most cases “no disruption” is desired.                                                                                                                                                                                   |
|    | Scale impact on downstream & external dependencies, per infrastructure component, are understood and documented.                                                                                                                                                                                                                                                 |
|    | Should talk about data partitioning (vertical and horizontal [sharding])                                                                                                                                                                                                                                                                     |
|    |                                                                                                                                                                                                                                                                                                         |
|    | Perfer services that support out-of-the-box scaling. Configure and go. Be aware of services that “scale up/out” only; some don’t support scale “down/in” once done with that burst need. Scale down in these cases can be very process/time intensive.                                                                                                                                                                             |
|    | When in doubt, POC! Test scaling behavior (delay, cost, in/out features, troubleshooting). Decide base on data. The scaling methods per component are optimized for the use case and capabilities of that component:                                                                                                                                                                                               |
|    | scale-out (horizontal) by adding additional replicas of the resource.                                                                                                                                                                                                                                                                      |
|    | logical and physical partitioning around functional boundaries, mirroring a single responsibility principle per process. Such as microservices deployed to separate infrastructure.                                                                                                                                                                                                               |
|    | logical and physical partitioning around data boundaries, using discoverable data to define segmentation boundaries. Such as geography, tenant, date, organizational unit.                                                                                                                                                                                                                    |
| PE: 05 | Choose the right infrastructure, resources, and SKUs to support your performance targets. The selections should weigh the benefits of using platform features or building a custom implementation.                                                                                                                                                                                                        |
|    | Related guide/assessment content:                                                                                                                                                                                                                                                                                        |
|    | Select Azure resources, their SKUs, regions & zones, and features that support your performance requirements in an optimized way. Compare the performance impact of custom implementation versus offloading functionality to the platform.                                                                                                                                                                                    |
|    | See more at .                                                                                                                                                                                                                                                                                                  |
|    |                                                                                                                                                                                                                                                                                                         |
|    | With the whole workload usage & lifecycle in mind, select right-sized, right-featured Azure services.                                                                                                                                                                                                                                                      |
|    | All infrastructure components provisioned for the workload are Azure resources, their SKUs, their quantities, and their instance that:                                                                                                                                                                                                                                      |
|    | Offload functionality to platform features where they meet your performance requirements, develop custom code when platform features don’t suffice.                                                                                                                                                                                                                               |
|    | support scaling in , including your partitioning strategy,                                                                                                                                                                                                                                                                            |
|    | supports your data sharding strategy,                                                                                                                                                                                                                                                                                      |
|    | and can achieve your established and can to prove it.                                                                                                                                                                                                                                                                             |
|    | Be sure to talk about sku limits/boundaries. There is a central URL that links to all per-service limits. Predict future data and usage volume growing over the next n years. Plan for reasonable growth. Also understand the cliffs in the design – once you hit a cliff, it’s a re-architecture and migration exercise.                                                                                                                                           |
|    | Some organizations have an “allow list” of services (or features of services). That’s a constraint that might limit the ability to have complete freedom.                                                                                                                                                                                                                            |
|    | Pay attention to all migration or cross-premises scenarios. “Like-for-like” isn’t always going to give you same performance characteristics. Must test at load.                                                                                                                                                                                                                         |
|    |                                                                                                                                                                                                                                                                                                         |
|    |                                                                                                                                                                                                                                                                                                         |
|    | Skill of team might impact SKU selection. K8s vs app service vs spring. Team expertise. Choice of the database is a huge one. We are a “SQL” or “mySQL” shop or whatever…                                                                                                                                                                                                                   |
|    | When your solution spans availability zones across subscriptions, ensure you’ve considered the zone mapping between the regions that comprise your solution. Zone 1 in a subscription’s region might not be Zone 1 in the same region in another subscription.                                                                                                                                                                          |
| PE: 06 | Design components to distribute load. The load distribution should be across multiple resources or resource instances to enable load balancing and scale-out operations.                                                                                                                                                                                                                     |
|    |                                                                                                                                                                                                                                                                                                         |
|    | Related guide/assessment content:                                                                                                                                                                                                                                                                                        |
|    | Components are designed to distribute and redistribute load across multiple resources or resource instances, avoiding reliance on pinning or singletons.                                                                                                                                                                                                                             |
|    | Where possible, avoid solutions that require client affinity, data locking, or state affinity to a single instance to ensure that a client or process can always be directed to a resource that has capacity. This enables simplified load balancing & scale operations.                                                                                                                                                                     |
|    | These are “bottlenecks” in your design.                                                                                                                                                                                                                                                                                     |
| PE: 07 | Measure the effects of operations on performance. The performance effects of software development lifecycle and other routine operations should be known and minimal.                                                                                                                                                                                                                      |
|    |                                                                                                                                                                                                                                                                                                         |
|    | Related guide/assessment content:                                                                                                                                                                                                                                                                                        |
|    | Respect your performance targets while performing SDLC and routine operations.                                                                                                                                                                                                                                                                  |
|    | as guide examples: such as deploying a new version, performing periodic or one-off backups, or performing audits.                                                                                                                                                                                                                                                |
|    | Deploying a new version into production should be done “at scale” of the current run state of the system. Do not deploy to a “minimum/default” and force the system to immediately perform a scale operation.                                                                                                                                                                                                  |
|    | Build & execute lifecycle operation processes that respect your performance targets.                                                                                                                                                                                                                                                               |
|    | Ensure the actions/operations of lifecycle concerns, such as the deploying a new version of the workload, has understood, and ideally negligible, impact on the established performance KPIs. Your operations tasks are not of concern to your end users nor your business metrics.                                                                                                                                                               |
|    | Service features such as deployment slots. AKS doing side-by-side (B/G) deployments and do traffic shifting. Database point-in-time.                                                                                                                                                                                                                                      |
|    | Database changes should be carefully planned and announced. Can we learn anything from M365 teams for SharePoint Online?                                                                                                                                                                                                                                            |
|    |                                                                                                                                                                                                                                                                                                         |
|    |                                                                                                                                                                                                                                                                                                         |
|    |                                                                                                                                                                                                                                                                                                         |
|    | Be aware of IaC-based deployments not respecting current scaling. For example, your IaC may set an instance count of “2” and support scaling to “10” and the current deployed environment is running at “8.” If instance count of “2” is set at deployment time, you’ll negatively impact the run-state of that service.                                                                                                                                             |
| PE: 08 | Design all data stores, partitions, and indexes for their intended use in the workload.                                                                                                                                                                                                                                                             |
|    |                                                                                                                                                                                                                                                                                                         |
|    | Related guide/assessment content:                                                                                                                                                                                                                                                                                        |
|    | Design all data stores, partitions, & indexes explicitly for their intended usage in the workload.                                                                                                                                                                                                                                                        |
|    | Where your workload controls its own data, design all data stores, partitions, and indexes for their intended use in the workload.                                                                                                                                                                                                                                        |
|    | (guide?) Tune data shape and indexes based on coded CRUD usage patterns. Use eventual consistency where practical to facilitate data caching, shard replication, and deferred data capture.                                                                                                                                                                                                           |
|    |                                                                                                                                                                                                                                                                                                         |
|    | Implement a sustainable data sharding model to segment data across performance boundaries that avoids data and query hotspots. Index and shape data based on expected usage (CRUD) patterns. Use eventual consistency where possible to facilitate sharding and data caching.                                                                                                                                                                  |
|    | Maintenance jobs for indexes and statistics. PSQL, MySQL, etc insights for long-running queries, missed indexes. “Databases are never done.”                                                                                                                                                                                                                                  |
|    |                                                                                                                                                                                                                                                                                                         |
|    | If CAP theorem is evaluated for your workload’s data, remember that it does not have any provisions for performance. If data latency is a critical factor in your workload, consider using an alternative such as PACELC which puts latency measured against consistency.                                                                                                                                                                    |
| PE: 09 | Optimize use of workload resources. Code and infrastructure should only be used for their core purpose and only when necessary.                                                                                                                                                                                                                                         |
|    |                                                                                                                                                                                                                                                                                                         |
|    | Related guide/assessment content:                                                                                                                                                                                                                                                                                        |
|    | Keep all resource utilization limited to its core purpose and only use the resource when necessary by using architectural techniques like data caching, gateway processing, and utilizing available client resources. Also reduce resource utilization (such as CPU cores and memory) by optimizing code to avoid memory leaks, unnecessary large object heap allocations, seeking O(1) solutions, and taking advantage of the processor architectures and their threading models.                                                                |
|    |                                                                                                                                                                                                                                                                                                         |
|    | Optimize code and application vs optimize with brute force. Need to have skilled engineering team. This is an efficiency point. Investing where you’ll get ROI with minimum I.                                                                                                                                                                                                                |
|    | Reduce resource utilization to avoid memory leaks, unnecessary large object heap allocations, seeking 0(1) solutions. Take advantage of the processor architecture and threading models.                                                                                                                                                                                                             |
|    | Keep resource utilization limited to its core purpose and only use the resource when necessary.                                                                                                                                                                                                                                                         |
|    | Use techniques that ultimately minimize the need for usage of your system’s resources. For example:                                                                                                                                                                                                                                                       |
|    | Instill an expectation of reasonably up-to-date data in the workload so that you can offload/externalize responsibility and resource utilization to clients or intermediaries, such as search indexes and caches.                                                                                                                                                                                                |
|    | Offload security checks, such as web application firewalls, to gateway resources, and not within your code or your individual compute instances.                                                                                                                                                                                                                                 |
|    | Optimize all on-wire communication and the processing of it. Use techniques as appropriate to the situation such as minimizing data retrieved, using optimized protocols, using compression, or even avoiding communication altogether if redundant.                                                                                                                                                                               |
|    |                                                                                                                                                                                                                                                                                                         |
|    | Does data compression go here? How about connection pooling?                                                                                                                                                                                                                                                                           |
|    | Code that is optimized & defect free from the perspective of performance goes a long way in reducing your resource consumption. Avoiding bugs such as memory leaks is one thing, but optimizing your code to use less resources or to make better use of the resources you have available. Some examples would be looking for opportunities to replace O(N) operations with O(1) equivalents, reducing large object heap memory allocations, ensuring your code takes advantage of the CPU architecture of your compute, removing unnecessary busy-waiting conditions, using object and connection pooling, etc. |
| PE: 10 | Conduct formal capacity planning and drilling activities at key points in the lifecycle of the workload. Capacity planning should occur before predicted changes in usage patterns.                                                                                                                                                                                                               |
|    |                                                                                                                                                                                                                                                                                                         |
|    | Related guide/assessment content:                                                                                                                                                                                                                                                                                        |
|    | (initial business requirements, significant business model changes, marketing pushes, seasonal drift).                                                                                                                                                                                                                                                      |
|    | Formal capacity planning activities are performed at key points in the lifecycle of the workload.                                                                                                                                                                                                                                                        |
|    | This includes initial workload design based on initial business requirements, business model changes, seasonal drift, etc.                                                                                                                                                                                                                                            |
|    | The drilling part maybe should be put into PE:05 (testing)? Simulate the future (3 years). How do we know “how much capacity we need?” Buy until you get there?                                                                                                                                                                                                                         |
|    | Can we tie in capacity model into the formal capacity planning aspect here?                                                                                                                                                                                                                                                                   |
|    | Formal capacity modeling is a prediction exercise, months, years? Planning is the exercise to implement/resource the model. Is this actually a distinction with a difference?                                                                                                                                                                                                                 |
|    |                                                                                                                                                                                                                                                                                                         |
|    | Maybe we talk about “cliffs” in here as well?                                                                                                                                                                                                                                                                                  |
| PE: 11 | Perform a root cause analysis (RCA) on performance and scaling issues. The RCA should determine how to return to normal operations faster and incorporate preventive measures into the workload.                                                                                                                                                                                                         |
|    |                                                                                                                                                                                                                                                                                                         |
|    | Related guide/assessment content:                                                                                                                                                                                                                                                                                        |
|    |                                                                                                                                                                                                                                                                                                         |
|    | Learn from the issue and incorporate. How to get back to healthy faster and mitigate.                                                                                                                                                                                                                                                              |
|    | ways to introduce self-preservation and self-healing.                                                                                                                                                                                                                                                                              |
|    | The workload operations team can efficiently perform live-site activities related to potential performance or scaling malfunction.                                                                                                                                                                                                                                        |
|    | Your workload operations team has enough data, insights, & access to perform live-site triage and troubleshooting activities that are related to performance or scaling malfunction. This access needs to be across the whole stack: code, networking, compute, security, etc.                                                                                                                                                                  |
|    |                                                                                                                                                                                                                                                                                                         |
|    | 5xWhy                                                                                                                                                                                                                                                                                                      |
|    | How was the problem mitigated?                                                                                                                                                                                                                                                                                          |
|    | How are we preventing it from happening again?                                                                                                                                                                                                                                                                                  |
| PE: 12 | Prioritize the performance of critical flows and critical users. Prioritization should focus on where to invest limited resources.                                                                                                                                                                                                                                        |
|    |                                                                                                                                                                                                                                                                                                         |
|    | Related guide/assessment content:                                                                                                                                                                                                                                                                                        |
|    | Where practical, yield lower & non-priority usage to higher priority usage. This might align with your workload’s business or tenant model.                                                                                                                                                                                                                                   |
|    | Prioritize the performance of critical flows and users.                                                                                                                                                                                                                                                                             |
|    | Prioritize critical user, data, and workflows along with critical user access. This could align with workload business models, for example or tied back to business outcomes like revenue. Where practical yield lower & non-priority usage to higher priority usage. Use techniques such as rate limiting, priority queue processing, etc.                                                                                                                                   |
|    |                                                                                                                                                                                                                                                                                                         |
|    | This optimizes performance such that the service level provided for critical path interactions does not need to be extraneously extended to all components or all flows in the system.                                                                                                                                                                                                              |
| PE: 13 | Continuously optimize performance. The focus should be on components whose performance deteriorates over time, such as databases and networking features.                                                                                                                                                                                                                            |
|    |                                                                                                                                                                                                                                                                                                         |
|    | Related guide/assessment content:                                                                                                                                                                                                                                                                                        |
|    | Re-index relational databases                                                                                                                                                                                                                                                                                          |
|    | Institute continuous effort to optimize performance of solution components that may deteriorate over time (growth/usage), like databases and networking components. Consider developing or taking advantage of existing specialized resources across workloads.                                                                                                                                                                         |
|    | Continuous optimization of solution components                                                                                                                                                                                                                                                                                  |
|    | Teams with specialized skills, potentially dedicated to that. Automate where practical. Reduce manual effort/toil.                                                                                                                                                                                                                                               |
|    | Enable automated tuning of database resources provided by cloud service vendors such as automatic creating missing indexes, dropping unused indexes, and plan correction.                                                                                                                                                                                                                    |
|    |                                                                                                                                                                                                                                                                                                         |
|    |                                                                                                                                                                                                                                                                                                         |
|    | Use the automated tuning features that cloud service vendors provide. These features include automatic creating missing indexes, dropping unused indexes, and plan correction.                                                                                                                                                                                                                  |
|    | Automatic tuning options can be independently enabled or disabled for each database, or they can be configured at the server-level and applied on every database that inherits settings from the server.                                                                                                                                                                                                     |
| PE: 14 | [Recommendation text]                                                                                                                                                                                                                                                                                              |
|    | Related guide/assessment content:                                                                                                                                                                                                                                                                                        |
|    | [Pithy one sentence summary]                                                                                                                                                                                                                                                                                           |
|    | Formal capacity planning vs deploy and be ready to instantly adapt                                                                                                                                                                                                                                                                        |
|    |                                                                                                                                                                                                                                                                                                         |
|    | Have the knowledge and skills team to be able to react. They need to understand the tooling, the architecture, and the impact profile of failure. Especially cross-team (team boundaries). DB team vs app team. CROSS-TEAM Drilling can help sort out bottlenecks in people/process.                                                                                                                                                             |
|    |                                                                                                                                                                                                                                                                                                         |
|    |                                                                                                                                                                                                                                                                                                         |
|    | LEARN FROM PRODUCTION – that’s a key point                                                                                                                                                                                                                                                                                    |
|    | [Free-form guide “seed” content.]                                                                                                                                                                                                                                                                                        |
| PE: 15 | Related guide/assessment content:                                                                                                                                                                                                                                                                                        |
|    | [Pithy one sentence summary]                                                                                                                                                                                                                                                                                           |
|    | [Free-form guide “seed” content.]                                                                                                                                                                                                                                                                                        |
| PE: 16 | Related guide/assessment content:                                                                                                                                                                                                                                                                                        |
|    | [Pithy one sentence summary]                                                                                                                                                                                                                                                                                           |
|    | [Free-form guide “seed” content.]                                                                                                                                                                                                                                                                                        |
|    | Automatic tuning options can be independently enabled or disabled for each database, or they can be configured at the server-level and applied on every database that inherits settings from the server.                                                                                                                                                                                                     |