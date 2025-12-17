package org.hkust.objects;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Core object representing a query execution plan.
 * This is the main output of JSON parsing and input to code generation.
 *
 * TODO: Implement the following:
 * - List of RelationProcessFunction objects (one per relation in the query)
 * - List of AggregateProcessFunction objects (for GROUP BY and aggregations)
 * - Join structure map (parent-child relationships between relations)
 * - Methods to add and retrieve process functions
 * - Query metadata (root relation, output schema, etc.)
 */
public class Node {
    private List<RelationProcessFunction> relationProcessFunctions;
    private List<AggregateProcessFunction> aggregateProcessFunctions;
    private Map<String, String> joinStructure;

    public Node() {
        this.relationProcessFunctions = new ArrayList<>();
        this.aggregateProcessFunctions = new ArrayList<>();
        this.joinStructure = new HashMap<>();
    }

    // TODO: Add full implementation

    public List<RelationProcessFunction> getRelationProcessFunctions() {
        return relationProcessFunctions;
    }

    public List<AggregateProcessFunction> getAggregateProcessFunctions() {
        return aggregateProcessFunctions;
    }

    public Map<String, String> getJoinStructure() {
        return joinStructure;
    }
}
