package org.hkust.schema;

/**
 * Represents an attribute (column) in a TPC-H relation.
 *
 * TODO: Implement the following:
 * - Attribute name
 * - Data type (VARCHAR, INTEGER, DOUBLE, DATE, etc.)
 * - Parent relation reference
 * - Getter and setter methods
 */
public class Attribute {
    private String name;
    private String dataType;
    private String relationName;

    public Attribute(String name, String dataType, String relationName) {
        this.name = name;
        this.dataType = dataType;
        this.relationName = relationName;
    }

    // TODO: Add full implementation

    public String getName() {
        return name;
    }

    public String getDataType() {
        return dataType;
    }

    public String getRelationName() {
        return relationName;
    }
}
