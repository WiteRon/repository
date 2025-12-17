package org.hkust.objects;

import java.util.ArrayList;
import java.util.List;

/**
 * Represents an AggregateProcessFunction that handles GROUP BY and aggregation operations.
 *
 * TODO: Implement the following:
 * - Function name (class name for generated code)
 * - This key (grouping key)
 * - Output key (key for final output)
 * - List of AggregateValue objects (SUM, COUNT, AVG, etc.)
 * - Having conditions (filters on aggregated results)
 * - Methods to compute aggregations incrementally
 * - Methods to handle insertions and deletions in streaming context
 */
public class AggregateProcessFunction {
    private String name;
    private String thisKey;
    private String outputKey;
    private List<AggregateValue> aggregateValues;

    public AggregateProcessFunction(String name) {
        this.name = name;
        this.aggregateValues = new ArrayList<>();
    }

    // TODO: Add full implementation

    public String getName() {
        return name;
    }

    public String getThisKey() {
        return thisKey;
    }

    public List<AggregateValue> getAggregateValues() {
        return aggregateValues;
    }
}
