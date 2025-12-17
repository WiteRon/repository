package org.hkust.objects;

/**
 * Represents an aggregation operation (SUM, COUNT, AVG, MIN, MAX).
 *
 * TODO: Implement the following:
 * - Aggregate name (e.g., "revenue", "total_quantity")
 * - Value to aggregate (can be an Expression like l_extendedprice * (1 - l_discount))
 * - Aggregation operator (SUM, COUNT, AVG, MIN, MAX)
 * - Value type (data type of the aggregated value)
 * - Methods to update aggregate incrementally (for inserts/deletes)
 */
public class AggregateValue {
    private String name;
    private Value value;
    private String aggregation;
    private String valueType;

    public AggregateValue(String name, String aggregation) {
        this.name = name;
        this.aggregation = aggregation;
    }

    // TODO: Add full implementation

    public String getName() {
        return name;
    }

    public String getAggregation() {
        return aggregation;
    }

    public Value getValue() {
        return value;
    }
}
