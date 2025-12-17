package org.hkust.flink;

import org.apache.flink.api.common.state.MapState;
import org.apache.flink.configuration.Configuration;
import org.apache.flink.streaming.api.functions.KeyedProcessFunction;
import org.apache.flink.util.Collector;
import org.hkust.objects.AggregateProcessFunction;
import org.hkust.objects.AggregateValue;

/**
 * Flink KeyedProcessFunction for computing aggregations incrementally.
 *
 * This function maintains aggregate state and handles:
 * 1. Incremental updates for SUM, COUNT, AVG, MIN, MAX
 * 2. Insert/delete operations on aggregates
 * 3. HAVING clause filtering
 *
 * TODO: Implement the following:
 * - State declarations for each aggregate (MapState)
 * - open() method to initialize state
 * - processElement() to handle incoming tuples
 * - For each AggregateValue:
 *   - Update aggregate on insert (+)
 *   - Reverse aggregate on delete (-)
 * - Apply HAVING conditions
 * - Emit aggregated results
 * - Handle COUNT DISTINCT specially
 */
public class AggregateKeyedProcessFunction extends KeyedProcessFunction<String, Object, Object> {

    private AggregateProcessFunction apf;

    // TODO: Add state variables for aggregates
    // private transient MapState<String, Double> sumState;
    // private transient MapState<String, Long> countState;

    public AggregateKeyedProcessFunction(AggregateProcessFunction apf) {
        this.apf = apf;
    }

    @Override
    public void open(Configuration parameters) throws Exception {
        super.open(parameters);
        // TODO: Initialize state descriptors for each aggregate
    }

    @Override
    public void processElement(Object value, Context ctx, Collector<Object> out) throws Exception {
        // TODO: Implement aggregate processing logic

        // Steps:
        // 1. Parse input tuple
        // 2. Extract grouping key
        // 3. Determine if insert (+) or delete (-)
        // 4. For each aggregate:
        //    - SUM: add/subtract value
        //    - COUNT: increment/decrement
        //    - AVG: update sum and count
        //    - MIN/MAX: recompute if necessary
        // 5. Apply HAVING conditions
        // 6. Emit aggregate result

        throw new UnsupportedOperationException("Aggregate processing not yet implemented");
    }

    /**
     * Update SUM aggregate.
     */
    private void updateSum(String key, double value, boolean isInsert) {
        // TODO: Implement
    }

    /**
     * Update COUNT aggregate.
     */
    private void updateCount(String key, boolean isInsert) {
        // TODO: Implement
    }
}
