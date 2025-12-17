package org.hkust.objects;

import org.hkust.schema.Relation;
import java.util.ArrayList;
import java.util.List;

/**
 * Represents a RelationProcessFunction that handles stream processing for a single relation.
 * This includes filtering (WHERE conditions), projection, and joining with parent/child relations.
 *
 * TODO: Implement the following:
 * - Function name (class name for generated code)
 * - Associated relation
 * - This key (key for current relation state)
 * - Next key (key for output/join with next relation)
 * - Child nodes count
 * - Flags: isRoot, isLast
 * - Select conditions (WHERE clause filters)
 * - Attribute renaming rules
 * - Methods to evaluate conditions on tuples
 */
public class RelationProcessFunction {
    private String name;
    private Relation relation;
    private String thisKey;
    private String nextKey;
    private int childNodes;
    private boolean isRoot;
    private boolean isLast;
    private List<SelectCondition> selectConditions;

    public RelationProcessFunction(String name) {
        this.name = name;
        this.selectConditions = new ArrayList<>();
    }

    // TODO: Add full implementation

    public String getName() {
        return name;
    }

    public boolean isRoot() {
        return isRoot;
    }

    public boolean isLast() {
        return isLast;
    }
}
