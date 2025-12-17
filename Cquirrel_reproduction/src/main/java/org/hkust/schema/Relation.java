package org.hkust.schema;

import java.util.ArrayList;
import java.util.List;

/**
 * Represents a TPC-H relation (table).
 *
 * TODO: Implement the following:
 * - Relation name (e.g., lineitem, orders, customer)
 * - List of attributes (columns)
 * - Primary key definition
 * - Foreign key relationships
 * - Methods to access attributes by name
 */
public class Relation {
    private String name;
    private List<Attribute> attributes;
    private List<String> primaryKey;

    public Relation(String name) {
        this.name = name;
        this.attributes = new ArrayList<>();
        this.primaryKey = new ArrayList<>();
    }

    // TODO: Add full implementation

    public String getName() {
        return name;
    }

    public List<Attribute> getAttributes() {
        return attributes;
    }

    public void addAttribute(Attribute attribute) {
        this.attributes.add(attribute);
    }
}
