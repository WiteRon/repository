package org.hkust.schema;

import java.util.HashMap;
import java.util.Map;

/**
 * Defines the complete TPC-H schema including all 8 relations:
 * - lineitem (LI)
 * - orders (OR)
 * - customer (CU)
 * - part (PA)
 * - partsupp (PS)
 * - supplier (SU)
 * - nation (NA)
 * - region (RI)
 *
 * TODO: Implement the following:
 * - Define all 8 TPC-H tables with their complete schemas
 * - Define all attributes with correct data types
 * - Define primary and foreign key relationships
 * - Provide methods to get relations by name
 * - Create table prefix mapping (LI -> lineitem, OR -> orders, etc.)
 */
public class RelationSchema {
    private static RelationSchema instance;
    private Map<String, Relation> relations;
    private Map<String, String> prefixToRelationName;

    private RelationSchema() {
        this.relations = new HashMap<>();
        this.prefixToRelationName = new HashMap<>();
        initializeSchema();
    }

    public static RelationSchema getInstance() {
        if (instance == null) {
            instance = new RelationSchema();
        }
        return instance;
    }

    /**
     * TODO: Initialize all TPC-H relations with their schemas.
     *
     * Example structure for lineitem:
     * - l_orderkey (INTEGER) - FK to orders
     * - l_partkey (INTEGER) - FK to part
     * - l_suppkey (INTEGER) - FK to supplier
     * - l_linenumber (INTEGER)
     * - l_quantity (DOUBLE)
     * - l_extendedprice (DOUBLE)
     * - l_discount (DOUBLE)
     * - l_tax (DOUBLE)
     * - l_returnflag (VARCHAR)
     * - l_linestatus (VARCHAR)
     * - l_shipdate (DATE)
     * - l_commitdate (DATE)
     * - l_receiptdate (DATE)
     * - l_shipinstruct (VARCHAR)
     * - l_shipmode (VARCHAR)
     * - l_comment (VARCHAR)
     *
     * Similarly define: orders, customer, part, partsupp, supplier, nation, region
     */
    private void initializeSchema() {
        // TODO: Add complete schema definitions

        // Initialize table prefix mapping
        prefixToRelationName.put("LI", "lineitem");
        prefixToRelationName.put("OR", "orders");
        prefixToRelationName.put("CU", "customer");
        prefixToRelationName.put("PA", "part");
        prefixToRelationName.put("PS", "partsupp");
        prefixToRelationName.put("SU", "supplier");
        prefixToRelationName.put("NA", "nation");
        prefixToRelationName.put("RI", "region");
    }

    public Relation getRelation(String name) {
        return relations.get(name);
    }

    public String getRelationNameByPrefix(String prefix) {
        return prefixToRelationName.get(prefix);
    }
}
